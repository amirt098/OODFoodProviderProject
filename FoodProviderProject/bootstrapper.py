import logging
from apps.accounts.services import UserService
from apps.accounts.abstraction import AbstractUserService

from apps.order.abstraction import AbstractOrderService
from apps.provider.abstraction import AbstractProviderService
from apps.logistic.abstraction import AbstractDriverService
from apps.cart.abstraction import AbstractCartService

from apps.order.services import OrderService
from apps.provider.services import ProviderService
from apps.logistic.services import DriverService
from apps.cart.services import CartService

logger = logging.getLogger(__name__)


class Borg:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class Bootstrapper(Borg):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Bootstrapper, cls).__new__(cls)
        return cls._instance

    def __init__(self, kwargs=None):
        if kwargs is None:
            kwargs = {}
        Borg.__init__(self)
        if not hasattr(self, '_initialized'):  # Only initialize once

            logger.debug(f'kwargs:{kwargs}')

            self._accounts_service = kwargs.get(
                'accounts_service',
                UserService()
            )

            self._cart_service = kwargs.get('cart_service',
                                            None)

            self._logins_service = kwargs.get(
                'logins_service',
                DriverService(
                ))
            self._provider_service = kwargs.get(
                'provider_service',
                ProviderService()
            )
            self._orders_service = kwargs.get(
                'orders_service',
                OrderService(
                    account_service=self._accounts_service,
                    provider_service=self._provider_service
                ))
            self._initialized = True  # Mark as initialized

    def get_accounts_service(self) -> AbstractUserService:
        return self._accounts_service

    def get_cart_service(self) -> AbstractCartService:
        return self._cart_service

    def get_orders_service(self) -> AbstractOrderService:
        return self._orders_service

    def get_logistic_service(self) -> AbstractDriverService:
        return self._logins_service

    def get_provider_service(self) -> AbstractProviderService:
        return self._provider_service
