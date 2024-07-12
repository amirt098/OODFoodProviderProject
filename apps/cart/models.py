from django.db import models
from accounts.models import User, Address
from provider.models import Provider, Product

from django.utils.translation import gettext as _

# Create your models here.
class Cart(models.Model):
    uid = models.PositiveIntegerField(
        unique=True
    )

    user = models.ForeignKey(
        User, 
        verbose_name=_("User"), 
        related_name="carts", 
        on_delete=models.CASCADE
    )

    provider = models.ForeignKey(
        Provider, 
        verbose_name=_("Provider"), 
        related_name="carts", 
        on_delete=models.CASCADE
    )

    products = models.ManyToManyField(
        Product,
        verbose_name=_("Products"),
        related_name="carts",
        through="CartItem"
    )

    address = models.ForeignKey(
        Address, 
        verbose_name=_("Address"), 
        related_name="carts", 
        on_delete=models.CASCADE
    )

class CartItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    order = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    quantity = models.IntegerField(
        _("Quantity"),
        default=1
    )

    price = models.PositiveBigIntegerField(
        _("Sell Price"),
    )

    @property
    def get_total_order_product_price(self):
        return self.quantity * self.price

    