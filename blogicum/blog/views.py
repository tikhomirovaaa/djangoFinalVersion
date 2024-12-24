"""
Файл, в котором я описала представления,
которые нужны для реализации таких заданий как:
 добавление комментариев к публикации,
создание и удаление постов и так далее.
"""

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from .forms import CommentForm, PostForm
from .models import Category, Comment, Post

NUMBER_OF_POSTS = 10


class AuthorView(UserPassesTestMixin):
    """Класс, который проверяет является ли текущий пользователь автором."""

    def test_func(self):
        return self.get_object().author == self.request.user


class PostView(AuthorView, LoginRequiredMixin):
    """Представление для отображения постов."""

    model = Post
    template_name = 'blog/create.html'
    form_class = PostForm
    pk_url_kwarg = 'post_id'

    def handle_no_permission(self):
        """
        Обработка случая, когда у пользователя нет разрешения.
        Перенаправляет пользователя на страницу деталей постов.
        """
        return redirect('blog:post_detail',
                        self.kwargs[self.pk_url_kwarg])

    def get_success_url(self):
        """Возвращает URL для редиректа после успешного выполнения действий."""
        return reverse('blog:profile',
                       kwargs={'username': self.request.user.username})

    def get_context_data(self, **kwargs):
        """
        Возвращает контекст для шаблона,
        добавляя форму для работы с постом.
        """
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.get_object())
        return context


class CommentView(LoginRequiredMixin):
    """Представление для создания и редактирования комментариев."""

    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.kwargs['post_id']})


class IndexListView(ListView):
    """Представление для отображения списка постов на главной странице."""

    template_name = 'blog/index.html'
    paginate_by = NUMBER_OF_POSTS
    queryset = Post.objects.filter_posts_for_publication().count_comments()


class PostDetailView(ListView):
    """Представление для отображения деталей конкретного поста"""

    template_name = 'blog/detail.html'
    paginate_by = NUMBER_OF_POSTS

    def get_object(self):
        """
        Получает объект поста, связанным с данным идентификатором,
        проверяя права доступа.
        """
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        if self.request.user == post.author:
            return post
        return get_object_or_404(Post.objects.filter_posts_for_publication(),
                                 pk=self.kwargs['post_id'])

    def get_queryset(self):
        """Возвращает комментарии к конкретному посту."""
        return self.get_object().comments.all()

    def get_context_data(self, **kwargs):
        """
        Возвращает контекст для шаблона деталей поста, добавляя форму для
        комментария.
        """
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['post'] = self.get_object()
        return context


class PostUpdateView(PostView, UpdateView):
    """
    Представление для редактирования существующего поста.
    Наследует функционал PostView и UpdateView.
    """

    pass


class PostDeleteView(PostView, DeleteView):
    """
    Представление для удаления поста.
    Наследует функционал PostView и DeleteView.
    """

    pass


class CommentCreateView(CommentView, CreateView):
    """Представление для создания нового комментария к посту."""

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(
            Post.objects.filter_posts_for_publication(),
            pk=self.kwargs['post_id']
        )
        return super().form_valid(form)


class CreatePostView(LoginRequiredMixin, CreateView):
    """
    Представление для создания нового поста.
    Доступно только для авторизованных пользователей.
    """

    model = Post  # Модель, с которой будет работать представление
    form_class = PostForm  # Форма, используемая для создания поста
    template_name = 'blog/create.html'  # Шаблон для отображения

    def form_valid(self, form):
        """
        Вызывается, когда форма успешно проходит валидацию.
        Устанавливает текущего пользователя как автора поста.
        """
        form.instance.author = self.request.user
        # Присваивает текущего пользователя как автора
        return super().form_valid(form)
    # Продолжает с обработкой валидной формы

    def get_success_url(self):
        """
        Возвращает URL для перенаправления
        после успешного создания поста.
        """
        return reverse('blog:profile',
                       kwargs={'username': self.request.user.username})
    # Перенаправляет на профиль автора


class CommentUpdateView(CommentView, AuthorView, UpdateView):
    """
    Представление для редактирования комментария.
    Наследует функционал CommentView и AuthorView для проверки прав доступа.
    """


class CommentDeleteView(CommentView, AuthorView, DeleteView):
    """
    Представление для удаления комментария.
    Наследует функционал CommentView и AuthorView для проверки прав доступа.
    """


class CategoryDetailView(ListView):
    """Представление для отображения деталей определенной категории постов."""

    template_name = 'blog/category.html'
    paginate_by = NUMBER_OF_POSTS
    slug_url_kwarg = 'category_slug'

    def get_category(self):
        """
        Получает объект категории по переданному слагу и проверяет,
        что она опубликована.
        """
        return get_object_or_404(
            Category, slug=self.kwargs[self.slug_url_kwarg], is_published=True)

    def get_context_data(self, **kwargs):
        """
        Возвращает контекст для шаблона категории,
        добавляя информацию о категории.
        """
        context = super().get_context_data(**kwargs)
        context['category'] = self.get_category()
        return context

    def get_queryset(self):
        """
        Возвращает список постов, относящихся к данной категории,
        которые могут быть опубликованы.
        """
        return self.get_category().posts.filter_posts_for_publication()


class ProfileView(ListView):
    """Представление для отображения профиля пользователя."""

    template_name = 'blog/profile.html'
    paginate_by = NUMBER_OF_POSTS
    slug_url_kwarg = 'username'

    def get_profile(self):
        """
        Получает объект пользователя по имени пользователя,
        проверяя его существование.
        """
        return get_object_or_404(User, username=self.kwargs['username'])

    def get_queryset(self):
        """
        Возвращает посты, созданные пользователем.
        Если пользователь является текущим авторизованным пользователем,
        возвращает все посты, иначе - только опубликованные.
        """
        author = self.get_profile()
        posts = author.posts.count_comments()
        if author == self.request.user:
            return posts  # Возвращает все посты текущего пользователя
        # Возвращает только опубликованные посты для других пользователей
        return posts.filter_posts_for_publication()

    def get_context_data(self, **kwargs):
        """
        Возвращает контекст для шаблона профиля,
        добавляя информацию о пользователе.
        """
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_profile()
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Представление для редактирования профиля пользователя."""

    template_name = 'blog/user.html'
    fields = ('first_name', 'last_name', 'email')
    slug_url_kwarg = 'username'
    slug_field = 'username'

    def get_object(self, queryset=None):
        """
        Получает текущего авторизованного пользователя
        для редактирования.
        """
        return self.request.user

    def get_success_url(self):
        """
        Возвращает URL для редиректа после успешного
        редактирования профиля.
        """
        return reverse('blog:profile',
                       kwargs={'username': self.kwargs[self.slug_url_kwarg]})
