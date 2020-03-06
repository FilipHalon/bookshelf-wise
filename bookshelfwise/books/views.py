import operator
from functools import reduce

import requests
from django.db.models import Q
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
from books.models import Book
from books.serializers import BookSerializer


def index(request):
    return render(request, "index.html")


class BookList(FilterView):
    filterset_class = BookFilter
    template_name = "books.html"
    context_object_name = "books"
    paginate_by = 10


# great many thanks for get, post and get_object to
# https://stackoverflow.com/questions/17192737/django-class-based-view-for-both-create-and-update
class BookCreateUpdate(
    SingleObjectTemplateResponseMixin, ModelFormMixin, ProcessFormView
):
    model = Book
    template_name = "book-create-update.html"
    success_url = "/books"
    form_class = BookCreateUpdateForm

    def create_or_update_object(self, data):
        author_list = Book.get_m2m_id_list("filter_form", data, "author")
        isbn_list = Book.get_m2m_id_list("filter_form", data, "isbn")
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

    def get_object(self, queryset=None):
        try:
            return super().get_object()
        except AttributeError:
            return None

    def form_valid(self, form):
        data = self.request.POST.copy()
        self.create_or_update_object(data)
        return HttpResponseRedirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class GoogleBookAPISearch(View):
    @staticmethod
    def prepare_to_serialize(volume):
        try:
            volume_info = volume["volumeInfo"]
            authors = volume_info.pop("authors")
            author_list = [{"name": author} for author in authors]
            volume_info["author"] = author_list
            volume_info["publication_date"] = volume_info.pop("publishedDate")
            isbns = volume_info.pop("industryIdentifiers")
            isbn_list = [{"number": identifier["identifier"]} for identifier in isbns]
            volume_info["isbn"] = isbn_list
            if volume_info.get("pageCount"):
                volume_info["num_of_pages"] = volume_info.pop("pageCount")
            else:
                volume_info["num_of_pages"] = 0
            volume_info["link_to_cover"] = volume_info.pop("imageLinks")[
                "smallThumbnail"
            ]
            volume_info["publication_lang"] = volume_info.pop("language")
        except KeyError:
            return None
        return volume_info

    @staticmethod
    def construct_url(cleaned_data):
        url = "https://www.googleapis.com/books/v1/volumes"
        q = cleaned_data.pop("q")
        url += f"?q={q}"
        for key, val in cleaned_data.items():
            if val:
                url += f"+{key}:{val}"
        url += (
            "&fields=items(volumeInfo(title, authors, publishedDate,"
            " industryIdentifiers(identifier), pageCount, language, imageLinks(smallThumbnail)))"
        )
        return url

    def get(self, request):
        form = GoogleBookAPISearchForm()
        return render(request, "google-book-api-search.html", {"form": form})

    def post(self, request):
        form = GoogleBookAPISearchForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            url = self.construct_url(cleaned_data)
            resp = requests.get(url).json()
            if resp:
                volumes = resp.json()["items"]
                for volume in volumes:
                    volume_info = self.prepare_to_serialize(volume)
                    if volume_info:
                        serializer = BookSerializer(data=volume_info)
                        if serializer.is_valid():
                            serializer.save()
        return redirect(reverse("expand"))


class BookAPIList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "title",
        "author__name",
        "publication_date",
        "isbn__number",
        "num_of_pages",
        "publication_lang",
    ]

    def filter_queryset(self, queryset):
        query_params = self.request.query_params
        if "title" in query_params and queryset:
            # many thank for the solution to
            # https://stackoverflow.com/questions/4824759/django-query-using-contains-each-value-in-a-list
            queryset = Book.objects.filter(
                reduce(
                    operator.or_,
                    (Q(title__icontains=phrase) for phrase in query_params["title"]),
                )
            )
        if "author" in query_params and queryset:
            queryset = Book.objects.filter(
                reduce(
                    operator.or_,
                    (
                        Q(author__name__icontains=phrase)
                        for phrase in query_params["author"]
                    ),
                )
            )
        if "isbn" in query_params and queryset:
            queryset = Book.objects.filter(
                reduce(
                    operator.or_,
                    (
                        Q(isbn__number__icontains=phrase)
                        for phrase in query_params["isbn"]
                    ),
                )
            )
        return super().filter_queryset(queryset)
