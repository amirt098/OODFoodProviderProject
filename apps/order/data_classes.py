import dataclasses
from typing import List
from xmlrpc.client import DateTime


@dataclasses.dataclass
class OrderFilter:
    user__uid: str
    state: str
    created__lte: int
    created__gte: int
    provider__uid: str
    driver__uid: str

@dataclasses.dataclass
class OrderItemInfo:
    product_uid: str
    price: int
    quantity: int

@dataclasses.dataclass
class OrderInfo:
    uid: str
    user_uid: str
    provider_uid: str
    created: DateTime
    state: str
    footnote: str
    order_items: List[OrderItemInfo]

