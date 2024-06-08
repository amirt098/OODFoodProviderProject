from typing import List

from pydantic import BaseModel, EmailStr, constr
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    CONSUMER = "consumer"
    PROVIDER_MANAGER = "provider_manager"
    DRIVER = "driver"


class UserClaim(BaseModel):
    uid: int
    username: str
    email: EmailStr
    role: UserRole


class UserInfo(BaseModel):
    username: constr(min_length=1)
    password: constr(min_length=1)
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    role: UserRole
    uid: int = None


class LoginData(BaseModel):
    username: str
    password: str


class AddressInfo(BaseModel):
    title: str
    state: str
    city: str
    detail: str
    location: str
    postal_code: str


class AddressList(BaseModel):
    addresses: List[AddressInfo]
