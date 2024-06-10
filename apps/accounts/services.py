import uuid

from apps.accounts.abstraction import AbstractAccountService
from .data_classes import UserRole, UserInfo, AddressList, UserClaim, AddressInfo
from .models import User
from .exceptions import UsernameNotFound, PasswordNotFound, UIDNotFound
from typing import List


class AccountService(AbstractAccountService):
    def __init__(self):
        self.logged_in_users = {}

    def login(self, username: str, password: str) -> UserClaim:
        print(f'username: {username}, password: {password}')
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                user_claim = UserClaim(uid=user.uid, username=user.username, email=user.email, role=user.role, id=user.id)
                self.logged_in_users[username] = user_claim
                return user_claim
            else:
                print('Invalid password')
                raise PasswordNotFound()
        except User.DoesNotExist:
            print('User not found')
            raise UsernameNotFound()

    def logout(self, caller: UserClaim):
        if caller.username in self.logged_in_users:
            del self.logged_in_users[caller.username]
        else:
            raise UsernameNotFound()

    def register_user(self, request: UserInfo) -> UserInfo:
        if User.objects.filter(username=request.username).exists():
            raise ValueError("Username already exists")

        user = User(
            uid=str(uuid.uuid4()),
            username=request.username,
            email=request.email,
            first_name=request.first_name,
            last_name=request.last_name,
            phone_number=request.phone_number,
            role=request.role
        )
        user.set_password(request.password)
        user.save()
        return request

    def modify_user(self, request: UserInfo, caller: UserClaim) -> UserInfo:
        try:
            user = User.objects.get(uid=caller.uid)
            user.username = request.username
            user.email = request.email
            user.first_name = request.first_name
            user.last_name = request.last_name
            user.phone_number = request.phone_number
            user.role = request.role
            if request.password:
                user.set_password(request.password)
            user.save()
            return request
        except User.DoesNotExist:
            raise UIDNotFound()

    def get_addresses(self, caller: UserClaim) -> AddressList:
        # Assuming you have a related Address model
        try:
            user = User.objects.get(uid=caller.uid)
            addresses = AddressInfo.objects.filter(user=user)  # Adjust as per your actual Address model
            address_list = [
                AddressInfo(uid=str(address.uid), title=address.title, state=address.state, city=address.city,
                            detail=address.detail, location=address.location, postal_code=address.postal_code) for
                address in addresses]
            return AddressList(addresses=address_list)
        except User.DoesNotExist:
            raise UIDNotFound()

    def get_info(self, caller: UserClaim) -> UserInfo:
        try:
            user = User.objects.get(uid=caller.uid)
            return UserInfo(
                uid=user.uid,
                username=user.username,
                password='',  # Not returning the password for security reasons
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                phone_number=user.phone_number,
                role=user.role
            )
        except User.DoesNotExist:
            raise UIDNotFound()

    def get_full_name(self, caller: UserClaim) -> str:
        try:
            user = User.objects.get(uid=caller.uid)
            return f"{user.first_name} {user.last_name}"
        except User.DoesNotExist:
            raise UIDNotFound()

    def get_role(self, caller: UserClaim) -> UserRole:
        try:
            user = User.objects.get(uid=caller.uid)
            return user.role
        except User.DoesNotExist:
            raise UIDNotFound()
