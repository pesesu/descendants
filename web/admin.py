from django.contrib import admin
from django.contrib.admin.decorators import register
from django.contrib.admin.sites import site
from .models import Married, Person, Married, PersonChildren, PersonParent


# Register your models here.
admin.site.register(Person)
admin.site.register(Married)
admin.site.register(PersonChildren)
admin.site.register(PersonParent)

