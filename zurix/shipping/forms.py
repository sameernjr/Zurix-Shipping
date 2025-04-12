from django import forms
from .models import ShippingOrder

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingOrder
        exclude = ['user', 'created_at', 'base_price', 'express_fee', 'total_price']
        widgets = {
            # Existing fields...
            'pickup_contact_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact person for pickup',
                'required': 'required'
            }),
            'pickup_contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number for pickup',
                'required': 'required'
            }),
            'destination_contact_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Recipient phone number',
                'required': 'required'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields except pick_up_point required
        for field in self.fields:
            if field not in ['pick_up_point']:
                self.fields[field].required = True