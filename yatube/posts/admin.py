from django.contrib import admin

from .models import Group

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Перечисляем поля, которые должны отображаться в админке."""
    list_display = ('pk', 'text', 'pub_date', 'author', 'group')
    """Добавляем интерфейс для поиска по тексту постов."""
    search_fields = ('text',)
    """Добавляем поле редактирования групп."""
    list_editable = ('group',)
    """Добавляем возможность фильтрации по дате."""
    list_filter = ('pub_date',)
    """Добавляем значение для пустого поля."""
    empty_value_display = '-пусто-'


"""@admin.register(Group)."""
"""При регистрации модели Post источником конфигурации для неё назначаем
класс PostAdmin. admin.site.register(Post, PostAdmin)."""
"""Pегистрация модели Group."""
admin.site.register(Group)
