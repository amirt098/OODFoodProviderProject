import abc
from typing import List

from .data_classes import CartInfo

class AbstractCartService(abc.ABC):
    @abc.abstractmethod
    def get_cart(self, uid: str) -> CartInfo:
        """
        Get a cart by uid.
        Args:
            uid (int): uid of the cart
        Raise:
           UIDNotFound : If the cart uid is not found
        Return:
            CartInfo: Cart information
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def get_carts(self, uid: str) -> List[CartInfo]:
        """
        Get all cart belonging to the user
        Args:
            uid (int): uid of the user
        Raise:
           UIDNotFound : If the user uid is not found
        Return:
            List[CartInfo]: Lisr of cart informations
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def add_to_cart(self, cart_uid: str, product_uid: str) -> None:
        """
        Add a product to a cart
        Args:
            cart_uid (int): uid of the cart
            product_uid (int): uid of the product
        Raise:
           UIDNotFound : If the cart or product uid is not found
        Return:
            None
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def delete_from_cart(self, cart_uid: str, product_uid: str) -> None:
        """
        Delete a product to a cart
        Args:
            cart_uid (int): uid of the cart
            product_uid (int): uid of the product
        Raise:
           UIDNotFound : If the cart or product uid is not found
        Return:
            None
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def update_quantity(self, cart_uid: str, product_uid: str, quantity: int) -> None:
        """
        Update a product quantity in a cart
        Args:
            cart_uid (int): uid of the cart
            product_uid (int): uid of the product
            quantity (int): new quantity of the product
        Raise:
           UIDNotFound : If the cart or product uid is not found
        Return:
            None
        """
        raise NotImplementedError()
