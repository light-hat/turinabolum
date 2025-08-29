from django.contrib.auth.models import User
from django.db import models

from .case import Case


class TTP(models.Model):
    technique_id = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="ID техники",
        help_text="Идентификатор техники по MITRE ATT&CK (например, T1059.003)",
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Название",
        help_text="Название техники по MITRE ATT&CK",
    )
    tactic = models.CharField(
        max_length=100,
        verbose_name="Тактика",
        help_text="Тактика MITRE ATT&CK, к которой относится техника",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
        help_text="Подробное описание техники, методов обнаружения и рекомендации",
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата и время добавления техники в систему",
    )
    modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения",
        help_text="Дата и время последнего обновления информации о технике",
    )

    class Meta:
        verbose_name = "TTP"
        verbose_name_plural = "TTPs"
        ordering = ["technique_id"]

    def __str__(self):
        return f"{self.technique_id} - {self.name}"


class CaseTTP(models.Model):
    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        verbose_name="Расследование",
        help_text="Расследование, в котором была обнаружена техника",
    )
    ttp = models.ForeignKey(
        TTP,
        on_delete=models.CASCADE,
        verbose_name="TTP",
        help_text="Техника, тактика или процедура, обнаруженная в расследовании",
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Заметки",
        help_text="Заметки по применению техники в данном расследовании",
    )
    detected_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата обнаружения",
        help_text="Дата и время обнаружения техники в расследовании",
    )
    detected_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Обнаружено",
        help_text="Пользователь, обнаруживший применение техники",
    )

    class Meta:
        verbose_name = "TTP расследования"
        verbose_name_plural = "TTPs расследований"
        unique_together = ("case", "ttp")

    def __str__(self):
        return f"{self.case} - {self.ttp}"
