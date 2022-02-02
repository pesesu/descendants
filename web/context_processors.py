from .models import Person 
from django.contrib.auth.models import User
from django.urls import reverse

def verified(request):
    verified_users = Person.objects.filter(verified=True) 
    return dict(verified_users=verified_users)

def unverified(request):
    unverified_users = Person.objects.filter(verified=False)
    return dict(unverified_users=unverified_users)

def render_user(request):
    user = 'No user'
    try:
        user = User.objects.get(id=request.user.id)
    except:
        pass   
    return dict(user=user)

def user_url(request):
    url = None
    try:
        person = Person.objects.get(user=request.user)
        url = reverse('person-page', args=[person.id])
    except:
        pass
    return dict(url=url)
