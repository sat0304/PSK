from http import HTTPStatus

import shutil
import tempfile

from django.core.cache import cache
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from ..models import Comment, Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='HasNoName')
        cls.auth = User.objects.create_user(username='auser')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.auth,
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
        """Клиент неавторизован."""
        self.guest_client = Client()
        """Клиент авторизован."""
        self.authorized_client = Client()
        self.authorized_client.force_login(self.auth)

    def test_authorized_user_create_comment(self):
        """Авторизованный пользователь может комментировать посты"""
        comments_count = Comment.objects.count()
        post = Post.objects.create(
            text='Текст поста',
            author=self.auth)
        form_data = {'text': 'Тест коментарий'}
        response = self.authorized_client.post(
            reverse(
                'posts:add_comment',
                kwargs={'post_id': post.id}),
            data=form_data,
            follow=True)
        comment = Comment.objects.latest('id')
        self.assertEqual(Comment.objects.count(), comments_count + 1)
        self.assertEqual(comment.text, form_data['text'])
        self.assertEqual(comment.author, self.auth)
        self.assertEqual(comment.post_id, post.id)
        self.assertRedirects(
            response, reverse('posts:post_detail', args={post.id}))

    def test_nonauthorized_user_create_comment(self):
        """Неавторизованный пользователь не может создать комментарий"""
        comments_count = Comment.objects.count()
        post = Post.objects.create(
            text='Текст поста редактирования',
            author=self.user)
        form_data = {'text': 'Тест коментарий'}
        response = self.client.post(
            reverse(
                'posts:add_comment',
                kwargs={'post_id': post.id}),
            data=form_data,
            follow=True)
        redirect = reverse('login') + '?next=' + reverse(
            'posts:add_comment', kwargs={'post_id': post.id})
        self.assertEqual(Comment.objects.count(), comments_count)
        self.assertRedirects(response, redirect)

    def test_comment_exist_on_post_page(self):
        """Комментарий появился на странице поста."""
        comment_count = Comment.objects.count()
        form_fields = {'text': 'Тестовый_комментарий'}
        response = self.authorized_client.post(
            reverse('posts:add_comment', args={self.post.id}),
            data=form_fields,
            follow=True
        )
        if (response.status_code == HTTPStatus.OK):
            comment_new = Post.objects.count()
            self.assertEqual(comment_new, comment_count + 1)
            self.assertTrue(Comment.objects.filter(
                text='Тестовый_комментарий').exists()
            )
