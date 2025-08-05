from django.shortcuts import render
from rest_framework import viewsets
from .serializers import BookSerializer
from .models.book_models import Book
from rest_framework.permissions import AllowAny

# Create your views here.
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer