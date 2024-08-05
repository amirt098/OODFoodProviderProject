from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.provider.models import Provider, Product, Category
from apps.provider.services import ProviderService
from apps.provider.data_classes import ProviderInfo, ProductInfo, CategoryInfo

User = get_user_model()


class ProviderServiceTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345', uid='user123')
        self.provider_service = ProviderService()

        self.provider_info = ProviderInfo(
            manager_uid=self.user.uid,
            name='Test Provider',
            is_available=True,
            uid='provider123'
        )

        self.category = Category.objects.create(
            uid='category123',
            title='Test Category'
        )

        self.product_info = ProductInfo(
            title='Test Product',
            description='A test product',
            is_active=True,
            in_stock=10,
            image_path='/path/to/image.jpg',
            category_uid=self.category.uid,
            uid='product123'
        )

    def test_create_provider(self):
        self.provider_service.create_provider(self.provider_info)
        provider = Provider.objects.get(uid='provider123')
        self.assertEqual(provider.name, 'Test Provider')
        self.assertEqual(provider.manager, self.user)
        self.assertTrue(provider.is_available)

    def test_get_provider_id(self):
        provider = Provider.objects.create(
            name='Test Provider',
            uid='provider123',
            manager=self.user,
            is_available=True
        )
        provider_id = self.provider_service.get_provider_id('provider123')
        self.assertEqual(provider_id, provider.id)

    def test_open_provider(self):
        provider = Provider.objects.create(
            name='Test Provider',
            uid='provider123',
            manager=self.user,
            is_available=False
        )
        self.provider_service.open_provider('provider123')
        provider.refresh_from_db()
        self.assertTrue(provider.is_available)

    def test_close_provider(self):
        provider = Provider.objects.create(
            name='Test Provider',
            uid='provider123',
            manager=self.user,
            is_available=True
        )
        self.provider_service.close_provider('provider123')
        provider.refresh_from_db()
        self.assertFalse(provider.is_available)

    def test_add_product(self):
        provider = Provider.objects.create(
            name='Test Provider',
            uid='provider123',
            manager=self.user,
            is_available=True
        )
        self.provider_service.add_product(provider.uid, self.product_info)
        product = Product.objects.get(uid='product123')
        self.assertEqual(product.title, 'Test Product')
        self.assertEqual(product.description, 'A test product')
        self.assertTrue(product.is_active)
        self.assertEqual(product.in_stock, 10)
        self.assertEqual(product.image_path, '/path/to/image.jpg')
        self.assertEqual(product.provider, provider)
        self.assertEqual(product.category, self.category)

    def test_disable_product(self):
        product = Product.objects.create(
            title='Test Product',
            uid='product123',
            description='A test product',
            is_active=True,
            in_stock=10,
            image_path='/path/to/image.jpg',
            provider=Provider.objects.create(
                name='Test Provider',
                uid='provider123',
                manager=self.user,
                is_available=True
            ),
            category=self.category
        )
        self.provider_service.disable_product('product123')
        product.refresh_from_db()
        self.assertFalse(product.is_active)

    def test_update_product_price(self):
        product = Product.objects.create(
            title='Test Product',
            uid='product123',
            description='A test product',
            is_active=True,
            in_stock=10,
            image_path='/path/to/image.jpg',
            provider=Provider.objects.create(
                name='Test Provider',
                uid='provider123',
                manager=self.user,
                is_available=True
            ),
            category=self.category,
            price=100
        )
        self.provider_service.update_product_price('product123', 200)
        product.refresh_from_db()
        self.assertEqual(product.price, 200)

    def test_update_product_stock(self):
        product = Product.objects.create(
            title='Test Product',
            uid='product123',
            description='A test product',
            is_active=True,
            in_stock=10,
            image_path='/path/to/image.jpg',
            provider=Provider.objects.create(
                name='Test Provider',
                uid='provider123',
                manager=self.user,
                is_available=True
            ),
            category=self.category
        )
        self.provider_service.update_product_stock('product123', 20)
        product.refresh_from_db()
        self.assertEqual(product.in_stock, 20)

    def test_create_category(self):
        category_info = CategoryInfo(
            title='New Category',
            parent_category_uid=None,
            uid='category124'
        )
        self.provider_service.create_category(category_info)
        category = Category.objects.get(uid='category124')
        self.assertEqual(category.title, 'New Category')
        self.assertIsNone(category.parent)
