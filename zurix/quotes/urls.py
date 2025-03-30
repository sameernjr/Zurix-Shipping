from django.urls import path
from .views import ShippingQuoteView, QuoteDetailView

urlpatterns = [
    path('quote/', ShippingQuoteView.as_view(), name='quote-form'),
    path('quote/<str:quote_id>/', QuoteDetailView.as_view(), name='quote-detail'),  # Ensure this matches
]