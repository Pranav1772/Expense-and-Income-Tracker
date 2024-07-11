from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from spend_smart.models import *
from django.contrib import messages
from django.http import JsonResponse
import datetime

# Create your views here.

@login_required(login_url="spendsmart/authentication/login")
def expense(request):
    expenses = Expense.objects.filter(owner=request.user)        
    currency = UserPreferences.objects.get(user=request.user).currency
    context = {
        'expenses': expenses,
        'currency':currency
    }
    return render(request,'spend_smart/expenses_tracker/epxenses.html',context=context)

@login_required(login_url="spendsmart/authentication/login")
def add_expense(request):
    categories = Category.objects.all()
    context={'categories':categories}
    if request.method=='POST':
        amount = request.POST['amount']
        desc = request.POST['desc']
        category = request.POST.get('category')
        date = request.POST['date']
        if not (amount and desc and category and date):
            messages.error(request,'All fields are required')
            context.update({
                'amount': amount,
                'desc': desc,
                'selected_category': category,
                'date': date,
            })
            return render(request,'spend_smart/expenses_tracker/add_epxenses.html',context=context)
        Expense.objects.create(amount=amount,date=date,category=category,description=desc,owner=request.user)  
        messages.success(request,'Expense added successfully')
        return redirect('expenses')  
    return render(request,'spend_smart/expenses_tracker/add_epxenses.html',context=context)

@login_required(login_url="spendsmart/authentication/login")
def expenses_summary(request):
    return render(request,'spend_smart/expenses_tracker/expense_summary.html')

@login_required(login_url="spendsmart/authentication/login")
def delete_expense(request,id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request,'Expense deleted successfully')
    return redirect('expenses')

@login_required(login_url="spendsmart/authentication/login")
def edit_expense(request,id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    formatted_date = expense.date.strftime('%Y-%m-%d') 
    context = {
        'expense': expense,
        'categories':categories,
        'date':formatted_date
    }
    if request.method == 'POST':
        amount = request.POST['amount']
        desc = request.POST['desc']
        category = request.POST.get('category')
        date = request.POST['date']
        if not (amount and desc and category and date):
            messages.error(request,'All fields are required')
            return render(request,'spend_smart/expenses_tracker/edit_expense.html',context=context)
        expense.amount=amount
        expense.date=date
        expense.category=category
        expense.description=desc 
        expense.save()       
        messages.success(request,'Expense updated successfully')
        return redirect('expenses')
    return render(request,'spend_smart/expenses_tracker/edit_expense.html',context)

def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months = todays_date - datetime.timedelta(days=30*6)
    expense = Expense.objects.filter(owner=request.user,date__gte=six_months,date__lte=todays_date)
    finalrep={}
    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category,expense)))
    
    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expense.filter(category=category)
        for item in filtered_by_category:
            amount += item.amount
        return amount
    for n in expense:
        
        for y in category_list:
            
            finalrep[y] = get_expense_category_amount(y)
    return JsonResponse({'expense_category_data':finalrep},safe=False)


    
    
    
    