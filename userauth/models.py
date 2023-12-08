from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


# custom user code begins
# custom model manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password, **extra_fields):
        if not email:
            raise ValueError(_('Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must be staff'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have superuser set to true'))
        return self.create_user(email, name, password, **extra_fields)


# user model - using AbstractBaseUser
class Customer(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(_('First and last name'), max_length=250)
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = CustomUserManager()

    def __str__(self):
        return self.email
# custom user code ends


# account info for shipping
class AccountInfo(models.Model):
    COUNTRIES = (
        ('GH', 'Ghana'),
        ('UK', 'United Kingdom'),
        ('USA', 'United States')
    )
    house_number = models.CharField(max_length=250)
    street = models.CharField(max_length=250)
    town = models.CharField(max_length=250)
    region_or_county = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    country = models.CharField(max_length=100, choices=COUNTRIES, default='UK')
    phone = models.CharField(max_length=20)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.customer.email
