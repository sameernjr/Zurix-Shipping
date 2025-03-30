import uuid
import logging
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http import HttpResponse

from zurix.quotes.forms import ShippingQuoteForm

logger = logging.getLogger(__name__)

class ShippingQuoteView(View):
    def get(self, request):
        form = ShippingQuoteForm()
        return render(request, 'quotes/quote_form.html', {'form': form})
    
    def post(self, request):
        form = ShippingQuoteForm(request.POST)
        
        # Extensive logging for debugging
        logger.info("Form submission received")
        logger.info(f"Form data: {request.POST}")
        
        if form.is_valid():
            logger.info("Form is valid")
            try:
                quote = form.save(commit=False)
                quote.quote_id = f"SQ-{uuid.uuid4().hex[:8].upper()}"

                # Log form cleaned data for verification
                logger.info(f"Cleaned data: {form.cleaned_data}")

                # Region-specific origin and destination
                if quote.region == 'within_malaysia':
                    quote.origin = f"{form.cleaned_data['origin_country']}, Malaysia"
                    quote.destination = f"{form.cleaned_data['destination_country']}, Malaysia"
                else:
                    quote.origin = form.cleaned_data['origin_country']
                    quote.destination = form.cleaned_data['destination_country']

                quote.origin_address = form.cleaned_data['origin_address']
                quote.destination_address = form.cleaned_data['destination_address']

                # Pricing calculation
                weight = float(quote.weight)
                base_rate = weight * 5

                if quote.shipping_method == 'standard':
                    quote.estimated_price = base_rate
                    quote.estimated_delivery_time = '3-5 business days'
                elif quote.shipping_method == 'express':
                    quote.estimated_price = base_rate + 10
                    quote.estimated_delivery_time = '1-2 business days'
                else:
                    quote.estimated_price = base_rate + 20
                    quote.estimated_delivery_time = '1 business day'

                quote.estimated_price = round(quote.estimated_price, 2)

                if request.user.is_authenticated:
                    quote.user = request.user

                # Save the quote
                quote.save()
                logger.info(f"Quote saved with ID: {quote.quote_id}")

                # Detailed redirect debugging
                try:
                    redirect_url = reverse('quote-detail', kwargs={'quote_id': quote.quote_id})
                    logger.info(f"Generated redirect URL: {redirect_url}")
                    return redirect(redirect_url)
                except Exception as redirect_error:
                    logger.error(f"Redirect error: {redirect_error}")
                    # Fallback response if redirect fails
                    return HttpResponse(f"Quote created. Quote ID: {quote.quote_id}", status=200)

            except Exception as e:
                logger.error(f"Unexpected error in quote creation: {str(e)}")
                form.add_error(None, f"An error occurred: {str(e)}")
        else:
            # Log form errors
            logger.error("Form is invalid")
            logger.error(f"Form errors: {form.errors}")
        
        # If something goes wrong, re-render the form
        return render(request, 'quotes/quote_form.html', {'form': form})