from django.test import TestCase

from django.test import TestCase
from django.utils import timezone
from .models import Driver
from .services import DriverService
from .data_classes import DriverInfo, DriverFilter
from .exceptions import UIDNotFound
from ..accounts.models import User


class TestDriverService(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(uid='user1')
        self.driver1 = Driver.objects.create(
            uid='driver1',
            user=self.user1,
            plate_number='ABC123',
            location='Location A',
            is_available=True,
            last_paycheck=timezone.now()
        )
        self.service = DriverService()

    def test_get_driver(self):
        driver_info = self.service.get_driver('driver1')
        self.assertEqual(driver_info.plate_number, 'ABC123')
        self.assertEqual(driver_info.location, 'Location A')
        self.assertTrue(driver_info.is_available)
        self.assertIsInstance(driver_info.last_paycheck, int)
        self.assertEqual(driver_info.user_uid, 'user1')
        self.assertEqual(driver_info.uid, 'driver1')

    def test_get_driver_not_found(self):
        with self.assertRaises(UIDNotFound):
            self.service.get_driver('non_existent_uid')

    def test_get_drivers(self):
        filter = DriverFilter(
            plate_number_contains='',
            location='',
            is_available=None,
            last_paycheck__gte=0,
            last_paycheck__lte=timezone.now().timestamp()
        )
        driver_list = self.service.get_drivers(filter)
        self.assertEqual(len(driver_list.drivers), 1)
        self.assertEqual(driver_list.drivers[0].plate_number, 'ABC123')

    def test_get_nearest_driver(self):
        driver_info = self.service.get_nearest_driver('Location A')
        self.assertEqual(driver_info.plate_number, 'ABC123')

    def test_get_nearest_driver_not_found(self):
        Driver.objects.all().delete()
        with self.assertRaises(UIDNotFound):
            self.service.get_nearest_driver('Location A')

    def test_update_location(self):
        self.service.update_location('driver1', 'New Location')
        driver = Driver.objects.get(uid='driver1')
        self.assertEqual(driver.location, 'New Location')

    def test_update_location_not_found(self):
        with self.assertRaises(UIDNotFound):
            self.service.update_location('non_existent_uid', 'New Location')

    # def test_update_paycheck(self):
    #     self.service.update_paycheck('driver1')
    #     driver = Driver.objects.get(uid='driver1')
    #     self.assertGreater(driver.last_paycheck, self.driver1.last_paycheck)

    def test_update_paycheck_not_found(self):
        with self.assertRaises(UIDNotFound):
            self.service.update_paycheck('non_existent_uid')

    def test_get_balance(self):
        balance = self.service.get_balance('driver1')
        self.assertEqual(balance, 1000)  # Placeholder value

    def test_get_balance_not_found(self):
        with self.assertRaises(UIDNotFound):
            self.service.get_balance('non_existent_uid')

    def test_get_location(self):
        location = self.service.get_location('driver1')
        self.assertEqual(location, 'Location A')

    def test_get_location_not_found(self):
        with self.assertRaises(UIDNotFound):
            self.service.get_location('non_existent_uid')

    def test_update_availability(self):
        self.service.update_availability('driver1', False)
        driver = Driver.objects.get(uid='driver1')
        self.assertFalse(driver.is_available)

    def test_update_availability_not_found(self):
        with self.assertRaises(UIDNotFound):
            self.service.update_availability('non_existent_uid', False)

    def test_create_driver(self):
        driver_info = DriverInfo(
            plate_number='XYZ456',
            location='Location B',
            is_available=True,
            last_paycheck=int(timezone.now().timestamp()),
            user_uid='user2'
        )
        self.service.create_driver(driver_info)
        driver = Driver.objects.get(plate_number='XYZ456')
        self.assertEqual(driver.location, 'Location B')
        self.assertTrue(driver.is_available)
        self.assertEqual(driver.user.uid, 'user2')