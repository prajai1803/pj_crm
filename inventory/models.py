from django.db import models
from organizations.models import Organization

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='inventory_category', null=True)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True,null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_in_stock = models.IntegerField(default=0)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='inventory_product', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
