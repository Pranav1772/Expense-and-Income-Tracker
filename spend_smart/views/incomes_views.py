from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from spend_smart.models import *
from django.contrib import messages
from django.http import JsonResponse
import datetime
# Create your views here.

@login_required(login_url="spendsmart/authentication/login")
def income(request):
    return render(request,'spend_smart/income/income.html')

@login_required(login_url="spendsmart/authentication/login")
def income(request):
    incomes = Income.objects.filter(owner=request.user)        
    currency = UserPreferences.objects.get(user=request.user).currency
    context = {
        'incomes': incomes,
        'currency':currency
    }
    return render(request,'spend_smart/income/income.html',context=context)

@login_required(login_url="spendsmart/authentication/login")
def add_income(request):
    sources = Source.objects.all()
    context={'sources':sources}
    if request.method=='POST':
        amount = request.POST['amount']
        desc = request.POST['desc']
        source = request.POST.get('source')
        date = request.POST['date']
        if not (amount and desc and source and date):
            messages.error(request,'All fields are required')
            context.update({
                'amount': amount,
                'desc': desc,
                'selected_category': source,
                'date': date,
            })
            return render(request,'spend_smart/income/add_income.html',context=context)
        Income.objects.create(amount=amount,date=date,source=source,description=desc,owner=request.user)  
        messages.success(request,'Expense added successfully')
        return redirect('income')  
    return render(request,'spend_smart/income/add_income.html',context=context)

@login_required(login_url="spendsmart/authentication/login")
def income_summary(request):
    return render(request,'spend_smart/income/income_summary.html')


@login_required(login_url="spendsmart/authentication/login")
def delete_income(request,id):
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request,'Income deleted successfully')
    return redirect('income')

@login_required(login_url="spendsmart/authentication/login")
def edit_income(request,id):
    income = Income.objects.get(pk=id)
    source = Source.objects.all()
    formatted_date = income.date.strftime('%Y-%m-%d') 
    context = {
        'income': income,
        'sources':source,
        'date':formatted_date
    }
    print(request.POST)
    if request.method == 'POST':
        amount = request.POST['amount']
        desc = request.POST['desc']
        source = request.POST.get('source')
        date = request.POST['date']
        if not (amount and desc and source and date):
            messages.error(request,'All fields are required')
            return render(request,'spend_smart/income/edit_income.html',context=context)
        income.amount=amount
        income.date=date
        income.source=source
        income.description=desc 
        income.save()       
        messages.success(request,'Income updated successfully')
        return redirect('income')
    return render(request,'spend_smart/income/edit_income.html',context)

def income_source_summary(request):
    todays_date = datetime.date.today()
    six_months = todays_date - datetime.timedelta(days=30*6)
    incomes = Income.objects.filter(owner=request.user,date__gte=six_months,date__lte=todays_date)
    finalrep={}
    def get_source(incomes):
        return incomes.source
    source_list = list(set(map(get_source,incomes)))
    
    def get_incomes_source_amount(source):
        amount = 0
        filtered_by_source = incomes.filter(source=source)
        for item in filtered_by_source:
            amount += item.amount
        return amount
    
    for n in incomes:
        
        for y in source_list:
            
            finalrep[y] = get_incomes_source_amount(y)
    return JsonResponse({'income_source_data':finalrep},safe=False)
    