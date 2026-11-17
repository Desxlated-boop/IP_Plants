"""Владельцы домашних растений."""
from django.db import models


class Owner(models.Model):
    name = models.CharField("Имя", max_length=200)
    email = models.EmailField("Электронная почта", blank=True)

    class Meta:
        ordering = ["name", "pk"]
        verbose_name = "Владелец"
        verbose_name_plural = "Владельцы"

    def __str__(self):
        return self.name
