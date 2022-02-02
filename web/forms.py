from django import forms
from django.db import models
from django.db.models import fields
from django.db.models.enums import Choices
from django.db.models.fields import EmailField
from django.forms.models import ModelChoiceIterator
from django.forms.widgets import Select
from .models import Person, Married, PersonChildren, PersonParent

class PersonForm(forms.ModelForm):
    SEX = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    COMPLEXION = (
        ('Dark', 'Dark'),
        ('Fair', ('Fair'))
    )
    surname = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control font'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control font'}))
    middle_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control font'}), required=False)
    alias = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control font'}), required=False)
    image = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control font'}), required=False)
    sex = forms.Select(choices=SEX)
    complexion = forms.Select(choices=COMPLEXION)
    birth_date = forms.DateField(widget=forms.TextInput(attrs={'class':'form-control', 'type':'date'}), required=False)
    phone = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control font'}), required=False)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control font'}), required=False)
    short_history = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control font'}), required=False)
    is_spouse = forms.BooleanField(required=False)

    class Meta:
        model = Person
        fields = '__all__'


class MarriedForm(forms.ModelForm):
    per = Person.objects.filter(verified=True)
    person = forms.ModelChoiceField(queryset=per, required=False)
    spouse = forms.ModelMultipleChoiceField(queryset=per, required=False, widget=forms.SelectMultiple(attrs={'class':'form-control font'}))
    class Meta:
        model = Married
        exclude = ['person']


class PersonChildrenForm(forms.ModelForm):
    per = Person.objects.filter(verified=True)

    person = forms.ModelChoiceField(queryset=per, required=False)
    children = forms.ModelMultipleChoiceField(queryset=per, required=False, widget=forms.SelectMultiple(attrs={'class':'form-control font'}))
    class Meta:
        model = PersonChildren
        fields = ['children']

class PersonParentForm(forms.ModelForm):
    per = Person.objects.filter(verified=True)
    father = Person.objects.filter(sex='Male', verified=True)
    mother = Person.objects.filter(sex='Female', verified=True)

    person = forms.ModelChoiceField(queryset=per, required=False, widget=forms.Select(attrs={'class':'form-control font'}))
    father = forms.ModelChoiceField(queryset=father, required=False, widget=forms.Select(attrs={'class':'form-control font'}))
    mother = forms.ModelChoiceField(queryset=mother, required=False, widget=forms.Select(attrs={'class':'form-control font'}))
    class Meta:
        model = PersonParent
        fields = ['father', 'mother']

class UserCreationpersonForm(forms.Form):
    pers = Person.objects.filter(user=None)
    person = forms.ModelChoiceField(queryset=pers, widget=forms.Select(attrs={'class': 'form-control'}), required=True)


class PersonUpdate(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control font'}), required=False)
    short_history = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control font'}), required=False)
    class Meta:
        model = Person
        fields = ['image', 'short_history']
