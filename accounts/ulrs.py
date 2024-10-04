from django.urls import path
from .views import login, refresh_token,get_user_profile, update_user
urlpatterns = [
    path('login', login, name='login'),
    path('get-profile/<str:user_id>', get_user_profile, name='login'),
    path('refresh-token', refresh_token, name='refresh_token'),
    path('update-profile', update_user, name='update_profile')

]
