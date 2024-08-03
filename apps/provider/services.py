from typing import List

from apps.provider.abstraction import AbstractProviderService
from apps.provider.models import (
    Provider,
    Product,
    Category
)
from apps.provider.data_classes import (
    ProductInfo,
    CategoryInfo,
    ProductFilter,
)


class ProviderService(AbstractProviderService):

    def get_provider_id(self, uid: str):
        return Provider.objects.get(uid=uid).id

    def get_product_id(self, uid: str):
        return Product.objects.get(uid=uid).id
    
    def open_provider(self, uid: str) -> None:
        provider = Provider.objects.get(uid=uid)
        provider.is_available = True
        provider.save()

    def close_provider(self, uid: str) -> None:
        provider = Provider.objects.get(uid=uid)
        provider.is_available = False
        provider.save()

    def add_product(self, provider_uid: str, product: ProductInfo) -> None:
        provider = Provider.objects.get(uid=provider_uid)
        category = Category.objects.get(uid=product.category_uid)
        product = Product.objects.create(
            uid=product.uid,
            title=product.title,
            description=product.description,
            is_active=product.is_active,
            in_stock=product.in_stock,
            image_path=product.image_path,
            provider=provider,
            category=category,
        )
        product.save()

    def disable_product(self, uid: str) -> None:
        product = Product.objects.get(uid=uid)
        product.is_active = False
        product.save()

    def update_product_price(self, uid: str, price: int) -> None:
        product = Product.objects.get(uid=uid)
        product.price = price
        product.save()

    def update_product_stock(self, uid: str, stock: int) -> None:
        product = Product.objects.get(uid=uid)
        product.in_stock = stock
        product.save()

    def get_product(self, uid: str) -> ProductInfo:
        product = Product.objects.get(uid=uid)
        return ProductInfo(
            uid=product.uid,
            title=product.title,
            description=product.description,
            is_active=product.is_active,
            in_stock=product.in_stock,
            image_path=product.image_path,
            categoty_uid=product.categoty.uid,
        )

    def get_products(self, filter: ProductFilter) -> List[ProductInfo]:
        return [ProductInfo(
            uid=product.uid,
            title=product.title,
            description=product.description,
            is_active=product.is_active,
            in_stock=product.in_stock,
            image_path=product.image_path,
            categoty_uid=product.categoty.uid,
        ) for product in Product.objects.filter(**filter)]
    
    def create_category(self, category: CategoryInfo) -> None:
        category = Category.objects.create(
            uid=category.uid,
            title=category.title,
            parent=Category.object.get(uid=category.parent_category_uid),
        )
        category.save()


