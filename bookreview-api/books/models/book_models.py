from datetime import datetime
from typing import Optional
from core.models.base import BaseModel
from django.db import models
from django.utils import timezone
from books.models.book_genre_models import BookGenre


# Create your models here.
class Book(BaseModel):
    title: str = models.CharField(max_length=255)
    author: str = models.CharField(max_length=255)
    description: str = models.TextField()
    genre: BookGenre = models.ForeignKey(BookGenre, on_delete=models.CASCADE,
                                         related_name="books")
    date_published: Optional[datetime] = models.DateField()
    number_of_copies: int = models.PositiveIntegerField(default=0)
    cover_img: models.ImageField = models.ImageField(
        default='default_cover.jpg')

    def __str__(self) -> str:
        return str(self.title)
