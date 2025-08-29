from django.db import models

from .incident import Incident


class ThreatActor(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Название",
        help_text="Уникальное название угрозного актора (например, APT29)",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
        help_text="Подробное описание угрозного актора, методов, целей и т.д.",
    )
    aliases = models.TextField(
        blank=True,
        verbose_name="Псевдонимы",
        help_text="Известные псевдонимы и названия угрозного актора",
    )
    origin = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Происхождение",
        help_text="Предполагаемое географическое или организационное происхождение",
    )
    target_sectors = models.TextField(
        blank=True,
        verbose_name="Целевые секторы",
        help_text="Секторы промышленности, на которые нацелен актор",
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата и время добавления актора в систему",
    )
    modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения",
        help_text="Дата и время последнего обновления информации об акторе",
    )

    class Meta:
        verbose_name = "Угрозный актор"
        verbose_name_plural = "Угрозные акторы"
        ordering = ["name"]

    def __str__(self):
        return self.name


class IncidentThreatActor(models.Model):
    CONFIDENCE_CHOICES = [
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]

    incident = models.ForeignKey(
        Incident,
        on_delete=models.CASCADE,
        verbose_name="Инцидент",
        help_text="Инцидент, связанный с угрозным актором",
    )
    threat_actor = models.ForeignKey(
        ThreatActor,
        on_delete=models.CASCADE,
        verbose_name="Угрозный актор",
        help_text="Угрозный актор, связанный с инцидентом",
    )
    confidence = models.CharField(
        max_length=10,
        choices=CONFIDENCE_CHOICES,
        default="Medium",
        verbose_name="Достоверность",
        help_text="Уровень достоверности связи инцидента с угрозным актором",
    )
    evidence = models.TextField(
        blank=True,
        verbose_name="Доказательства",
        help_text="Доказательства, подтверждающие связь инцидента с угрозным актором",
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата и время установления связи",
    )

    class Meta:
        verbose_name = "Связь инцидента с угрозным актором"
        verbose_name_plural = "Связи инцидентов с угрозными акторами"
        unique_together = ("incident", "threat_actor")

    def __str__(self):
        return f"{self.incident} - {self.threat_actor}"
