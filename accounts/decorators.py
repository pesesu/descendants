from django.shortcuts import redirect
from django.contrib.auth import logout
from django.http import HttpResponse
from web.models import Person

def admin_only(view_func):
    def wrapper(request, *args, **kwargs):
        allow = False
        if request.user.is_authenticated:
            if request.user.is_staff:
                allow = True
            else:
                allow = False
        else: return redirect('login')
        if allow:
            return view_func(request, *args, **kwargs)
        else: return HttpResponse('You are not allowed to view this page')
    return wrapper


def verified(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.is_staff:
                 return view_func(request, *args, **kwargs)
            else:
                print('in else statement')
                persons = Person.objects.filter(user=request.user)
                print(persons[0].verified)
                if persons.count() != 0 and persons[0].verified:
                    return view_func(request, *args, **kwargs)
                else:
                    print('In second else statement')
                    logout(request)
                    return HttpResponse('You are not yet verified.')
        else:
            return redirect('login')
    return wrapper


def non_authenticated(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You cannot view this page while you are logged in.')
    return wrapper
