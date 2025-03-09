from django import forms
from .models import ShipingOrder

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShipingOrder
        fields = ['item_name', 'weight', 'dimensions', 'shipping_address']