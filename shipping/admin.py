from django.contrib import admin
from .models import Shipping

@admin.register(Shipping)
class ShippingAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'order_date', 'shipping_location', 'status', 'destination_location', 'shipping_type')
    list_filter = ('shipping_location', 'shipping_type', 'status', 'order_date')
    search_fields = ('order_id', 'user__username', 'destination_location')
    readonly_fields = ('order_id', 'order_date', 'user', 'weight', 'shipping_location', 
                       'pickup_location', 'pickup_contact', 'destination_location', 
                       'destination_contact', 'shipping_type')
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_id', 'order_date', 'user', 'status')
        }),
        ('Package Details', {
            'fields': ('weight', 'shipping_location', 'shipping_type')
        }),
        ('Pickup Information', {
            'fields': ('pickup_location', 'pickup_contact')
        }),
        ('Destination Information', {
            'fields': ('destination_location', 'destination_contact')
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        # If not staff or superuser, make all fields readonly
        if not request.user.is_staff and not request.user.is_superuser:
            return self.readonly_fields + ('status',)
        # Otherwise, make all fields except status readonly when editing
        if obj:
            return self.readonly_fields
        return ()
        
    def has_change_permission(self, request, obj=None):
        # Allow staff and superusers to change status
        if obj and (request.user.is_staff or request.user.is_superuser):
            return True
        return False
