from django.urls import reverse
from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from posts.models import Group, Post

User = get_user_model()


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='HasNoName')
        cls.group = Group.objects.create(
            title='Тестовое название группы',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст поста',
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.author_client = Client()
        self.author_client.force_login(self.user)
        self.user = User.objects.create_user(username='NewAuthor')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_exists_at_desired_location(self):
        """Страницы доступны любому пользователю"""
        pages_status_code = {
            reverse('posts:index'): HTTPStatus.OK,
            reverse('posts:group_list',
                    kwargs={'slug': self.group.slug}): HTTPStatus.OK,
            reverse('posts:profile',
                    kwargs={'username': self.user.username}): HTTPStatus.OK,
            reverse('posts:post_detail',
                    kwargs={'post_id': self.post.id}): HTTPStatus.OK,
            '/unexisting_page/': HTTPStatus.NOT_FOUND,
        }
        for page, code in pages_status_code.items():
            with self.subTest(page=page, code=code):
                response = self.guest_client.get(page)
                self.assertEqual(response.status_code, code)

    def test_post_create_exists_at_desired_location_authorized(self):
        """Страница /create/ доступна авторизованому."""
        pages_status = {
            reverse('posts:post_create'): HTTPStatus.OK,
        }
        for page, code in pages_status.items():
            with self.subTest(page=page, code=code):
                response = self.authorized_client.get(page)
                self.assertEqual(response.status_code, code)

    def test_post_edit_url_exists_at_desired_location(self):
        """Страница /posts/<int:post_id>/edit/ доступна автору."""
        pages_status = {
            reverse('posts:post_detail',
                    kwargs={'post_id': self.post.id}): HTTPStatus.OK,
        }
        for page, code in pages_status.items():
            with self.subTest(page=page, code=code):
                response = self.author_client.get(page)
                self.assertEqual(response.status_code, code)

    def test_post_create_redirect_anonymous_on_login(self):
        """Страница /create/ перенаправит анонимного
        пользователя на страницу логина."""
        pages_status = {
            reverse('posts:post_create'): HTTPStatus.FOUND,
        }
        for page, code in pages_status.items():
            with self.subTest(page='/auth/login/?next=/create/', code=code):
                response = self.guest_client.get(page)
                self.assertEqual(response.status_code, code)

    def test_post_edit_redirect_client_on_post_page(self):
        """Страница /posts/<int:post_id>/edit/ перенаправит неавтора поста
        на страницу поста.
        """
        pages_status = {
            reverse('posts:post_edit',
                    kwargs={'post_id': self.post.id}): HTTPStatus.FOUND,
        }
        for page, code in pages_status.items():
            with self.subTest(page=page, code=code):
                response = self.authorized_client.get(page)
                self.assertEqual(response.status_code, code)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': self.group.slug}):
            'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': self.user.username}):
            'posts/profile.html',
            reverse('posts:post_detail', kwargs={'post_id': self.post.id}):
            'posts/post_detail.html',
            reverse('posts:post_edit', kwargs={'post_id': self.post.id}):
            'posts/create_post.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            '/unexisting_page/': 'core/404.html',
        }
        for adress, template in templates_url_names.items():
            with self.subTest(adress=adress, template=template):
                response = self.author_client.get(adress)
                self.assertTemplateUsed(response, template)
