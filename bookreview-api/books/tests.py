# Create your tests here.
from django.test import TestCase
from books.models.book_models import Book
from books.models.book_genre_models import BookGenre
from books.models.book_instance_models import BookInstance


class BookTests(TestCase):
    def setUp(self):
        self.genre = BookGenre.objects.create(name="Fiction")
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            description="Test Description",
            genre=self.genre,
            date_published="2025-01-01",
            number_of_copies=3,
        )
        for _ in range(self.book.number_of_copies):
            BookInstance.objects.create(book=self.book)

    def test_book_creation(self):
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.genre.name, "Fiction")

    def test_book_instance_creation(self):
        instances = BookInstance.objects.filter(book=self.book)
        self.assertEqual(instances.count(), 3)
        self.assertTrue(all(instance.is_available for instance in instances))
