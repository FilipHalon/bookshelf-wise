from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView
from django_filters.views import FilterView

from books.filters import BookFilter
from books.forms import BookCreateUpdateForm
from books.models import Book, Author, ISBN


class BookList(FilterView):
    filterset_class = BookFilter
    template_name = "books.html"
    context_object_name = "books"
    paginate_by = 40


# great many thanks for get, post and get_object to https://stackoverflow.com/questions/17192737/django-class-based-view-for-both-create-and-update
class BookCreateUpdate(SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView):
    model = Book
    template_name = 'book-create-update.html'
    success_url = '/books'
    form_class = BookCreateUpdateForm

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

    def form_valid(self, form):
        data = self.request.POST.copy()
        authors = ''.join(data.get("author")).split(', ')
        author_list = []
        for author in authors:
            new_author = Author.objects.get_or_create(name=author)[0]
            author_list.append(new_author)
        isbns = ''.join(data.get("isbn")).split(', ')
        isbn_list = []
        for isbn in isbns:
            new_isbn = ISBN.objects.get_or_create(number=isbn)[0]
            isbn_list.append(new_isbn)
        if not self.object:
            self.object = Book()
        self.object.title = data.get("title")
        self.object.publication_date = data.get("publication_date")
        self.object.num_of_pages = data.get("num_of_pages")
        self.object.link_to_cover = data.get("link_to_cover")
        self.object.publication_lang = data.get("publication_lang")
        self.object.save()
        self.object.author.set(author_list)
        self.object.isbn.set(isbn_list)
        return HttpResponseRedirect(self.get_success_url())


class GoogleBookAPISearch(View):
    def get(self, request):
        return render(request, 'google-book-api-search.html')
