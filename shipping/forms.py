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

    def clean(self):
        cleaned_data = super().clean()
        weight = cleaned_data.get('weight')
        shipping_location = cleaned_data.get('shipping_location')
        shipping_type = cleaned_data.get('shipping_type')
        
        if weight is not None and weight <= 0:
            self.add_error('weight', "Weight must be greater than zero.")
        
        if not shipping_location:
            self.add_error('shipping_location', "Please select a shipping location.")
            
        if not shipping_type:
            self.add_error('shipping_type', "Please select a shipping type.")
            
        return cleaned_data