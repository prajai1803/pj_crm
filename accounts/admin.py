from django.contrib import admin

from accounts.models import CustomUser,OTP

# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(CustomUser, AuthorAdmin)
admin.site.register(OTP, AuthorAdmin)