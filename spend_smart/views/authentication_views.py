from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes,force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from spend_smart.utils import token_generator
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
token_generator2 = PasswordResetTokenGenerator()


from django.contrib.auth import views as auth_views
from spend_smart.decorators import redirect_if_logged_in
# Create your views here.

# class RegistrationView(View):
#     def get(self, request):
#         return render(request, 'authentication/register.html')
    
#     def post(self, request):
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         user = User.objects.create_user(username=username,email=email)
#         user.set_password(password)
#         user.is_active = False
#         user.save()
        
#         uid64 = urlsafe_base64_encode(force_bytes(user.pk))
        
#         domain = get_current_site(request).domain
#         link=reverse('activate',kwargs={'uid64':uid64,'token':token_generator.make_token(user)})
        
#         activate_link = 'http://'+domain+link
        
#         send_mail(
#             "Activate your account",
#             "Hi "+user.username+' Please use following link to verify your account\n'+activate_link,
#             "pranavsawant862@gmail.com",
#             [email],
#             fail_silently=False,
#         )
        
#         messages.success(request,'Account successfully created')
#         return render(request, 'authentication/verify-email.html',context={'email':email})

# class VerificationView(View):
#     def get(self,request,uid64,token):
#         try:
#             id=force_str(urlsafe_base64_decode(uid64))    
#             user=User.objects.get(pk=id)
#             if not token_generator.check_token(user,token):
#                 messages.success(request,'User already active')
#                 return redirect('login')
#             if user.is_active:
#                 return redirect('login')
#             user.is_active=True
#             user.save()
#             messages.success(request,'Account activated successfully')
#             return redirect('login')
#         except Exception as e:
#             print(e)
#             messages.success(request,'Account activation failed')
#             return redirect('login')
   
# class UsernameValidationView(View):
#     def post(self, request):
#         data  = json.loads(request.body)
#         username = data['username']
#         if not str(username).isalnum():
#             return JsonResponse({'username_error':'Username should only contain alphanumeric characters'},status=400)
#         if User.objects.filter(username=username).exists():
#             return JsonResponse({'username_error':'It already exists please choose another one'},status=409)
#         return JsonResponse({"username_valid":True})
    
# class EmailValidationView(View):
#     def post(self, request):
#         data  = json.loads(request.body)
#         email = data['email']
#         if not validate_email(email):
#             return JsonResponse({'email_error':'Email is invalid'},status=400)
#         if  User.objects.filter(email=email).exists():
#             return JsonResponse({'email_error':'It already exists please choose another one'},status=409)
#         return JsonResponse({"email_valid":True})
    
# class PasswordValidationView(View):
#     def post(self, request):
#         data  = json.loads(request.body)
#         password = data['password']
#         try:
#             validate_password(password)
#             return JsonResponse({"password_valid":True})
#         except ValidationError as e:
#             return JsonResponse({'password_error':e.messages[0]},status=400)        
    
# # Login Page
    
# class LoginView(View):
#     def get(self, request):
#         return render(request, 'authentication/login.html')
    
#     def post(self,request):
#         username = request.POST['username']
#         password = request.POST['password']        
#         try:
#             user = User.objects.get(username=username)
#             if user.is_active:
#                 user = auth.authenticate(username=username, password=password)
#                 if user is not None:
#                     auth.login(request, user)
#                     messages.success(request, 'Welcome, ' + user.username + '. You are now logged in.')
#                     return render(request, 'expenses_tracker/dashboard.html')
#                 else:
#                     messages.error(request, 'Invalid credentials, try again.')
#                     return render(request, 'authentication/login.html')
#             else:
#                 messages.error(request, 'Account is not active. Please check your email.')
#                 return render(request, 'authentication/login.html')
#         except User.DoesNotExist:
#             messages.error(request, 'Username does not exist. Please check and try again.')
#             return render(request, 'authentication/login.html')

# class IsUsernameValidationView(View):
#     def post(self, request):
#         data  = json.loads(request.body)
#         username = data['username']
#         if not str(username).isalnum():
#             return JsonResponse({'username_error':'Username should only contain alphanumeric characters'},status=400)
#         if not User.objects.filter(username=username).exists():
#             return JsonResponse({'username_error':'Username not found. Please verify and try again.'},status=409)
#         return JsonResponse({"username_valid":True})

# def logout(request):
#     auth.logout(request)
#     messages.error(request, 'Logged out successfully')
#     return redirect('login')








