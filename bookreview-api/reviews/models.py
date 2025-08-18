from datetime import datetime
from typing import Optional, Type
from core.models.base import BaseModel
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from borrowing.models import Borrow
from books.models.book_models import Book
from rest_framework.exceptions import APIException


# Create your models here.
class Review(BaseModel):
    user: Type[User] = models.ForeignKey(settings.AUTH_USER_MODEL,
                                          on_delete=models.CASCADE,
                                          related_name='reviews')
    book: Book = models.ForeignKey(Book, on_delete=models.CASCADE,
                                   related_name='reviews')
    rating: int = models.PositiveIntegerField()
    comment: str = models.TextField(blank=True, null=True)
    date_reviewed: Optional[datetime] = models.DateTimeField(
        auto_now_add=True)

    class Meta:
        unique_together = ('book', 'user')

    def clean(self) -> None:
        with transaction.atomic():
            if not Borrow.objects.filter(user=self.user, book_instance__book=self.book).exists():
                raise DoubleReview("You can only review books you have borrowed.")

            if not self.book:
                raise ValidationError("Book must be provided.")

            if Review.objects.filter(user=self.user, book=self.book).exists():
                raise DoubleReview()

    def save(self, *args, **kwargs) -> None:
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"Review by {self.user.username} for {self.book.title}"


class DoubleReview(APIException):
    status_code = 400
    default_detail = "You have already reviewed this book!"
    default_code = "review_exists"
