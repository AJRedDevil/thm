
from django.http import Http404
from django.shortcuts import render, redirect

from users.models import UserProfile
from users.forms import VerifyPhoneForm

from users import handler as user_handler


def is_superuser(a_view):
    """
    Checks if a user is super user
    """
    def _wrapped_function(request, *args, **kwargs):
        if request.user.is_authenticated():
            phone = request.user.phone
            try:
                user = UserProfile.objects.get(phone=phone)
                if user:
                    if user.is_superuser:
                        return a_view(request, *args, **kwargs)
                    else:
                        return redirect('home')
                return redirect('home')
            except UserProfile.DoesNotExist:
                raise Http404
        return redirect('signin')
    return _wrapped_function


def is_verified(a_view):
    """
    Checks if the user's phone is verified
    """
    def _wrapped_function(request, *args, **kwargs):
        if request.user.is_authenticated():
            um = user_handler.UserManager()
            user = um.getUserDetails(request.user.id)
            if user.phone_status:
                return a_view(request, *args, **kwargs)
            else:
                return redirect('verifyPhone')
        return redirect('signin')
    return _wrapped_function
