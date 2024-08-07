from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

# Create a router and register our viewset with it.
router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]