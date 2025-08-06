from django.db import models
from books.models.book_models import Book
from core.models.base import BaseModel

class BookInstance(BaseModel):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='instances')
    is_available = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} ({'Available' if self.is_available else 'Not Available'})"