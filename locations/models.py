"""Места размещения растений."""
from django.db import models


class Location(models.Model):
    class Light(models.TextChoices):
        BRIGHT = "яркий", "Яркий"
        INDIRECT = "рассеянный", "Рассеянный"
        SHADE = "тень", "Тень"

    name = models.CharField("Название", max_length=200)
    light = models.CharField("Освещение", max_length=20, choices=Light.choices)

    class Meta:
        ordering = ["name", "pk"]
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return self.name
