from http import HTTPStatus
from django.test import TestCase


class ViewTestClass(TestCase):
    def test_error_page(self):
        """Тестирование страницы 404"""
        pages_status_code = {
            '/unexisting_page/': HTTPStatus.NOT_FOUND,
        }
        for page, code in pages_status_code.items():
            with self.subTest(page=page, code=code):
                response = self.client.get(page)
                self.assertEqual(response.status_code, code)

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            '/unexisting_page/': 'core/404.html',
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress, template=template):
                response = self.client.get(adress)
                self.assertTemplateUsed(response, template)
