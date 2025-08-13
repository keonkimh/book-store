from books.models.book_instance_models import BookInstance
from django.conf import settings
from django.db import models
from django.utils import timezone
from config.settings import MAX_BORROW_DAYS, FEE_PER_DAY, LOST_BORROW_DAYS
from datetime import timedelta

# Create your models here.
class Borrow(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrows"
    )
    book_instance = models.ForeignKey(
        BookInstance, on_delete=models.CASCADE, related_name="borrows"
    )
    date_borrowed = models.DateTimeField(null=True, blank=True)
    date_returned = models.DateTimeField(null=True, blank=True)

    # fees system
    fees_amount = models.PositiveIntegerField(default=0)
    fees_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book_instance.book.title} on {self.date_borrowed.strftime('%Y-%m-%d')}"

    def save(self, *args, **kwargs):
        if not self.book_instance.is_available:
            raise ValueError("This book is already borrowed.")

        self.book_instance.is_available = False
        self.book_instance.date_returned = None
        self.book_instance.date_borrowed = timezone.now() - timedelta(days=91)
        self.date_borrowed = timezone.now() - timedelta(days=91)
        self.book_instance.save()
        super().save(*args, **kwargs)

    def due_date(self):
        return self.date_borrowed + timezone.timedelta(days=MAX_BORROW_DAYS)

    def compute_fees(self):
        if self.date_returned is None and timezone.now() > self.due_date():
            overdue_days = (timezone.now() - self.due_date()).days
            self.fees_amount = overdue_days * FEE_PER_DAY
        else:
            self.fees_amount = 0
        return self.fees_amount

    def make_payment(self):
        if self.fees_paid is True:
            raise ValueError("You paid already, return the book now.")
        else:
            self.fees_paid = True
            self.paid_at = timezone.now()
            self.save()
            raise ValueError({
                "message": f"Your fee is: {self.fees_amount}. Make a payment via PromptPay to 123-456-7890"
            })

    def lost_date(self):
        return self.book_instance.date_borrowed + timezone.timedelta(days=LOST_BORROW_DAYS)

    def mark_as_lost(self):
        if not self.book_instance.is_available and not self.book_instance.is_lost:
            if timezone.now() > self.lost_date():
                self.book_instance.is_lost = True
                self.book_instance.save()
                print(self.book_instance.book.title)

    def delete_lost_book(self):
        if self.book_instance.is_lost:
            self.book_instance.delete()


    def mark_as_returned(self):
        if self.book_instance.is_available:
            raise ValueError("This book is already returned.")
        self.book_instance.is_available = True
        self.book_instance.date_returned = timezone.now()
        fees = self.compute_fees()
        self.fees_amount = fees
        if self.fees_paid is False:
            self.make_payment()
        self.book_instance.save()
        self.delete()
