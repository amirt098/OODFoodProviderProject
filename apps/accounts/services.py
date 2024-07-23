import uuid

from .abstraction import AbstractUserService
from .data_classes import UserInfo, UserRole, AddressList, AddressInfo, UserClaim
from .models import User, Address
from .exceptions import UsernameNotFound, PasswordNotFound, UIDNotFound
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from typing import List


class UserService(AbstractUserService):
    def login(self, username: str, password: str) -> UserClaim:
        try:
            user = get_user_model().objects.get(username=username)
            if check_password(password, user.password):
                user_claim = UserClaim(
                    uid=user.uid,
                    username=user.username,
                    email=user.email,
                    role=user.role,
                    id=user.id
                )
                return user_claim
            else:
                raise PasswordNotFound()
        except get_user_model().DoesNotExist:
            raise UsernameNotFound()

    def logout(self, request):
        if request.user.is_authenticated:
            request.session.flush()

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

    def modify_user(self, request: UserInfo, current_user: UserClaim) -> UserInfo:
        if request.uid != current_user.uid:
            raise PermissionError("You can only modify your own account.")
        try:
            user = User.objects.get(uid=request.uid)
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

    def get_addresses(self, username: str) -> AddressList:
        try:
            user = User.objects.get(username=username)
            addresses = user.addresses.all()
            address_list = [
                AddressInfo(
                    uid=address.id,
                    user_uid=user.uid,
                    title=address.title,
                    state=address.state,
                    city=address.city,
                    detail=address.detail,
                    location=address.location,
                    postal_code=address.postal_code
                ) for address in addresses
            ]
            return AddressList(addresses=address_list)
        except User.DoesNotExist:
            raise UIDNotFound()

    def get_info(self, username: str) -> UserInfo:
        try:
            user = User.objects.get(username=username)
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

    def get_full_name(self, username: str) -> str:
        try:
            user = User.objects.get(username=username)
            return f"{user.first_name} {user.last_name}"
        except User.DoesNotExist:
            raise UIDNotFound()

    def get_role(self, username: str) -> UserRole:
        try:
            user = User.objects.get(username=username)
            return user.role
        except User.DoesNotExist:
            raise UIDNotFound()
