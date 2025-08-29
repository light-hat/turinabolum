from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название тега",
        help_text="Уникальное название тега для категоризации артефактов",
    )
    color = models.CharField(
        max_length=7,
        default="#007bff",
        verbose_name="Цвет",
        help_text="Цвет для визуального выделения тега в формате HEX (#RRGGBB)",
    )

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name
