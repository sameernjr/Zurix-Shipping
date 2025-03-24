from django import forms
from .models import ShippingQuote

class ShippingQuoteForm(forms.ModelForm):

    REGION_CHOICES = [
        ('within_malaysia', 'Within Malaysia'),
        ('within_asia','Within Asia'),
        ('international', 'International'),
    ]
    MALAYSIA_STATES = [
        ('','Select State'),
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

    ASIAN_COUNTRIES = [
        ('','Select Country'),
        ('afghanistan', 'Afghanistan'),
        ('bahrain', 'Bahrain'),
        ('bangladesh', 'Bangladesh'),
        ('bhutan', 'Bhutan'),
        ('brunei', 'Brunei'),
        ('cambodia', 'Cambodia'),
        ('china', 'China'),
        ('india', 'India'),
        ('indonesia', 'Indonesia'),
        ('iran', 'Iran'),
        ('iraq', 'Iraq'),
        ('israel','Israel'),
        ('japan','Japan'),
        ('jordan','Jordan'),
        ('kazakhstan','Kazakhstan'),
        ('kuwait','Kuwait'),
        ('kyrgyzstan','Kyrgyzstan'),
        ('laos','Laos'),
        ('lebanon','Lebanon'),
        ('malaysia','Malaysia'),
        ('maldives','Maldives'),
        ('mongolia','Mongolia'),
        ('myanmar','Myanmar'),
        ('nepal','Nepal'),
        ('north korea','North Korea'),
        ('oman','Oman'),
        ('pakistan','Pakistan'),
        ('philippines','Philippines'),
        ('qatar','Qatar'),
        ('saudi arabia','Saudi Arabia'),
        ('singapore','Singapore'),
        ('south korea','South Korea'),
        ('sri lanka','Sri Lanka'),
        ('syria','Syria'),
        ('taiwan','Taiwan'),
        ('tajikistan','Tajikistan'),
        ('thailand','Thailand'),
        ('turkmenistan','Turkmenistan'),
        ('united arab emirates','United Arab Emirates'),
        ('uzbekistan','Uzbekistan'),
        ('vietnam','Vietnam'),
        ('yemen','Yemen'),
    ]

    INTERNATIONAL_COUNTRIES = [
        ('','Select Country'),
        ('australia', 'Australia'),
        ('austria', 'Austria'),
        ('belgium','Belgium'),
        ('brazil','Brazil'),
        ('canada','Canada'),
        ('chile','Chile'),
        ('colombia','Colombia'),
        ('czech republic','Czech Republic'),
        ('denmark','Denmark'),
        ('egypt','Egypt'),
        ('finland','Finland'),
        ('finland','Finland'),
        ('france','France'),
        ('germany','Germany'),
        ('greece','Greece'),
        ('iceland','Iceland'),
        ('ireland','Ireland'),
        ('italy','Italy'),
        ('jamaica','Jamaica'),
        ('japan','Japan'),
        ('kenya','Kenya'),
        ('mexico','Mexico'),
        ('netherlands','Netherlands'),
        ('new zealand','New Zealand'),
        ('norway','Norway'),
        ('pakistan','Pakistan'),
        ('poland','Poland'),
        ('portugal','Portugal'),
        ('russia','Russia'),
        ('singapore','Singapore'),
        ('south africa','South Africa'),
        ('spain','Spain'),
        ('sweden','Sweden'),
        ('switzerland','Switzerland'),
        ('thailand','Thailand'),
        ('turkey','Turkey'),
        ('united kingdom','United Kingdom'),
        ('united states','United States'),
        ('vietnam','Vietnam'),
    ]


    region = forms.ChoiceField(
        choices=REGION_CHOICES, 
        required=True, 
        widget=forms.Select(attrs={'class':'form-control', 'id':'id_region'})
    )
    
    origin_country = forms.ChoiceField(
        choices=[('','Select Country')], 
        required=False, 
        widget=forms.Select(attrs={'class':'form-control', 'id':'id_origin_country'})
    )

    destination_country = forms.ChoiceField(
        choices=[('','Select Country')], 
        required=False, 
        widget=forms.Select(attrs={'class':'form-control', 'id':'id_destination_country'})
    )

    origin_state = forms.ChoiceField(
        choices=[('','Select State')], 
        required=False, 
        widget=forms.Select(attrs={'class':'form-control', 'id':'id_origin_state'})
    )

    destination_state = forms.ChoiceField(
        choices=[('','Select State')], 
        required=False, 
        widget=forms.Select(attrs={'class':'form-control', 'id':'id_destination_state'})
    )

    origin_address = forms.CharField(
        widget=forms.Textarea(attrs={'class':'form-control', 'rows':'3'}),
        required=True, 
    )

    class Meta:
        model = ShippingQuote
        fields = [
            'region', 'origin_country', 'origin_state', 'origin_address',
            'destination_country', 'destination_state', 'destination_address',
            'weight', 'dimensions', 'item_description', 'shipping_method'
        ]

        widgets = {
            'region': forms.Select(attrs={'class':'form-control', 'id':'id_region'}),
            'weight': forms.NumberInput(attrs={'class':'form-control'}),
            'dimensions': forms.TextInput(attrs={'class':'form-control','placeholder':'Length x Width x Height'}),
            'item_description': forms.Textarea(attrs={'class':'form-control', 'rows':'3'}),
            'shipping_method': forms.Select(attrs={'class':'form-control'}, choices=[
                ('standard', 'Standard Shipping'),
                ('express', 'Express Shipping'),
                ('overnight', 'Overnight Shipping'),
            ]),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(**args, **kwargs)

        self.fields['origin_country'].required = False
        self.fields['destination_country'].required = False
        self.fields['origin_state'].required = False
        self.fields['destination_state'].required = False

    def clean(self):
        cleaned_data = super().clean()
        region = cleaned_data.get('region')

        if region == 'within_malaysia':
            origin_country = cleaned_data.get('origin_country')
            destination_country = cleaned_data.get('destination_country')
            origin_state = cleaned_data.get('origin_state')
            destination_state = cleaned_data.get('destination_state')

            if origin_country != 'malaysia':
                self.add_error('origin_country', 'Must select Malaysia for this region')
            if destination_country != 'malaysia':
                self.add_error('destination_country', 'Must select Malaysia for this region')

            if not origin_state:
                self.add_error('origin_state', 'State is regquired for Malaysia')
            if not destination_state:
                self.add_error('destination_state','State is required for Malaysia')

        elif region == 'within_asia':
            origin_country = cleaned_data.get('origin_country')
            destination_country = cleaned_data.get('destination_country')

            asian_country_codes = [country[0] for country in self.ASIAN_COUNTRIES[1:]]

            if origin_country and origin_country not in asian_country_codes:
                self.add_error('origin_country', 'Must select an Asian country')
            if destination_country and destination_country not in asian_country_codes:
                self.add_error('destination_country', 'Must select an Asian country')

        elif region == 'international':
            origin_country = cleaned_data.get('origin_country')
            destination_country = cleaned_data.get('destination_country')

            international_country_codes = [country[0] for country in self.INTERNATIONAL_COUNTRIES[1:]]

            if origin_country and origin_country not in international_country_codes:
                self.add_error('origin_country', 'Must select an International country')

            if destination_country and destination_country not in international_country_codes:
                self.add_error('destination_country', 'Must select an International country')

        return cleaned_data