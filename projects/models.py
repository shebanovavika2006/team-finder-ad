from django.conf import settings
from django.db import models

from .constants import PROJECT_TITLE_MAX_LEN, STATUS_MAX_LEN


class StatusChoices(models.TextChoices):
    OPEN = "open", "Open"
    CLOSED = "closed", "Closed"


class Project(models.Model):
    name = models.CharField("Название проекта", max_length=PROJECT_TITLE_MAX_LEN)
    description = models.TextField("Описание", blank=True, default="")
    github_url = models.URLField("Ссылка на GitHub", blank=True, default="")
    status = models.CharField(
        "Статус",
        max_length=STATUS_MAX_LEN,
        choices=StatusChoices.choices,
        default=StatusChoices.OPEN,
    )
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_projects",
        verbose_name="Владелец",
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="participated_projects",
        blank=True,
        verbose_name="Участники",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self):
        return self.name
