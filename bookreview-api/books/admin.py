# Register your models here.
from django.contrib import admin
from .models.book_models import Book
from .models.book_genre_models import BookGenre
from .models.book_instance_models import BookInstance

@admin.register(BookGenre)
class BookGenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('name',)
