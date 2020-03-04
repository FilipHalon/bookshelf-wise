from django.db import DataError
from django.db.transaction import TransactionManagementError
from django.test import TestCase, Client, TransactionTestCase
from rest_framework.test import APIClient

from books.models import Book, Author, ISBN


# def test_get_request_no_params_code_200(self):
#     r = self.c.get(self.url)
#     self.assertEqual(r.status_code, 200)


class BookListRequestTypeTestCase(TestCase):
    def setUp(self):
        self.c = Client()
        self.url()

    def test_get_request_no_params_code_200(self):
        r = self.c.get('/books/')
        self.assertEqual(r.status_code, 200)

    def test_get_request_not_filter_params_code_200(self):
        r = self.c.get('/books/', {'param': 'param'})
        self.assertEqual(r.status_code, 200)

    def test_post_request_status_405(self):
        r = self.c.post('/books/')
        self.assertEqual(r.status_code, 405)

    def test_patch_request_status_405(self):
        r = self.c.patch('/books/')
        self.assertEqual(r.status_code, 405)

    def test_put_request_status_405(self):
        r = self.c.put('/books/')
        self.assertEqual(r.status_code, 405)


class BookModelsTestCase(TransactionTestCase):
    def setUp(self):
        self.book_attrs = {
            "title": "Book",
            "publication_date": "2020-03-01",
            "num_of_pages": 123,
            "link_to_cover": "https://en.wikipedia.org/wiki/Book#/media/File:Liji2_no_bg.png",
            "publication_lang": "en"
        }
        # self.book = Book.objects.create(**self.book_attrs)
        # self.author = Author.objects.create(name="Author")
        # self.isbn = ISBN.objects.create(number="1234567890")
        self.book = Book(**self.book_attrs)
        self.author = Author(name="Author")
        self.isbn = ISBN(number="1234567890")

    def tearDown(self):
        if self.book.pk:
            self.book.delete()
        # self.author.delete()
        # self.isbn.delete()

    def test_book_title_char_length_data_error(self):
        self.book.title = "a" * 257
        self.assertRaises(DataError)
        self.book.title = "a" * 256
        self.assertEqual(self.book.title, "a" * 256)

    def test_book_title_int_instead_of_str_no_errors(self):
        self.book.title = 1
        self.book.save()
        self.assertTrue(self.book.pk)
        self.assertTrue(self.book.__str__(), "1")


# class BookListEndpointTestCase(TestCase):
#     def setUp(self):
#         self.c = APIClient()

