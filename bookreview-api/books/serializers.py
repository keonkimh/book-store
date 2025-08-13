from borrowing.models import Borrow
from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from books.models.book_genre_models import BookGenre
from django.db import transaction
from .models.book_models import Book
from reviews.serializers import ReviewSerializer
from books.models.book_instance_models import BookInstance

class BookInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInstance
        fields = ("id", "is_available", "date_added", "date_borrowed", "date_returned", "is_lost")

class BookGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookGenre
        fields = ('id', 'name', 'created_at', 'updated_at')


class BookSerializer(serializers.ModelSerializer):
    genre = BookGenreSerializer(read_only=True)
    genre_id = serializers.PrimaryKeyRelatedField(
        queryset=BookGenre.objects.all(), source="genre", write_only=True
    )
    number_of_copies = serializers.IntegerField(write_only=True)
    available_count = serializers.SerializerMethodField()
    earliest_available_date = serializers.SerializerMethodField()
    reviews = ReviewSerializer(many=True, read_only=True)
    instances = BookInstanceSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "author",
            "description",
            "genre",
            "genre_id",
            "date_published",
            "number_of_copies",
            "available_count",
            "earliest_available_date",
            "reviews",
            "instances",
            "cover_url",
            "average_rating",
        )

    def create(self, validated_data):
        number_of_copies = validated_data.pop("number_of_copies", 0)
        with transaction.atomic():
            book = Book.objects.create(**validated_data)
            from books.models.book_instance_models import BookInstance
            for _ in range(number_of_copies):
                BookInstance.objects.create(book=book)
        return book

    def get_available_count(self, obj):
        return obj.instances.filter(is_available=True).count()

    def get_earliest_available_date(self, obj):
        if obj.instances.filter(is_available=True).exists():
            return None

        earliest_borrow = (
            Borrow.objects.filter(
                book_instance__book=obj, book_instance__is_available=False
            )
            .order_by("date_borrowed")
            .first()
        )

        if earliest_borrow is None:
            return None

        return earliest_borrow.date_borrowed + timezone.timedelta(
            days=settings.MAX_BORROW_DAYS
        )

    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return None
        total_rating = sum(review.rating for review in reviews)
        return total_rating / len(reviews) if len(reviews) > 0 else None
