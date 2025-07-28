from django.contrib import admin
from lead.models import (
    Lead, LeadSource, LeadStatus, LeadGender,
    LeadFollowUp, LeadHistory, CallLog
)

# Generic admin for all models except Lead
class DefaultAdmin(admin.ModelAdmin):
    pass

# Custom admin for Lead with list_display
@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('lead_name', 'contact_number', 'lead_status','organization')
    search_fields = ('lead_name', 'contact_number', 'email')
    list_filter = ('lead_source', 'lead_status', 'gender')
    ordering = ('-created_on',)  # Sort by latest first
    date_hierarchy = 'created_on'  # Date-based drilldown navigation
    list_per_page = 25  # Pagination control
    readonly_fields = ('created_on', 'updated_on')  # If you want to make them non-editable
    fieldsets = (
        (None, {
            'fields': ('lead_name', 'contact_number', 'email', 'gender')
        }),
        ('Source & Status', {
            'fields': ('lead_source', 'lead_status')
        }),
        ('Timestamps', {
            'fields': ('created_on', 'updated_on'),
            'classes': ('collapse',),
        }),
    )


@admin.register(CallLog)
class CallLogAdmin(admin.ModelAdmin):
    list_display = ('lead_id', 'call_type', 'call_duration', 'organization')
    list_filter = ['organization']
    ordering = ('-created_on',)
    list_per_page = 25
    

# Register remaining models with DefaultAdmin
admin.site.register(LeadSource, DefaultAdmin)
admin.site.register(LeadStatus, DefaultAdmin)
admin.site.register(LeadGender, DefaultAdmin)
admin.site.register(LeadFollowUp, DefaultAdmin)
admin.site.register(LeadHistory, DefaultAdmin)
