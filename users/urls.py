from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("", views.user_list, name="user_list"),
    path("list/", views.user_list, name="user_list"),
    path("<int:user_id>/", views.user_detail, name="user_detail"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("change-password/", views.change_password, name="change_password"),
    path("login/", views.user_login, name="login"),
    path("register/", views.user_register, name="register"),
    path("logout/", views.user_logout, name="logout"),
]
