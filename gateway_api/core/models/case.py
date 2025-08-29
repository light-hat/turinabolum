from django.contrib.auth.models import User
from django.db import models

from .incident import Incident


class Case(models.Model):
    incident = models.ForeignKey(
        Incident,
        on_delete=models.CASCADE,
        related_name="cases",
        verbose_name="Инцидент",
        help_text="Связанный инцидент, для которого создано расследование",
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Название расследования",
        help_text="Краткое название расследования или кейса",
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Подробное описание целей и задач расследования",
    )
    status = models.CharField(
        max_length=50,
        verbose_name="Статус",
        help_text="Текущий статус расследования (например: Active, On Hold, Completed)",
    )
    lead_investigator = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Ведущий следователь",
        help_text="Пользователь, ведущий расследование",
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата и время создания расследования",
    )
    modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения",
        help_text="Дата и время последнего изменения расследования",
    )

    class Meta:
        verbose_name = "Расследование"
        verbose_name_plural = "Расследования"
        ordering = ["-created_date"]

    def __str__(self):
        return f"Кейс: {self.title} (Инцидент: {self.incident_id})"
