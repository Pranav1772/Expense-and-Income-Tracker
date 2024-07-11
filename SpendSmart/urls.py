from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.to_login,name='to_login'),
    path('spendsmart/', views.index,name='index'),
    path('spendsmart/dashboard/', views.dashboard,name='dashboard'),
    path('spendsmart/authentication/', include('spend_smart.urls.authentication_urls')),
    path('spendsmart/expenses/', include('spend_smart.urls.expenses_urls')),
    path('spendsmart/incomes/', include('spend_smart.urls.incomes_urls')),
    path('spendsmart/user_preferences/', include('spend_smart.urls.userPreferences_urls')),
]