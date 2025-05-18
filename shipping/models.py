from django.db import models

class Shipping(models.Model):
    class TypeChoices(models.TextChoices):
        MALAYSIA = 'MY', 'Malaysia'
        ASIA = 'AS', 'Asia'
        INTERNATIONAL = 'INT', 'International'

    class ShippingType(models.TextChoices):
        STANDARD = 'ST', 'Standard'
        EXPRESS = 'EX', 'Express'
        
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    shipping_location = models.CharField(max_length=255, choices=TypeChoices.choices)
    pickup_location = models.CharField(max_length=255)
    pickup_contact = models.CharField(max_length=255)
    destination_location = models.CharField(max_length=255)
    destination_contact = models.CharField(max_length=255)
    shipping_type = models.CharField(max_length=2, choices=ShippingType.choices)

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
    
    
