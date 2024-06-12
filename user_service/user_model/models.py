from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class Fullname(models.Model):
    first_name = models.CharField(max_length=150, blank=True)
    mid_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    class Meta:
        db_table = 'fullnames'


class Address(models.Model):
    no_house = models.CharField(max_length=20)
    street = models.CharField(max_length=150)
    district = models.CharField(max_length=150)
    city = models.CharField(max_length=150)

    class Meta:
        db_table = 'addresses'


class Account(AbstractUser):
    first_name = None
    last_name = None
    mobile_number = models.CharField(max_length=12)

    class Meta:
        db_table = 'accounts'

    REQUIRED_FIELDS = []


class User(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    full_name = models.OneToOneField(Fullname, on_delete=models.SET_NULL, null=True)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'users'


