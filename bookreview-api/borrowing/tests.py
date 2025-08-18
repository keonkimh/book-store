from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from books.models.book_models import Book
from books.models.book_genre_models import BookGenre
from books.models.book_instance_models import BookInstance
from borrowing.models import Borrow
from django.contrib.auth import get_user_model

User = get_user_model()  # Use the correct user model dynamically


class BorrowTests(TestCase):
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

    def test_borrow_book(self):
        borrow = Borrow.objects.create(user=self.user, book_instance=self.book_instance)
        self.assertEqual(borrow.user.username, "testuser")
        self.assertEqual(borrow.book_instance.book.title, "Test Book")
        self.assertFalse(borrow.book_instance.is_available)

    def test_return_book(self):
        borrow = Borrow.objects.create(user=self.user, book_instance=self.book_instance)
        borrow.mark_as_returned()
        self.assertTrue(borrow.book_instance.is_available)
        self.assertIsNotNone(borrow.book_instance.date_returned)

    def test_compute_fees(self):
        borrow = Borrow.objects.create(user=self.user, book_instance=self.book_instance, date_borrowed=timezone.now() - timedelta(days=10))
        fees = borrow.compute_fees()
        self.assertEqual(fees, 3 * 50)

    def test_mark_as_lost_and_replace(self):
        borrow = Borrow.objects.create(user=self.user, book_instance=self.book_instance, date_borrowed=timezone.now() - timedelta(days=91))
        borrow.mark_as_lost()
        self.assertTrue(borrow.book_instance.is_lost)
        self.assertFalse(borrow.book_instance.is_available)
        # to check if a replacement book has been purchased
        self.assertEqual(BookInstance.objects.filter(book=self.book).count(), 2)
        self.assertEqual(
            BookInstance.objects.filter(book=self.book, is_available=True, is_lost=False).count(),
            1,
        )
