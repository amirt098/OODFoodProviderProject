from apps.account.abstraction import AbstractAccountService
from . import data_classes
from .data_classes import UserRole, UserInfo, AddressList


class AccountService(AbstractAccountService):

    def __init__(self):
        pass

    def get_addresses(self, username: str) -> AddressList:
        pass

    def get_info(self, username: str) -> UserInfo:
        pass

    def get_full_name(self, username: str) -> str:
        pass

    def get_role(self, username: str) -> UserRole:
        pass

    def login(self, username: str, password: str):
        pass

    def logout(self):
        pass

    def register_user(self, request: data_classes.UserInfo) -> data_classes.UserInfo:
        pass

    def modify_user(self, request: data_classes.UserInfo) -> data_classes.UserInfo:
        pass
