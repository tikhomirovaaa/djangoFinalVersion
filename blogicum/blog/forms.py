"""файл, в котором я описала формы для последующего их создания."""
from django import forms
from django.utils import timezone

from blog.models import Comment, Post


class PostForm(forms.ModelForm):
    """
    Форма для создания или редактирования постов.

    Атрибуты:
        - pub_date (datetime): Дата и время публикации поста,
          автоматически инициализируется текущим временем.
    """

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы.
        Параметры:
            - args: Позиционные аргументы - кортеж.
            - kwargs: Именованные аргументы - словарь.

        Устанавливает начальное значение поля 'pub_date' на текущее время.
        """
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['pub_date'].initial = timezone.now()

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'format': '%Y-%m-%dT%H:%M'
            }),
        }


class CommentForm(forms.ModelForm):
    """
    Форма для создания или редактирования комментариев.
    Атрибуты:
        - author (ForeignKey): Пользователь, оставляющий комментарий.
        - post (ForeignKey): Пост, к которому добавляется комментарий.
        - is_published (bool): Флаг, указывающий, опубликован ли комментарий.
    """

    class Meta:
        model = Comment
        exclude = ('author', 'post', 'is_published')
