from django.db import models

class BookInstance(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='instances')
    is_available = models.BooleanField(default=True)
    barcode = models.CharField(max_length=100, unique=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.book.title} - {self.barcode} ({'Available' if self.is_available else 'Not Available'})"