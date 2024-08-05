# tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import Mock
from datetime import datetime, timezone
from apps.logistic.models import Driver
from apps.order.models import Order, OrderItem, Review
from apps.order.data_classes import OrderInfo, OrderFilter, OrderItemInfo
from apps.accounts import abstraction as accounts_abstractions
from apps.order.services import OrderService
from apps.provider import abstraction as provider_abstractions
from apps.provider.models import Provider, Product
from apps.accounts.models import User
from django.db.utils import IntegrityError

User = get_user_model()


class OrderServiceTests(TestCase):

    def setUp(self):
        # Create mocks for services
        self.account_service = Mock(spec=accounts_abstractions.AbstractUserService)
        self.provider_service = Mock(spec=provider_abstractions.AbstractProviderService)
        self.order_service = OrderService(self.account_service, self.provider_service)

        # Create users, providers, and products
        self.user = User.objects.create_user(uid='user1', username='testuser', password='password')
        self.provider = Provider.objects.create(uid='provider1', name='Test Provider', manager=self.user,
                                                is_active=True)
        self.product = Product.objects.create(
            uid='product1',
            title='Test Product',
            description='Test Description',
            is_active=True,
            in_stock=10,
            image_path='test/path',
            provider=self.provider,
            price=100
        )
        self.driver = Driver.objects.create(uid='driver1', name='Test Driver')

        self.account_service.get_user_id.return_value = self.user.id
        self.provider_service.get_provider_id.return_value = self.provider.id
        self.provider_service.get_product_id.return_value = self.product.id

        self.order_info = OrderInfo(
            uid='order1',
            state='pending',
            footnote='Test Order',
            user_uid=self.user.uid,
            provider_uid=self.provider.uid,
            order_items=[
                OrderItemInfo(
                    product_uid=self.product.uid,
                    price=100,
                    quantity=2
                )
            ]
        )

        self.order = Order.objects.create(
            uid='order1',
            state='pending',
            footnote='Test Order',
            user=self.user,
            provider=self.provider
        )
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=100,
            quantity=2
        )

    def test_create_order(self):
        self.order_service.create_order(self.order_info)
        order = Order.objects.get(uid='order1')
        self.assertEqual(order.uid, 'order1')
        self.assertEqual(order.state, 'pending')
        self.assertEqual(order.footnote, 'Test Order')
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.provider, self.provider)
        self.assertEqual(order.orderitem_set.count(), 1)
        order_item = OrderItem.objects.get(order=order)
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.price, 100)
        self.assertEqual(order_item.quantity, 2)

    def test_get_orders(self):
        filters = OrderFilter(uid='order1')
        orders = self.order_service.get_orders(filters)
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0].uid, 'order1')

    def test_get_order(self):
        order_info = self.order_service.get_order('order1')
        self.assertEqual(order_info.uid, 'order1')
        self.assertEqual(order_info.state, 'pending')
        self.assertEqual(order_info.footnote, 'Test Order')
        self.assertEqual(order_info.user_uid, self.user.id)
        self.assertEqual(order_info.provider_uid, self.provider.id)
        self.assertEqual(len(order_info.order_items), 1)

    def test_change_state(self):
        self.order_service.change_state('order1', 'completed')
        order = Order.objects.get(uid='order1')
        self.assertEqual(order.state, 'completed')

    def test_add_review(self):
        review_data = {
            'reting': 5,
            'message': 'Excellent service',
            'driver_rating': 4
        }
        self.order_service.add_review(self.user.uid, 'order1', review_data)
        review = Review.objects.get(order=self.order)
        self.assertEqual(review.reting, 5)
        self.assertEqual(review.message, 'Excellent service')
        self.assertEqual(review.driver_rating, 4)
        self.assertEqual(review.user, self.user)

    def test_set_driver(self):
        self.order_service.set_driver(self.driver.uid, 'order1')
        order = Order.objects.get(uid='order1')
        self.assertEqual(order.driver, self.driver)

    def test_get_items(self):
        items = self.order_service.get_items('order1')
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].product_uid, self.product.uid)
        self.assertEqual(items[0].price, 100)
        self.assertEqual(items[0].quantity, 2)

    def test_accept_order(self):
        self.order_service.accept_order('order1')
        order = Order.objects.get(uid='order1')
        self.assertEqual(order.state, 'processing')

    def test_reject_order(self):
        self.order_service.reject_order('order1')
        order = Order.objects.get(uid='order1')
        self.assertEqual(order.state, 'cancelled')

    def test_declare_delivered(self):
        self.order_service.declare_delivered('order1')
        order = Order.objects.get(uid='order1')
        self.assertEqual(order.state, 'delivered')

    def test_declare_not_received(self):
        self.order_service.declare_not_received('order1')
        order = Order.objects.get(uid='order1')
        self.assertEqual(order.state, 'shipped')

    def test_get_reviews(self):
        review_data = {
            'reting': 5,
            'message': 'Great experience',
            'driver_rating': 5
        }
        self.order_service.add_review(self.user.uid, 'order1', review_data)
        reviews = self.order_service.get_reviews('order1')
        self.assertEqual(len(reviews), 1)
        self.assertEqual(reviews[0].rating, 5)
        self.assertEqual(reviews[0].message, 'Great experience')

    def test_create_order_invalid_product(self):
        self.provider_service.get_product_id.side_effect = IntegrityError
        with self.assertRaises(IntegrityError):
            self.order_service.create_order(self.order_info)
