from django.shortcuts import render,redirect
from django.contrib.staticfiles import finders
import json
from spend_smart.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

login_required(login_url="spendsmart/authentication/login")
def preferences(request):
    user_preference, created = UserPreferences.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        currency = request.POST.get('currency')
        if currency:
            user_preference.currency = currency
            user_preference.save()
            messages.success(request, 'Preference changed successfully')
            return redirect('preferences')

    currency_data = []
    file_path = finders.find('spend_smart/currencies.json')
    if file_path:
        with open(file_path) as json_file:
            data = json.load(json_file)
            for k, v in data.items():
                currency_data.append({'name': k, 'value': v})

    return render(request, 'spend_smart/user_preferences/preferences.html', {
        'currencies': currency_data,
        'user_preference': user_preference
    })

login_required(login_url="spendsmart/authentication/login")
def profile(request):
    user = User.objects.get(username=request.user)    
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        print(first_name and last_name and email)
        if first_name and last_name and email:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            messages.success(request,'Profile updated successfully')
            return redirect('profile')    
        messages.error(request,'All fields are required')
        return redirect('profile')
    return render(request, 'spend_smart/user_preferences/profile.html',context={'user':user})