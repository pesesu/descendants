from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



class Person(models.Model):
    SEX = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )

    COMPLEXION = (
        ('Dark', 'Dark'),
        ('Fair', ('Fair'))
    )
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    surname = models.CharField(max_length=50, null=True)
    first_name = models.CharField(max_length=50, null=True)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    image = models.FileField(null=True, blank=True)
    alias = models.CharField(max_length=50, null=True, blank=True)
    sex = models.CharField(max_length=10, choices=SEX, null=True)
    complexion = models.CharField(max_length=10, choices=COMPLEXION, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    short_history = models.TextField(null= True, blank=True)
    is_spouse = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    init = models.BooleanField(default=True)
    
    class Meta:
        #verbose_name = 'Person'
        verbose_name_plural = 'People'
        ordering = ['surname', 'first_name']
        
    def __str__(self):
        if self.surname is not None and  self.first_name is not None:
            return f'{self.surname} {self.first_name}'
        else:
            return f'{self.user.email} {self.user.username} '




class Married(models.Model):
    person = models.ForeignKey(Person, null=True, blank=True, on_delete=models.CASCADE)
    spouse = models.ManyToManyField(Person, blank=True, related_name='spouse')

    class Meta:
        #verbose_name = 'Married'
        verbose_name_plural = 'Married'
        ordering = ['person']
    def __str__(self):
        return str(self.person)

    


class PersonChildren(models.Model):
    person = models.ForeignKey(Person, null=True, blank=True, on_delete=models.CASCADE)
    children = models.ManyToManyField(Person, blank=True, related_name='children')

    class Meta:
        #verbose_name = 'PersonChildren'
        verbose_name_plural = 'Persons Children'
        ordering = ['person']

    def __str__(self):
        return str(self.person)




class PersonParent(models.Model):
    person = models.ForeignKey(Person, blank=True,  on_delete=models.CASCADE)
    father = models.ForeignKey(Person, blank=True, null=True, on_delete=models.SET_NULL, related_name='father')
    mother = models.ForeignKey(Person, blank=True, null=True, on_delete=models.SET_NULL, related_name='mother')

    class Meta:
        #verbose_name = 'PersonParent'
        verbose_name_plural = 'Persons Parents'
        ordering = ['person']

    def __str__(self):
        return str(self.person)
