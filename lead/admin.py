from django.contrib import admin

from lead.models import Lead

# Register your models here.

# Register your models here.
class AuthorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Lead, AuthorAdmin)