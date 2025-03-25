from django.test import TestCase

from taxi.models import Car, Driver, Manufacturer


class TestModelsStr(TestCase):

    def setUp(self):
        self.driver = Driver.objects.create_user(
            username="test_123",
            password="test_password",
            first_name="test",
            last_name="test",
            license_number="DFD123",
        )
        self.manufacturer = Manufacturer.objects.create(
            name="test_",
            country="test-country",
        )
        self.car = Car.objects.create(
            drivers=self.driver,
            manufacturer=self.manufacturer,
            model="Toyota",
        )

    def test_str(self):
        self.assertEqual(str(self.car), self.car.model)
        self.assertEqual(
            str(self.manufacturer), f"{self.manufacturer.name} {self.manufacturer.country}"
        )
        self.assertEqual(
            str(self.driver), f"{self.driver.username} ({self.driver.first_name} {self.driver.last_name})"
        )
