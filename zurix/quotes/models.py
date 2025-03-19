from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ShippingQuote(models.Model):
    REGION_CHOICES = [
        ('malaysia', 'Within Malaysia'),
        ('asia','Within Asia'),
        ('international', 'International'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    origin = models.Charfield(max_length=100)
    destination = models.CharField(max_length=100)
    region = models.CharField(max_length=100, choices=REGION_CHOICES)

    origin_country = models.CharField(max_length=100, blank=True)
    destination_country = models.CharField(max_length=100, blank=True)

    origin_address = models.TextField(blank=True)
    destination_address = models.TextField(blank=True)

    weight = models.DecimalField(max_digits=10, decimal_places=2)
    dimensions = models.CharField(max_length=50)
    item_description = models.TextField()
    shipping_method = models.CharField(max_length=50)
    estimated_price = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_delivery_time=models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    quote_id = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Quote {self.quote_id} - {self.origin} to {self.destination}"

    
