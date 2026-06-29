from http import HTTPStatus

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import Project
from .forms import ProjectForm


def get_paginated_queryset(queryset, request, per_page=12):
    """
    Вспомогательная функция для пагинации.
    Возвращает объекты с разбивкой по страницам.
    """
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)


def project_list(request):
    """Главная страница: список проектов с пагинацией"""
    projects = Project.objects.select_related("owner").all().order_by("-created_at")
    projects_page = get_paginated_queryset(projects, request, per_page=12)

    return render(
        request,
        "projects/project_list.html",
        {
            "projects": projects_page,
            # Для навигации пагинации в шаблоне
            "page_obj": projects_page,
        },
    )


def project_detail(request, project_id):
    """Страница проекта"""
    # Выбираем проект вместе с автором и участниками
    project = get_object_or_404(
        Project.objects.select_related("owner").prefetch_related("participants"),
        pk=project_id,
    )

    return render(request, "projects/project-details.html", {"project": project})


@login_required
def toggle_participate(request, project_id):
    """Присоединиться/отказаться от участия в проекте"""
    if request.method != "POST":
        return JsonResponse({"status": "error"}, status=HTTPStatus.METHOD_NOT_ALLOWED)

    project = Project.objects.filter(pk=project_id).first()
    if project is None:
        return JsonResponse({"error": "Проект не найден"}, status=HTTPStatus.NOT_FOUND)
    user = request.user

    is_participating = project.participants.filter(pk=user.pk).exists()

    if is_participating:
        # Автор не может покинуть свой проект
        if project.owner == user:
            return JsonResponse(
                {"error": "Автор не может покинуть свой проект  "},
                status=HTTPStatus.FORBIDDEN,
            )
        project.participants.remove(user)
    else:
        project.participants.add(user)

    # Вычисляем новое состояние один раз, без дублирования в ветках
    participating = not is_participating

    return JsonResponse(
        {
            "status": "ok",
            "participating": participating,
            "participants_count": project.participants.count(),
        }
    )


@login_required
def complete_project(request, project_id):
    """Завершить проект (только для владельца)"""
    if request.method != "POST":
        return JsonResponse({"status": "error"}, status=HTTPStatus.METHOD_NOT_ALLOWED)

    project = Project.objects.filter(pk=project_id, owner=request.user).first()
    if project is None:
        return JsonResponse(
            {"error": "Проект не найден или доступ запрещён"},
            status=HTTPStatus.NOT_FOUND,
        )

    # Проверка прав: только владелец может закрыть
    if project.owner != request.user:
        return JsonResponse(
            {"error": "Доступ запрещён. Только владелец может завершить проект"},
            status=HTTPStatus.FORBIDDEN,
        )

    if project.status == "open":
        project.status = "closed"
        project.save()
        return JsonResponse({"status": "ok", "project_status": "closed"})

    return JsonResponse(
        {"status": "error", "message": "Проект уже закрыт"},
        status=HTTPStatus.BAD_REQUEST,
    )


@login_required
def toggle_favorite(request, project_id):
    """Добавить/удалить проект из избранного (AJAX)"""
    if request.method != "POST":
        return JsonResponse({"status": "error"}, status=HTTPStatus.METHOD_NOT_ALLOWED)

    project = Project.objects.filter(pk=project_id).first()
    if project is None:
        return JsonResponse({"error": "Проект не найден"}, status=HTTPStatus.NOT_FOUND)
    user = request.user

    is_favorited = user.favorites.filter(pk=project_id).exists()

    if is_favorited:
        user.favorites.remove(project)
    else:
        user.favorites.add(project)

    favorited = not is_favorited

    return JsonResponse({"status": "ok", "favorited": favorited})


@login_required
def create_project(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)

        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()

            project.participants.add(request.user)

            return redirect("projects:project_detail", project_id=project.id)
        else:
            print("Ошибки:", form.errors)
    else:
        form = ProjectForm()

    return render(
        request, "projects/create-project.html", {"form": form, "is_edit": False}
    )


@login_required
def edit_project(request, project_id):
    """Редактирование проекта"""
    project = get_object_or_404(Project, pk=project_id, owner=request.user)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("projects:project_detail", project_id=project.id)
    else:
        form = ProjectForm(instance=project)

    return render(
        request,
        "projects/create-project.html",
        {
            "form": form,
            "is_edit": True,
            "project": project,
        },
    )


@login_required
def project_favorites(request):
    """Страница избранных проектов"""
    # Получаем проекты, которые есть в избранном у текущего юзера
    favorites = request.user.favorites.all().order_by("-created_at")

    return render(
        request,
        "projects/project_list.html",
        {
            "projects": favorites,
            # Передаем заголовок для шаблона
            "page_title": "Избранные проекты",
        },
    )
