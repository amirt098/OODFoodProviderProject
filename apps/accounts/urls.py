from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AccountView

urlpatterns = [
    path('login/', AccountView.as_view(), {'action': 'login'}, name='accounts-login'),
    path('logout/', AccountView.as_view(), {'action': 'logout'}, name='accounts-logout'),
    path('register/', AccountView.as_view(), {'action': 'register'}, name='accounts-register'),
    path('profile/', AccountView.as_view(), {'action': 'profile'}, name='accounts-profile'),
]