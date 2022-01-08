import shutil
import tempfile

from http import HTTPStatus

from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django import forms

from posts.models import Group, Follow, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class FollowTests(TestCase):
    """ Тест страниц сайта."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.user2 = User.objects.create_user(username='test_user2')
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
        cls.follow_count = Follow.objects.count()
        cls.follow = Follow.objects.create(
            user=cls.user,
            author=cls.auth,
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
        """Клиент авторизован  и подписывается на автора."""
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        """Клиент авторизован но не подписывается на автора."""
        self.authorized_client2 = Client()
        self.authorized_client2.force_login(self.user)
        """Автор авторизован."""
        self.authorized_author = Client()
        self.authorized_author.force_login(self.auth)

    def test_authorized_user_follow (self):
        """Клиент авторизован и может подписываться на автора."""
        author = self.auth
        response = self.authorized_client.get(
            reverse(
                'posts:profile_follow',
                kwargs={'username': author.username}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Follow.objects.count(), self.follow_count + 1)
        self.assertTrue(Follow.objects.filter(
            user=self.user, author=author).exists()
        )

    def test_authorized_user_following_exists (self):
        """Клиент авторизован и подписка на автора появилась в ленте."""
        author = self.auth
        response = self.authorized_client.get(reverse('posts:follow_index'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Follow.objects.count(), self.follow_count + 1)
        self.assertTrue(Follow.objects.filter(
            user=self.user, author=author).exists()
        )

    def test_authorized_user_following_not_exists (self):
        """Клиент авторизован но подписка на 
        автора не появилась в ленте."""
        author = self.auth
        response = self.authorized_client2.get(reverse('posts:follow_index'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Follow.objects.count(), self.follow_count + 1)
        self.assertFalse(Follow.objects.filter(
            user=self.user2, author=author).exists()
        )

    def test_authorized_user_unfollow (self):
        """Клиент авторизован и может отписаться от автора."""
        author = self.auth
        response = self.authorized_client.get(
            reverse(
                'posts:profile_unfollow',
                kwargs={'username': author.username}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Follow.objects.count(), self.follow_count)
        self.assertFalse(Follow.objects.filter(
            user=self.user, author=author).exists()
        )
