# apps/provider/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.provider.forms import ProviderForm, ProductForm
from apps.provider.models import Provider, Product

class ProviderViewSet(viewsets.ViewSet):

    def list(self, request):
        providers = Provider.objects.all()
        return render(request, 'provider/provider_list.html', {'providers': providers})

    def create(self, request):
        if request.method == 'POST':
            form = ProviderForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Provider created successfully.')
                return redirect('provider-list')
            else:
                messages.error(request, 'Error creating provider.')
        else:
            form = ProviderForm()
        return render(request, 'provider/provider_form.html', {'form': form})

    def retrieve(self, request, pk=None):
        provider = get_object_or_404(Provider, pk=pk)
        return render(request, 'provider/provider_detail.html', {'provider': provider})

    def update(self, request, pk=None):
        provider = get_object_or_404(Provider, pk=pk)
        if request.method == 'POST':
            form = ProviderForm(request.POST, instance=provider)
            if form.is_valid():
                form.save()
                messages.success(request, 'Provider updated successfully.')
                return redirect('provider-list')
            else:
                messages.error(request, 'Error updating provider.')
        else:
            form = ProviderForm(instance=provider)
        return render(request, 'provider/provider_form.html', {'form': form})

    def destroy(self, request, pk=None):
        provider = get_object_or_404(Provider, pk=pk)
        if request.method == 'POST':
            provider.delete()
            messages.success(request, 'Provider deleted successfully.')
            return redirect('provider-list')
        return render(request, 'provider/provider_confirm_delete.html', {'provider': provider})

class ProductViewSet(viewsets.ViewSet):

    def list(self, request):
        products = Product.objects.all()
        return render(request, 'provider/product_list.html', {'products': products})

    def create(self, request):
        if request.method == 'POST':
            form = ProductForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Product created successfully.')
                return redirect('product-list')
            else:
                messages.error(request, 'Error creating product.')
        else:
            form = ProductForm()
        return render(request, 'provider/product_form.html', {'form': form})

    def retrieve(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        return render(request, 'provider/product_detail.html', {'product': product})

    def update(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        if request.method == 'POST':
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, 'Product updated successfully.')
                return redirect('product-list')
            else:
                messages.error(request, 'Error updating product.')
        else:
            form = ProductForm(instance=product)
        return render(request, 'provider/product_form.html', {'form': form})

    def destroy(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        if request.method == 'POST':
            product.delete()
            messages.success(request, 'Product deleted successfully.')
            return redirect('product-list')
        return render(request, 'provider/product_confirm_delete.html', {'product': product})


