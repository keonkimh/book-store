from rest_framework import serializers
from django.db import transaction
from .models import Review
from books.models.book_models import Book
from rest_framework.exceptions import APIException

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'rating', 'comment', 'date_reviewed']
        read_only_fields = ['id', 'date_reviewed']
        validators = []

    def create(self, validated_data):
        with transaction.atomic():
            # Ensure the book exists
            book = validated_data.get('book')
            user = validated_data.get('user')
            if not book:
                raise serializers.ValidationError("Book must be provided.")

            if Review.objects.filter(user=user, book=book).exists():
                raise DoubleReview("You have already reviewed this book!")
            # Create the review
            review = Review.objects.create(**validated_data)
            return review

class DoubleReview(APIException):
        status_code = 400
        default_detail = "You have already reviewed this book!"
        default_code = "review_exists"
