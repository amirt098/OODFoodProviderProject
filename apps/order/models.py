from django.db import models

# Create your models here.
from django.db import models
from accounts.models import User
from provider.models import Product, Provider
from logistic.models import Driver

from django.utils.translation import gettext as _

# Create your models here.
class Order(models.Model):

    class OrderStates(models.TextChoices):
        waiting = ('W', _("Waiting for payment"),)
        expired = ('E', _("Expired payment"),)
        cancelled = ('C', _("Cancelled"),)
        prossesing = ('P', _("Processing"),)
        shipped = ('S', _("Shipped"),)
        delivered = ('D', _("Delivered"),)


    uid = models.PositiveIntegerField(
        unique=True
    )

    created_at = models.DateTimeField(
        _('Created at'),
    )

    state = models.CharField(
        _("Status"),
        max_length=1,
        choices=OrderStates.choices,
        default=OrderStates.waiting,
    )

    footnote = models.TextField(
        _("Footnote"),
        help_text=_("any additional info needed by admins"),
        null =True,
        blank=True
    )

    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        related_name="orders",
        on_delete=models.PROTECT
    )

    driver = models.ForeignKey(
        Driver,
        verbose_name=_("Driver"),
        related_name="orders",
        on_delete=models.PROTECT
    )

    provider = models.ForeignKey(
        Provider,
        verbose_name=_("Provider"),
        related_name="orders",
        on_delete=models.PROTECT
    )

    products = models.ManyToManyField(
        Product,
        verbose_name=_("Products"),
        related_name="orders",
        through="OrderItem"
    )

class OrderItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_items"
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="order_items"
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

    
class Review(models.Model):
    uid = models.PositiveIntegerField(
        unique=True
    )

    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        related_name="orders",
        on_delete=models.CASCADE
    )

    reting = models.PositiveSmallIntegerField(
        _("Rating")
    )

    created_at = models.DateTimeField(
        _('Created at')
    )

    message = models.CharField(
        _("Message"),
        max_length=300
    )

    driver_rating = models.PositiveSmallIntegerField(
        _("Driver rating")
    )