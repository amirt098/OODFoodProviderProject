from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.utils.translation import gettext as _

from helpers.model_mixins import TrackingTimeStampMixin

class UserRole(models.TextChoices, TrackingTimeStampMixin):
    ADMIN = 'ADMIN', 'Admin'
    CUSTOMER = 'CUSTOMER', 'Customer'
    DRIVER = 'DRIVER', 'Driver'
    PROVIDER_MANAGER = 'PROVIDER_MANAGER', 'Provider Manager'


class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.CUSTOMER)
    uid = models.CharField(unique=True)
    username = models.CharField(unique=True, max_length=30)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True)

    USERNAME_FIELD = 'username'


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    title = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    detail = models.TextField()
    location = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=20)