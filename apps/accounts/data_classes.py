import dataclasses
from typing import List

from pydantic import BaseModel, EmailStr, constr
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "Admin"
    CUSTOMER = "Customer"
    PROVIDER_MANAGER = "Provider Manager"
    DRIVER = "Driver"


@dataclasses.dataclass
class UserClaim:
    id: int
    uid: str
    username: str
    email: EmailStr
    role: UserRole


@dataclasses.dataclass
class UserInfo:
    username: constr(min_length=1)
    password: constr(min_length=1)
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    role: UserRole
    uid: int | None = None


class AddressInfo(BaseModel):
    uid: int
    user_uid: int
    title: str
    state: str
    city: str
    detail: str
    location: str
    postal_code: str


class AddressList(BaseModel):
    addresses: List[AddressInfo]
