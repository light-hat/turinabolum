from django.db import models
from django.contrib.auth.models import User

class Incident(models.Model):
    INCIDENT_STATUS_CHOICES = [
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('On Hold', 'On Hold'),
        ('Closed', 'Closed'),
        ('Reopened', 'Reopened'),
    ]
    SEVERITY_CHOICES = [
        ('Critical', 'Critical'),
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
        ('Info', 'Info'),
    ]
    CLASSIFICATION_CHOICES = [
        ('Malware', 'Malware'),
        ('Phishing', 'Phishing'),
        ('Data Exfiltration', 'Data Exfiltration'),
        ('Insider Threat', 'Insider Threat'),
    ]

    title = models.CharField(
        max_length=255,
        verbose_name="Название инцидента",
        help_text="Краткое описательное название инцидента"
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Подробное описание инцидента, обстоятельств обнаружения и т.д."
    )
    status = models.CharField(
        max_length=20,
        choices=INCIDENT_STATUS_CHOICES,
        default='New',
        verbose_name="Статус",
        help_text="Текущий статус обработки инцидента"
    )
    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        verbose_name="Критичность",
        help_text="Уровень критичности инцидента"
    )
    classification = models.CharField(
        max_length=50,
        choices=CLASSIFICATION_CHOICES,
        verbose_name="Классификация",
        help_text="Тип инцидента согласно классификации"
    )
    confidentiality = models.CharField(
        max_length=50,
        default='Internal',
        verbose_name="Конфиденциальность",
        help_text="Уровень конфиденциальности информации об инциденте"
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата и время регистрации инцидента в системе"
    )
    modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения",
        help_text="Дата и время последнего изменения данных инцидента"
    )
    closed_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата закрытия",
        help_text="Дата и время закрытия инцидента"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='created_incidents',
        verbose_name="Кем создан",
        help_text="Пользователь, зарегистрировавший инцидент в системе"
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='assigned_incidents',
        null=True,
        blank=True,
        verbose_name="Ответственный",
        help_text="Пользователь, ответственный за расследование инцидента"
    )

    class Meta:
        verbose_name = "Инцидент"
        verbose_name_plural = "Инциденты"
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.title} (ID: {self.id})"
