from django import forms
from .models import ShippingOrder

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingOrder
        fields = [
            'package_weight',
            'region',
            'origin_state_country',
            'origin_address',
            'pick_up_point',
            'pickup_contact_name',
            'pickup_contact_number',
            'destination_state_country',
            'destination_address',
            'destination_contact_name',
            'destination_contact_number',
            'shipping_method'
        ]
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
        # Make all fields except pick_up_point required
        for field_name, field in self.fields.items():
            if field_name != 'pick_up_point':
                field.required = True
            field.widget.attrs.update({'class': 'form-control'})