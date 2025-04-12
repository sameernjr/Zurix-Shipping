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

    #User Relationship

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')

    created_at = models.DateTimeField(auto_now_add=True)

    #Package Information
    package_weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinLengthValidator(0.1)],
        help_text="Weight in kg",
    )

    