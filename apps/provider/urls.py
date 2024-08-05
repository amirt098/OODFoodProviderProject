
from .views import ProviderViewSet, ProductViewSet

from django.urls import path, include
from rest_framework.routers import DefaultRouter
#
#
# router = DefaultRouter()
# router.register(r'provider', ProviderViewSet, basename='provider')
# router.register(r'product', ProductViewSet, basename='product')
#
# urlpatterns = [
#     path('', include(router.urls)),
# ]
# apps/provider/urls.py
from django.urls import path
from apps.provider.views import ProviderViewSet, ProductViewSet

provider_list = ProviderViewSet.as_view({'get': 'list'})
provider_create = ProviderViewSet.as_view({'get': 'create', 'post': 'create'})
provider_update = ProviderViewSet.as_view({'get': 'update', 'post': 'update'})
provider_destroy = ProviderViewSet.as_view({'post': 'destroy'})
provider_detail = ProviderViewSet.as_view({'get': 'retrieve'})

product_list = ProductViewSet.as_view({'get': 'list'})
product_create = ProductViewSet.as_view({'get': 'create', 'post': 'create'})
product_update = ProductViewSet.as_view({'get': 'update', 'post': 'update'})
product_delete = ProductViewSet.as_view({'post': 'delete'})

urlpatterns = [
    path('providers/', provider_list, name='provider-list'),
    path('providers/create/', provider_create, name='provider-create'),
    path('providers/update/<int:pk>/', provider_update, name='provider-update'),
    path('providers/destroy/<int:pk>/', provider_destroy, name='provider-destroy'),
    path('providers/detail/<int:pk>/', provider_detail, name='provider-detail'),
    path('products/', product_list, name='product-list'),
    path('products/create/', product_create, name='product-create'),
    path('products/update/<int:pk>/', product_update, name='product-update'),
    path('products/delete/<int:pk>/', product_delete, name='product-delete'),
]
