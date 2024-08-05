# urls.py
from django.urls import path
from apps.cart.views import (
    CartListView, CartCreateView, CartUpdateView, CartDeleteView,
    CartItemListView, CartItemCreateView, CartItemUpdateView, CartItemDeleteView
)

urlpatterns = [
    path('carts/', CartListView.as_view(), name='cart-list'),
    path('carts/create/', CartCreateView.as_view(), name='cart-create'),
    path('carts/update/<int:pk>/', CartUpdateView.as_view(), name='cart-update'),
    path('carts/delete/<int:pk>/', CartDeleteView.as_view(), name='cart-delete'),

    path('cartitems/', CartItemListView.as_view(), name='cartitem-list'),
    path('cartitems/create/', CartItemCreateView.as_view(), name='cartitem-create'),
    path('cartitems/update/<int:pk>/', CartItemUpdateView.as_view(), name='cartitem-update'),
    path('cartitems/delete/<int:pk>/', CartItemDeleteView.as_view(), name='cartitem-delete'),
    path('add-to-cart/<str:product_uid>/', CartItemCreateView.as_view(), name='add-to-cart'),

]
