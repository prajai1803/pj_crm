from django.urls import path
from .views import get_all_leads,create_lead,get_all_lead_cards
urlpatterns = [
    path('get-leads', get_all_leads, name='get leads'),
    path('get-leadcards', get_all_lead_cards, name='get leads'),
    path('create-lead', create_lead, name='create lead'),
]
