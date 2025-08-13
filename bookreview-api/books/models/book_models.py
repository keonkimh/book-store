from core.models.base import BaseModel
from django.db import models
from books.models.book_genre_models import BookGenre

# Create your models here.
class Book(BaseModel):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.ForeignKey(BookGenre, on_delete=models.CASCADE, related_name="books")
    date_published = models.DateField()
    number_of_copies = models.PositiveIntegerField(default=0)
    cover_img = models.ImageField(default='default_cover.jpg')

    def __str__(self):
        return self.title
