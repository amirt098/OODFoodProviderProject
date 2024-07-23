from typing import List

from apps.order.abstraction import AbstractOrderService
from apps.order.models import (
    Order,
    OrderItem,
    Review,
)
from apps.order.data_classes import (
    OrderInfo,
    OrderFilter, 
    OrderItemInfo,
)
from apps.accounts.services import AccountService
from apps.provider.services import ProviderService


class OrderService(AbstractOrderService):

    account_service = AccountService()
    provider_service = ProviderService()
    
    def create_order(self, orderinfo: OrderInfo) : # -> Order
        order = Order(
            uid=orderinfo.uid,
            state=orderinfo.state,
            footnote=orderinfo.footnote,
            user_id=self.account_service.get_user_id(uid=orderinfo.user_uid),
            provider_id=self.provider_service.get_provider_id(uid=orderinfo.provider_uid),
        )
        order.save()
        for item in orderinfo.order_items:
            orderitem = OrderItem(
                order=order,
                product_id=self.provider_service.get_product_id(uid=item.product_uid),
                price=item.price,
                quantity=item.quantity,
            )
            orderitem.save()

    def get_orders(self, filters: OrderFilter) -> List[OrderInfo]:
        return [OrderInfo(
            uid=order.uid,
            user_uid=order.user.id,
            provider_uid=order.provider.id,
            created=order.created,
            state=order.state,
            footnote=order.footnote,
            order_items=self.get_items(order.uid),
        ) for order in Order.objects.filter(**filters)]

    def get_order(self, uid: str) -> OrderInfo:
        order = Order.objects.get(uid=uid)
        return OrderInfo(
            uid=order.uid,
            user_uid=order.user.id,
            provider_uid=order.provider.id,
            created=order.created,
            state=order.state,
            footnote=order.footnote,
            order_items=self.get_items(uid),
        )
    
    def change_state(self, uid: str, state: str) -> None:
        order = Order.objects.get(uid=uid)
        order.state = state
        order.save()

    def add_review(self, user_uid: str, order_uid: str, review: dict) -> None:
        review = Review(
            user=self.account_service.get_user_id(uid=user_uid),
            order=Order.objects.get(uid=order_uid),
            reting=review['reting'],
            message=review['message'],
            driver_rating=review['driver_rating'],
        )
        review.save()

    def set_driver(self, deriver_uid: str, order_uid: str) -> None:
        order = Order.objects.get(uid=order_uid)
        #TODO: fix after implementing driver_service
        order.driver = Driver.objects.get(uid=deriver_uid)
        order.save()

    def get_items(self, uid: str):
        order = Order.objects.get(uid=uid)
        return [OrderItemInfo(
                product_uid = item.product.uid,
                price = item.price,
                quantity = item.quantity,
        ) for item in order.products]
    
    def accept_order(self, uid: str) -> None:
        order = Order.objects.get(uid=uid)
        order.state = Order.OrderStates.prossesing
        order.save()

    def reject_order(self, uid: str) -> None:
        order = Order.objects.get(uid=uid)
        order.state = Order.OrderStates.cancelled
        order.save()

    def declare_delivered(self, uid: str) -> None:
        order = Order.objects.get(uid=uid)
        order.state = Order.OrderStates.delivered
        order.save()
        
    def declare_not_received(self, uid: str) -> None:
        order = Order.objects.get(uid=uid)
        order.state = Order.OrderStates.shipped
        order.save()

    def get_reviews(self, uid: str) -> List[Review]:
        return list(Order.objects.get(uid=uid).reviews)
    



