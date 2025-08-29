from django.contrib.auth.models import User
from django.db import models


class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = [
        ("Correlation", "Correlation"),
        ("Incident", "Incident"),
        ("System", "System"),
        ("TI", "Threat Intelligence"),
    ]
    SEVERITY_CHOICES = [
        ("Critical", "Critical"),
        ("High", "High"),
        ("Medium", "Medium"),
        ("Low", "Low"),
        ("Info", "Info"),
    ]

    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок",
        help_text="Краткий заголовок уведомления",
    )
    message = models.TextField(
        verbose_name="Сообщение", help_text="Подробное содержание уведомления"
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPE_CHOICES,
        verbose_name="Тип уведомления",
        help_text="Тип уведомления",
    )
    severity = models.CharField(
        max_length=10,
        choices=SEVERITY_CHOICES,
        default="Medium",
        verbose_name="Критичность",
        help_text="Уровень критичности уведомления",
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата и время создания уведомления",
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name="Прочитано",
        help_text="Отметка о прочтении уведомления",
    )
    read_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата прочтения",
        help_text="Дата и время прочтения уведомления",
    )
    related_object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="ID связанного объекта",
        help_text="Идентификатор связанного объекта (например, инцидента)",
    )
    related_content_type = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Тип связанного объекта",
        help_text="Тип связанного объекта (например, 'incident')",
    )

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"
        ordering = ["-created_date"]
        indexes = [
            models.Index(fields=["is_read", "created_date"]),
            models.Index(fields=["notification_type", "severity"]),
        ]

    def __str__(self):
        return f"{self.notification_type}: {self.title}"


class UserNotification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Пользователь, для которого предназначено уведомление",
    )
    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        verbose_name="Уведомление",
        help_text="Связанное уведомление",
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name="Прочитано",
        help_text="Отметка о прочтении уведомления пользователем",
    )
    read_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата прочтения",
        help_text="Дата и время прочтения уведомления пользователем",
    )

    class Meta:
        verbose_name = "Пользовательское уведомление"
        verbose_name_plural = "Пользовательские уведомления"
        unique_together = ("user", "notification")
        indexes = [
            models.Index(fields=["user", "is_read"]),
        ]

    def __str__(self):
        return f"{self.user} - {self.notification}"
