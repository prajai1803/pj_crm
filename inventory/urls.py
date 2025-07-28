from django.urls import path
from .views import create_category, update_category, delete_category, list_categories
from .views import create_product, update_product, delete_product, fetch_product


urlpatterns = [
    path('create-category', create_category, name='create_category'),
    path('update-category/<int:pk>', update_category, name='update_category'),
    path('delete-category/<int:pk>', delete_category, name='delete_category'),
    path('fetch-categories', list_categories, name='list_categories'),
    
    # Product URLs
    path('create-product', create_product, name='create_product'),
    path('update-product/<int:pk>', update_product, name='update_product'),
    path('delete-product/<int:pk>', delete_product, name='delete_product'),
    path('fetch-product', fetch_product, name='fetch_product'),

]