from django.urls import path
from . import views

app_name = 'shipping'

urlpatterns = [
    path('create/', views.create_shipping, name='create_shipping'),
    path('preview/', views.shipping_preview, name='preview'),
    path('confirm/', views.confirm_shipping, name='confirm_shipping'),
    path('detail/<str:order_id>/', views.shipping_detail, name='shipping_detail'),
]
