from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),

    # 1. Перенаправление с корня на список проектов (чтобы сайт открывался по /)
    path('', lambda request: redirect('projects:project_list'), name='home'),

    # 2. Подключаем проекты с префиксом 'projects/' (чтобы работали твои шаблоны и JS)
    path('projects/', include('projects.urls')),

    # 3. Пользователи (оставляем как было)
    path('users/', include('users.urls')),
]

# Настройка для отдачи медиа-файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
