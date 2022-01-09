import shutil
import tempfile

from django.core.cache import cache
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from ..models import Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auser')
        cls.authorized_client = Client()
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст',
            group=cls.group,
        )
        cls.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        cls.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=cls.small_gif,
            content_type='image/gif'
        )
        cls.form_data = {
            'text': 'Тестовый_текст_1',
            'group': cls.group.pk,
            'image': cls.uploaded,
        }

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
        cache.clear()

    def setUp(self):
        self.authorized_client.force_login(self.user)

    def test_post_creation_form(self):
        """Проверяем, что при отправке валидной формы создается новая запись в БД
        и происходт редирект."""
        post_count = Post.objects.count()
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=self.form_data,
            follow=True,
        )
        post = Post.objects.order_by('pk').last()
        self.assertRedirects(response, reverse(
            'posts:profile', args=[self.user.username])
        )
        image_content = open(
            f'{TEMP_MEDIA_ROOT}/{post.image.name}',
            'rb'
        ).read()
        self.post.refresh_from_db()
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertEqual(
            post.text, self.form_data['text']
        )
        self.assertEqual(
            post.group.pk, self.form_data['group']
        )
        self.assertEqual(
            image_content, self.small_gif
        )
        self.assertTrue(
            Post.objects.filter(
                group=self.group.pk,
                text='Тестовый_текст_1',
                image='posts/small.gif'
            )
        )
