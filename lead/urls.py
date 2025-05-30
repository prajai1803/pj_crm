from django.urls import path
from .views import get_all_leads,create_lead,get_all_lead_cards,update_lead,delete_lead,lead_initial_data, get_lead
from .views import create_lead_reminder, delete_lead_reminder, fetch_reminder
urlpatterns = [
    path('get-leads', get_all_leads, name='get leads'),
    path('get-leadcards', get_all_lead_cards, name='get leads'),
    path('create-lead', create_lead, name='create lead'),
    path('get-lead/<int:lead_id>', get_lead, name='get leads'),
    path('update-lead/<int:lead_id>', update_lead, name='update lead'),
    path('delete-lead/<int:lead_id>', delete_lead, name='delete lead'),
    path('lead-initial-data', lead_initial_data, name='lead dropdown'),
    
    #Lead Reminder
     path('add-lead-reminder', create_lead_reminder, name='add lead reminder'),
     path('delete-lead-reminder/<int:lead_id>', create_lead_reminder, name='delete lead reminder'),
     path('fetch-lead-reminder', fetch_reminder, name='fetch reminder')
]
