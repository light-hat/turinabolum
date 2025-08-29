from django.contrib.auth.models import User
from django.db import models

from .evidence import EvidenceSource
from .tag import Tag


class Artifact(models.Model):
    ARTIFACT_TYPE_CHOICES = [
        ("File", "File"),
        ("Registry Key", "Registry Key"),
        ("Process", "Process"),
        ("Network Connection", "Network Connection"),
        ("Event Log", "Event Log"),
        ("Browser History", "Browser History"),
        ("Scheduled Task", "Scheduled Task"),
        ("Windows Service", "Windows Service"),
        ("Memory Allocation", "Memory Allocation"),
        ("URL", "URL"),
    ]

    source = models.ForeignKey(
        EvidenceSource,
        on_delete=models.CASCADE,
        related_name="artifacts",
        verbose_name="Источник",
        help_text="Источник доказательств, из которого был извлечен артефакт",
    )
    type = models.CharField(
        max_length=50,
        choices=ARTIFACT_TYPE_CHOICES,
        verbose_name="Тип артефакта",
        help_text="Тип цифрового артефакта",
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Название",
        help_text="Имя или идентификатор артефакта",
    )
    path = models.TextField(
        blank=True,
        verbose_name="Путь",
        help_text="Полный путь к артефакту в исходной системе",
    )
    size = models.BigIntegerField(
        null=True,
        blank=True,
        verbose_name="Размер",
        help_text="Размер артефакта в байтах",
    )
    created_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата создания",
        help_text="Дата и время создания артефакта в исходной системе",
    )
    modified_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата изменения",
        help_text="Дата и время последнего изменения артефакта в исходной системе",
    )
    accessed_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата доступа",
        help_text="Дата и время последнего доступа к артефакту в исходной системе",
    )
    hash_md5 = models.CharField(
        max_length=32,
        blank=True,
        verbose_name="MD5 хеш",
        help_text="MD5 хеш-сумма артефакта (если применимо)",
    )
    hash_sha1 = models.CharField(
        max_length=40,
        blank=True,
        verbose_name="SHA-1 хеш",
        help_text="SHA-1 хеш-сумма артефакта (если применимо)",
    )
    hash_sha256 = models.CharField(
        max_length=64,
        blank=True,
        verbose_name="SHA-256 хеш",
        help_text="SHA-256 хеш-сумма артефакта (если применимо)",
    )
    is_suspicious = models.BooleanField(
        default=False,
        verbose_name="Подозрительный",
        help_text="Отметка о подозрительной природе артефакта",
    )
    raw_data_reference = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на данные",
        help_text="Путь к raw-данным артефакта в системе хранения (если хранятся отдельно)",
    )

    class Meta:
        verbose_name = "Артефакт"
        verbose_name_plural = "Артефакты"

    def __str__(self):
        return f"{self.type} - {self.name}"


class ArtifactTag(models.Model):
    artifact = models.ForeignKey(
        Artifact,
        on_delete=models.CASCADE,
        verbose_name="Артефакт",
        help_text="Артефакт, к которому применяется тег",
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name="Тег",
        help_text="Тег, применяемый к артефакту",
    )
    added_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Кем добавлен",
        help_text="Пользователь, добавивший тег к артефакту",
    )
    added_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления",
        help_text="Дата и время добавления тега к артефакту",
    )

    class Meta:
        verbose_name = "Тег артефакта"
        verbose_name_plural = "Теги артефактов"
        unique_together = ("artifact", "tag")

    def __str__(self):
        return f"{self.artifact} - {self.tag}"
