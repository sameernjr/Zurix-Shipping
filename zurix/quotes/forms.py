from django import forms
from .models import ShippingQuote

class ShippingQuoteForm(forms.ModelForm):
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

    origin_country = forms.ChoiceField(choices=[], required=False, widget=forms.Select(attrs={'class':'form-control'})) 
    destination_country = forms.ChoiceField(choices=[], required=False, widget=forms.Select(attrs={'class':'form-control'}))

    origin_address = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'rows':3}), required=True)

    class Meta:
        model = ShippingQuote
        fields = ['region', 'origin_country', 'origin_address', 'destination_country', 'destination_address', 'weight', 'dimensions', 'item_description', 'shipping_method']

        widgets = {
            'region': forms.Select(attrs={'class':'form-control', 'id': 'id_region'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'dimensions': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Length x Width x Height'}),
            'item_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'shipping_method': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('standard', 'Standard Shipping'),
                ('express', 'Express Shipping'),
                ('overnight', 'Overnight Shipping'),
            ]),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['origin_country'].required = False
        self.fields['destination_country'].required = False
