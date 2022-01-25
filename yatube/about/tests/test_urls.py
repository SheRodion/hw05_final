from django.urls import reverse
from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_author_tech_pages(self):
        """Проверяем страницу автора и тех"""
        pages_status_code = {
            reverse('about:author'): HTTPStatus.OK,
            reverse('about:tech'): HTTPStatus.OK,
        }
        for page, code in pages_status_code.items():
            with self.subTest(page=page, code=code):
                response = self.guest_client.get(page)
                self.assertEqual(response.status_code, code.value)
