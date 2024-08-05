from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext as _


class UserRole(models.TextChoices):
    ADMIN = 'ADMIN', 'Admin'
    CUSTOMER = 'CUSTOMER', 'Customer'
    DRIVER = 'DRIVER', 'Driver'
    PROVIDER_MANAGER = 'PROVIDER_MANAGER', 'Provider Manager'


class User(AbstractUser):
    phone_number = models.CharField(max_length=20)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.CUSTOMER)
    uid = models.CharField(unique=True, max_length=120)
    created_at = models.BigIntegerField(blank=True, null=True)

    groups = models.ManyToManyField(Group, related_name='accounts_user_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='accounts_user_permissions', blank=True)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    title = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    detail = models.TextField()
    location = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=20)