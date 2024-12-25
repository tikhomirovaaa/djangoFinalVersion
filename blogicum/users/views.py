"""
Этот файл у меня содержит представление для регистрации новых пользователей в приложении Django.
Используется класс `CreateView` для обработки создания нового пользователя через форму.
"""

from django.contrib.auth import get_user_model  # Импортируем модель пользователя
from django.contrib.auth.forms import UserCreationForm  # Импортируем форму для создания пользователя
from django.urls import reverse_lazy  # Импортируем функцию для обратной сериализации URL
from django.views.generic import CreateView  # Импортируем класс для создания представления


class UserCreateView(CreateView):
    """Представление для регистрации нового пользователя."""

    model = get_user_model()  # Получаем модель пользователя, используемую в проекте

    template_name = 'registration/registration_form.html'  # Шаблон для страницы регистрации

    form_class = UserCreationForm  # Форма, используемая для регистрации пользователей

    success_url = reverse_lazy('blog:index')  # URL-адрес, на который будет перенаправлен пользователь после успешной регистрации
