from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from django.shortcuts import render, redirect
from .services import AccountService
from .data_classes import UserInfo, UserClaim
from .exceptions import UsernameNotFound, PasswordNotFound, UIDNotFound
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from pydantic import ValidationError

account_service = AccountService()

class UserViewSet(viewsets.ViewSet):
    # Remove JWTAuthentication from authentication_classes
    authentication_classes = []

    @action(detail=False, methods=['get', 'post'], permission_classes=[], url_path='register', name='user-register')
    def register(self, request):
        if request.method == 'POST':
            """
            API action to register a user.
            """
            try:
                data = {
                    'username': request.POST.get('username'),
                    'password': request.POST.get('password'),
                    'first_name': request.POST.get('first_name'),
                    'last_name': request.POST.get('last_name'),
                    'email': request.POST.get('email'),
                    'phone_number': request.POST.get('phone_number'),
                    'role': request.POST.get('role')
                }
                user_info = UserInfo(**data)
                new_user = account_service.register_user(user_info)
                return redirect('user-login')
            except ValueError as e:
                return render(request, 'register.html', {'error': str(e)})
            except ValidationError as e:
                return render(request, 'register.html', {'error': e.errors()})

        return render(request, 'register.html')

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='info', name='user-info')
    def user_info(self, request):
        """
        API action to get user information.
        """
        if request.user.is_authenticated:
            try:
                user_claim = UserClaim(
                    uid=request.user.id,
                    username=request.user.username,
                    email=request.user.email,
                    role=request.user.role
                )
                user_info = account_service.get_info(user_claim)
                return render(request, 'user_info.html', {'user_info': user_info.dict()})
            except UIDNotFound:
                return render(request, 'user_info.html', {'error': 'User not found'})
        else:
            return redirect('user-login')

    @action(detail=False, methods=['get', 'post'], permission_classes=[], url_path='login', name='user-login')
    def login(self, request):
        if request.method == 'POST':
            """
            API action to login a user.
            """
            try:
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('user-info')
                else:
                    return render(request, 'login.html', {'error': 'Invalid username or password'})
            except UsernameNotFound:
                return render(request, 'login.html', {'error': 'Username not found'})
            except PasswordNotFound:
                return render(request, 'login.html', {'error': 'Incorrect password'})

        return render(request, 'login.html')

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """
        API action to logout a user.
        """
        logout(request)
        return redirect('user-login')

    @action(detail=True, methods=['get', 'post'], url_path='modify', permission_classes=[IsAuthenticated], name='user-modify')
    def modify_user(self, request, uid):
        """
        API action to modify a user.
        """
        if request.method == 'POST':
            try:
                user_data = request.POST
                user_info = UserInfo(**user_data)
                caller = UserClaim(
                    uid=request.user.id,
                    username=request.user.username,
                    email=request.user.email,
                    role=request.user.role
                )
                modified_user = account_service.modify_user(user_info, caller)
                return redirect('user-info')
            except UIDNotFound:
                return render(request, 'modify_user.html', {'error': 'User not found'})
            except ValidationError as e:
                return render(request, 'modify_user.html', {'error': e.errors()})

        user_info = account_service.get_info(request.user)
        return render(request, 'modify_user.html', {'user_info': user_info.dict()})


def main_page_view(request):
    return render(request, 'main_page.html')
