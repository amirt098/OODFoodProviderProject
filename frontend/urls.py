from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HomeView, AboutView, ContactView

router = DefaultRouter()
# URL Configuration
urlpatterns = [
    path('', HomeView.as_view(), name='frontend-home'),  # Home page
    path('about/', AboutView.as_view(), name='frontend-about'),  # About page
    path('contact/', ContactView.as_view(), name='frontend-contact'),  # Contact page
    # path('services/', ServicesView.as_view(), name='frontend-services'),  # Uncomment if needed
]