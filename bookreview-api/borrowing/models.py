from django.db import models
from django.conf import settings
from books.models.book_models import BookInstance

# Create your models here.
class Borrow(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='borrows')
    book_instance = models.ForeignKey(BookInstance, on_delete=models.CASCADE, related_name='borrows')
    date_borrowed = models.DateTimeField(auto_now_add=True)
    date_returned = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)
    days_remaining = models.PositiveIntegerField(default=7) # default borrowing period 7 days

    def __str__(self):
        return f"{self.user.username} borrowed {self.book_instance.book.title} on {self.date_borrowed.strftime('%Y-%m-%d')}"