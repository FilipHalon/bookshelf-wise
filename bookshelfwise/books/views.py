from django_filters.views import FilterView

from books.filters import BookFilter


class BookList(FilterView):
    filterset_class = BookFilter
    template_name = "books.html"
    context_object_name = "books"
    paginate_by = 40
