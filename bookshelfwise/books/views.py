from django.shortcuts import render
from django.views.generic import ListView

from books.models import Book


class BookList(ListView):
    model = Book
    template_name = "books.html"
    context_object_name = "books"
    # paginate_by = ""
    # page_kwarg = ""

    # def get_queryset(self):
