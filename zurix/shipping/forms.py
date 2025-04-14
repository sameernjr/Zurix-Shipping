from django import forms
from .models import ShippingOrder

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingOrder
        fields = '__all__'
        exclude = ['user','created_at','base_price', 'express_fee', 'total_price']
        widgets = {
            'package_weight': forms.NumberInput(attrs={
                'step': '0.1',
                'min': '0.1',
                'required': 'required',
                'placeholder': 'Weight in kg'
            }),
            'region': forms.Select(attrs={'required': 'required'}),
            'origin_state_country': forms.TextInput(attrs={
                'placeholder': 'State or country',
                'required': 'required'
            }),
            'origin_address': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Full address',
                'required': 'required'
            }),
            'pick_up_point': forms.TextInput(attrs={
                'placeholder': 'Specific pick up location if needed'
            }),
            'pickup_contact_name': forms.TextInput(attrs={
                'placeholder': 'Contact person for pickup',
                'required': 'required'
            }),
            'pickup_contact_phone': forms.TextInput(attrs={
                'placeholder': 'Phone number for pickup',
                'required': 'required'
            }),
            'destination_state_country': forms.TextInput(attrs={
                'placeholder': 'State or country',
                'required': 'required'
            }),
            'destination_address': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Full address',
                'required': 'required'
            }),
            'destination_contact_name': forms.TextInput(attrs={
                'placeholder': 'Recipient name',
                'required': 'required'
            }),
            'destination_contact_number': forms.TextInput(attrs={
                'placeholder': 'Recipient phone number',
                'required': 'required'
            }),
            'shipping_method': forms.Select(attrs={'required': 'required'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove any string validators that might have been added
        if 'package_weight' in self.fields:
            self.fields['package_weight'].validators = [
                v for v in self.fields['package_weight'].validators 
                if not hasattr(v, 'code') or v.code != 'max_length'
            ]