from django.urls import path
from spend_smart.views import expenses_views as views
urlpatterns = [    
    path('',views.expense,name='expenses'),    
    path('add-expenses/',views.add_expense,name='add_expense'),
    path('expenses-summary/',views.expenses_summary,name='expenses_summary'),
    path('delete-expense/<int:id>/',views.delete_expense,name='delete_expense'),
    path('edit-expense/<int:id>/',views.edit_expense,name='edit_expense'),
    path('expense-category-summary',views.expense_category_summary,name="expense_category_summary"),
]