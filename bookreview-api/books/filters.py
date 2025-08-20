import django_filters
from .models.book_models import Book


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr="icontains")
    genre = django_filters.CharFilter(field_name="genre__name",
                                      lookup_expr="icontains")
    date_published = django_filters.DateFilter()

    class Meta:
        model = Book
        fields = ["title", "genre", "date_published"]
