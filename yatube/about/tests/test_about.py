from http import HTTPStatus

from django.test import Client, TestCase


class StaticURLTests(TestCase):
    """ Тест страниц сайта."""

    def setUp(self):
        """Клиент неавторизован."""
        self.guest_client = Client()

    def test_author(self):
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_tech(self):
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
