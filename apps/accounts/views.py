from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from FoodProviderProject.bootstrapper import Bootstrapper
from .forms import LoginForm, RegisterForm, UserProfileForm
from .exceptions import UsernameNotFound, PasswordNotFound, UIDNotFound
from .data_classes import UserInfo
import dataclasses
from django.shortcuts import render


class AccountViewSet(viewsets.ViewSet):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = Bootstrapper().get_accounts_service()

    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user_claim = self.service.login(username, password)
                user = authenticate(username=username, password=password)
                if user:
                    login(request, user)
                    return Response({"detail": "Login successful"}, status=status.HTTP_200_OK)
                return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            except UsernameNotFound:
                return Response({"detail": "Username not found"}, status=status.HTTP_404_NOT_FOUND)
            except PasswordNotFound:
                return Response({"detail": "Invalid password"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='logout', permission_classes=[IsAuthenticated])
    def logout(self, request):
        self.service.logout(request)
        logout(request)
        return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get', 'post'], url_path='register')
    def register(self, request):
        if request.method == 'GET':
            form = RegisterForm()
            return render(request, 'accounts/register.html', {'form': form})

        form = RegisterForm(request.POST)

        if form.is_valid():
            try:
                user_info = form.cleaned_data
                self.service.register_user(UserInfo(**user_info))
                return Response({"detail": "Registration successful"}, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get', 'post'], url_path='profile', permission_classes=[IsAuthenticated])
    def profile(self, request):
        """
        User profile management method.
        """
        if request.method == 'GET':
            user_claim = self.service.get_info(request.user.username)
            form = UserProfileForm(initial=dataclasses.asdict(user_claim))
            return Response(form.initial, status=status.HTTP_200_OK)

        elif request.method == 'POST':
            form = UserProfileForm(request.POST)
            if form.is_valid():
                try:
                    user_claim = self.service.get_info(request.user.username)
                    self.service.modify_user(UserInfo(**form.cleaned_data), user_claim)
                    return Response({"detail": "Profile updated"}, status=status.HTTP_200_OK)
                except UIDNotFound:
                    return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
                except PermissionError:
                    return Response({"detail": "You can only modify your own account."},
                                    status=status.HTTP_403_FORBIDDEN)
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
