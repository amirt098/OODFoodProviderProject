import dataclasses
from typing import List


@dataclasses.dataclass
class CartInfo:
    uid: str
    user_uid: str
    created: int
    footnote: str
    address_uid: str
    provider_uid: str


