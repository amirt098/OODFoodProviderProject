from typing import List

from apps.cart.abstraction import AbstractCartService
from apps.cart.models import (
    Cart,
    CartItem,
)
from apps.cart.data_classes import CartInfo
from apps.provider.services import ProviderService

class CartService(AbstractCartService):

    provider_service = ProviderService()

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
        return [self.get_cart(cart.uid) for cart in Cart.objects.filter(user__uid=user_uid)]
    
    def add_to_cart(self, cart_uid: str, product_uid: str) -> None:
        cart = Cart.objects.get(uid=cart_uid)
        item = CartItem.objects.create(
            product=self.provider_service.get_product_id(product_uid),
            cart=cart,
            quantity=1,
        )
        item.save()
        return

    def delete_from_cart(self, cart_uid: str, product_uid: str) -> None:
        CartItem.objects.get(product__uid=product_uid, cart__uid=cart_uid).delete()
        return
    
    def update_quantity(self, cart_uid: str, product_uid: str, quantity: int) -> None:
        item = CartItem.objects.get(product__uid=product_uid, cart__uid=cart_uid)
        item.quantity = quantity
        item.save()
        return

