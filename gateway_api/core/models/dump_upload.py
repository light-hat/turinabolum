import hashlib
from django.contrib.auth.models import User
from django.db import models
from core.storage import MediaMinIOStorage


class DumpUpload(models.Model):
    DUMP_TYPE_CHOICES = [
        ("Memory", "Memory Dump"),
        ("Disk", "Disk Image"),
        ("Network", "PCAP"),
        ("Logs", "Log Files"),
        ("Other", "Other"),
    ]
    STATUS_CHOICES = [
        ("Uploaded", "Uploaded"),
        ("Processing", "Processing"),
        ("Analyzed", "Analyzed"),
        ("Failed", "Failed"),
    ]

    upload_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата загрузки",
        help_text="Дата и время загрузки дампа",
    )
    dump_type = models.CharField(
        max_length=20,
        choices=DUMP_TYPE_CHOICES,
        verbose_name="Тип дампа",
        help_text="Тип загруженного дампа",
    )
    original_filename = models.CharField(
        max_length=500,
        verbose_name="Исходное имя файла",
        help_text="Оригинальное имя загруженного файла",
    )
    dump_file = models.FileField(
        #upload_to="dumps/%Y/%m/%d/",
        max_length=500
        storage=MediaMinIOStorage(),
        verbose_name="Файл дампа",
        help_text="Файл дампа, загруженный в систему хранения",
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Кем загружен",
        help_text="Пользователь, загрузивший дамп",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Uploaded",
        verbose_name="Статус",
        help_text="Текущий статус обработки дампа",
    )
    file_size = models.BigIntegerField(
        default=0, verbose_name="Размер файла", help_text="Размер файла дампа в байтах"
    )
    md5_hash = models.CharField(
        max_length=32,
        blank=True,
        verbose_name="MD5 хеш",
        help_text="MD5 хеш-сумма файла дампа",
    )
    sha1_hash = models.CharField(
        max_length=40,
        blank=True,
        verbose_name="SHA-1 хеш",
        help_text="SHA-1 хеш-сумма файла дампа",
    )
    sha256_hash = models.CharField(
        max_length=64,
        blank=True,
        verbose_name="SHA-256 хеш",
        help_text="SHA-256 хеш-сумма файла дампа",
    )
    processing_log = models.TextField(
        blank=True,
        verbose_name="Лог обработки",
        help_text="Лог процесса обработки дампа (ошибки, предупреждения, результаты)",
    )
    analysis_results = models.JSONField(
        null=True,
        blank=True,
        verbose_name="Результаты анализа",
        help_text="Результаты автоматического анализа дампа в формате JSON",
    )

    class Meta:
        verbose_name = "Загрузка дампа"
        verbose_name_plural = "Загрузки дампов"
        ordering = ["-upload_date"]
        indexes = [
            models.Index(fields=["uploaded_by", "status"]),
            models.Index(fields=["md5_hash", "sha1_hash", "sha256_hash"]),
        ]

    def __str__(self):
        return f"{self.dump_type} Dump: {self.original_filename}"

    def calculate_file_hashes(self):
        """Calculate MD5, SHA1, and SHA256 hashes for the uploaded file."""
        if not self.dump_file:
            return

        try:
            file_obj = self.dump_file.open("rb")

            md5_hash = hashlib.md5()
            sha1_hash = hashlib.sha1()
            sha256_hash = hashlib.sha256()

            for chunk in iter(lambda: file_obj.read(8192), b""):
                md5_hash.update(chunk)
                sha1_hash.update(chunk)
                sha256_hash.update(chunk)

            file_obj.close()

            self.md5_hash = md5_hash.hexdigest()
            self.sha1_hash = sha1_hash.hexdigest()
            self.sha256_hash = sha256_hash.hexdigest()
            self.file_size = self.dump_file.size

            self.save(
                update_fields=["md5_hash", "sha1_hash", "sha256_hash", "file_size"]
            )

        except Exception as e:
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Failed to calculate hashes for {self.original_filename}: {e}")

    def get_file_url(self):
        """Return the URL for accessing the uploaded file."""
        return self.dump_file.url if self.dump_file else None

    def delete_file(self):
        """Delete the physical file from storage."""
        if self.dump_file and self.dump_file.storage.exists(self.dump_file.name):
            self.dump_file.storage.delete(self.dump_file.name)

    def save(self, *args, **kwargs):
        """Override save to calculate hashes on new files."""
        if not self.pk and self.dump_file:
            super().save(*args, **kwargs)
            self.calculate_file_hashes()
        else:
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Override delete to remove the physical file."""
        self.delete_file()
        super().delete(*args, **kwargs)
