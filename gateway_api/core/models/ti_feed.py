from django.db import models


class ThreatIntelFeed(models.Model):
    FEED_TYPE_CHOICES = [
        ("STIX", "STIX"),
        ("TAXII", "TAXII"),
        ("CSV", "CSV"),
        ("JSON", "JSON"),
        ("RSS", "RSS"),
    ]
    STATUS_CHOICES = [
        ("Active", "Active"),
        ("Paused", "Paused"),
        ("Error", "Error"),
    ]

    name = models.CharField(
        max_length=255,
        verbose_name="Название фида",
        help_text="Уникальное название фида Threat Intelligence",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
        help_text="Подробное описание фида и его содержания",
    )
    feed_type = models.CharField(
        max_length=10,
        choices=FEED_TYPE_CHOICES,
        verbose_name="Тип фида",
        help_text="Формат данных фида",
    )
    url = models.URLField(
        verbose_name="URL фида", help_text="URL адрес для доступа к фиду"
    )
    api_key = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="API ключ",
        help_text="API ключ для доступа к фиду (если требуется)",
    )
    collection_name = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Название коллекции",
        help_text="Название коллекции TAXII (если применимо)",
    )
    polling_interval = models.IntegerField(
        default=3600,
        verbose_name="Интервал опроса",
        help_text="Интервал опроса фида в секундах",
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="Active",
        verbose_name="Статус",
        help_text="Текущий статус фида",
    )
    last_successful_poll = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Последний успешный опрос",
        help_text="Дата и время последнего успешного опроса фида",
    )
    last_error = models.TextField(
        blank=True,
        verbose_name="Последняя ошибка",
        help_text="Текст последней ошибки при опросе фида",
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата и время добавления фида в систему",
    )
    modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения",
        help_text="Дата и время последнего изменения настроек фида",
    )

    class Meta:
        verbose_name = "Threat Intelligence фид"
        verbose_name_plural = "Threat Intelligence фиды"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ThreatIntelIOC(models.Model):
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

    feed = models.ForeignKey(
        ThreatIntelFeed,
        on_delete=models.CASCADE,
        verbose_name="Фид",
        help_text="Фид, из которого получен IOC",
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
        help_text="Контекст и пояснения по данному IOC из фида",
    )
    first_seen = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Первое появление",
        help_text="Дата и время первого появления IOC в фиде",
    )
    last_seen = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Последнее появление",
        help_text="Дата и время последнего появления IOC в фиде",
    )
    confidence = models.CharField(
        max_length=10,
        choices=[("High", "High"), ("Medium", "Medium"), ("Low", "Low")],
        default="Medium",
        verbose_name="Достоверность",
        help_text="Уровень достоверности индикатора согласно фиду",
    )
    severity = models.CharField(
        max_length=10,
        choices=[
            ("Critical", "Critical"),
            ("High", "High"),
            ("Medium", "Medium"),
            ("Low", "Low"),
        ],
        default="Medium",
        verbose_name="Критичность",
        help_text="Уровень критичности индикатора согласно фиду",
    )
    tlp = models.CharField(
        max_length=10,
        choices=[
            ("RED", "RED"),
            ("AMBER", "AMBER"),
            ("GREEN", "GREEN"),
            ("WHITE", "WHITE"),
        ],
        default="WHITE",
        verbose_name="TLP",
        help_text="Уровень распространения по протоколу TLP",
    )
    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
        help_text="Дата и время добавления IOC в систему",
    )
    modified_date = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения",
        help_text="Дата и время последнего обновления IOC",
    )

    class Meta:
        verbose_name = "Threat Intelligence IOC"
        verbose_name_plural = "Threat Intelligence IOC"
        indexes = [
            models.Index(fields=["type", "value"]),
            models.Index(fields=["feed", "created_date"]),
        ]
        unique_together = ("feed", "type", "value")

    def __str__(self):
        return f"{self.type}: {self.value}"
