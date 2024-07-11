from django.shortcuts import redirect
from functools import wraps

def redirect_if_logged_in(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')  # Redirect to the home page or any other page you want
        return view_func(request, *args, **kwargs)
    return _wrapped_view