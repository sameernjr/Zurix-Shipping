from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
import uuid

class Shipping(models.Model):
    class TypeChoices(models.TextChoices):
        MALAYSIA = 'MY', 'Malaysia'
        ASIA = 'AS', 'Asia'
        INTERNATIONAL = 'INT', 'International'

    class ShippingType(models.TextChoices):
        STANDARD = 'ST', 'Standard'
        EXPRESS = 'EX', 'Express'
        
    class StatusChoices(models.TextChoices):
        PENDING = 'P', 'Pending'
        PROCESSING = 'PR', 'Processing'
        SHIPPED = 'S', 'Shipped'
        DELIVERED = 'D', 'Delivered'
        CANCELLED = 'C', 'Cancelled'
    
    order_id = models.CharField(primary_key=True, max_length=255, editable=False)
    order_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    weight = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0.01, message="Weight must be greater than zero.")]
    )
    shipping_location = models.CharField(max_length=255, choices=TypeChoices.choices)
    pickup_location = models.CharField(max_length=255)
    pickup_contact = models.CharField(max_length=255)
    destination_location = models.CharField(max_length=255)
    destination_contact = models.CharField(max_length=255)
    shipping_type = models.CharField(max_length=2, choices=ShippingType.choices)
    status = models.CharField(
        max_length=2, 
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        help_text="Current status of the shipping order"
    )


    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self._generate_unique_order_id()
        super().save(*args, **kwargs)

    def _generate_unique_order_id(self):

        from datetime import datetime
        year = datetime.now().year
        unique_id = str(uuid.uuid4()).split('-')[0].upper()
        order_id = f"ZX-{year}-{unique_id}"

        while Shipping.objects.filter(order_id=order_id).exists():
            unique_id = str(uuid.uuid4()).split('-')[0].upper()
            order_id = f"ZX-{year}-{unique_id}"

        return order_id

    def calculate_shipping_cost(self):

        location_rates = {
            self.TypeChoices.MALAYSIA: 10.00,
            self.TypeChoices.ASIA: 20.00,
            self.TypeChoices.INTERNATIONAL: 30.00,
        }

        base_rate = location_rates.get(self.shipping_location, 0)
        base_cost = float(self.weight) * base_rate

        if self.shipping_type == self.ShippingType.EXPRESS:
            base_cost += 20

        return base_cost

    def clean(self):
        from django.core.exceptions import ValidationError
        
        errors = {}
        
        # Ensure destination is different from pickup
        if self.destination_location == self.pickup_location:
            errors['destination_location'] = "Destination cannot be the same as pickup location."
        
        # Validate contacts (example: validate phone number format)
        if not (self.pickup_contact and len(self.pickup_contact) >= 5):
            errors['pickup_contact'] = "Please provide a valid pickup contact."
        
        if not (self.destination_contact and len(self.destination_contact) >= 5):
            errors['destination_contact'] = "Please provide a valid destination contact."
        
        if errors:
            raise ValidationError(errors)

class ShippingPreview:

    def __init__(self, form_data):
        self.weight = form_data.get('weight')
        self.shipping_location = form_data.get('shipping_location')
        self.pickup_location = form_data.get('pickup_location')
        self.pickup_contact = form_data.get('pickup_contact')
        self.destination_location = form_data.get('destination_location')
        self.destination_contact = form_data.get('destination_contact')
        self.shipping_type = form_data.get('shipping_type')

    def get_shipping_location_display(self):
        location_choices = dict(Shipping.TypeChoices.choices)
        return location_choices.get(self.shipping_location, '')
    
    def get_shipping_type_display(self):
        type_choices = dict(Shipping.ShippingType.choices)
        return type_choices.get(self.shipping_type, '')
    
    def calculate_shipping_cost(self):
        location_rates = {
            Shipping.TypeChoices.MALAYSIA: 10.00,
            Shipping.TypeChoices.ASIA: 20.00,
            Shipping.TypeChoices.INTERNATIONAL: 30.00,
        }

        # Validate weight
        if not self.weight:
            return 0
        
        try:
            weight = float(self.weight)
        except (ValueError, TypeError):
            return 0
        
        # Validate shipping location
        if not self.shipping_location or self.shipping_location not in [choice[0] for choice in Shipping.TypeChoices.choices]:
            return 0
        
        # Validate shipping type
        if not self.shipping_type or self.shipping_type not in [choice[0] for choice in Shipping.ShippingType.choices]:
            # Use standard shipping as fallback if type is invalid
            self.shipping_type = Shipping.ShippingType.STANDARD
        
        base_rate = location_rates.get(self.shipping_location, 0)
        base_cost = weight * base_rate

        if self.shipping_type == Shipping.ShippingType.EXPRESS:
            base_cost += 20

        return base_cost


