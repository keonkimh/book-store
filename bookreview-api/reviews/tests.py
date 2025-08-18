# Create your tests here.
from django.test import TestCase
from books.models.book_models import Book
from books.models.book_genre_models import BookGenre
from books.models.book_instance_models import BookInstance
from borrowing.models import Borrow
from reviews.models import Review
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import serializers as drf_serializers
from reviews.serializers import ReviewSerializer
from rest_framework.request import Request

User = get_user_model()

class ReviewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.genre = BookGenre.objects.create(name="Fiction")
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            description="Test Description",
            genre=self.genre,
            date_published="2025-01-01",
            number_of_copies=1,
        )
        self.book_instance = BookInstance.objects.create(book=self.book, is_available=True)
        Borrow.objects.create(user=self.user, book_instance=self.book_instance)

    def test_create_review(self):
        review = Review.objects.create(user=self.user, book=self.book, rating=5, comment="Great book!")
        self.assertEqual(review.user.username, "testuser")
        self.assertEqual(review.book.title, "Test Book")
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Great book!")

    def test_review_without_borrowing(self):
        other_user = User.objects.create(username="otheruser", email="example@gmail.com")
        with self.assertRaises(Exception):
            Review.objects.create(user=other_user, book=self.book, rating=4, comment="Nice book!")
        self.assertEqual(Review.objects.count(), 0)
