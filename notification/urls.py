from django.urls import path
from .views import notification

urlpatterns = [
    path('get', notification, name='login'),

]