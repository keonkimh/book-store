from datetime import datetime
from typing import Optional
from books.models.book_models import Book
from core.models.base import BaseModel
from django.db import models
from django.utils import timezone


class BookInstance(BaseModel):
    book: Book = models.ForeignKey(Book, on_delete=models.CASCADE,
                                   related_name="instances")
    is_available: bool = models.BooleanField(default=True)
    date_added: Optional[datetime] = models.DateTimeField(
        auto_now_add=True)
    date_borrowed: Optional[datetime] = models.DateTimeField(
        null=True, blank=True)
    date_returned: Optional[datetime] = models.DateTimeField(
        null=True, blank=True)
    is_lost: bool = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.book.title} {'Available' if self.is_available else 'Not Available'}"
