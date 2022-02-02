from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registration, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.out_user, name='logout')
]
