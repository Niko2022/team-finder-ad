from django.db import models
from django.conf import settings

NAME_MAX_LENGTH = 200
STATUS_OPEN = "open"
STATUS_CLOSED = "closed"

STATUS_CHOICES = [
    (STATUS_OPEN, "Открыт"),
    (STATUS_CLOSED, "Закрыт"),
]


class Project(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, verbose_name="Название проекта")
    description = models.TextField(blank=True, verbose_name="Описание")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects",
        verbose_name="Автор",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    github_url = models.URLField(blank=True, null=True, verbose_name="GitHub")
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="open", verbose_name="Статус"
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="participated_projects",
        blank=True,
        verbose_name="Участники",
    )

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return self.name
