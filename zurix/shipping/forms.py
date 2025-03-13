from django import forms
from .models import ShippingOrder

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingOrder
        fields = ['item_name', 'weight', 'dimensions', 'shipping_address']