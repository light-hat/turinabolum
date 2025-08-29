from django.contrib.auth.models import User
from django.db import models

from .artifact import Artifact
from .ioc import IOC
from .ti_feed import ThreatIntelIOC


class CorrelationResult(models.Model):
    CORRELATION_TYPE_CHOICES = [
        ("TI", "Threat Intelligence"),
        ("Internal", "Internal IOC"),
        ("Behavioral", "Behavioral"),
    ]
    SEVERITY_CHOICES = [
        ("Critical", "Critical"),
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
        ("Info", "Info"),
    ]

    artifact = models.ForeignKey(
        Artifact,
        on_delete=models.CASCADE,
        verbose_name="Артефакт",
        help_text="Артефакт, для которого обнаружена корреляция",
    )
    correlation_type = models.CharField(
        max_length=20,
        choices=CORRELATION_TYPE_CHOICES,
        verbose_name="Тип корреляции",
        help_text="Тип обнаруженной корреляции",
    )
    source_ioc = models.ForeignKey(
        IOC,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Внутренний IOC",
        help_text="Внутренний IOC, с которым обнаружена корреляция",
    )
    source_ti_ioc = models.ForeignKey(
        ThreatIntelIOC,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="TI IOC",
        help_text="Threat Intelligence IOC, с которым обнаружена корреляция",
    )
    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_CHOICES,
        default="Medium",
        verbose_name="Критичность",
        help_text="Уровень критичности корреляции",
    )
    confidence = models.FloatField(
        default=0.0,
        validators=[models.MinValueValidator(0.0), models.MaxValueValidator(1.0)],
        verbose_name="Достоверность",
        help_text="Уровень достоверности корреляции от 0.0 до 1.0",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
        help_text="Подробное описание корреляции и ее контекста",
    )
    detected_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата обнаружения",
        help_text="Дата и время обнаружения корреляции",
    )
    detected_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Обнаружено",
        help_text="Пользователь или система, обнаружившая корреляцию",
    )
    is_false_positive = models.BooleanField(
        default=False,
        verbose_name="Ложное срабатывание",
        help_text="Отметка о том, является ли корреляция ложным срабатыванием",
    )
    false_positive_reason = models.TextField(
        blank=True,
        verbose_name="Причина ложного срабатывания",
        help_text="Причина, по которой корреляция была помечена как ложное срабатывание",
    )

    class Meta:
        verbose_name = "Результат корреляции"
        verbose_name_plural = "Результаты корреляции"
        ordering = ["-detected_date"]
        indexes = [
            models.Index(fields=["artifact", "correlation_type"]),
            models.Index(fields=["detected_date", "severity"]),
        ]

    def __str__(self):
        return f"Correlation: {self.artifact} - {self.correlation_type}"
