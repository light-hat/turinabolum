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
