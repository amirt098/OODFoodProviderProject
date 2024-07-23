from django.db import models
from accounts.models import User

from django.utils.translation import gettext as _

# Create your models here.
class Driver(models.Model):
    uid = models.CharField(
        _("Druver UID"),
        unique=True,
    )

    user = models.OneToOneField(
        User, 
        verbose_name=_("User"), 
        related_name="driver", 
        on_delete=models.CASCADE
    )
    
    plate_number = models.CharField(
        _("Plate number"), 
        max_length=20
    )

    location = models.CharField(
        _("Location"), 
        max_length=100
    )

    is_available = models.BooleanField(
        _("Is available"), 
        default=False
    )
    
    last_paycheck = models.DateTimeField(
        _("Last paycheck"),
    )

