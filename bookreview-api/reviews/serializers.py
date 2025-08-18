from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'rating', 'comment', 'date_reviewed']
        read_only_fields = ['id', 'date_reviewed', 'user']

    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user if request else None
        return Review.objects.create(user=user, **validated_data)
