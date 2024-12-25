from django.shortcuts import render
from django.views.generic import TemplateView


class AboutView(TemplateView):
    """Представление для страницы 'О нас'.
    Использует шаблон 'pages/about.html' для отображения информации о проекте.
    """

    template_name = 'pages/about.html'


class RulesView(TemplateView):
    """Представление для страницы 'Правила'.
    Использует шаблон 'pages/rules.html' для отображения правил использования проекта.
    """

    template_name = 'pages/rules.html'


def page_not_found(request, *args, **kwargs):
    """Обработка 404 ошибки (Страница не найдена).
    Возвращает шаблон 'pages/404.html' с кодом статуса 404,
    который отображается при отсутствии запрашиваемой страницы.
    """

    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, *args, **kwargs):
    """Обработка ошибки CSRF (403 ошибка).
    Возвращает шаблон 'pages/403csrf.html' с кодом статуса 403,
    который отображается при нарушении проверки CSRF токена.
    """

    return render(request, 'pages/403csrf.html', status=403)


def internal_error(request, *args, **kwargs):
    """Обработка 500 ошибки (Внутренняя ошибка сервера).
    Возвращает шаблон 'pages/500.html' с кодом статуса 500,
    который отображается при возникновении внутренней ошибки сервера.
    """

    return render(request, 'pages/500.html', status=500)
