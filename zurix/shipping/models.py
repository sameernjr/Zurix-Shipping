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

    #Origin Information

    region = models.CharField(
        max_length=20,
        choices=REGION_CHOICES
    )

    origin_state_country = models.Charfield(
        max_length=100,
    )
    origin_address = models.TextField()

    pick_up_point = models.CharField(
        max_length=225,
        blank=True,
        null=True,
    )
    pickup_contact_name = models.Charfield(
        max_length=100,
    )
    pickup_contact_number = models.CharField(
        max_length=20,
    )

    #Destination Information
    destination_state_country = models.CharField(
        max_length=100,
    )
    destination_address = models.TextField()
    destination_contact_name = models.CharField(
        max_length=100,
    )
    destination_contact_number = models.CharField(
        max_length=20,
    )

    #Shipping Method

    shipping_method = models.Charfield(
        max_length=20,
        choices=SHIPPING_METHOD_CHOICES,
    )

    #Pricing Information

    base_-price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    express_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def __str__(self):
        return f"Order #{self.id} ({self.total_price} USD)"
    
    def calculate_pricing(self):
        
        if self.region == 'Malaysia':
            self.base_price = 20 if float(self.package_weight) < 1 else 20* float(self.package_weight)
        elif self.region == 'Asia':
            self.base_price = 50 if float(self.package_weight) < 1 else 50 * float(self.package_weight)
        else:
            self.base_price = 100 if float(self.package_weight) < 1 else 100 * float(self.package_weight)

        # Calculate express fee
        self.express_fee = 30 if self.shipping_method == 'Express' else 0

        # Calculate total price
        self.total_price = self.base_price + self.express_fee

        def save(self, *args, **kwargs):
            self.calculate_pricing()
            super().save(*args, **kwargs)

        class Meta:
            ordering = ['created_at']



