from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
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

class AccountView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = Bootstrapper().get_accounts_service()

    def get(self, request, action):
        if action == 'login':
            form = LoginForm()
            return render(request, 'accounts/login.html', {'form': form})
        elif action == 'register':
            form = RegisterForm()
            return render(request, 'accounts/register.html', {'form': form})
        elif action == 'profile':
            print(request.user, '$$$')
            # user_claim = self.service.get_info(request.user.username)
            form = UserProfileForm()
            return render(request, 'accounts/profile.html', {'form': form})
        return redirect(reverse('frontend-home'))

    def post(self, request, action):
        if action == 'login':
            form = LoginForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                try:
                    user = self.service.login(request, username, password)
                    login(request, user)
                    request.session['role'] = user.role
                    messages.success(request, f'Login Successful, Welcome {user.username}')
                    return render(request, 'home.html')
                except Exception as e:
                    print(f'exception: {e}')
                    messages.error(request, "Invalid Credentials")
                    return render(request, 'home.html')
            messages.error(request, "Invalid form submission")
            return redirect(reverse('accounts-login'))

        elif action == 'logout':
            self.service.logout(request)
            messages.success(request, 'Logout Successful')
            return redirect(reverse('accounts-login'))

        elif action == 'register':
            form = RegisterForm(request.POST)
            if form.is_valid():
                try:
                    user_info = form.cleaned_data
                    self.service.register_user(UserInfo(**user_info))
                    messages.success(request, 'Registration Successful')
                    return redirect(reverse('accounts-login'))
                except Exception as e:
                    messages.error(request, f'Error: {e}')
                    return redirect(reverse('accounts-register'))
            messages.error(request, 'Invalid form submission')
            return redirect(reverse('accounts-register'))

        elif action == 'profile':
            form = UserProfileForm(request.POST)
            if form.is_valid():
                try:
                    self.service.modify_user(
                        UserInfo(**form.cleaned_data),
                        request.user.uid
                    )
                    messages.success(request, 'Profile updated')
                    return redirect(reverse('accounts-profile'))
                except UIDNotFound:
                    messages.error(request, 'Profile not found')
                except PermissionError:
                    messages.error(request, 'Profile permission denied')
            messages.error(request, 'Invalid form submission')
            return redirect(reverse('accounts-profile'))

        return redirect(reverse('frontend-home'))  # Default action
