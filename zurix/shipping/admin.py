from django.contrib import admin
from .models import ShippingOrder

# Register your models here.

@admin.register(ShippingOrder)
class ShippingOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'item_name', 'cost', 'created_at')
