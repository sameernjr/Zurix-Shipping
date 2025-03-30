from django import forms
from .models import ShippingQuote

class ShippingQuoteForm(forms.ModelForm):
    REGION_CHOICES = [
        ('within_malaysia', 'Within Malaysia'),
        ('within_asia', 'Within Asia'),
        ('international', 'International'),
    ]
    
    SHIPPING_METHOD_CHOICES = [
        ('standard', 'Standard Shipping'),
        ('express', 'Express Shipping'),
        ('overnight', 'Overnight Shipping'),
    ]

    MALAYSIA_STATES = [
        ('', 'Select State'),
        ('johor', 'Johor'),
        ('kedah', 'Kedah'),
        ('kelantan', 'Kelantan'),
        ('melaka', 'Melaka'),
        ('negeri sembilan', 'Negeri Sembilan'),
        ('pahang', 'Pahang'),
        ('perak', 'Perak'),
        ('perlis', 'Perlis'),
        ('penang', 'Penang'),
        ('sabah', 'Sabah'),
        ('sarawak', 'Sarawak'),
        ('selangor', 'Selangor'),
        ('terengganu', 'Terengganu'),
        ('wilayah persekutuan', 'Wilayah Persekutuan'),
    ]

    region = forms.ChoiceField(
        choices=REGION_CHOICES, 
        required=True, 
        widget=forms.Select(attrs={'class':'form-control', 'id':'id_region'})
    )
    
    origin_country = forms.ChoiceField(
        choices=[('', 'Select Country')], 
        required=False, 
        widget=forms.Select(attrs={'class':'form-control', 'id':'id_origin_country'})
    )

    destination_country = forms.ChoiceField(
        choices=[('', 'Select Country')], 
        required=False, 
        widget=forms.Select(attrs={'class':'form-control', 'id':'id_destination_country'})
    )

    origin_state = forms.ChoiceField(
        choices=[('', 'Select State')], 
        required=False, 
        widget=forms.Select(attrs={'class':'form-control', 'id':'id_origin_state'})
    )

    destination_state = forms.ChoiceField(
        choices=[('', 'Select State')], 
        required=False, 
        widget=forms.Select(attrs={'class':'form-control', 'id':'id_destination_state'})
    )

    shipping_method = forms.ChoiceField(
        choices=SHIPPING_METHOD_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class':'form-control', 'id':'id_shipping_method'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Predefined country choices for different regions
        malaysia_countries = [('malaysia', 'Malaysia')]
        asian_countries = [
            ('malaysia', 'Malaysia'),
            ('singapore', 'Singapore'),
            ('indonesia', 'Indonesia'),
            ('thailand', 'Thailand'),
            ('vietnam', 'Vietnam')
        ]
        international_countries = [
            ('malaysia', 'Malaysia'),
            ('australia', 'Australia'),
            ('canada', 'Canada'),
            ('united states', 'United States'),
            ('united kingdom', 'United Kingdom')
        ]

        # Update choices based on region
        if self.initial.get('region') == 'within_malaysia':
            self.fields['origin_country'].choices = [('', 'Select Country')] + malaysia_countries
            self.fields['destination_country'].choices = [('', 'Select Country')] + malaysia_countries
            self.fields['origin_state'].choices = self.MALAYSIA_STATES
            self.fields['destination_state'].choices = self.MALAYSIA_STATES
        elif self.initial.get('region') == 'within_asia':
            self.fields['origin_country'].choices = [('', 'Select Country')] + asian_countries
            self.fields['destination_country'].choices = [('', 'Select Country')] + asian_countries
        elif self.initial.get('region') == 'international':
            self.fields['origin_country'].choices = [('', 'Select Country')] + international_countries
            self.fields['destination_country'].choices = [('', 'Select Country')] + international_countries

    class Meta:
        model = ShippingQuote
        fields = [
            'region', 'origin_country', 'origin_state', 'origin_address',
            'destination_country', 'destination_state', 'destination_address',
            'weight', 'dimensions', 'item_description', 'shipping_method'
        ]

    def clean(self):
        cleaned_data = super().clean()
        region = cleaned_data.get('region')

        # Validation logic
        if region == 'within_malaysia':
            origin_country = cleaned_data.get('origin_country')
            destination_country = cleaned_data.get('destination_country')
            origin_state = cleaned_data.get('origin_state')
            destination_state = cleaned_data.get('destination_state')

            if not origin_country or origin_country != 'malaysia':
                self.add_error('origin_country', 'Must select Malaysia for this region')
            if not destination_country or destination_country != 'malaysia':
                self.add_error('destination_country', 'Must select Malaysia for this region')
            if not origin_state:
                self.add_error('origin_state', 'State is required for Malaysia')
            if not destination_state:
                self.add_error('destination_state', 'State is required for Malaysia')

        return cleaned_data