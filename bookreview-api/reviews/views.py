from django.shortcuts import render
from rest_framework import viewsets
from .models import Review
from .serializers import ReviewSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
