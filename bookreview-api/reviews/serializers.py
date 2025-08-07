from rest_framework import serializers
from django.db import transaction
from .models import Review
from books.models.book_models import Book

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'rating', 'comment', 'date_reviewed']
        read_only_fields = ['id', 'date_reviewed']

    def create(self, validated_data):
        with transaction.atomic():
            # Ensure the book exists
            book = validated_data.get('book')
            if not book:
                raise serializers.ValidationError("Book must be provided.")

            # Create the review
            review = Review.objects.create(**validated_data)
            return review
