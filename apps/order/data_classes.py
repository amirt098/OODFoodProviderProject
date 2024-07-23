import dataclasses
from typing import List
from xmlrpc.client import DateTime


@dataclasses.dataclass
class OrderFilter:
    user__uid: int
    state: str
    created_at__lte: int
    created_at__gte: int
    provider__uid: int
    driver__uid: int

@dataclasses.dataclass
class OrderItemInfo:
    product_uid: int
    price: int
    quantity: int

@dataclasses.dataclass
class OrderInfo:
    uid: int
    user_uid: int
    created_at: DateTime
    state: str
    footnote: str
    order_items: List[OrderItemInfo]

