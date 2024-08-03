from typing import List
from datetime import datetime

from apps.logistic.abstraction import AbstractDriverService
from apps.logistic.models import Driver
from apps.accounts.models import User
from apps.logistic.data_classes import (
    DriverInfo,
    DriverFilter,
    DriverList,
)

class DriverService(AbstractDriverService):
    def get_driver(self, uid: str) -> DriverInfo:
        driver = Driver.objects.get(uid=uid)
        return DriverInfo(
            plate_number=driver.plate_number,
            location=driver.location,
            is_available=driver.is_available,
            last_paycheck=driver.last_paycheck,
            user_uid=driver.user.uid,
            uid=driver.uid,
        )
    
    def get_drivers(self, filter: DriverFilter) -> List[DriverInfo]:
        return [DriverInfo(
            plate_number=driver.plate_number,
            location=driver.location,
            is_available=driver.is_available,
            last_paycheck=driver.last_paycheck,
            user_uid=driver.user.uid,
            uid=driver.uid,
        ) for driver in Driver.objects.filter(**filter)]
    
    def update_location(self, uid: str, location: str):
        driver = Driver.objects.get(uid=uid)
        driver.location = location
        driver.save()
        return
    
    def update_paycheck(self, uid: str):
        driver = Driver.objects.get(uid=uid)
        driver.last_paycheck = datetime.now()
        driver.save()
        return
    
    def get_location(self, uid: str) -> str:
        return Driver.objects.get(uid=uid).location
    
    def update_availability(self, uid: str, is_available: bool):
        driver = Driver.objects.get(uid=uid)
        driver.is_available = is_available
        driver.save()
        return
    
    def create_driver(self, driver: DriverInfo):
        driver = Driver.objects.create(
            plate_number=driver.plate_number,
            location=driver.location,
            is_available=driver.is_available,
            last_paycheck=driver.last_paycheck,
            user=User.objects.get(uid=driver.user_uid),
            uid=driver.uid,
        )
        driver.save()
        return
    