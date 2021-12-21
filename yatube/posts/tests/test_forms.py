from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User


class PostCreateFormTests(TestCase):
    """ Тест использования форм для создания постов."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.auth = User.objects.create_user(username='auth')
        cls.authorized_author = Client()
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.auth,
            text='Тестовый текст',
            group=cls.group,
        )

    def setUp(self):
        self.authorized_author.force_login(self.auth)

    def test_post_creation_forms(self):
        """Проверяем, что при отправке валидной формы создается
        новая запись в БД и происходт редирект."""
        post_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст_1',
            'group': self.group.id,
        }
        response = self.authorized_author.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(
            response, reverse(
                'posts:profile', args=['auth']
            )
        )
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(
            Post.objects.filter(text='Тестовый текст_1').exists()
        )

    def test_post_edit_forms(self):
        """Проверяем, что при редактировании меняется текст."""
        last_post = Post.objects.latest('id')
        response = self.authorized_author.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': self.post.pk}
            )
        )
        if (response.status_code == HTTPStatus.OK):
            form_data = {
                'text': 'Тестовый текст_2',
                'group': self.group.id,
                'is_edit': True
            }
            response = self.authorized_author.post(
                reverse('posts:post_create'),
                data=form_data,
                follow=True,
            )
            # print(self.post.text)
            # print(last_post.text)
            self.assertEqual(last_post.text, self.post.text)

    def test_post_edit(self):
        self.post = Post.objects.create(
            author=self.auth,
            text='Тестовый текст_3',
            group=self.group,
        )
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст_3',
            'group': self.group.id,
        }
        response = PostCreateFormTests.authorized_author.get(
            reverse('posts:post_edit', args=[self.post.pk]),
            data=form_data,
            follow=True
        )
        if (response.status_code == HTTPStatus.OK):
            self.assertEqual(self.post.text, 'Тестовый текст_3')
            self.assertEqual(Post.objects.count(), posts_count)
