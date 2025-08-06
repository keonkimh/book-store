import random

from books.models.book_instance_models import BookInstance
from books.models.book_models import Book
from borrowing.models import Borrow
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

fake = Faker()
User = get_user_model()


class Command(BaseCommand):
    help = "Seed database with sample data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")

        # Create Users
        users = []
        for i in range(5):
            user, _ = User.objects.get_or_create(
                username=f"user{i}",
                defaults={
                    "email": f"user{i}@example.com",
                    "password": "pbkdf2_sha256$260000$dummy$hashedpassword",
                },  # set real hashed pwd if needed
            )
            users.append(user)

        # Create Books & BookInstances
        books = []
        for _ in range(10):
            book = Book.objects.create(
                title=fake.sentence(nb_words=3),
                author=fake.name(),
                description=fake.text(),
                genre=random.choice(["Fiction", "Science", "History", "Fantasy"]),
                date_published=fake.date_this_century(),
            )
            books.append(book)

            # Create 3 copies of each book
            for _ in range(3):
                BookInstance.objects.create(book=book, is_available=True)

        # Create random borrows
        for _ in range(10):
            book_instance = random.choice(
                BookInstance.objects.filter(is_available=True)
            )
            user = random.choice(users)
            Borrow.objects.create(user=user, book_instance=book_instance)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully."))
