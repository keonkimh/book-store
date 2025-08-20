from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .filters import BookFilter
from .models.book_models import Book
from .serializers import BookSerializer
from rest_framework.parsers import MultiPartParser, FormParser


# Create your views here.
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    parser_classes = [MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter
