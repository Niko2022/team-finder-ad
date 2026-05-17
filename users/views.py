from django.shortcuts import render, get_object_or_404
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, update_session_auth_hash, authenticate
from django.shortcuts import render, redirect
from .forms import UserRegisterForm, ProfileEditForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm


def user_list(request):
    """Список всех пользователей"""
    users = User.objects.all().order_by('name')
    return render(request, 'users/user_list.html', {
        'users': users,
    })


def user_detail(request, user_id):
    """Страница пользователя с его проектами"""
    user = get_object_or_404(
        User.objects.prefetch_related('owned_projects', 'participated_projects', 'favorites'),
        pk=user_id
    )

    # Разделяем проекты: созданные и те, где участник
    owned_projects = user.owned_projects.all().order_by('-created_at')
    participated_projects = user.participated_projects.all().order_by('-created_at')

    return render(request, 'users/user-details.html', {
        # Переименовываем, чтобы не путать с request.user
        'profile_user': user,
        'owned_projects': owned_projects,
        'participated_projects': participated_projects,
    })


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:user_detail', user_id=user.id)
    else:
        form = ProfileEditForm(instance=user)

    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    """Смена пароля"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Важно: обновляем сессию, чтобы пользователя не выкинуло из аккаунта
            update_session_auth_hash(request, user)
            return redirect('users:user_detail', user_id=request.user.id)
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'users/change_password.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('projects:project_list')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Сразу входим после регистрации
            return redirect('projects:project_list')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('projects:project_list')
