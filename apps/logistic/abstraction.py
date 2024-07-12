import abc
from .data_classes import DriverInfo, DriverList, DriverFilter


class AbstractDriverService(abc.ABC):
    @abc.abstractmethod
    def get_driver(self, uid: int) -> DriverInfo:
        """
        Get driver information
        Args:
            uid (int): uid of the driver
        Raise:
           UIDNotFound : If the driver uid is not found
        Return:
            Driver information
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def get_drivers(self, filter: DriverFilter) -> DriverList:
        """
        Get drivers matching the given filter
        Args:
            filter (DriverFilter): filter class for drivers
        Return:
            List of driver informations
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_nearest_driver(self, location: str) -> DriverInfo:
        """
        Get nearest driver information
        Args:
            location (str): location of pickup point
        Return:
            Driver information
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def update_location(self, uid: int, location: str):
        """
        Update driver location.
        Args:
            uid (int): uid of the driver
            location (int): new location of driver
        Raise:
           UIDNotFound : If the driver uid is not found
        Return:
            None
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def update_paycheck(self, uid: int):
        """
        Update driver last peycheck.
        Args:
            uid (int): uid of the driver
        Raise:
           UIDNotFound : If the driver uid is not found
        Return:
            None
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_balance(self, uid: int) -> int:
        """
        Get driver current balance.
        Args:
            uid (int): uid of the driver
        Raise:
           UIDNotFound : If the driver uid is not found
        Return:
            int: Driver's currecnt balance
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_location(self, uid: int) -> str:
        """
        Get driver current location.
        Args:
            uid (int): uid of the driver
        Raise:
           UIDNotFound : If the driver uid is not found
        Return:
            str: Driver's currecnt location
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def update_availability(self, uid: int, is_available: bool):
        """
        Get driver current location.
        Args:
            uid (int): uid of the driver
            is_available (bool): new availability status
        Raise:
           UIDNotFound : If the driver uid is not found
        Return:
            None
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def create_driver(self, driver: DriverInfo):
        """
        Get driver current location.
        Args:
            uid (int): uid of the driver
            is_available (bool): new availability status
        Raise:
           UIDNotFound : If the driver uid is not found
        Return:
            None
        """
        raise NotImplementedError()








