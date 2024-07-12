import dataclasses
from typing import List


@dataclasses.dataclass
class CartInfo:
    uid: int
    user_uid: int
    created_at: int
    footnote: str
    address_uid: int
    provider_uid: int


