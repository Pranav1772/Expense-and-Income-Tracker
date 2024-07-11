from django.urls import path
from spend_smart.views import authentication_views as views

# urlpatterns = [
#     path('login',LoginView.as_view(),name='login'),
#     path('logout',logout,name='logout'),
#     path('register',RegistrationView.as_view(),name='register'),
#     path('validate-username',UsernameValidationView.as_view(),name='validate-username'),
#     path('validate-email',EmailValidationView.as_view(),name='validate-email'),   
#     path('validate-password',PasswordValidationView.as_view(),name='validate-password'),   
#     path('activate/<uid64>/<token>',VerificationView.as_view(),name='activate'),    
#     path('is-validate-username',IsUsernameValidationView.as_view(),name='is-validate-username'),
# ]

urlpatterns = [
    path('register/', views.register, name='register'),
    path('activate/<uid64>/<token>/', views.activate, name='activate'),
    path('validate-username/', views.validate_username, name='validate-username'),
    path('validate-email/', views.validate_email_view, name='validate-email'),
    path('validate-password/', views.validate_password_view, name='validate-password'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('is-username-valid/', views.is_username_valid, name='is-username-valid'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-user-password/<uid64>/<token>/', views.reset_password_check, name='reset-user-password'),
    path('validate-reset-email/', views.validate_email, name='validate-reset-email'),
]