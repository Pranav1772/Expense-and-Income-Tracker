from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from spend_smart.models import *
import datetime
from django.db.models import Sum

def to_login(request):
    return redirect('login')

def index(request):        
    return render(request, 'spend_smart/index.html')

@login_required(login_url="spendsmart/authentication/login")
def dashboard(request):
    # Get the current date
    today = datetime.date.today()

    # Calculate the first day of the current month
    first_day_of_month = today.replace(day=1)

    # Calculate the last day of the current month
    next_month = first_day_of_month.replace(day=28) + datetime.timedelta(days=4)
    last_day_of_month = next_month - datetime.timedelta(days=next_month.day)


    total_expenses = Expense.objects.filter(
    date__gte=first_day_of_month,
    date__lte=last_day_of_month,
    owner=request.user
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    expenses_entries = Expense.objects.filter(
    date__gte=first_day_of_month,
    date__lte=last_day_of_month,
    owner=request.user
    ).count()

    # Filter and aggregate income for the current month
    total_income = Income.objects.filter(
        date__gte=first_day_of_month,
        date__lte=last_day_of_month,
        owner=request.user
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Filter and aggregate income for the current month
    incomes_entries = Income.objects.filter(
        date__gte=first_day_of_month,
        date__lte=last_day_of_month,
        owner=request.user
    ).count()
    currency = UserPreferences.objects.get(user=request.user).currency
    
    expenses_by_category = Expense.objects.filter(
    date__gte=first_day_of_month,
    date__lte=last_day_of_month,
    owner=request.user
    ).values('category').annotate(total_amount=Sum('amount'))

    income_by_source = Income.objects.filter(
        date__gte=first_day_of_month,
        date__lte=last_day_of_month,
        owner=request.user
    ).values('source').annotate(total_amount=Sum('amount'))

    
    context = {'expense':expenses_entries,'incomes':incomes_entries,'currency':currency,'total_expenses': total_expenses,
               'total_income': total_income, 'expenses_by_category': expenses_by_category, 'income_by_source': income_by_source,}     
    return render(request, 'spend_smart/dashboard.html',context=context)