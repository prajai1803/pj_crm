from django.contrib import admin

from lead.models import Lead,LeadSource,LeadStatus,LeadGender,LeadFollowUp
from lead.models import LeadHistory
from lead.models import CallLogs

class AuthorAdmin(admin.ModelAdmin):
    pass

admin.site.register(LeadSource, AuthorAdmin)
admin.site.register(LeadStatus, AuthorAdmin)
admin.site.register(LeadGender, AuthorAdmin)
admin.site.register(LeadFollowUp, AuthorAdmin)
admin.site.register(Lead, AuthorAdmin)
admin.site.register(LeadHistory, AuthorAdmin)
admin.site.register(CallLogs,AuthorAdmin)