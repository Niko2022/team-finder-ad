from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


class UserRegisterForm(UserCreationForm):
    # Переопределяем поля для кастомизации
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Придумайте пароль"}
        ),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Повторите пароль"}
        ),
    )

    class Meta:
        model = User
        fields = ["name", "surname", "email", "password1", "password2"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Имя"}
            ),
            "surname": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Фамилия"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Email"}
            ),
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name", "surname", "about", "phone", "github_url", "avatar"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Имя"}
            ),
            "surname": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "Фамилия"}
            ),
            "about": forms.Textarea(
                attrs={
                    "class": "form-textarea",
                    "placeholder": "Расскажите о себе...",
                    "rows": 4,
                }
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-input", "placeholder": "+7 (999) 000-00-00"}
            ),
            "github_url": forms.URLInput(
                attrs={
                    "class": "form-input",
                    "placeholder": "https://github.com/username",
                }
            ),
            "avatar": forms.FileInput(
                attrs={"id": "id_avatar", "style": "display: none;"}
            ),
        }
