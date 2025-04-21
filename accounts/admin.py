from django.contrib import admin

from accounts.models import CustomUser,OTP
from organizations.models import Organization

# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Organization, AuthorAdmin)
admin.site.register(CustomUser, AuthorAdmin)
admin.site.register(OTP, AuthorAdmin)