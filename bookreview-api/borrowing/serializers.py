from rest_framework import serializers

from .models import Borrow


class BorrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrow
        fields = ("id", "user", "book_instance", "date_borrowed",
                  "date_returned", "fees_amount", "fees_paid", "paid_at")
        read_only_fields = ("id", "date_borrowed", "user", "date_returned",
                            "fees_amount", "fees_paid", "paid_at")
