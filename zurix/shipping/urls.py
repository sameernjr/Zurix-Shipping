from django.urls import path
from shipping.views import shipping_request, order_success, order_history

urlpatterns = [
    path('shipping/', shipping_request, name='shipping_request'),
    path('order/success/<int:order_id>/', order_success, name='order_success'),
    path('orders/', order_history, name='order_history'),
    # ... other URLs ...
]