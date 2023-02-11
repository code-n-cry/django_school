from django.test import TestCase, Client


class StaticUrlTests(TestCase):
    def test_catalog_endpoint(self):
        right_response_1 = Client().get('/catalog/')
        right_response_2 = Client().get('/catalog/1')
        error_response = Client().get('/catalog/hmmm')
        self.assertEqual(right_response_1.status_code, 200)
        self.assertEqual(right_response_2.status_code, 200)
        self.assertEqual(error_response.status_code, 404)
