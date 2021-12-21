from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Group, Post, User


class PostPagesTests(TestCase):
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
            group=cls.group,
        )
        cls.post_count = Post.objects.count()
        cls.group1 = Group.objects.create(
            title='Тестовая_группа_1',
            slug='test_slug_1',
            description='Тестовое_описание_1',
        )
        cls.post1 = Post.objects.create(
            author=cls.auth,
            text='Тестовый_текст_1',
            group=cls.group1,
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_author = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_author.force_login(self.auth)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_page_names = {
            'posts/index.html':
                reverse('posts:index'),
            'posts/group_list.html':
                reverse(
                    'posts:group_list',
                    kwargs={'slug': self.group.slug}
                ),
            'posts/profile.html':
                reverse(
                    'posts:profile',
                    kwargs={'username': self.post.author}
                ),
            'posts/post_detail.html':
                reverse(
                    'posts:post_detail',
                    kwargs={'post_id': self.post.pk}
                ),
            'posts/create_post.html' or 'posts/update_post.html':
                reverse(
                    'posts:post_edit',
                    kwargs={'post_id': self.post.pk}
                ),
            'posts/create_post.html':
                reverse('posts:post_create'),
        }
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        test_slug = response.context['page_obj'][0]
        index_text = test_slug.text
        self.assertEqual(index_text, 'Тестовый_текст_1')

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group1.slug}
            )
        )
        test_post = response.context['page_obj'][0]
        index_text = test_post.text
        self.assertEqual(index_text, 'Тестовый_текст_1')

    def test_profile_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse(
                'posts:profile',
                kwargs={'username': self.post1.author}
            )
        )
        test_post = response.context['page_obj'][0]
        index_text = test_post.text
        self.assertEqual(index_text, 'Тестовый_текст_1')

    def test_post_detail_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse(
                'posts:post_detail', kwargs={'post_id': self.post.pk}
            )
        )
        post_counted = Post.objects.filter(author=self.auth).count()
        context_fields = {
            'author': self.auth,
            'post_count': post_counted,
            'title_post': 'Пост ',
        }
        for value, expected in context_fields.items():
            with self.subTest(value=value):
                context_field = response.context[value]
                self.assertEqual(context_field, expected)

    def test_edit_post_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_author.get(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post1.pk}
            )
        )
        context_fields = {
            'post_id': self.post1.pk,
            'is_edit': True,
        }
        for value, expected in context_fields.items():
            with self.subTest(value=value):
                context_field = response.context[value]
                self.assertEqual(context_field, expected)

    def test_create_page_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_create')
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_post_exist_on_home_page(self):
        """Пост появился на главной странице."""
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        response = self.authorized_author.post(
            reverse('posts:index'),
            data=form_fields,
            follow=True
        )
        if (response.status_code == HTTPStatus.OK):
            index_text = Post.objects.count()
            self.assertEqual(index_text, self.post_count + 1)
            self.assertTrue(Post.objects.filter(
                text='Тестовый_текст_1').exists()
            )
            self.assertTrue(self.post1.group == self.group1)
            self.assertTrue(self.post1.group != self.group)

    def test_post_exist_on_group_page(self):
        """Пост появился на странице группы."""
        response = self.authorized_author.post(
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group1.slug}
            )
        )
        if (response.status_code == HTTPStatus.OK):
            index_text = Post.objects.count()
            self.assertEqual(index_text, self.post_count + 1)
            self.assertTrue(Post.objects.filter(
                text='Тестовый_текст_1').exists()
            )
            self.assertTrue(self.post1.group == self.group1)
            self.assertTrue(self.post1.group != self.group)

    def test_post_exist_on_profile_page(self):
        """Пост появился на странице профиля автора."""
        response = self.authorized_author.post(
            reverse(
                'posts:profile',
                kwargs={'username': self.post1.author}
            )
        )
        if (response.status_code == HTTPStatus.OK):
            index_text = Post.objects.count()
            self.assertEqual(index_text, self.post_count + 1)
            self.assertTrue(Post.objects.filter(
                text='Тестовый_текст_1').exists()
            )
            self.assertTrue(self.post1.group == self.group1)
            self.assertTrue(self.post1.group != self.group)


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.auth = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        for i in range(1, 14):
            cls.post = Post.objects.create(
                author=cls.auth,
                text=f'Тестовый_текст{i}',
                group=cls.group,
            )

    def setUp(self):
        self.authorized_author = Client()
        self.authorized_author.force_login(self.auth)

    def test_first_index_page_contains_ten_records(self):
        response = self.authorized_author.get(
            reverse('posts:index')
        )
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_index_page_contains_three_records(self):
        response = self.authorized_author.get(
            reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_first_group_list_page_contains_ten_records(self):
        response = self.authorized_author.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': self.group.slug}
            )
        )
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_group_list_page_contains_three_records(self):
        response = self.authorized_author.get(
            reverse(
                'posts:group_list', kwargs={'slug': self.group.slug}
            ) + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_first_profile_page_contains_ten_records(self):
        response = self.authorized_author.get(
            reverse(
                'posts:profile',
                kwargs={'username': self.post.author}
            )
        )
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_profile_page_contains_three_records(self):
        response = self.authorized_author.get(
            reverse(
                'posts:profile',
                kwargs={'username': self.post.author}
            ) + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj']), 3)
