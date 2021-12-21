from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Group, Post, User


class AboutPagesTests(TestCase):
    """ Тест страниц сайта."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='test')
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

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_author = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_author.force_login(self.auth)

    def test_about_guest_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_page_names = {
            'about/author.html':
                reverse('about:author'),
            'about/tech.html':
                reverse('about:tech'),
        }
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.guest_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_about_registered_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_page_names = {
            'about/author.html':
                reverse('about:author'),
            'about/tech.html':
                reverse('about:tech'),
        }
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_about_author_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_page_names = {
            'about/author.html':
                reverse('about:author'),
            'about/tech.html':
                reverse('about:tech'),
        }
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_author.get(reverse_name)
                self.assertTemplateUsed(response, template)
