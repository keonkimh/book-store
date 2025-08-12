from books.models.book_models import Book
from core.models.base import BaseModel
from django.db import models


class BookInstance(BaseModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="instances")
    is_available = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_borrowed = models.DateTimeField(null=True, blank=True)
    date_returned = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.book.title} ({'Available' if self.is_available else 'Not Available'})"
