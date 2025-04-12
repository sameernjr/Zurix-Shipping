from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

class ShippingOrder(models.Model):
    REGION_CHOICES = [
        ('Malaysia,','Malaysia'),
        ('Asia','Asia'),
        ('International','International'),
    ]

    SHIPPING_METHOD_CHOICES = [
        ('Standard','Standard'),
        ('Express','Express'),
    ]