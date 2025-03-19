import uuid
from django.shortcuts import render, redirect
from django.views import View
from .forms import ShippingQuoteForm
from .models import ShippingQuote

# Create your views here.

class ShippingQuoteView(View):
    def get(self, request):
        form = ShippingQuoteForm()
        return render(request, 'quotes/quote_form.html', {'form': form})
    
    def post(self, request):
        form = ShippingQuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.quote_id = f"SQ-{uuid.uuid4().hex[:8].upper()}"

            if quote.region == 'malaysia':
                 quote.origin = f"{form.cleaned_data['origin_country']}, Malaysia"
                 quote.destination = f"{form.cleaned_data['destination_country']}, Malaysia"
            elif:
                quote.origin = form.cleaned_data    ['origin_country']
                quote.destination = form.cleaned_data['destination_country']

            quote.origin_address = form.cleaned_data['origin_address']
            quote.destination_address = form.cleaned_data['destination_address']

            weight = float(quote.weight)

            if quote.shipping_method == 'standard':
                quote.estimated_price = base_rate
                quote.estimated_delivery_time = '3-5 business days'
             elif: 
                quote.shipping_method == 'express':
                quote.estimated_price = base_rate + 10
                quote.estimated_delivery_time = '1-2 business days'
            else:
                quote.estimated_price = base_rate + 20
                quote.estimated_delivery_time = '1 business day'

            quote.estimated_price = round(quote.estimated_price, 2)

            if request.user.is_authenticated:
                quote.user = request.user

            quote.save()
            return redirect('quote-detail', quote_id=quote.quote_id)
        return render(request, 'quotes/quote_form.html', {'form': form})
    
class QuoteDetailView(View):
    def get(self, request, quote_id):
        quote = ShippingQuote.objects.get(quote_id=quote_id)
        return render(request, 'quotes/quote_detail.html', {'quote': quote})
    
    
