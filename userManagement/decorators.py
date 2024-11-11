from django.http import HttpResponse
from django.shortcuts import redirect
from functools import wraps


def unauthenticated_user(view_func):
    @wraps(view_func)
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            # Check the user's role and redirect accordingly
            if request.user.is_mopd:
                return redirect('mopd_url')
            elif request.user.is_admin:
                return redirect('/admin')
            elif request.user.is_sector:
                return redirect('ministry')
            elif request.user.is_pm:
                return redirect('')
            else:
                # Default redirect for authenticated users
                return redirect('login_url')

        # If the user is not authenticated, allow them to access the original view
        return view_func(request, *args, **kwargs)

    return wrapper_func


def sector_user_required(view_func):
    @wraps(view_func)
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_sector:
            return view_func(request, *args, **kwargs)

        elif request.user.is_mopd:
            return redirect('mopd_url')
        else:
            return HttpResponse('You are not authorized to access this content.')
    return wrapper_func


def mopd_user_required(view_func):
    @wraps(view_func)
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_mopd:
            return view_func(request, *args, **kwargs)
        elif request.user.is_sector:
            return redirect('ministry')
        else:
            return HttpResponse('You are not authorized to access this content.')
    return wrapper_func


def pmo_user_required(view_func):
    @wraps(view_func)
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_pm:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authorized to access this content.')
    return wrapper_func


def admin_user_required(view_func):
    @wraps(view_func)
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_admin:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authorized to access this content.')
    return wrapper_func




def is_pm_required(view_func):
    @wraps(view_func)
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_pm:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You are not authorized to access this content.')
    return wrapper_func
