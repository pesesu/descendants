from django.urls import path
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('person-search/', views.person_search, name='person-search'),
    path('add-page/', views.add_page, name='add'),
    # path('delete/', views.delete),
    path('person-page/<str:pk>/', views.person_page, name='person-page'),
    path('person-update/<str:pk>/', views.update, name='person-update'),
    path('delete-search/', views.delete_search, name='delete-search' ),
    path('update-person/<str:pk>/', views.update_for_user, name='update-person'),
    path('delete-confirmation/<str:pk>', views.delete_confirmation, name='delete-confirmation'),
    path('users/', views.users, name='users'),
    path('after-signup/<str:pk>/', views.after_signup, name='after-signup')
]
