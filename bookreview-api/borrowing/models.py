from datetime import timedelta, datetime
from typing import Optional, Type
from books.models.book_instance_models import BookInstance
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from config.settings import MAX_BORROW_DAYS, FEE_PER_DAY, LOST_BORROW_DAYS


# Create your models here.
class Borrow(models.Model):
    user: Type[User] = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="borrows"
    )
    book_instance: BookInstance = models.ForeignKey(
        BookInstance, on_delete=models.CASCADE, related_name="borrows"
    )
    date_borrowed: Optional[datetime] = models.DateTimeField(
        null=True, blank=True)
    date_returned: Optional[datetime] = models.DateTimeField(
        null=True, blank=True)

    # fees system
    fees_amount: int = models.PositiveIntegerField(default=0)
    fees_paid: bool = models.BooleanField(default=False)
    paid_at: Optional[datetime] = models.DateTimeField(
        null=True, blank=True)

    def __str__(self) -> str:
        return (
            f"{self.user.username} borrowed "
            f"{self.book_instance.book.title} on "
            f"{self.date_borrowed.strftime('%Y-%m-%d')}"
        )

    def save(self, *args, **kwargs) -> None:
        if not self.book_instance.is_available:
            raise ValueError("This book is already borrowed.")

        self.book_instance.is_available = False
        self.book_instance.date_returned = None
        if not self.date_borrowed:
            self.date_borrowed = timezone.now()
            self.book_instance.date_borrowed = timezone.now()
        else:
            self.book_instance.date_borrowed = self.date_borrowed
        self.book_instance.save()
        super().save(*args, **kwargs)

    def due_date(self) -> datetime:
        return self.date_borrowed + timedelta(days=MAX_BORROW_DAYS)

    def compute_fees(self) -> int:
        if self.date_returned is None and timezone.now() > self.due_date():
            overdue_days = (timezone.now() - self.due_date()).days
            self.fees_amount = overdue_days * FEE_PER_DAY
        return self.fees_amount

    def make_payment(self) -> None:
        if self.fees_paid is False and self.fees_amount > 0:
            self.fees_paid = True
            self.paid_at = timezone.now()
            self.save()
            raise ValueError({
                "message": f"Your fee is: {self.fees_amount}. Make a payment via PromptPay to 123-456-7890"
            })

    def lost_date(self) -> datetime:
        return self.book_instance.date_borrowed + timedelta(
            days=LOST_BORROW_DAYS)

    def mark_as_lost(self) -> None:
        if not self.book_instance.is_available and not self.book_instance.is_lost:
            if timezone.now() > self.lost_date():
                self.book_instance.is_lost = True
                self.book_instance.is_available = False
                self.book_instance.save()
                print(self.book_instance.book.title)
                print("Buying the replacement book.")
                BookInstance.objects.create(book=self.book_instance.book,
                                            is_available=True)

    def mark_as_returned(self) -> None:
        if self.book_instance.is_available:
            raise ValueError("This book is already returned.")
        self.book_instance.is_available = True
        self.book_instance.date_returned = timezone.now()
        fees = self.compute_fees()
        self.fees_amount = fees
        if self.fees_paid is False:
            self.make_payment()
        self.book_instance.save()
