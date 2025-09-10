import hashlib
import os
#from django.core.files.storage import default_storage
from config.storages import MediaMinIOStorage
from django.contrib.auth.models import User
from django.db import models


class Case(models.Model):
    """
    Стержневая сущность, описывающая всё расследование
    конкретного инцидента ИБ.
    """

    CASE_STATUS_CHOICES = [
        ("New", "New"),
        ("In Progress", "In Progress"),
        ("On Hold", "On Hold"),
        ("Closed", "Closed"),
        ("Reopened", "Reopened"),
    ]

    SEVERITY_CHOICES = [
        ("Critical", "Critical"),
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
        ("Info", "Info"),
    ]

    CLASSIFICATION_CHOICES = [
        ("Malware", "Malware"),
        ("Phishing", "Phishing"),
        ("Data Exfiltration", "Data Exfiltration"),
        ("Insider Threat", "Insider Threat"),
    ]

    TLP_CHOICES = [
        ("RED", "RED"),
        ("AMBER", "AMBER"),
        ("GREEN", "GREEN"),
        ("WHITE", "WHITE"),
    ]

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
        help_text="Текущий статус расследования",
        choices=CASE_STATUS_CHOICES,
    )
    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        verbose_name="Критичность",
        help_text="Уровень критичности инцидента",
    )
    classification = models.CharField(
        max_length=50,
        choices=CLASSIFICATION_CHOICES,
        verbose_name="Классификация",
        help_text="Тип инцидента согласно классификации",
    )
    tlp = models.CharField(
        max_length=50,
        default="WHITE",
        verbose_name="TLP",
        help_text="Уровень конфиденциальности информации об инциденте",
        choices=TLP_CHOICES,
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата и время регистрации инцидента в системе",
    )
    modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения",
        help_text="Дата и время последнего изменения данных инцидента",
    )
    closed_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата закрытия",
        help_text="Дата и время закрытия инцидента",
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="created_incidents",
        verbose_name="Кем создан",
        help_text="Пользователь, зарегистрировавший инцидент в системе",
    )

    class Meta:
        verbose_name = "case"
        verbose_name_plural = "cases"
        ordering = ["-created_date"]

    def __str__(self):
        return f"{self.title} (ID: {self.id})"

class EvidenceUpload(models.Model):
    DUMP_TYPE_CHOICES = [
        ("Memory", "Memory Dump"),
        ("Disk", "Disk Image"),
        ("Network", "PCAP"),
        ("Logs", "Log Files"),
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
        max_length=255,
        verbose_name="Исходное имя файла",
        help_text="Оригинальное имя загруженного файла",
    )
    dump_file = models.FileField(
        storage=MediaMinIOStorage(),
        #upload_to="dumps/%Y/%m/%d/",
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
        """
        Calculate MD5, SHA1, and SHA256 hashes for the uploaded file.
        This method should be called after file upload.
        """
        if not self.dump_file:
            return

        try:
            # Read file in chunks to handle large files efficiently
            file_obj = default_storage.open(self.dump_file.name, "rb")

            md5_hash = hashlib.md5()
            sha1_hash = hashlib.sha1()
            sha256_hash = hashlib.sha256()

            # Read file in 8KB chunks
            for chunk in iter(lambda: file_obj.read(8192), b""):
                md5_hash.update(chunk)
                sha1_hash.update(chunk)
                sha256_hash.update(chunk)

            file_obj.close()

            # Update model fields
            self.md5_hash = md5_hash.hexdigest()
            self.sha1_hash = sha1_hash.hexdigest()
            self.sha256_hash = sha256_hash.hexdigest()

            # Calculate file size
            self.file_size = default_storage.size(self.dump_file.name)

            # Save without triggering signals
            self.save(
                update_fields=["md5_hash", "sha1_hash", "sha256_hash", "file_size"]
            )

        except Exception as e:
            # Log error but don't fail the upload
            import logging

            logger = logging.getLogger(__name__)
            logger.error(
                f"Failed to calculate hashes for {self.original_filename}: {e}"
            )

    def get_file_url(self):
        """
        Get the URL for accessing the uploaded file.
        """
        if self.dump_file:
            return default_storage.url(self.dump_file.name)
        return None

    def delete_file(self):
        """
        Delete the physical file from storage.
        """
        if self.dump_file and default_storage.exists(self.dump_file.name):
            default_storage.delete(self.dump_file.name)

    def save(self, *args, **kwargs):
        """
        Override save to handle file operations.
        """
        # If this is a new instance and has a file, calculate hashes
        if not self.pk and self.dump_file:
            super().save(*args, **kwargs)
            # Calculate hashes after saving (so we have a pk)
            self.calculate_file_hashes()
        else:
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Override delete to remove the physical file.
        """
        self.delete_file()
        super().delete(*args, **kwargs)
