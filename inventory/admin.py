from django.contrib import admin
from .models import Category, Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'price', 'quantity_in_stock', 'category', 'organization')
    search_fields = ('name', 'sku')
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization')
    search_fields = ('name',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(organization=request.user.organization) if request.user.organization else qs.none()
