"""
Файл, в котором я описала модели приложения blog,
модели описывают структуру используемых данных
и определяют взаимодействие с базой данных.
"""
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Count
from django.utils import timezone

from core.models import CreatedAt, IsPublished

LENGTH_STRING = 20
MAX_LENGTH = 256

User = get_user_model()


class PublishedQuerySet(models.QuerySet):
    """
    Набор запросов для фильтрации опубликованных постов.

    Методы:
        - filter_posts_for_publication: Фильтрует посты, которые опубликованы и имеют дату публикации меньше
        или равную текущей дате.
        - count_comments: Аннотирует количество комментариев для постов и выполняет выборку связанных объектов.
    """

    def filter_posts_for_publication(self):
        """
        Фильтрует посты для публикации.

        Возвращает QuerySet, содержащий посты, которые:
         - опубликованы (is_published=True)
         - имеют дату публикации, равную или меньшую текущей дате
         - принадлежат опубликованной категории (category__is_published=True)
        """
        return self.filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__is_published=True,
        )

    def count_comments(self):
        """
        Подсчитывает количество комментариев к постам.

        Возвращает QuerySet, аннотированный количеством комментариев,
        связанным с постами. Также выбирает связанные объекты для уменьшения
        числа запросов к базе данных.

        Возвращает:
            QuerySet: Посты с количеством комментариев.
        """
        return self.select_related(
            'category', 'location', 'author'
        ).annotate(comment_count=Count('comments')).order_by('-pub_date')


class Category(CreatedAt, IsPublished):
    """
    Модель для категорий публикаций.

    Атрибуты:
        - title (str): Заголовок категории.
        - description (str): Описание категории.
        - slug (str): Уникальный слаг для идентификации категории в URL.

    Вложенный класс Meta:
        - verbose_name: Название категории в единственном числе.
        - verbose_name_plural: Название категории во множественном числе.
    """

    title = models.CharField('Заголовок', max_length=MAX_LENGTH)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        unique=True,
        help_text='Идентификатор страницы для URL; разрешены символы '
                  'латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """Возвращает отображаемое название категории (с обрезкой)."""
        return self.title[:LENGTH_STRING]


class Location(CreatedAt, IsPublished):
    """
    Модель для местоположений, связанных с публикациями.

    Атрибуты:
        - name (str): Название местоположения.

    Вложенный класс Meta:
        - verbose_name: Название местоположения в единственном числе.
        - verbose_name_plural: Название местоположения во множественном числе.
    """

    name = models.CharField('Название места', max_length=MAX_LENGTH)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        """Возвращает отображаемое название местоположения (с обрезкой)."""
        return self.name[:LENGTH_STRING]


class Post(CreatedAt, IsPublished):
    """
    Модель для публикаций в блоге.

    Атрибуты:
        - title (str): Заголовок поста.
        - text (str): Текст поста.
        - pub_date (datetime): Дата и время публикации поста.
        - author (User): Автор публикации.
        - location (Location): Местоположение, связанное с публикацией.
        - category (Category): Категория, к которой относится публикация.
        - image (ImageField): Изображение, связанное с постом.

    Вложенный класс Meta:
        - verbose_name: Название публикации в единственном числе.
        - verbose_name_plural: Название публикаций во множественном числе.
        - ordering: Порядок сортировки по дате публикации (по убыванию).

    Методы:
        - __str__: Возвращает заголовок поста (с обрезкой).
    """

    title = models.CharField('Заголовок', max_length=MAX_LENGTH)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text='Если установить дату и время в будущем'
                  ' — можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
        related_name='posts',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
        related_name='posts'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
        related_name='posts'
    )
    image = models.ImageField(
        'Фото', blank=True, upload_to='posts_images/', null=True
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date',)

    objects = PublishedQuerySet.as_manager()

    def __str__(self):
        """Возвращает заголовок публикации (с обрезкой)."""
        return self.title[:LENGTH_STRING]


class Comment(CreatedAt):
    """
    Модель комментариев к публикациям.

    Атрибуты:
        - text (str): Текст комментария.
        - post (Post): Пост, к которому относится комментарий.
        - author (User): Автор комментария.

    Вложенный класс Meta:
        - ordering: Порядок сортировки комментариев по дате создания.
        - verbose_name: Название комментария в единственном числе.
        - verbose_name_plural: Название комментариев во множественном числе.
    """

    text = models.TextField('Текст')
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        verbose_name='Пост',
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
        related_name='comments'
    )

    class Meta:
        ordering = ('created_at',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        """Возвращает текст комментария (с обрезкой)."""
        return self.text[:LENGTH_STRING]
