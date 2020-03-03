from django.test import TestCase, Client


class BookListRequestTypeTestCase(TestCase):
    def setUp(self):
        self.c = Client()

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
