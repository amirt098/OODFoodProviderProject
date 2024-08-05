import abc
from typing import List
from .data_classes import ProductInfo, CategoryInfo, ProductFilter, ProviderInfo


class AbstractProviderService(abc.ABC):
    @abc.abstractmethod
    def get_provider_id(self, uid: str) -> int:
        """
        Get database id of the provider (only for foreign keys)
        Args:
            uid (str): uid of the provider
        Raise:
           UIDNotFound : If the provider uid is not found
        Return:
            int : database id of the provider
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def get_product_id(self, uid: str) -> int:
        """
        Get database id of the product (only for foreign keys)
        Args:
            uid (str): uid of the product
        Raise:
           UIDNotFound : If the product uid is not found
        Return:
            int : database id of the product
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def open_provider(self, uid: str) -> None:
        """
        Set provider status to open
        Args:
            uid (str): uid of the provider
        Raise:
           UIDNotFound : If the provider uid is not found
        Return:
            None
        """
        raise NotImplementedError()
         
    @abc.abstractmethod
    def close_provider(self, uid: str) -> None:
        """
        Set provider status to closed
        Args:
            uid (str): uid of the provider
        Raise:
           UIDNotFound : If the provider uid is not found
        Return:
            None
        """
        raise NotImplementedError()
         
    @abc.abstractmethod
    def add_product(self, provider_uid:int, product: ProductInfo) -> None:
        """
        Add a product to provider menu
        Args:
            provider_uid (str): uid of the provider
            product (ProductInfo): Product information
        Raise:
           UIDNotFound : If the provider uid is not found
        Return:
            None
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def disable_product(self, uid: str) -> None:
        """
        Disable a product
        Args:
            uid (str): uid of the product
        Raise:
           UIDNotFound : If the product uid is not found
        Return:
            None
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def update_product_price(self, uid: str, price: int) -> None:
        """
        Update a product price
        Args:
            uid (str): uid of the product
            price (int): new price of the product
        Raise:
           UIDNotFound : If the product uid is not found
        Return:
            None
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def update_product_stock(self, uid: str, stock: int) -> None:
        """
        Update a product stock
        Args:
            uid (str): uid of the product
            stock (int): new stock of the product
        Raise:
           UIDNotFound : If the product uid is not found
        Return:
            None
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_product(self, uid: str) -> ProductInfo:
        """
        Get a products information
        Args:
            uid (str): uid of the product
        Raise:
           UIDNotFound : If the product uid is not found
        Return:
            ProductInfo: Products information
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_products(self, filter: ProductFilter) -> List[ProductInfo]:
        """
        Get products matching the given filter
        Args:
            filter (ProductFilter): filter class for product
        Return:
            List of ProductInfo: List of product information
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def create_category(self, category: CategoryInfo) -> None:
        """
        Create Category
        Args:
            category (CategoryInfo): Category data class
        Return:
            None
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def create_provider(self, provider: ProviderInfo) -> None:
        """
        Create Provider
        Args:
            provider (CategoryInfo): provider data class
        Return:
            None
        """
        raise NotImplementedError()
