import dataclasses
from typing import List

from pydantic import BaseModel


@dataclasses.dataclass
class DriverInfo:
    uid: int | None = None
    user_uid: int
    plate_number: str
    location: str
    is_available: bool
    last_paycheck: int


@dataclasses.dataclass
class DriverFilter:
    plate_number_contains: str
    location: str
    is_available: bool
    last_paycheck__gte: int
    last_paycheck__lte: int


class DriverList(BaseModel):
    drivers: List[DriverInfo]


