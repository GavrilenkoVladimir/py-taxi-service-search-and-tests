from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from taxi.models import Car, Manufacturer, Driver


class CarTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)
        self.manufacturer = Manufacturer.objects.create(
            name="Lincoln",
            country="USA",
        )

    def test_create_car(self):
        response = self.client.post(
            reverse("taxi:car-create"),
            {
                "model": "Continental",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id],
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Car.objects.get(id=self.user.cars.first().id).model, "Continental"
        )

    def test_update_car(self):
        car = Car.objects.create(
            model="Continental",
            manufacturer=self.manufacturer,
        )
        response = self.client.post(
            reverse("taxi:car-update", kwargs={"pk": car.id}),
            {
                "pk": car.id,
                "model": "Not Continental",
                "manufacturer": self.manufacturer.id,
                "drivers": [self.user.id],
            },
        )
        Car.objects.get(id=car.id).refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Car.objects.get(id=car.id).model, "Not Continental")

    def test_delete_car(self):
        car = Car.objects.create(
            model="Continental",
            manufacturer=self.manufacturer,
        )
        response = self.client.post(reverse("taxi:car-delete", kwargs={"pk": car.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Car.objects.filter(id=car.id).exists())


class ManufacturerTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="admin.user",
            license_number="ADM12345",
            first_name="Admin",
            last_name="User",
            password="1qazcde3",
        )
        self.client.force_login(self.user)

    def test_create_manufacturer(self):
        response = self.client.post(
            reverse(
                "taxi:manufacturer-create",
            ),
            {"name": "Lincoln", "country": "USA"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Manufacturer.objects.get(id=1).name, "Lincoln")

    def test_update_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="Lincoln",
            country="USA",
        )
        response = self.client.post(
            reverse("taxi:manufacturer-update", kwargs={"pk": manufacturer.id}),
            {"name": "Not Lincoln", "country": "USA"},
        )
        Manufacturer.objects.get(id=manufacturer.id).refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            Manufacturer.objects.get(id=manufacturer.id).name, "Not Lincoln"
        )

    def test_delete_manufacturer(self):
        manufacturer = Manufacturer.objects.create(
            name="Lincoln",
            country="USA",
        )
        response = self.client.post(
            reverse("taxi:manufacturer-delete", kwargs={"pk": manufacturer.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Manufacturer.objects.filter(id=manufacturer.id).exists())

class SearchFormTests(TestCase):
    def setUp(self):
        self.manufacturer1 = Manufacturer.objects.create(name="Toyota", country="Japan")
        self.manufacturer2 = Manufacturer.objects.create(name="Ford", country="USA")

        self.car1 = Car.objects.create(model="Corolla", manufacturer=self.manufacturer1)
        self.car2 = Car.objects.create(model="Focus", manufacturer=self.manufacturer2)

        self.driver1 = Driver.objects.create_user(username="john_doe", password="password123", license_number="ABC12345")
        self.driver2 = Driver.objects.create_user(username="jane_smith", password="password123", license_number="XYZ67890")

    def test_manufacturer_search(self):
        response = self.client.get(reverse("taxi:manufacturer-list"), {"name": "Toyota"})
        self.assertContains(response, "Toyota")
        self.assertNotContains(response, "Ford")

    def test_manufacturer_search_case_insensitive(self):
        response = self.client.get(reverse("taxi:manufacturer-list"), {"name": "toyota"})
        self.assertContains(response, "Toyota")

    def test_manufacturer_search_partial_match(self):
        response = self.client.get(reverse("taxi:manufacturer-list"), {"name": "Toy"})
        self.assertContains(response, "Toyota")

    def test_car_model_search(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": "Corolla"})
        self.assertContains(response, "Corolla")
        self.assertNotContains(response, "Focus")

    def test_car_model_search_case_insensitive(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": "corolla"})
        self.assertContains(response, "Corolla")

    def test_car_model_search_partial_match(self):
        response = self.client.get(reverse("taxi:car-list"), {"model": "Cor"})
        self.assertContains(response, "Corolla")

    def test_driver_username_search(self):
        response = self.client.get(reverse("taxi:driver-list"), {"username": "john_doe"})
        self.assertContains(response, "john_doe")
        self.assertNotContains(response, "jane_smith")

    def test_driver_username_search_case_insensitive(self):
        response = self.client.get(reverse("taxi:driver-list"), {"username": "John_Doe"})
        self.assertContains(response, "john_doe")

    def test_driver_username_search_partial_match(self):
        response = self.client.get(reverse("taxi:driver-list"), {"username": "john"})
        self.assertContains(response, "john_doe")