@redirect_if_logged_in
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.is_active = False
        user.save()
        
        uid64 = urlsafe_base64_encode(force_bytes(user.pk))
        
        domain = get_current_site(request).domain
        link = reverse('activate', kwargs={'uid64': uid64, 'token': token_generator.make_token(user)})
        
        activate_link = 'http://' + domain + link
        
        send_mail(
            "Activate your account",
            "Hi " + user.username + ', Please use the following link to verify your account\n' + activate_link,
            "pranavsawant862@gmail.com",
            [email],
            fail_silently=False,
        )
        
        messages.success(request, 'Account successfully created')
        return render(request, 'spend_smart/authentication/verify-email.html', context={'email': email})
    return render(request, 'spend_smart/authentication/register.html')

def activate(request, uid64, token):
    try:
        id = force_str(urlsafe_base64_decode(uid64))    
        user = User.objects.get(pk=id)
        if not token_generator.check_token(user, token):
            messages.success(request, 'User already active')
            return redirect('login')
        if user.is_active:
            return redirect('login')
        user.is_active = True
        user.save()
        messages.success(request, 'Account activated successfully')
        return redirect('login')
    except Exception as e:
        print(e)
        messages.error(request, 'Account activation failed')
        return redirect('login')

def validate_username(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'It already exists, please choose another one'}, status=409)
        return JsonResponse({"username_valid": True})
    
def validate_email_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'It already exists, please choose another one'}, status=409)
        return JsonResponse({"email_valid": True})

def validate_password_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        password = data['password']
        try:
            validate_password(password)
            return JsonResponse({"password_valid": True})
        except ValidationError as e:
            return JsonResponse({'password_error': e.messages[0]}, status=400)
        
@redirect_if_logged_in
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']        
        try:
            user = User.objects.get(username=username)
            if user.is_active:
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' + user.username + '. You are now logged in.')
                    return redirect('dashboard')
                    return render(request, 'spend_smart/expenses_tracker/dashboard.html')
                else:
                    messages.error(request, 'Invalid credentials, try again.')
                    return render(request, 'spend_smart/authentication/login.html')
            else:
                messages.error(request, 'Account is not active. Please check your email.')
                return render(request, 'spend_smart/authentication/login.html')
        except User.DoesNotExist:
            messages.error(request, 'Username does not exist. Please check and try again.')
            return render(request, 'spend_smart/authentication/login.html')
    return render(request, 'spend_smart/authentication/login.html')

def is_username_valid(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should only contain alphanumeric characters'}, status=400)
        if not User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Username not found. Please verify and try again.'}, status=409)
        return JsonResponse({"username_valid": True})
    
def logout_view(request):
    auth.logout(request)
    messages.success(request, 'Log out successfully')
    return redirect('login')

def reset_password(request):
    if request.method=='POST':
        password = request.POST['password']
        confirmpassword = request.POST['confirm-password']
        id = request.POST['userid']
        if password != confirmpassword:
            messages.error(request, 'Passwords dont match')
            return render(request, 'spend_smart/authentication/reset-password.html',context={'password':password})
        user = User.objects.get(pk=id)
        user.set_password(password)
        user.save()
        messages.success(request, 'Password changed successfully')
        return redirect('login')
    return render(request, 'spend_smart/authentication/reset-password.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)  
            uid64 = urlsafe_base64_encode(force_bytes(user.pk))        
            domain = get_current_site(request).domain
            link = reverse('reset-user-password', kwargs={'uid64': uid64, 'token': token_generator2.make_token(user)})        
            activate_link = 'http://' + domain + link        
            send_mail(
                "Password Reset Request for Your spend smart Account",
                "Dear " + user.username + " please click the link below to reset your password: "+ activate_link +" If you did not request this, please ignore this email. Best regards.",            
                "pranavsawant862@gmail.com",
                [user.email],
                fail_silently=False,
            )
            messages.success(request, 'We have sent you emil with reset password link ')
            return redirect('forgot_password')
        except User.DoesNotExist:                            
            messages.error(request, 'This email does not exists')
            return render(request, 'spend_smart/authentication/forgot-password.html', context={'email': email})
    return render(request, 'spend_smart/authentication/forgot-password.html')


def reset_password_check(request, uid64, token):
    try:
        id = force_str(urlsafe_base64_decode(uid64))    
        user = User.objects.get(pk=id)
        if not token_generator2.check_token(user, token):
            messages.success(request, 'Invlid Link')
            return redirect('forgot_password')
        messages.success(request, 'Link verification successfull')
        return render(request, 'spend_smart/authentication/reset-password.html',context={'id':user.pk})
    except Exception as e:
        messages.error(request, 'Link verfication failed')
        return redirect('login')
    
def validate_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)        
        return JsonResponse({"email_valid": True})