"""Модель растения и его графика полива."""
from datetime import timedelta

from django.core.validators import MinValueValidator
from django.db import models
from django.db import transaction
from django.urls import reverse
from django.utils import timezone


class PlantQuerySet(models.QuerySet):
    def with_watering_count(self):
        return self.annotate(watering_count=models.Count("waterings"))

    def frequent_watering(self):
        """Растения с интервалом полива меньше двух недель."""
        return self.filter(interval_days__lt=14)


class Plant(models.Model):
    name = models.CharField("Название", max_length=200)
    slug = models.SlugField(
        "Адрес", max_length=200, unique=True, null=True, blank=True,
        help_text="Английский адрес; при отсутствии создаётся автоматически.",
    )
    species = models.CharField("Вид", max_length=200, blank=True)
    interval_days = models.PositiveIntegerField(
        "Интервал полива, дней", validators=[MinValueValidator(1)],
        help_text="Количество дней между поливами.",
    )
    is_infrequent = models.GeneratedField(
        expression=models.Case(
            models.When(interval_days__gte=14, then=models.Value(True)),
            default=models.Value(False),
            output_field=models.BooleanField(),
        ),
        output_field=models.BooleanField(), db_persist=True,
        verbose_name="Редкий полив",
    )
    last_watered = models.DateField("Последний полив")
    owner = models.ForeignKey(
        "owners.Owner", on_delete=models.PROTECT, related_name="plants",
        verbose_name="Владелец", null=True, blank=True,
    )
    location = models.ForeignKey(
        "locations.Location", on_delete=models.PROTECT, related_name="plants",
        verbose_name="Место", null=True, blank=True,
    )
    objects = PlantQuerySet.as_manager()

    class Meta:
        ordering = ["name", "pk"]
        verbose_name = "Растение"
        verbose_name_plural = "Растения"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if not self.slug and self.pk:
                self.slug = f"plant-{self.pk}"
            super().save(*args, **kwargs)
            if not self.slug:
                self.slug = f"plant-{self.pk}"
                type(self).objects.filter(pk=self.pk).update(slug=self.slug)

    def get_absolute_url(self):
        return reverse("plants:detail_slug", kwargs={"slug": self.slug})

    def last_watered_date(self):
        return self.last_watered

    def next_watering_date(self):
        return self.last_watered + timedelta(days=self.interval_days)

    def needs_watering(self, current_date=None):
        today = current_date or timezone.localdate()
        return self.next_watering_date() <= today
