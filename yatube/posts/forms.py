from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        help_texts = {
            'text': 'Здесь Вы можете напечатать все, что Вы думаете об этом',
            'group': 'Выберете название сообщества для публикации',
        }
