from http import HTTPStatus

from django.test import Client, TestCase


class StaticURLTests(TestCase):
    """ Тест страниц сайта."""

    def setUp(self):
        """Клиент неавторизован."""
        self.guest_client = Client()

    def test_404(self):
        response = self.guest_client.get('/nonexist-page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
