# forms.py
from django import forms
from apps.cart.models import Cart, CartItem

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['uid', 'user', 'provider', 'address', 'footnote']

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['cart', 'product', 'quantity', 'price']
