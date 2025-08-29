from django.db import models
from django.contrib.auth.models import User

class DumpUpload(models.Model):
    DUMP_TYPE_CHOICES = [
        ('Memory', 'Memory Dump'),
        ('Disk', 'Disk Image'),
        ('Network', 'PCAP'),
        ('Logs', 'Log Files'),
        ('Other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('Uploaded', 'Uploaded'),
        ('Processing', 'Processing'),
        ('Analyzed', 'Analyzed'),
        ('Failed', 'Failed'),
    ]

    upload_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата загрузки",
        help_text="Дата и время загрузки дампа"
    )
    dump_type = models.CharField(
        max_length=20,
        choices=DUMP_TYPE_CHOICES,
        verbose_name="Тип дампа",
        help_text="Тип загруженного дампа"
    )
    original_filename = models.CharField(
        max_length=255,
        verbose_name="Исходное имя файла",
        help_text="Оригинальное имя загруженного файла"
    )
    dump_file = models.FileField(
        upload_to='dumps/%Y/%m/%d/',
        verbose_name="Файл дампа",
        help_text="Файл дампа, загруженный в систему хранения"
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Кем загружен",
        help_text="Пользователь, загрузивший дамп"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Uploaded',
        verbose_name="Статус",
        help_text="Текущий статус обработки дампа"
    )
    file_size = models.BigIntegerField(
        default=0,
        verbose_name="Размер файла",
        help_text="Размер файла дампа в байтах"
    )
    md5_hash = models.CharField(
        max_length=32,
        blank=True,
        verbose_name="MD5 хеш",
        help_text="MD5 хеш-сумма файла дампа"
    )
    sha1_hash = models.CharField(
        max_length=40,
        blank=True,
        verbose_name="SHA-1 хеш",
        help_text="SHA-1 хеш-сумма файла дампа"
    )
    sha256_hash = models.CharField(
        max_length=64,
        blank=True,
        verbose_name="SHA-256 хеш",
        help_text="SHA-256 хеш-сумма файла дампа"
    )
    processing_log = models.TextField(
        blank=True,
        verbose_name="Лог обработки",
        help_text="Лог процесса обработки дампа (ошибки, предупреждения, результаты)"
    )
    analysis_results = models.JSONField(
        null=True,
        blank=True,
        verbose_name="Результаты анализа",
        help_text="Результаты автоматического анализа дампа в формате JSON"
    )
    kafka_message_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="ID сообщения Kafka",
        help_text="Идентификатор сообщения Kafka, отправленного для обработки дампа"
    )

    class Meta:
        verbose_name = "Загрузка дампа"
        verbose_name_plural = "Загрузки дампов"
        ordering = ['-upload_date']
        indexes = [
            models.Index(fields=['uploaded_by', 'status']),
            models.Index(fields=['md5_hash', 'sha1_hash', 'sha256_hash']),
        ]

    def __str__(self):
        return f"{self.dump_type} Dump: {self.original_filename}"
        