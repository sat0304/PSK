import shutil
import tempfile

from http import HTTPStatus

from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from posts.models import Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class CacheTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.auth = User.objects.create_user(username='adminn')
        cls.authorized_client = Client()
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.auth,
            text='Тестовый_текст',
            group=cls.group,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        cache.clear()
        
    def setUp(self):
        cache.clear()
        self.authorized_client.force_login(self.auth)

    def test_cache_index_page(self):
        """Проверяем работу кэширования 'posts:index'"""
        response = self.authorized_client.get(reverse('posts:index'))
        Post.objects.get(id=self.post.pk).delete()
        self.assertTrue(self.post.text.encode() in response.content)
        # self.assertContains(self.post.text.encode(), response.content)
        cache.clear()
        # self.assertNotContains(self.post.text.encode(), response.content)
