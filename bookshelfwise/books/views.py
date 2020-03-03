import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import ModelFormMixin, ProcessFormView
from django_filters.views import FilterView
from rest_framework import generics, filters

from books.filters import BookFilter
from books.forms import BookCreateUpdateForm, GoogleBookAPISearchForm
from books.models import Book, Author, ISBN
from books.serializers import BookSerializer


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
        form = GoogleBookAPISearchForm()
        return render(request, 'google-book-api-search.html', {'form': form})

    def post(self, request):
        url = "https://www.googleapis.com/books/v1/volumes"
        form = GoogleBookAPISearchForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            q = cleaned_data.pop("q")
            url += f"?q={q}"
            for key, val in cleaned_data.items():
                if val:
                    url += f"+{key}:{val}"
            url += "&fields=items(volumeInfo(title, authors, publishedDate, industryIdentifiers(identifier), pageCount, language, imageLinks(smallThumbnail)))"
            resp = requests.get(url)
            volumes = resp.json()['items']
            for volume in volumes:
                volume_info = volume["volumeInfo"]
                authors = volume_info.pop("authors")
                author_list = [{'name': author} for author in authors]
                volume_info['author'] = author_list
                volume_info['publication_date'] = volume_info.pop("publishedDate")
                isbns = volume_info.pop("industryIdentifiers")
                isbn_list = [{'number': identifier['identifier']} for identifier in isbns]
                volume_info['isbn'] = isbn_list
                volume_info['num_of_pages'] = volume_info.pop("pageCount")
                volume_info['link_to_cover'] = volume_info.pop("imageLinks")["smallThumbnail"]
                volume_info["publication_lang"] = volume_info.pop("language")
                serializer = BookSerializer(data=volume_info)
                if serializer.is_valid():
                    serializer.save()
        return redirect(reverse("expand"))


class BookAPIList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'author__name', 'publication_date', 'isbn__number', 'num_of_pages', 'publication_lang']
