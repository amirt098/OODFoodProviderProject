# tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import datetime
from apps.cart.models import Cart, CartItem
from apps.provider.models import Product
from apps.cart.data_classes import CartInfo
from apps.cart.exceptions import UIDNotFound
from apps.accounts.models import User
from apps.provider.models import Provider
from apps.cart.service import CartService
from apps.accounts import abstraction as accounts_abstractions
from apps.order import abstraction as orders_abstractions
from unittest.mock import Mock

User = get_user_model()

class CartServiceTests(TestCase):

    def setUp(self):
        # Create mocks for services
        self.accounts_service = Mock(spec=accounts_abstractions.AbstractUserService)
        self.orders_service = Mock(spec=orders_abstractions.AbstractOrderService)
        self.cart_service = CartService(self.accounts_service, self.orders_service)

        # Create users, providers, and products
        self.user = User.objects.create_user(uid='user1', username='testuser', password='password')
        self.provider = Provider.objects.create(uid='provider1', name='Test Provider', manager=self.user, is_active=True)
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
        self.cart = Cart.objects.create(
            uid='cart1',
            user=self.user,
            provider=self.provider,
            address=None,
            footnote='Test Cart'
        )

    def test_get_cart(self):
        cart_info = self.cart_service.get_cart('cart1')
        self.assertEqual(cart_info.uid, 'cart1')
        self.assertEqual(cart_info.user_uid, self.user.uid)
        self.assertEqual(cart_info.footnote, 'Test Cart')

    def test_get_carts(self):
        carts = self.cart_service.get_carts(self.user.uid)
        self.assertEqual(len(carts), 1)
        self.assertEqual(carts[0].uid, 'cart1')

    def test_add_to_cart(self):
        self.cart_service.add_to_cart('cart1', 'product1', self.user.uid)
        cart_item = CartItem.objects.get(product=self.product, order=self.cart)
        self.assertEqual(cart_item.quantity, 1)
        self.assertEqual(cart_item.price, 100)

    def test_add_to_cart_existing_item(self):
        self.cart_service.add_to_cart('cart1', 'product1', self.user.uid)
        self.cart_service.add_to_cart('cart1', 'product1', self.user.uid)
        cart_item = CartItem.objects.get(product=self.product, order=self.cart)
        self.assertEqual(cart_item.quantity, 2)

    def test_delete_from_cart(self):
        self.cart_service.add_to_cart('cart1', 'product1', self.user.uid)
        self.cart_service.delete_from_cart('cart1', 'product1')
        with self.assertRaises(CartItem.DoesNotExist):
            CartItem.objects.get(product=self.product, order=self.cart)

    def test_update_quantity(self):
        self.cart_service.add_to_cart('cart1', 'product1', self.user.uid)
        self.cart_service.update_quantity('cart1', 'product1', 5)
        cart_item = CartItem.objects.get(product=self.product, order=self.cart)
        self.assertEqual(cart_item.quantity, 5)

    def test_get_cart_not_found(self):
        with self.assertRaises(UIDNotFound):
            self.cart_service.get_cart('nonexistent_uid')

    def test_get_carts_user_not_found(self):
        with self.assertRaises(UIDNotFound):
            self.cart_service.get_carts('nonexistent_user_uid')

    def test_add_to_cart_cart_not_found(self):
        with self.assertRaises(UIDNotFound):
            self.cart_service.add_to_cart('nonexistent_cart_uid', 'product1', self.user.uid)

    def test_add_to_cart_product_not_found(self):
        with self.assertRaises(UIDNotFound):
            self.cart_service.add_to_cart('cart1', 'nonexistent_product_uid', self.user.uid)

    def test_update_quantity_cart_not_found(self):
        with self.assertRaises(UIDNotFound):
            self.cart_service.update_quantity('nonexistent_cart_uid', 'product1', 5)

    def test_update_quantity_product_not_found(self):
        with self.assertRaises(UIDNotFound):
            self.cart_service.update_quantity('cart1', 'nonexistent_product_uid', 5)

    def test_update_quantity_item_not_found(self):
        with self.assertRaises(UIDNotFound):
            self.cart_service.update_quantity('cart1', 'product1', 5)
