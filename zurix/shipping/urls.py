from django.urls import path
from . import views

urlpatterns = [
    path('', views.shipping_form, name='shipping_form'),
    path('receipt/<int:order_id>/', views.generate_receipt, name='generate_receipt'),
    path('history/', views.user_history, name='user_history'),
    path('admin/dashboard/', views.user_history, name='admin_dashboard'),
]
