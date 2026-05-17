from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.core.paginator import Paginator
from .models import Project
from .forms import ProjectForm


def project_list(request):
    """Главная страница: список проектов с пагинацией"""
    # Получаем все проекты, сортируем от новых к старым
    projects = Project.objects.select_related('owner').all().order_by('-created_at')

    # Пагинация: 12 проектов на странице
    paginator = Paginator(projects, 12)
    page_number = request.GET.get('page', 1)
    projects_page = paginator.get_page(page_number)

    return render(request, 'projects/project_list.html', {
        'projects': projects_page,
        # Для навигации пагинации в шаблоне
        'page_obj': projects_page,
    })


def project_detail(request, project_id):
    """Страница проекта"""
    # Выбираем проект вместе с автором и участниками
    project = get_object_or_404(
        Project.objects.select_related('owner').prefetch_related('participants'),
        pk=project_id
    )

    return render(request, 'projects/project-details.html', {
        'project': project
    })


@login_required
def toggle_participate(request, project_id):
    """Присоединиться/отказаться от участия в проекте"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error'}, status=405)

    project = get_object_or_404(Project, pk=project_id)
    user = request.user

    if project.participants.filter(pk=user.pk).exists():
        project.participants.remove(user)
        participating = False
    else:
        project.participants.add(user)
        participating = True

    return JsonResponse({'status': 'ok', 'participating': participating})


@login_required
def complete_project(request, project_id):
    """Завершить проект (только для владельца)"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error'}, status=405)

    project = get_object_or_404(Project, pk=project_id)

    # Проверка прав: только владелец может закрыть
    if project.owner != request.user:
        return HttpResponseForbidden()

    if project.status == 'open':
        project.status = 'closed'
        project.save()
        return JsonResponse({'status': 'ok', 'project_status': 'closed'})

    return JsonResponse({'status': 'error', 'message': 'Проект уже закрыт'}, status=400)


@login_required
def toggle_favorite(request, project_id):
    """Добавить/удалить проект из избранного (AJAX)"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error'}, status=405)

    project = get_object_or_404(Project, pk=project_id)
    user = request.user

    if user.favorites.filter(pk=project_id).exists():
        user.favorites.remove(project)
        favorited = False
    else:
        user.favorites.add(project)
        favorited = True

    return JsonResponse({'status': 'ok', 'favorited': favorited})


@login_required
def create_project(request):
    if request.method == 'POST':
        print("🟡 DEBUG: POST запрос получен")
        form = ProjectForm(request.POST)

        if form.is_valid():
            print(" DEBUG: Форма валидна, начинаю сохранение...")
            project = form.save(commit=False)
            project.owner = request.user
            project.save()

            print(f"🟢 DEBUG: Проект сохранён в БД. ID: {project.id}")
            project.participants.add(request.user)
            print(f"🟢 DEBUG: Участник добавлен. Всего в списке: {project.participants.count()}")

            return redirect('projects:project_detail', project_id=project.id)
        else:
            print("🔴 DEBUG: Форма НЕ прошла валидацию!")
            print("Ошибки:", form.errors)
    else:
        form = ProjectForm()

    return render(request, 'projects/create-project.html', {'form': form, 'is_edit': False})


@login_required
def edit_project(request, project_id):
    """Редактирование проекта"""
    project = get_object_or_404(Project, pk=project_id, owner=request.user)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects:project_detail', project_id=project.id)
    else:
        form = ProjectForm(instance=project)

    return render(request, 'projects/create-project.html', {
        'form': form,
        'is_edit': True,
        'project': project,
    })


@login_required
def project_favorites(request):
    """Страница избранных проектов"""
    # Получаем проекты, которые есть в избранном у текущего юзера
    favorites = request.user.favorites.all().order_by('-created_at')

    return render(request, 'projects/project_list.html', {
        'projects': favorites,
        # Передаем заголовок для шаблона
        'page_title': 'Избранные проекты',
    })
