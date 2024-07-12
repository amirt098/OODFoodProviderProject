import abc
from typing import List
from .data_classes import ProductInfo, CategoryInfo, ProductFilter


class AbstractProviderService(abc.ABC):
    @abc.abstractmethod
    def open_provider(self, uid: int) -> None:
        """
        Set provider status to open
        Args:
            uid (int): uid of the provider
        Raise:
           UIDNotFound : If the provider uid is not found
        Return:
            None
        """
        raise NotImplementedError()
         
    @abc.abstractmethod
    def close_provider(self, uid: int) -> None:
        """
        Set provider status to closed
        Args:
            uid (int): uid of the provider
        Raise:
           UIDNotFound : If the provider uid is not found
        Return:
            None
        """
        raise NotImplementedError()
         
    @abc.abstractmethod
    def add_product(self, uid:int, product: ProductInfo) -> None:
        """
        Add a product to provider menu
        Args:
            uid (int): uid of the provider
            product (ProductInfo): Product information
        Raise:
           UIDNotFound : If the provider uid is not found
        Return:
            None
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def disable_product(self, uid: int) -> None:
        """
        Disable a product
        Args:
            uid (int): uid of the product
        Raise:
           UIDNotFound : If the product uid is not found
        Return:
            None
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def update_product_price(self, uid: int, price: int) -> None:
        """
        Update a product price
        Args:
            uid (int): uid of the product
            price (int): new price of the product
        Raise:
           UIDNotFound : If the product uid is not found
        Return:
            None
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def update_product_stock(self, uid: int, stock: int) -> None:
        """
        Update a product stock
        Args:
            uid (int): uid of the product
            stock (int): new stock of the product
        Raise:
           UIDNotFound : If the product uid is not found
        Return:
            None
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_product(self, uid: int) -> ProductInfo:
        """
        Get a products information
        Args:
            uid (int): uid of the product
        Raise:
           UIDNotFound : If the product uid is not found
        Return:
            ProductInfo: Products information
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_product(self, filter: ProductFilter) -> List[ProductInfo]:
        """
        Get products matching the given filter
        Args:
            filter (ProductFilter): filter class for product
        Return:
            List of ProductInfo: List of product informations
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def create_category(self, category: CategoryInfo) -> None:
        """
        Get products matching the given filter
        Args:
            category (CategoryInfo): Category data class
        Return:
            None
        """
        raise NotImplementedError()