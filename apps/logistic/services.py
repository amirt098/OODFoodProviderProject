from django.core.exceptions import ObjectDoesNotExist
from typing import List

from django.utils import timezone

from .abstraction import AbstractDriverService
from .models import Driver
from .data_classes import DriverInfo, DriverList, DriverFilter
from .exceptions import UIDNotFound  # Assuming you have a custom exception defined

class DriverService(AbstractDriverService):
    def get_driver(self, uid: str) -> DriverInfo:
        try:
            driver = Driver.objects.get(uid=uid)
            return DriverInfo(
                plate_number=driver.plate_number,
                location=driver.location,
                is_available=driver.is_available,
                last_paycheck=int(driver.last_paycheck.timestamp()),  # Convert to timestamp
                user_uid=driver.user.uid,
                uid=driver.uid
            )
        except ObjectDoesNotExist:
            raise UIDNotFound(f"Driver with UID {uid} not found.")

    def get_drivers(self, filter: DriverFilter) -> DriverList:
        drivers_query = Driver.objects.all()

        if filter.plate_number_contains:
            drivers_query = drivers_query.filter(plate_number__icontains=filter.plate_number_contains)

        if filter.location:
            drivers_query = drivers_query.filter(location=filter.location)

        if filter.is_available is not None:
            drivers_query = drivers_query.filter(is_available=filter.is_available)

        if filter.last_paycheck__gte:
            drivers_query = drivers_query.filter(last_paycheck__gte=filter.last_paycheck__gte)

        if filter.last_paycheck__lte:
            drivers_query = drivers_query.filter(last_paycheck__lte=filter.last_paycheck__lte)

        drivers_info = [
            DriverInfo(
                plate_number=driver.plate_number,
                location=driver.location,
                is_available=driver.is_available,
                last_paycheck=int(driver.last_paycheck.timestamp()),
                user_uid=driver.user.uid,
                uid=driver.uid
            ) for driver in drivers_query
        ]

        return DriverList(drivers=drivers_info)

    def get_nearest_driver(self, location: str) -> DriverInfo:
        # Here you would implement a method to find the nearest driver based on location
        # For simplicity, we will just return the first available driver
        try:
            driver = Driver.objects.filter(is_available=True).first()
            if driver:
                return DriverInfo(
                    plate_number=driver.plate_number,
                    location=driver.location,
                    is_available=driver.is_available,
                    last_paycheck=int(driver.last_paycheck.timestamp()),
                    user_uid=driver.user.uid,
                    uid=driver.uid
                )
            else:
                raise UIDNotFound("No available drivers found.")
        except ObjectDoesNotExist:
            raise UIDNotFound("No drivers found.")

    def update_location(self, uid: str, location: str):
        try:
            driver = Driver.objects.get(uid=uid)
            driver.location = location
            driver.save()
        except ObjectDoesNotExist:
            raise UIDNotFound(f"Driver with UID {uid} not found.")

    def update_paycheck(self, uid: str):
        try:
            driver = Driver.objects.get(uid=uid)
            driver.last_paycheck = timezone.now()  # Assuming you want to set it to the current time
            driver.save()
        except ObjectDoesNotExist:
            raise UIDNotFound(f"Driver with UID {uid} not found.")

    def get_balance(self, uid: str) -> int:
        # Assuming you have a method to calculate balance, here we will return a placeholder
        try:
            driver = Driver.objects.get(uid=uid)
            return 1000  # Placeholder for balance calculation
        except ObjectDoesNotExist:
            raise UIDNotFound(f"Driver with UID {uid} not found.")

    def get_location(self, uid: str) -> str:
        try:
            driver = Driver.objects.get(uid=uid)
            return driver.location
        except ObjectDoesNotExist:
            raise UIDNotFound(f"Driver with UID {uid} not found.")

    def update_availability(self, uid: str, is_available: bool):
        try:
            driver = Driver.objects.get(uid=uid)
            driver.is_available = is_available
            driver.save()
        except ObjectDoesNotExist:
            raise UIDNotFound(f"Driver with UID {uid} not found.")

    def create_driver(self, driver_info: DriverInfo):
        driver = Driver(
            uid=driver_info.uid,
            plate_number=driver_info.plate_number,
            location=driver_info.location,
            is_available=driver_info.is_available,
            last_paycheck=timezone.now(),  # Set to current time or any other logic
            user=User.objects.get(uid=driver_info.user_uid)  # Assuming you have a user with this UID
        )
        driver.save()