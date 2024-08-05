from django import forms
from .models import Provider, Product, Category


class ProviderForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = '__all__'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
