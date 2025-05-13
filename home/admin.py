from django.contrib import admin
from .models import Contact

# Register your models here.
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject_display', 'created_at')
    list_filter = ('subject',)
    search_fields = ('name', 'email', 'message')
    
    def subject_display(self, obj):
        return obj.get_subject_display()
    subject_display.short_description = 'Subject'

admin.site.register(Contact, ContactAdmin)