import copy
import json

from django.db import DataError
from django.test import TestCase, Client, TransactionTestCase, RequestFactory

from books.models import Book, Author, ISBN
from books.views import BookList, GoogleBookAPISearch

example_book_attrs = {
    "title": "Unique_Book_Title",
    "publication_date": "2020-03-01",
    "num_of_pages": 123,
    "link_to_cover": "https://en.wikipedia.org/wiki/Book#/media/File:Liji2_no_bg.png",
    "publication_lang": "en",
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
        self.factory = RequestFactory()
        self.req = self.factory.get(self.url)


class BookListRequestTypeTestCase(TestCase):
    c = Client()
    url = "/books/"

    def test_get_request_no_params_code_200(self):
        r = self.c.get(self.url)
        self.assertEqual(r.status_code, 200)

    def test_get_request_not_filter_params_code_200(self):
        r = self.c.get(self.url, {"param": "param"})
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


class BookListViewTestCase(RequestFactoryTests):
    c = Client()
    url = "/books/"
    filter_params = [
        "title__icontains",
        "publication_lang",
        "author",
        "from_date",
        "to_date",
    ]

    def setUp(self):
        super().setUp()
        self.view = BookList()
        self.view.setup(self.req)

    def test_context_object_name_books(self):
        self.assertIn("books", self.view.context_object_name)


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


class PrepareToSerializeTestCase(RequestFactoryTests):
    url = "/expand"
    test_json = json.loads(
        '{"volumeInfo": {"title": "Unique_Book_Title", "authors": ["Unique_Book_Author"], "publishedDate": "2020-03-01", "industryIdentifiers": [{"identifier": "1A2S3D4F5G6H"}], "pageCount": 123, "imageLinks": {"smallThumbnail": "https://en.wikipedia.org/wiki/Book#/media/File:Liji2_no_bg.png"}, "language": "en"}}'
    )
    keys = ["title", "author", "publication_date", "isbn", "num_of_pages", "link_to_cover", "publication_lang"]

    def setUp(self):
        super().setUp()
        self.view = GoogleBookAPISearch()
        self.view.setup(self.req)

    def test_correct_json_successful_conversion(self):
        volume_info = self.view.prepare_to_serialize(self.test_json)
        self.assertIsNotNone(volume_info)
        book_data = example_book_attrs.copy()
        book_data["author"] = [example_author_attrs]
        book_data["isbn"] = [example_isbn_attrs]
        for key in self.keys:
            self.assertIn(key, volume_info)
            self.assertEqual(book_data[key], volume_info[key])

    def test_json_missing_value_returns_none(self):
        for key in self.keys:
            temp_volume_info = copy.deepcopy(self.test_json)
            del temp_volume_info["volumeInfo"][key]
            self.assertIsNone(self.view.prepare_to_serialize(temp_volume_info))


class BookListEndpointContentTestCase(CreateOneInstanceEachTests):
    c = Client()
    url = "/api/books"
    filter_params = ['title', 'author', 'isbn']

    def setUp(self):
        super().setUp()
        self.query_params = [
            {"title": self.book.title},
            {"author": self.author.name},
            {"isbn": self.isbn.number},
        ]

    def assert_book_in_data(self, param):
        r_full = self.c.get(self.url, param)
        data = r_full.json()["results"][0]["id"]
        self.assertEqual(self.book.id, data)

    def test_single_filter_param_request_object_found(self):
        for param in self.query_params:
            self.assert_book_in_data(param)
            for key, val in param.items():
                partial_phrase = {key: val[:-1]}
                self.assert_book_in_data(partial_phrase)
                search_phrase = {"search": val}
                self.assert_book_in_data(search_phrase)
                partial_search_phrase = {"search": val[:-1]}
                self.assert_book_in_data(partial_search_phrase)
