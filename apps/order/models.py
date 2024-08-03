from django.db import models
from django.utils.translation import gettext as _

from helpers.model_mixins import TrackingTimeStampMixin
from apps.accounts.models import User
from apps.provider.models import Product, Provider
from apps.logistic.models import Driver


# Create your models here.
class Order(TrackingTimeStampMixin):

    class OrderStates(models.TextChoices):
        waiting = ('W', _("Waiting for payment"),)
        expired = ('E', _("Expired payment"),)
        cancelled = ('C', _("Cancelled"),)
        prossesing = ('P', _("Processing"),)
        shipped = ('S', _("Shipped"),)
        delivered = ('D', _("Delivered"),)


    uid = models.CharField(
        _("Order UID"),
        unique=True
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
        null=True,
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

    
class Review(TrackingTimeStampMixin):
    uid = models.CharField(
        _("Review UID"),
        unique=True
    )
    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        related_name="reviews",
        on_delete=models.CASCADE
    )
    order = models.ForeignKey(
        Order,
        verbose_name=_("order"),
        related_name="reviews",
        on_delete=models.CASCADE
    )
    rating = models.PositiveSmallIntegerField(
        _("Rating")
    )
    message = models.CharField(
        _("Message"),
        max_length=300
    )
    driver_rating = models.PositiveSmallIntegerField(
        _("Driver rating")
    )