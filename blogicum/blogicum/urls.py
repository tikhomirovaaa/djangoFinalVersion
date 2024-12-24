"""
В этом файле у м еня находятся основные пути и ссылки
на приложения проекта, а также на страницу регистрации и выхода.
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('pages/', include('pages.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('auth/registration/', include('users.urls')),
]
"""Подключила к проекту кастомные страницы ошибок. """
handler403 = 'pages.views.csrf_failure'

handler404 = 'pages.views.page_not_found'

handler500 = 'pages.views.internal_error'

if settings.DEBUG:
    import debug_toolbar
    # Добавить к списку urlpatterns список адресов из приложения debug_toolbar:
    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)

# Добавляет URL-адреса для доступа к медиафайлам в режиме разработки.
# Это необходимо для правильного отображения загружаемых медиафайлов.
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
