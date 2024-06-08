from apps.account.abstraction import AbstractAccountService
from . import data_classes


class AccountService(AbstractAccountService):

    def __init__(self):
        pass

    def login(self, username: str, password: str):
        pass

    def logout(self):
        pass

    def register_user(self, request: data_classes.UserInfo) -> data_classes.UserInfo:
        pass

    def modify_user(self, request: data_classes.UserInfo) -> data_classes.UserInfo:
        pass


