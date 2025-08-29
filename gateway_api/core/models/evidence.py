from django.db import models
from .case import Case

class EvidenceSource(models.Model):
    SOURCE_TYPE_CHOICES = [
        ('Disk Image', 'Disk Image'),
        ('Memory Dump', 'Memory Dump'),
        ('Network PCAP', 'Network PCAP'),
        ('Cloud Logs', 'Cloud Logs'),
        ('Endpoint Agent', 'Endpoint Agent'),
        ('Mobile Device', 'Mobile Device'),
        ('Email Archive', 'Email Archive'),
    ]

    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name='evidence_sources',
        verbose_name="Расследование",
        help_text="Расследование, к которому относится данный источник доказательств"
    )
    type = models.CharField(
        max_length=50,
        choices=SOURCE_TYPE_CHOICES,
        verbose_name="Тип источника",
        help_text="Тип источника цифровых доказательств"
    )
    name = models.CharField(
        max_length=255,
        verbose_name="Название",
        help_text="Идентификационное название источника доказательств"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
        help_text="Подробное описание источника доказательств и контекста его получения"
    )
    hash_md5 = models.CharField(
        max_length=32,
        blank=True,
        verbose_name="MD5 хеш",
        help_text="MD5 хеш-сумма образа или файла источника"
    )
    hash_sha1 = models.CharField(
        max_length=40,
        blank=True,
        verbose_name="SHA-1 хеш",
        help_text="SHA-1 хеш-сумма образа или файла источника"
    )
    hash_sha256 = models.CharField(
        max_length=64,
        blank=True,
        verbose_name="SHA-256 хеш",
        help_text="SHA-256 хеш-сумма образа или файла источника"
    )
    acquisition_date = models.DateTimeField(
        verbose_name="Дата получения",
        help_text="Дата и время получения/создания образа доказательств"
    )
    acquisition_tool = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Инструмент получения",
        help_text="Название инструмента, использованного для получения доказательств"
    )
    custodian = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Владелец",
        help_text="Владелец устройства или данных"
    )
    storage_location = models.CharField(
        max_length=500,
        verbose_name="Место хранения",
        help_text="Путь к файлу в системе хранения (например, в S3)"
    )

    class Meta:
        verbose_name = "Источник доказательств"
        verbose_name_plural = "Источники доказательств"

    def __str__(self):
        return f"{self.type}: {self.name}"
