from rest_framework import serializers
from django.conf import settings
from django.utils import timezone
from .models.book_models import Book
from borrowing.models import Borrow

class BookSerializer(serializers.ModelSerializer):
    available_count = serializers.SerializerMethodField()
    earliest_available_date = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ('id', 'title', 'author', 'description', 'genre', 'date_published', 'available_count', 'earliest_available_date')

    def create(self, validated_data):
        book = Book.objects.create(**validated_data)
        return book

    def get_available_count(self, obj):
        return obj.instances.filter(is_available=True).count()

    def get_earliest_available_date(self, obj):
        if obj.instances.filter(is_available=True).exists():
            return None

        earliest_borrow = (
            Borrow.objects.filter(book_instance__book=obj, book_instance__is_available=False).order_by("date_borrowed")
            .first()
        )

        if earliest_borrow:
            return earliest_borrow.date_borrowed + timezone.timedelta(days=settings.MAX_BORROW_DAYS)
            
        return None
