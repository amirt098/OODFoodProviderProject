from django.db import models
from accounts.models import User

from django.utils.translation import gettext as _

# Create your models here.
class Provider(models.Model):
    uid = models.PositiveIntegerField(
        unique=True
    )

    manager = models.OneToOneField(
        User, 
        verbose_name=_("User"), 
        related_name="provider", 
        on_delete=models.CASCADE
    )
    
    name = models.CharField(
        _("Name"), 
        max_length=50
    )

    is_available = models.BooleanField(
        _("Is available"), 
        default=False
    )


class Category(models.Model):
    uid = models.PositiveIntegerField(
        unique=True
    )

    title = models.CharField(
        _("Title"),
        max_length=50
    )

    parent = models.ForeignKey(
        'self',
        verbose_name=_("parent"),
        related_name="children",
        on_delete=models.PROTECT,
        null=True,
    )



class Product(models.Model):
    uid = models.PositiveIntegerField(
        unique=True
    )

    title = models.CharField(
        _("Title"),
        max_length=50
    )

    description = models.CharField(
        _("Description"),
        max_length=300
    )

    is_active = models.BooleanField(
        _("Is active"), 
        default=False
    )

    in_stock = models.PositiveSmallIntegerField(
        _("Stock")
    )

    image_path = models.CharField(
        _("Image"),
        max_length=100
    )

    provider = models.ForeignKey(
        Provider,
        verbose_name=_("Provider"),
        related_name="Products",
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        verbose_name=_("Category"),
        related_name="products",
        on_delete=models.PROTECT
    )
