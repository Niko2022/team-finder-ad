from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .utils import generate_avatar
from .managers import CustomUserManager

NAME_MAX_LENGTH = 124
SURNAME_MAX_LENGTH = 124


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Email")
    name = models.CharField(max_length=NAME_MAX_LENGTH, verbose_name="Имя")
    surname = models.CharField(max_length=SURNAME_MAX_LENGTH, verbose_name="Фамилия")
    avatar = models.ImageField(upload_to="avatars/", verbose_name="Аватар")
    phone = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Телефон"
    )
    github_url = models.URLField(blank=True, null=True, verbose_name="GitHub")
    about = models.TextField(max_length=256, blank=True, verbose_name="О себе")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # избранное
    favorites = models.ManyToManyField(
        "projects.Project",
        related_name="interested_users",
        blank=True,
        verbose_name="Избранные проекты",
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["-id"]

    def __str__(self):
        return f"{self.surname} {self.name}"

    def save(self, *args, **kwargs):
        # Генерация аватара при создании пользователя
        if not self.avatar and not self.pk:
            self.avatar = generate_avatar(self.name)
        super().save(*args, **kwargs)
