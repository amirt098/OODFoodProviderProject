from django.db import models
from apps.accounts.models import User, Address
from apps.provider.models import Provider, Product

from django.utils.translation import gettext as _


class CartItem(models.Model):
    product = models.ForeignKey(
        Product,
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


class Cart(models.Model):
    uid = models.CharField(
        _("Cart UID"),
        max_length=150,
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

    cart_items = models.ManyToManyField(
        CartItem,
        verbose_name=_("Products"),
        related_name="carts",
        through="CartItem"
    )

    address = models.ForeignKey(
        Address,
        verbose_name=_("Address"),
        related_name="carts",
        on_delete=models.CASCADE,
        null=True, blank=True
    )

    footnote = models.TextField(null=True, blank=True)
