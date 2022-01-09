import shutil
import tempfile

from http import HTTPStatus

from django.core.cache import cache
from django.conf import settings
from django.test import Client, TestCase, override_settings

from posts.models import Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostURLTests(TestCase):
    """ Тест страниц сайта."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.auth = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.auth,
            text='Тестовый_текст',
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        cache.clear()

    def setUp(self):
        cache.clear()
        """Клиент неавторизован."""
        self.guest_client = Client()
        """Клиент авторизован."""
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_author = Client()
        self.authorized_author.force_login(self.auth)
        self.edit = '/edit/'

    def test_url_exists_at_desired_location_auth(self):
        """URL-адрес существует для автора поста."""
        templates_url_names = {
            settings.HOME_PAGE: HTTPStatus.OK,
            f'{settings.GROUP}{self.group.slug}/': HTTPStatus.OK,
            f'{settings.PROFILE}{self.post.author}/': HTTPStatus.OK,
            f'{settings.POSTS}{self.post.pk}/': HTTPStatus.OK,
            f'{settings.POSTS}{self.post.pk}{self.edit}': HTTPStatus.OK,
            f'{settings.CREATE}': HTTPStatus.OK,
            'unexist.html': HTTPStatus.NOT_FOUND,
        }
        for template, status in templates_url_names.items():
            with self.subTest(status=status):
                response = self.authorized_author.get(template)
                self.assertEqual(response.status_code, status)

    def test_url_exists_at_desired_location_user(self):
        """URL-адрес существует для зарегистрированного."""
        templates_url_names = {
            settings.HOME_PAGE: HTTPStatus.OK,
            f'{settings.GROUP}{self.group.slug}/': HTTPStatus.OK,
            f'{settings.PROFILE}{self.post.author}/': HTTPStatus.OK,
            f'{settings.POSTS}{self.post.pk}/': HTTPStatus.OK,
            f'{settings.POSTS}{self.post.pk}{self.edit}': HTTPStatus.FOUND,
            f'{settings.CREATE}': HTTPStatus.OK,
            'unexist.html': HTTPStatus.NOT_FOUND,
        }
        for template, status in templates_url_names.items():
            with self.subTest(status=status):
                response = self.authorized_client.get(template)
                self.assertEqual(response.status_code, status)

    def test_url_exists_at_desired_location_not_auth(self):
        """URL-адрес существует для незарегистрированного."""
        templates_url_names = {
            settings.HOME_PAGE: HTTPStatus.OK,
            f'{settings.GROUP}{self.group.slug}/': HTTPStatus.OK,
            f'{settings.PROFILE}{self.post.author}/': HTTPStatus.FOUND,
            f'{settings.POSTS}{self.post.pk}/': HTTPStatus.OK,
            f'{settings.POSTS}{self.post.pk}{self.edit}': HTTPStatus.FOUND,
            f'{settings.CREATE}': HTTPStatus.FOUND,
            'unexist.html': HTTPStatus.NOT_FOUND,
        }
        for template, status in templates_url_names.items():
            with self.subTest(status=status):
                response = self.guest_client.get(template)
                self.assertEqual(response.status_code, status)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            'posts/index.html': settings.HOME_PAGE,
            'posts/group_list.html': f'{settings.GROUP}{self.group.slug}/',
            'posts/profile.html': f'{settings.PROFILE}{self.post.author}/',
            'posts/post_detail.html': f'{settings.POSTS}{self.post.pk}/',
            'posts/create_post.html' or 'posts/update_post.html':
                f'/posts/{self.post.pk}{self.edit}',
            'posts/create_post.html': f'{settings.CREATE}',
        }
        for template, adress in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)
