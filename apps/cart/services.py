from datetime import datetime
from typing import List

from apps.cart.abstraction import AbstractCartService
from apps.cart.models import (
    Cart,
    CartItem,
)
from . import data_classes

from typing import List
from .models import Cart, CartItem
from .data_classes import CartInfo
from .exceptions import UIDNotFound
from ..accounts.models import User
from ..provider.models import Product
from apps.accounts import abstraction as accounts_abstractions
from apps.order import abstraction as orders_abstractions

class CartService(AbstractCartService):

    def __init__(
            self,
            accounts_service: accounts_abstractions.AbstractUserService,
            orders_service: orders_abstractions.AbstractOrderService
    ):
        self.accounts_service = accounts_service
        self.orders_service = orders_service



    # def create_cart(self, input: data_classes.CreateCartInput) -> data_classes.CartOutput:
    #     cart = Cart.objects.create(
    #         user_id=input.user_uid,
    #         provider_id=input.provider_uid,
    #         address_id=input.address_uid,
    #         footnote=input.footnote
    #     )
    #     for item in input.items:
    #         CartItem.objects.create(
    #             order=cart,
    #             product_id=item.product_uid,
    #             quantity=item.quantity
    #         )
    #     return data_classes.CartOutput(
    #         uid=cart.uid,
    #         user_uid=cart.user_id,
    #         created=cart.created.timestamp(),
    #         footnote=cart.footnote,
    #         address_uid=cart.address_id,
    #         provider_uid=cart.provider_id,
    #         items=[data_classes.CartItemInfo(product_uid=item.product_id, quantity=item.quantity) for item in cart.items.all()]
    #     )

    def get_cart(self, uid: str) -> CartInfo:
        try:
            cart = Cart.objects.get(uid=uid)
            return CartInfo(
                uid=cart.uid,
                user_uid=cart.user.uid,
                created=cart.created.timestamp(),
                footnote=cart.footnote,
                address_uid=cart.address.uid,
                provider_uid=cart.provider.uid
            )
        except Cart.DoesNotExist:
            raise UIDNotFound(f"Cart with uid {uid} not found.")

    def get_carts(self, user_uid: str) -> List[CartInfo]:
        try:
            carts = Cart.objects.filter(user__uid=user_uid)
            return [
                CartInfo(
                    uid=cart.uid,
                    user_uid=cart.user.uid,
                    created=cart.created.timestamp(),
                    footnote=cart.footnote,
                    address_uid=cart.address.uid,
                    provider_uid=cart.provider.uid
                ) for cart in carts
            ]
        except User.DoesNotExist:
            raise UIDNotFound(f"User with uid {user_uid} not found.")

    def add_to_cart(self, cart_uid: str, product_uid: str, user_uid: str) -> None:
        try:
            cart = Cart.objects.get_or_create(
                uid=cart_uid,
                defaults={
                    "user_id": user_uid,
                    "provider_id": product_uid,
                    "address_id": self.accounts_service.get_addresses(self.accounts_service.get_info(user_uid))
                })
            product = Product.objects.get(uid=product_uid)
            cart_item, created = CartItem.objects.get_or_create(
                order=cart,
                product=product,
                defaults={'quantity': 1, 'price': product.price}
            )
            if not created:
                cart_item.quantity += 1
                cart_item.save()
        except (Cart.DoesNotExist, Product.DoesNotExist):
            raise UIDNotFound("Cart or product UID not found.")

    def delete_from_cart(self, cart_uid: str, product_uid: str) -> None:
        try:
            cart = Cart.objects.get(uid=cart_uid)
            product = Product.objects.get(uid=product_uid)
            CartItem.objects.filter(order=cart, product=product).delete()
        except (Cart.DoesNotExist, Product.DoesNotExist):
            raise UIDNotFound("Cart or product UID not found.")

    def update_quantity(self, cart_uid: str, product_uid: str, quantity: int) -> None:
        try:
            cart = Cart.objects.get(uid=cart_uid)
            product = Product.objects.get(uid=product_uid)
            cart_item = CartItem.objects.get(order=cart, product=product)
            cart_item.quantity = quantity
            cart_item.save()
        except (Cart.DoesNotExist, Product.DoesNotExist, CartItem.DoesNotExist):
            raise UIDNotFound("Cart or product UID not found.")
