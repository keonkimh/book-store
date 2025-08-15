from django.core.management.base import BaseCommand
from borrowing.models import Borrow
from datetime import timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = "Mark books as lost if borrowed for more than 90 days and not returned."

    def handle(self, *args, **kwargs):
        overdue_borrows = Borrow.objects.filter(
            book_instance__is_available = False
        )
        print(overdue_borrows)
        for borrow in overdue_borrows:
            borrow.mark_as_lost()
        self.stdout.write(self.style.SUCCESS("Marked overdue books as lost"))
