from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from web.models import Person, Married, PersonChildren, PersonParent
from .decorators import non_authenticated

# Create your views here.
def out_user(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    else:
        return redirect('login')

@non_authenticated
def login_view(request):
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(request, username, password)
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            try:
                person = Person.objects.get(user=request.user)
                if person.user.is_staff:
                    return redirect('users')
                else:
                    return redirect('person-page', pk=str(person.id))
            except: return redirect('home')
        else:
            message = 'Incorrect username or password. Register if you do not have account.'

    context = {'message': message}
    return render(request, 'accounts/login.html', context)


def registration(request):
    user_exists = False
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 =request.POST.get('password1')
        password2 = request.POST.get('password2')
        sex = request.POST.get('sex')
        try:
            User.objects.get(username_icontains=username)
        except:
            user_exists = True
            message = 'User already exists.'
        if not user_exists:
            if password1 == password2:
                if sex:
                    if sex == 'Male':
                        image = 'male.png'
                    else:
                        image = 'female.png'
                    user = User.objects.create_user(
                        username=username,
                        email=email,
                        password=password1,
                    )
                    user.save()
                    person = Person.objects.create(
                        user = user,
                        email=email,
                        image=image,
                        sex=sex
                    )
                    person.save()
                    married = Married.objects.create(person=person)
                    person.save()
                    person_children = PersonChildren.objects.create(person=person)
                    person_children.save()
                    person_parent = PersonParent.objects.create(person=person)
                    person_parent.save()
                    return redirect('after-signup', pk=str(person.id))
                else:
                    message = 'Select a gender.'
            else:
                message ='Password does not match.'
        else:
            message = 'A user with that username already exists.'

    context = {'message': message}
    return render(request, 'accounts/register.html', context)
