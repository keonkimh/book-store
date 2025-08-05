from rest_framework import serializers
from .models.book_models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'description', 'genre', 'date_published', 'book_available_count')

    def create(self, validated_data):
        book = Book.objects.create(**validated_data)
        return book
