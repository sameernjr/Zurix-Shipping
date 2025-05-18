from django import forms
from .models import Shipping

class ShippingForm(forms.ModelForm):
    class Meta:
        model = Shipping
        fields = [
            'weight',
            'shipping_location',
            'pickup_location',
            'pickup_contact',
            'destination_location',
            'destination_contact',
            'shipping_type',
        ]