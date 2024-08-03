from dataclasses import dataclass
from typing import List


@dataclass
class CartInfo:
    uid: str
    user_uid: str
    created: int
    footnote: str
    address_uid: str
    provider_uid: str


@dataclass
class CartItemInfo:
    product_uid: str
    quantity: int

@dataclass
class CreateCartInput:
    user_uid: str
    provider_uid: str
    address_uid: str
    footnote: str
    items: List[CartItemInfo]

@dataclass
class CartOutput:
    uid: str
    user_uid: str
    created: int
    footnote: str
    address_uid: str
    provider_uid: str
    items: List[CartItemInfo]
