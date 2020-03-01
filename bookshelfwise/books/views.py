from django.views.generic import UpdateView
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView
from django_filters.views import FilterView

from books.filters import BookFilter
from books.forms import BookAddEditForm
from books.models import Book


class BookList(FilterView):
    filterset_class = BookFilter
    template_name = "books.html"
    context_object_name = "books"
    paginate_by = 40


# many thanks to https://stackoverflow.com/questions/17192737/django-class-based-view-for-both-create-and-update
class BookCreateUpdate(SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    model = Book
    template_name = 'book-create-update.html'
    success_url = '/books'
    form_class = BookAddEditForm

    def get_object(self, queryset=None):
        try:
            return super().get_object()
        except AttributeError:
            return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)
