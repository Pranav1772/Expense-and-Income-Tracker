from django.urls import path
from spend_smart.views import userPreferences_views as views
urlpatterns = [
    path('preferences/',views.preferences,name='preferences'),
    path('profile/',views.profile,name='profile'),      
]
