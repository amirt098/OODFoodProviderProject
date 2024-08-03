import abc
from typing import List
from .data_classes import OrderInfo, OrderFilter, OrderItemInfo


class AbstractOrderService(abc.ABC):
    @abc.abstractmethod
    def create_order(self, order: OrderInfo) -> None:
        """
        Create a new order
        Args:
            order (OrderInfo): Order information
        Return:
            None
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def get_order(self, uid: str) -> OrderInfo:
        """
        Get an order by uid
        Args:
            uid (str): uid of the order
        Raise:
           UIDNotFound : If the order uid is not found
        Return:
            OrderInfo: Order information
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def get_orders(self, filter: OrderFilter) -> List[OrderInfo]:
        """
        Get orders matching the given filter
        Args:
            filter (OrderFilter): filter class for order
        Return:
            OrderInfo: Order information
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def change_state(self, uid: str, state: str) -> None:
        """
        Change the state of an order
        Args:
            uid (str): uid of the order
            state (str): new state to be assigned
        Raise:
           UIDNotFound : If the order uid is not found
        Return:
            None
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def add_review(self, user_uid: str, order_uid: str, review: dict) -> None:
        """
        Add a new review to an order
        Args:
            user_uid (str): uid of the user
            order_uid (str): uid of the order
            review (dict): review to be added
        Raise:
           UIDNotFound : If the user or order uid is not found
        Return:
            None
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def set_driver(self, order_uid: str, driver_uid: str) -> None:
        """
        Assign a driver to an order
        Args:
            order_uid (str): uid of the order
            driver_uid (str): uid of the driver
        Raise:
           UIDNotFound : If the order or driver uid is not found
        Return:
            None
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def get_items(self, uid: str) -> List[OrderItemInfo]:
        """
        Get all items of an order
        Args:
            uid (str): uid of the order
        Raise:
           UIDNotFound : If the order uid is not found
        Return:
            List[OrderItemInfo]: list of all order items
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def accept_order(self, uid: str) -> None:
        """
        Accept an order by provider
        Args:
            uid (str): uid of the order
        Raise:
           UIDNotFound : If the order uid is not found
        Return:
            None
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def reject_order(self, uid: str) -> None:
        """
        Reject an order by provider
        Args:
            uid (str): uid of the order
        Raise:
           UIDNotFound : If the order uid is not found
        Return:
            None
        """
        raise NotImplementedError()
