"""
В данном файле у меня описаны основные настройки для моего проекта.
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent  # Определяет базовую директорию проекта


# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--8^bwsu-l^(yfk+)r&e!+2(wbncaem$t2btk^@z0$h3w+c8yce'  # Секретный ключ для криптографических операций

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Включает режим отладки (не сохраняйте в продакшене)

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']  # Разрешенные хосты для вашего приложения

# Application definition
INSTALLED_APPS = [
    'blog.apps.BlogConfig',  # Приложение блога
    'pages.apps.PagesConfig',  # Приложение страниц
    'django.contrib.admin',  # Админ-панель Django
    'django.contrib.auth',  # Модуль аутентификации
    'django.contrib.contenttypes',  # Модуль для работы с типами контента
    'django.contrib.sessions',  # Поддержка сессий
    'django.contrib.messages',  # Поддержка сообщений
    'django.contrib.staticfiles',  # Статические файлы
    'debug_toolbar',  # Инструмент отладки
    'django_bootstrap5',  # Подключение Bootstrap 5
]

# Настройки медиафайлов
MEDIA_ROOT = BASE_DIR / 'media'  # Папка для хранения загружаемых медиафайлов
MEDIA_URL = 'media/'  # URL для доступа к медиафайлам

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Защита приложения
    'django.contrib.sessions.middleware.SessionMiddleware',  # Обработка сессий
    'django.middleware.common.CommonMiddleware',  # Общие промежуточные действия
    'django.middleware.csrf.CsrfViewMiddleware',  # Защита от CSRF-атак
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Аутентификация пользователя
    'django.contrib.messages.middleware.MessageMiddleware',  # Обработка сообщений
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Защита от Clickjacking
]

ROOT_URLCONF = 'blogicum.urls'  # Модуль с URL-ами приложения

TEMPLATES_DIR = BASE_DIR / 'templates'  # Директория для шаблонов

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Движок шаблонов Django
        'DIRS': [TEMPLATES_DIR],  # Директория для дополнительных шаблонов
        'APP_DIRS': True,  # Включает поиск шаблонов в директории приложений
        'OPTIONS': {
            'context_processors': [  # Контекстные процессоры
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blogicum.wsgi.application'  # WSGI-приложение для запуска проекта


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Движок базы данных (SQLite)
        'NAME': BASE_DIR / 'db.sqlite3',  # Путь к файлу базы данных
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',  # Проверка схожести паролей с атрибутами пользователей
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',  # Минимальная длина пароля
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',  # Проверка на распространенность пароля
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',  # Проверка на использование только цифр в пароле
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'  # Код языка приложения

TIME_ZONE = 'UTC'  # Часовой пояс

USE_I18N = True  # Включение интернационализации

USE_L10N = False  # Отключение локализации формата даты и времени

USE_TZ = True  # Включение поддержки временных зон


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'  # URL для доступа к статическим файлам

STATICFILES_DIRS = [
    BASE_DIR / 'static_dev'  # Директория для статических файлов во время разработки
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Тип первичного ключа для новых моделей


INTERNAL_IPS = [
    '127.0.0.1',  # Локальные IP-адреса для отладки
]

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'  # Используемый бэкенд для отправки почты (только для тестирования)

EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'  # Директория для хранения отправленных писем (в тестовом режиме)

CSRF_FAILURE_VIEW = 'pages.views.csrf_failure'  # Представление для обработки ошибок CSRF

LOGIN_REDIRECT_URL = 'blog:index'  # URL для перенаправления после успешной аутентификации пользователя
