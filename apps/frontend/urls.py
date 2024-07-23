from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FrontendViewSet

router = DefaultRouter()
router.register(r'', FrontendViewSet, basename='frontend')

urlpatterns = [
    path('', include(router.urls)),
]
