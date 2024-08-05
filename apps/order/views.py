# views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound

from apps.order.models import Order
from apps.order.data_classes import OrderInfo, OrderFilter
from apps.order.forms import OrderSerializer, ReviewSerializer
from apps.order.services import OrderService
from apps.accounts.abstraction import AbstractUserService
from apps.provider.abstraction import AbstractProviderService

class OrderViewSet(viewsets.ViewSet):
    def __init__(self, *args, **kwargs):
        self.account_service = kwargs.pop('account_service', None)
        self.provider_service = kwargs.pop('provider_service', None)
        super().__init__(*args, **kwargs)

    def get_service(self):
        return OrderService(self.account_service, self.provider_service)

    def create(self, request):
        data = request.data
        order_info = OrderInfo(
            uid=data.get('uid'),
            state=data.get('state'),
            footnote=data.get('footnote'),
            user_uid=data.get('user_uid'),
            provider_uid=data.get('provider_uid'),
            order_items=data.get('order_items')
        )
        service = self.get_service()
        service.create_order(order_info)
        return Response(status=status.HTTP_201_CREATED)

    def list(self, request):
        filters = request.query_params
        order_filter = OrderFilter(**filters)
        service = self.get_service()
        orders = service.get_orders(order_filter)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        service = self.get_service()
        try:
            order_info = service.get_order(pk)
            serializer = OrderSerializer(order_info)
            return Response(serializer.data)
        except Exception as e:
            raise NotFound(detail=str(e))

    def update(self, request, pk=None):
        data = request.data
        state = data.get('state')
        service = self.get_service()
        try:
            if state not in ['processing', 'cancelled', 'delivered', 'shipped']:
                return Response({"detail": "Invalid state"}, status=status.HTTP_400_BAD_REQUEST)
            if state == 'processing':
                service.accept_order(pk)
            elif state == 'cancelled':
                service.reject_order(pk)
            elif state == 'delivered':
                service.declare_delivered(pk)
            elif state == 'shipped':
                service.declare_not_received(pk)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            raise NotFound(detail=str(e))

    @action(detail=True, methods=['post'])
    def add_review(self, request, pk=None):
        user_uid = request.data.get('user_uid')
        review_data = {
            'reting': request.data.get('reting'),
            'message': request.data.get('message'),
            'driver_rating': request.data.get('driver_rating'),
        }
        service = self.get_service()
        try:
            service.add_review(user_uid, pk, review_data)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            raise NotFound(detail=str(e))

    @action(detail=True, methods=['post'])
    def set_driver(self, request, pk=None):
        driver_uid = request.data.get('driver_uid')
        service = self.get_service()
        try:
            service.set_driver(driver_uid, pk)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            raise NotFound(detail=str(e))

    @action(detail=True, methods=['get'])
    def get_reviews(self, request, pk=None):
        service = self.get_service()
        try:
            reviews = service.get_reviews(pk)
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data)
        except Exception as e:
            raise NotFound(detail=str(e))
