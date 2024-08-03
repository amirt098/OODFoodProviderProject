"""
URL configuration for FoodProviderProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path


from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter


urlpatterns = [
    # path('', main_page_view, name='main_page'),
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    # path('cart/', include('cart.urls')),   # Cart app
    # path('orders/', include('order.urls')), # Order app
    path('account/', include('apps.accounts.urls')), # Account app
    # path('provider/', include('provider.urls')), # Provider app
    # path('driver/', include('driver.urls')),   # Driver app

]
