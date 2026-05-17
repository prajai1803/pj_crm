from rest_framework import serializers
from .models import Category
from .models import Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductFetchSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'category_name', 'sku', 'quantity_in_stock']
    
        def get_category_name(self, obj):
            return obj.category.name if obj.category else None
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
