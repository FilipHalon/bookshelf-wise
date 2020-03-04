from django.db import DataError
from django.test import TestCase, Client, TransactionTestCase, RequestFactory
from rest_framework.test import APIClient

from books.models import Book, Author, ISBN

example_book_attrs = {
            "title": "Unique_Book_Title",
            "publication_date": "2020-03-01",
            "num_of_pages": 123,
            "link_to_cover": "https://en.wikipedia.org/wiki/Book#/media/File:Liji2_no_bg.png",
            "publication_lang": "en"
        }

example_author_attrs = {"name": "Unique_Book_Author"}
example_isbn_attrs = {"number": "1A2S3D4F5G6H"}


class CreateOneInstanceEachTests(TestCase):
    def setUp(self):
        self.book = Book.objects.create(**example_book_attrs)
        self.isbn = ISBN.objects.create(**example_isbn_attrs)
        self.author = Author.objects.create(**example_author_attrs)
        self.book.author.add(self.author)
        self.book.isbn.add(self.isbn)

    def tearDown(self):
        self.book.delete()
        self.isbn.delete()
        self.author.delete()


class RequestFactoryTests(CreateOneInstanceEachTests):
    def setUp(self):
        super().setUp()


class BookListRequestTypeTestCase(TestCase):
    c = Client()
    url = "/books/"

    def test_get_request_no_params_code_200(self):
        r = self.c.get(self.url)
        self.assertEqual(r.status_code, 200)

    def test_get_request_not_filter_params_code_200(self):
        r = self.c.get(self.url, {'param': 'param'})
        self.assertEqual(r.status_code, 200)

    def test_post_request_status_405(self):
        r = self.c.post(self.url)
        self.assertEqual(r.status_code, 405)

    def test_patch_request_status_405(self):
        r = self.c.patch(self.url)
        self.assertEqual(r.status_code, 405)

    def test_put_request_status_405(self):
        r = self.c.put(self.url)
        self.assertEqual(r.status_code, 405)


class BookListViewTestCase(BookListRequestTypeTestCase):
    filter_params = ["title__icontains", "publication_lang", "author", "from_date", "to_date"]


class BookModelsTestCase(TransactionTestCase):
    def setUp(self):
        self.book = Book(**example_book_attrs)
        self.author = Author(**example_author_attrs)
        self.isbn = ISBN(**example_isbn_attrs)

    def tearDown(self):
        if self.book.pk:
            self.book.delete()

    def test_book_title_char_length_data_error(self):
        self.book.title = "a" * 257
        self.assertRaises(DataError)
        self.book.title = "a" * 256
        self.assertEqual(self.book.title, "a" * 256)

    def test_book_title_not_str_no_errors(self):
        self.book.title = 1
        self.book.save()
        self.assertTrue(self.book.pk)
        self.assertTrue(self.book.__str__(), "1")


class BookListEndpointTestCase(BookListRequestTypeTestCase):
    c = APIClient()
    url = "/api/books"


class BookListEndpointViewTestCase(RequestFactoryTests):
    filter_params = ['title', 'author', 'isbn']
    search_param = "search"

    def setUp(self):
        super().setUp()
        self.query_params = [
            {"title": self.book.title},
            {"author": self.author.name},
            {"isbn": self.isbn.number}
        ]

    # def test_filter_params_full_phrase_find_object(self):
    #     for param in self.query_params:
    #         r = self.c.get(self.url, param)
    #         print(r)
