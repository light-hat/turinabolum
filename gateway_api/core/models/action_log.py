from django.db import models
from django.contrib.auth.models import User

class ActionLog(models.Model):
    ACTION_TYPE_CHOICES = [
        ('Create', 'Create'),
        ('Read', 'Read'),
        ('Update', 'Update'),
        ('Delete', 'Delete'),
        ('Export', 'Export'),
        ('Login', 'Login'),
        ('Logout', 'Logout'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name="Пользователь",
        help_text="Пользователь, выполнивший действие"
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время",
        help_text="Дата и время выполнения действия"
    )
    action_type = models.CharField(
        max_length=10,
        choices=ACTION_TYPE_CHOICES,
        verbose_name="Тип действия",
        help_text="Тип выполненного действия (создание, чтение, обновление, удаление)"
    )
    table_name = models.CharField(
        max_length=100,
        verbose_name="Таблица",
        help_text="Название таблицы (модели), над которой выполнено действие"
    )
    record_id = models.PositiveIntegerField(
        verbose_name="ID записи",
        help_text="Идентификатор записи, над которой выполнено действие"
    )
    details = models.TextField(
        verbose_name="Детали",
        help_text="Подробная информация о действии (например, изменения в JSON формате)"
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name="IP адрес",
        help_text="IP адрес, с которого было выполнено действие"
    )
    user_agent = models.TextField(
        blank=True,
        verbose_name="User Agent",
        help_text="Информация о браузере или клиенте, с которого было выполнено действие"
    )

    class Meta:
        verbose_name = "Лог действия"
        verbose_name_plural = "Логи действий"
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'timestamp']),
            models.Index(fields=['table_name', 'record_id']),
        ]

    def __str__(self):
        return f"{self.user} {self.action_type} {self.table_name}:{self.record_id} at {self.timestamp}"
        