"""Записи о поливе."""
from django.db import models


class WateringLog(models.Model):
    plant = models.ForeignKey(
        "plants.Plant", on_delete=models.PROTECT, related_name="waterings",
        verbose_name="Растение",
    )
    watered_on = models.DateField("Дата полива")
    note = models.TextField("Заметка", blank=True)

    class Meta:
        ordering = ["-watered_on", "-pk"]
        verbose_name = "Полив"
        verbose_name_plural = "Поливы"

    def __str__(self):
        return f"{self.plant} — {self.watered_on}"
