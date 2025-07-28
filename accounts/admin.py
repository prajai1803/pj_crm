from django.contrib import admin

from accounts.models import CustomUser,OTP
from organizations.models import Organization

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'website')
    search_fields = ('name', 'website')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'is_active', 'organization')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_active', 'organization')

admin.site.register(OTP, UserAdmin)