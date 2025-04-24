from django.contrib import admin

from django.contrib import admin
from .models import ShippingOrder

class ShippingOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'region', 'shipping_method', 'total_price', 'status')
    list_filter = ('region', 'shipping_method', 'created_at')
    search_fields = ('user__username', 'destination_contact_name', 'pickup_contact_name')
    readonly_fields = ('created_at', 'base_price', 'express_fee', 'total_price')
    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'created_at', 'status')
        }),
        ('Package Information', {
            'fields': ('package_weight', 'region', 'shipping_method')
        }),
        ('Pricing', {
            'fields': ('base_price', 'express_fee', 'total_price')
        }),
        ('Origin Information', {
            'fields': ('origin_state_country', 'origin_address', 'pickup_contact_name', 'pickup_contact_number', 'pick_up_point')
        }),
        ('Destination Information', {
            'fields': ('destination_state_country', 'destination_address', 'destination_contact_name', 'destination_contact_number')
        }),
    )

    def status(self, obj):
        return "Completed"
    status.short_description = 'Status'

admin.site.register(ShippingOrder, ShippingOrderAdmin)
