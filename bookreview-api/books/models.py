from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.CharField(max_length=100)
    date_published = models.DateField()
    book_available_count = models.PositiveIntegerField(default=0)
    # isbn = models.CharField(max_length=13, unique=True)
    # might keep isbn for future use if required

    def __str__(self):
        return self.title