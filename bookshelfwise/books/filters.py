import django_filters
from django import forms

from books.models import Book


class DateInput(forms.DateInput):
    input_type = "date"


class BookFilter(django_filters.FilterSet):
    author = django_filters.CharFilter(lookup_expr="name__icontains")
    from_date = django_filters.DateFilter(
        widget=DateInput, field_name="publication_date", lookup_expr="gte", label="From"
    )
    to_date = django_filters.DateFilter(
        widget=DateInput, field_name="publication_date", lookup_expr="lte", label="To"
    )

    class Meta:
        model = Book
        fields = {
            "title": ("icontains",),
            "publication_lang": ("exact",),
        }
