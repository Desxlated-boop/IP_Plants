"""Проверки ORM, фильтрации и административной панели."""
from datetime import date

from django.contrib.auth import get_user_model
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import reverse

from locations.models import Location
from owners.models import Owner
from plants.models import Plant
from waterings.models import WateringLog


class CollectionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = Owner.objects.create(name="Анна")
        cls.location = Location.objects.create(name="Окно", light="яркий")
        cls.plant = Plant.objects.create(
            name="Фикус", species="Ficus", interval_days=7,
            last_watered=date(2026, 10, 1), owner=cls.owner,
            location=cls.location,
        )
        for day in range(1, 13):
            WateringLog.objects.create(
                plant=cls.plant, watered_on=date(2026, 10, day)
            )
        cls.admin_user = get_user_model().objects.create_superuser(
            username="admin_test", password="test-password"
        )

    def test_related_objects_are_protected(self):
        with self.assertRaises(ProtectedError):
            self.plant.delete()

    def test_generated_field_updates(self):
        self.plant.refresh_from_db()
        self.assertFalse(self.plant.is_infrequent)
        self.plant.interval_days = 21
        self.plant.save(update_fields=["interval_days"])
        self.plant.refresh_from_db()
        self.assertTrue(self.plant.is_infrequent)

    def test_slug_detail(self):
        self.assertEqual(self.plant.slug, f"plant-{self.plant.pk}")
        response = self.client.get(self.plant.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Фикус")
        missing = self.client.get("/plants/p/missing/")
        self.assertEqual(missing.status_code, 404)

    def test_journal_filter_and_pagination(self):
        response = self.client.get(reverse("waterings:list"), {
            "q": "Фикус", "date_from": "2026-10-05", "sort": "oldest"
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["page"].paginator.count, 8)
        self.assertEqual(response.context["logs"][0].watered_on.day, 5)
        response = self.client.get(reverse("waterings:list"), {"page": 2})
        self.assertEqual(len(response.context["logs"]), 2)
        response = self.client.get(reverse("waterings:list"), {
            "owner": self.owner.pk, "plant": self.plant.pk,
            "date_to": "2026-10-03",
        })
        self.assertEqual(response.context["page"].paginator.count, 3)

    def test_admin_model_registration(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse("admin:plants_plant_changelist"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Фикус")

    def test_statistics_use_orm(self):
        response = self.client.get(reverse("plants:statistics"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Фикус: 12")

    def test_admin_action_records_watering(self):
        self.client.force_login(self.admin_user)
        response = self.client.post(reverse("admin:plants_plant_changelist"), {
            "action": "water_today", "_selected_action": [self.plant.pk],
        })
        self.assertEqual(response.status_code, 302)
        self.plant.refresh_from_db()
        self.assertEqual(self.plant.waterings.count(), 13)

    def test_admin_action_uses_database_expression(self):
        self.client.force_login(self.admin_user)
        response = self.client.post(reverse("admin:plants_plant_changelist"), {
            "action": "extend_interval", "_selected_action": [self.plant.pk],
        })
        self.assertEqual(response.status_code, 302)
        self.plant.refresh_from_db()
        self.assertEqual(self.plant.interval_days, 8)

    def test_admin_requires_permission(self):
        user = get_user_model().objects.create_user(
            username="staff_test", password="test-password", is_staff=True
        )
        self.client.force_login(user)
        response = self.client.get(reverse("admin:plants_plant_changelist"))
        self.assertEqual(response.status_code, 403)
