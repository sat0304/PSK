from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    """Таблица, содержащая группы пользователей."""
    title = models.CharField('Сообщество', max_length=200)
    slug = models.SlugField(
        unique=True,
        default='title'
    )
    description = models.TextField('Записи сообщества')

    class Meta:
        verbose_name_plural = 'Сообщества'

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    """Таблица, содержащая сообщения (посты) пользователей."""
    text = models.TextField(
        verbose_name='Текст поста',
        help_text='Введите текст поста'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='posts'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Группа',
        help_text='Выберите группу'
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = 'Публикации'

    def __str__(self) -> str:
        return self.text[:15]
