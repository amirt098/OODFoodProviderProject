from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from apps.cart.models import Cart, CartItem
from apps.cart.forms import CartForm, CartItemForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from apps.cart.models import Cart, CartItem
from apps.provider.models import Product

class CartListView(ListView):
    model = Cart
    template_name = 'cart/cart_list.html'
    context_object_name = 'carts'


class CartCreateView(CreateView):
    model = Cart
    form_class = CartForm
    template_name = 'cart/cart_form.html'
    success_url = reverse_lazy('cart-list')


class CartUpdateView(UpdateView):
    model = Cart
    form_class = CartForm
    template_name = 'cart/cart_form.html'
    success_url = reverse_lazy('cart-list')


class CartDeleteView(DeleteView):
    model = Cart
    template_name = 'cart/cart_confirm_delete.html'
    success_url = reverse_lazy('cart-list')


class CartItemListView(ListView):
    model = CartItem
    template_name = 'cart/cartitem_list.html'
    context_object_name = 'cartitems'


class CartItemCreateView(CreateView):
    model = CartItem
    form_class = CartItemForm
    template_name = 'cart/cartitem_form.html'
    success_url = reverse_lazy('cartitem-list')


class CartItemUpdateView(UpdateView):
    model = CartItem
    form_class = CartItemForm
    template_name = 'cart/cartitem_form.html'
    success_url = reverse_lazy('cartitem-list')


class CartItemDeleteView(DeleteView):
    model = CartItem
    template_name = 'cart/cartitem_confirm_delete.html'
    success_url = reverse_lazy('cartitem-list')


class AddToCartView(CreateView):
    model = CartItem
    form_class = CartItemForm
    template_name = 'cart/cartitem_form.html'

    def post(self, request, *args, **kwargs):
        product_uid = kwargs.get('product_uid')
        product = get_object_or_404(Product, uid=product_uid)
        cart_uid = request.session.get('cart_uid')

        if not cart_uid:
            cart = Cart.objects.create(uid=str(uuid.uuid4()), user=request.user)
            request.session['cart_uid'] = cart.uid
        else:
            cart = get_object_or_404(Cart, uid=cart_uid)

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': 1, 'price': product.price}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return HttpResponseRedirect(reverse('provider-detail', args=[product.provider.pk]))