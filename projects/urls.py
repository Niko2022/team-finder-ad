from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    # Главная страница - список всех проектов
    path("", views.project_list, name="project_list"),
    # Страница избранных проектов
    path("favorites/", views.project_favorites, name="project_favorites"),
    # Редактирование проекта (должно быть ВЫШЕ чем project_detail!)
    path("<int:project_id>/edit/", views.edit_project, name="edit_project"),
    # AJAX: Добавить/удалить из избранного
    path(
        "<int:project_id>/toggle-favorite/",
        views.toggle_favorite,
        name="toggle_favorite",
    ),
    # AJAX: Присоединиться/покинуть проект
    path(
        "<int:project_id>/toggle-participate/",
        views.toggle_participate,
        name="toggle_participate",
    ),
    # AJAX: Завершить проект (только для автора)
    path("<int:project_id>/complete/", views.complete_project, name="complete_project"),
    # Детальная страница проекта (должна быть в конце!)
    path("<int:project_id>/", views.project_detail, name="project_detail"),
    # Создание нового проекта
    path("create-project/", views.create_project, name="create_project"),
]
