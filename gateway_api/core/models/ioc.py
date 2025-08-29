from django.db import models

from .case import Case


class IOC(models.Model):
    IOC_TYPE_CHOICES = [
        ("Hash", "Hash"),
        ("IP Address", "IP Address"),
        ("Domain", "Domain"),
        ("URL", "URL"),
        ("Email", "Email"),
        ("Filename", "Filename"),
        ("Mutex", "Mutex"),
        ("Registry Key", "Registry Key"),
        ("User Agent", "User Agent"),
    ]
    TLP_CHOICES = [
        ("RED", "RED"),
        ("AMBER", "AMBER"),
        ("GREEN", "GREEN"),
        ("WHITE", "WHITE"),
    ]
    CONFIDENCE_CHOICES = [
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
    ]

    case = models.ForeignKey(
        Case,
        on_delete=models.CASCADE,
        related_name="iocs",
        verbose_name="Расследование",
        help_text="Расследование, в рамках которого был обнаружен IOC",
    )
    type = models.CharField(
        max_length=20,
        choices=IOC_TYPE_CHOICES,
        verbose_name="Тип IOC",
        help_text="Тип индикатора компрометации",
    )
    value = models.CharField(
        max_length=500,
        verbose_name="Значение",
        help_text="Фактическое значение индикатора компрометации",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
        help_text="Контекст и пояснения по данному IOC",
    )
    first_seen = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Первое появление",
        help_text="Дата и время первого обнаружения данного IOC",
    )
    last_seen = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Последнее появление",
        help_text="Дата и время последнего обнаружения данного IOC",
    )
    tlp = models.CharField(
        max_length=10,
        choices=TLP_CHOICES,
        default="WHITE",
        verbose_name="TLP",
        help_text="Уровень распространения по протоколу TLP",
    )
    confidence = models.CharField(
        max_length=10,
        choices=CONFIDENCE_CHOICES,
        default="Medium",
        verbose_name="Достоверность",
        help_text="Уровень достоверности индикатора",
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата и время добавления IOC в систему",
    )

    class Meta:
        verbose_name = "IOC"
        verbose_name_plural = "IOCs"
        indexes = [
            models.Index(fields=["type", "value"]),
            models.Index(fields=["value"]),
        ]

    def __str__(self):
        return f"{self.type}: {self.value}"
