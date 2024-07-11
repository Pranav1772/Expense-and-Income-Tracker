from django.urls import path
from spend_smart.views import incomes_views as views
urlpatterns = [
    path('income/',views.income,name='income'),  
    path('add-income/',views.add_income,name='add_income'),
    path('income-summary/',views.income_summary,name='income_summary'),
    path('delete-income/<int:id>/',views.delete_income,name='delete_income'),
    path('edit-income/<int:id>/',views.edit_income,name='edit_income'),    
    path('income-source-summary/',views.income_source_summary,name="income_source_summary"),
]