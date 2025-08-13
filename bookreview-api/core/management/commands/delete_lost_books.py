from django.core.management.base import BaseCommand
from borrowing.models import Borrow

class Command(BaseCommand):
    help = 'Replace books in the database with new data from a JSON file.'

    def handle(self, *args, **kwargs):
        lost_book = []
        overdue_borrows = Borrow.objects.filter(
            book_instance__is_lost = True
        )
        for borrow in overdue_borrows:
            lost_book.append(borrow.book_instance.book.title)
            print(lost_book)
            borrow.delete_lost_book()
        self.stdout.write(self.style.SUCCESS("Deleted lost book"))
