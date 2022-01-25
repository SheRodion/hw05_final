from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls.base import reverse
from posts.models import Post, Group, Comment
from posts.forms import PostForm

User = get_user_model()


class PostCreateTest(TestCase):
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
        cls.form = PostForm()

    def setUp(self):
        self.guest_client = Client()
        self.author_client = Client()
        self.author_client.force_login(self.user)

    def test_create_form(self):
        """Создание поста при отправке валидной формы"""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый новый пост',
            'group': self.group.pk
        }
        response = self.author_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertRedirects(response, reverse(
            'posts:profile',
            kwargs={'username': self.user.username}))

    def test_edit_form(self):
        """Редактирование поста при отпрвке валидной формы"""
        posts_count = Post.objects.count()
        test_post = Post.objects.create(
            text='Новый посТ',
            author=self.user
        )
        form_data_edit = {
            'text': 'Измененный пост',
            'group': self.group.pk
        }
        response = self.author_client.post(
            reverse('posts:post_edit', kwargs={'post_id': test_post.pk}),
            data=form_data_edit)
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertRedirects(response, reverse(
            'posts:post_detail',
            kwargs={'post_id': test_post.pk}))
        self.assertTrue(
            Post.objects.filter(
                text='Измененный пост',
                group=self.group.pk,
            ).exists()
        )

    def test_comment(self):
        """Авторизованный может комментировать"""
        comment_count = Comment.objects.count()
        post_id = self.post.pk
        form_data = {
            'text': 'Новый комментарий',
        }
        response = self.author_client.post(
            reverse('posts:add_comment', kwargs={'post_id': post_id}),
            data=form_data,
            follow=True
        )
        self.assertEqual(Comment.objects.count(), comment_count + 1)
        self.assertTrue(Comment.objects.filter(
            text='Новый комментарий').exists()
        )
        self.assertRedirects(response, reverse(
            'posts:post_detail',
            kwargs={'post_id': post_id}))
