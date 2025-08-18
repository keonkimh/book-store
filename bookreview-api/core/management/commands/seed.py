import random
from datetime import timedelta
from books.models.book_instance_models import BookInstance
from books.models.book_models import Book
from books.models.book_genre_models import BookGenre
from borrowing.models import Borrow
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker
from django.utils.timezone import now

fake = Faker()
User = get_user_model()


class Command(BaseCommand):
    help = "Seed database with sample data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")

        # Create or get genres
        genre_names = ["Fiction", "Science", "History", "Fantasy"]
        book_genres = []
        for name in genre_names:
            genre, _ = BookGenre.objects.get_or_create(name=name)
            book_genres.append(genre)

        # Create users
        users = []
        for i in range(5):
            user, _ = User.objects.get_or_create(
                username=f"user{i}",
                defaults={
                    "email": f"user{i}@example.com",
                    "password": "pbkdf2_sha256$260000$dummy$hashedpassword",
                },
            )
            users.append(user)

        # Create books and instances
        books = []
        for _ in range(10):
            book = Book.objects.create(
                title=fake.sentence(nb_words=3),
                author=fake.name(),
                description=fake.text(),
                genre=random.choice(book_genres),
                date_published=fake.date_this_century(),
            )
            books.append(book)

            for _ in range(3):
                BookInstance.objects.create(book=book, is_available=True)

        # Create random borrows
        for _ in range(10):
            available_instances = BookInstance.objects.filter(is_available=True)
            if not available_instances.exists():
                break
            book_instance = random.choice(list(available_instances))
            user = random.choice(users)
            Borrow.objects.create(user=user, book_instance=book_instance, date_borrowed=now() - timedelta(days=8))

        self.stdout.write(self.style.SUCCESS("Database seeded successfully."))
