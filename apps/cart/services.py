from typing import List

from apps.cart.abstraction import AbstractCartService
from apps.cart.models import (
    Cart,
    CartItem,
)
from apps.cart.data_classes import CartInfo

class CartService(AbstractCartService):

    def get_cart(self, uid: str) -> CartInfo:
        cart = Cart.objects.get(uid=uid)
        return CartInfo(
            uid=cart.uid,
            user_uid=cart.user.uid,
            created=cart.created,
            footnote=cart.footnote,
            address_uid=cart.address.uid,
            provider_uid=cart.provider.uid,
        )
    
    def get_carts(self, user_uid: str) -> List[CartInfo]:
        return 
