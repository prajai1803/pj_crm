from django.contrib import admin

from lead.models import Lead,LeadSource,LeadStatus,LeadGender,LeadHistory

# Register your models here.

# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    pass

admin.site.register(LeadSource, AuthorAdmin)
admin.site.register(LeadStatus, AuthorAdmin)
admin.site.register(LeadGender, AuthorAdmin)
admin.site.register(Lead, AuthorAdmin)
admin.site.register(LeadHistory, AuthorAdmin)