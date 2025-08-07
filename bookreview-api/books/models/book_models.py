from core.models.base import BaseModel
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from books.models.book_genre_models import BookGenre


# Create your models here.
class Book(BaseModel):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField()
    genre = models.ForeignKey(BookGenre, on_delete=models.CASCADE, related_name="books")
    date_published = models.DateField()
    number_of_copies = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


@receiver(post_save, sender=Book)
def create_book_instance(sender, instance, created, **kwargs):
    try:
        if created:
            from books.models.book_instance_models import BookInstance
            for _ in range(instance.number_of_copies):
                BookInstance.objects.create(book=instance)
    except Exception as e:
        print(f"Error creating BookInstance: {e}")
