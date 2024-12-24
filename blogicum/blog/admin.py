"""
Этот файл я сделала, чтобы он отвечал за настройку административной панели Django для модели блога.
Он предоставляет интерфейс для управления четырьмя основными моделями проекта:
Post (посты), Category (категории), Location (местоположения) и Comment (комментарии).

Пользователи с правами администратора могут добавлять, редактировать и удалять записи в этих моделях,
а также настраивать, какие поля отображаются, как они могут быть отредактированы,
и как данные можно фильтровать и искать в админском интерфейсе.

Функции и классы определяют следующие аспекты:
- Настройку отображаемых полей и их редактируемости для каждой модели.
- Опции фильтрации, чтобы упростить поиск нужной информации.
- Обработка и отображение сокращенных текстовых представлений для длинных
строк, чтобы улучшить читаемость интерфейса администрирования.
"""
from django.contrib import admin
from .models import Category, Comment, Location, Post

LENGTH_STRING = 50  # Максимальная длина строки для отображения
NUMBER_OF_POSTS = 10  # Количество постов на странице в админке


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Кастомизация админки для модели Post."""

    list_display = (
        'title',  # Поле для отображения заголовка поста
        'text_short',  # Поле для отображения короткой версии текста
        'location',  # Поле для отображения местоположения
        'category',  # Поле для отображения категории поста
        'pub_date',  # Поле для отображения даты публикации
        'is_published',  # Поле для отображения статуса публикации
    )

    list_editable = (
        'location',  # Поле местоположения доступно для редактирования
        'category',  # Поле категории доступно для редактирования
        'pub_date',  # Дата публикации доступна для редактирования
        'is_published',  # Статус публикации доступен для редактирования
    )

    search_fields = (
        'title',  # Поля, по которым можно осуществлять поиск
        'text',  # Текст поста для поиска
        'location',  # Местоположение для поиска
    )

    list_per_page = NUMBER_OF_POSTS  # Количество постов на странице

    @staticmethod
    @admin.display(description='Текст')
    def text_short(object: Post) -> str:
        """Возвращает сокращенную версию текста поста."""
        return f'{object.text[:LENGTH_STRING]}...'  # Сокращает текст до определенной длины


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Кастомизация админки для модели Category."""

    list_display = (
        'title',  # Поле для отображения названия категории
        'description_short',  # Поле для отображения короткого описания
        'slug',  # Поле для отображения слага
        'is_published',  # Поле для отображения статуса публикации
        'created_at',  # Поле для отображения даты создания
    )

    list_editable = (
        'slug',  # Поле слага доступно для редактирования
    )

    list_filter = (
        'title',  # Фильтрация по названию категории
        'description',  # Фильтрация по описанию категории
    )

    list_per_page = NUMBER_OF_POSTS  # Количество категорий на странице

    @staticmethod
    @admin.display(description='Описание')
    def description_short(object: Category) -> str:
        """Возвращает сокращенную версию описания категории."""
        return f'{object.description[:LENGTH_STRING]}...'  # Сокращает описание до определенной длины


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Кастомизация админки для модели Location."""

    list_display = (
        'name',  # Поле для отображения названия местоположения
        'is_published',  # Поле для отображения статуса публикации
        'created_at',  # Поле для отображения даты создания
    )

    list_editable = (
        'is_published',  # Поле статуса публикации доступно для редактирования
    )

    list_filter = (
        'name',  # Фильтрация по названию местоположения
    )

    list_per_page = NUMBER_OF_POSTS  # Количество местоположений на странице


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Кастомизация админки для модели Comment."""

    list_display = (
        'text',  # Поле для отображения текста комментария
        'post',  # Поле для отображения связанного поста
        'author',  # Поле для отображения автора комментария
        'created_at',  # Поле для отображения даты создания комментария
    )

    list_filter = (
        'text',  # Фильтрация по тексту комментария
    )

    list_per_page = NUMBER_OF_POSTS  # Количество комментариев на странице
