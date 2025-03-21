from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class ShippingOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    item_name = models.CharField(max_length=100)
    weight = models.FloatField()
    dimensions = models.CharField(max_length=50)
    shipping_address = models.TextField()
    cost = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #(self.id) by {self.user.username}"