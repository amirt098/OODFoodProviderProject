from typing import List

from apps.cart.abstraction import AbstractCartService
from apps.cart.models import (
    Cart,
    CartItem,
)
from apps.cart.data_classes import CartInfo

class CartService(AbstractCartService):