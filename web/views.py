from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib.auth.models import User

from django.conf import settings
from django.conf.urls import url

import os

from accounts.decorators import admin_only, verified
from .models import Person, PersonParent, PersonChildren, Married
from .forms import PersonForm, MarriedForm, PersonChildrenForm, PersonParentForm, UserCreationpersonForm, PersonUpdate


def home(request):
    print(request.user)
    return render(request, 'web/home.html')

#@verified
def person_search(request):
    result = list()
    message = ''
    if request.method == 'GET':
        search = request.GET.get('search')
        if search is not '' and search is not None:
            surname_firstname = search.strip().split(' ')

            if len(surname_firstname) == 2:
                result1 = list(Person.objects.filter(Q(surname__icontains = surname_firstname[0]) & Q(first_name__icontains =surname_firstname[1]) & Q(verified=True)))
                result2 = list(Person.objects.filter(Q(surname__icontains = surname_firstname[1]) & Q(first_name__icontains =surname_firstname[0]) & Q(verified=True)))
                result = result1 + result2
            else:
                result = Person.objects.filter((Q(first_name__icontains = search) & Q(verified=True)) | (Q(surname__icontains = search) & Q(verified=True)))
            if len(result)== 0:
                message = 'No result found.'
            else: message = f'{len(result)} results found'

    context = {'result': result, 'message': message}
    print(context['result'])
    return render(request, 'web/person-search.html', context)


@login_required
@admin_only
@verified
def add_page(request):
    form = PersonForm()
    married = MarriedForm()
    person_children = PersonChildrenForm()
    person_parent = PersonParentForm()

    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES)
        married = MarriedForm(request.POST)
        person_children = PersonChildrenForm(request.POST)
        person_parent = PersonParentForm(request.POST)

        if form.is_valid() and married.is_valid() and person_children.is_valid() and person_parent.is_valid():
            image = form.cleaned_data['image']
            spouse = married.cleaned_data['spouse']
            children = person_children.cleaned_data['children']
            father = person_parent.cleaned_data['father']
            mother = person_parent.cleaned_data['mother']

            person = form.save()
            person.init = False
            person.verified = True
            person.save()

            if person.sex == 'Male' and image == None:
                person.image = 'male.png'
                person.save()
            elif person.sex == 'Female' and image == None:
                person.image = 'female.png'
                person.save()

            if spouse is not None:
                m = Married.objects.create(person=person)
                m.spouse.set(spouse)
                for spou in spouse:
                    Married.objects.get_or_create(person=spou)
                    pers_spouse = Married.objects.get(person=spou)
                    if person not in list(pers_spouse.spouse.all()):
                        pers_spouse.spouse.add(person)
                        pers_spouse.save()


            if children is not None:
                p = PersonChildren.objects.create(person=person)
                p.children.set(children)

            if father != None and mother != None:
                PersonParent.objects.create(person=person, father=father, mother=mother)
                PersonChildren.objects.get_or_create(person=father)
                f = PersonChildren.objects.get(person=father)
                f.children.add(person)
                f.save()
                PersonChildren.objects.get_or_create(person=mother)
                m = PersonChildren.objects.get(person=mother)
                m.children.add(person)
                m.save()

            elif father != None and mother == None:
                print('Inside')
                PersonParent.objects.create(person=person, father=father, mother=mother)
                PersonChildren.objects.get_or_create(person=father)
                f = PersonChildren.objects.get(person=father)
                f.children.add(person)
                f.save()

            elif father == None and mother != None:
                PersonChildren.objects.get_or_create(person=mother)
                m = PersonChildren.objects.get(person=mother)
                m.children.add(person)
                m.save()

            else: PersonParent.objects.create(person=person)

            form = PersonForm()
            married = MarriedForm()
            person_children = PersonChildrenForm()
            person_parent = PersonParentForm()

    context = {'form': form,
               'married': married,
               'person_children': person_children,
               'person_parent': person_parent
              }

    return render(request, 'web/add.html', context)

@login_required
@verified
def update(request, pk):
    person = Person.objects.get(id=pk)
    user = person.user
    form = PersonForm(instance=person)

    person_as_married = Married.objects.get(person=person)
    married = MarriedForm(instance=person_as_married)

    pers_children = PersonChildren.objects.get(person=person)
    person_children = PersonChildrenForm(instance=pers_children)

    per_parent = PersonParent.objects.get(person=person)
    per_father = per_parent.father
    per_mother = per_parent.mother
    person_parent = PersonParentForm(instance=per_parent)

    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES, instance=person)
        married = MarriedForm(request.POST, instance=person_as_married)
        person_children = PersonChildrenForm(request.POST, instance=pers_children)
        person_parent = PersonParentForm(request.POST, instance=per_parent)


        if form.is_valid() and married.is_valid() and person_children.is_valid() and person_parent.is_valid():
            spouse = married.cleaned_data['spouse']
            children = person_children.cleaned_data['children']
            father = person_parent.cleaned_data['father']
            mother = person_parent.cleaned_data['mother']

            print(form.cleaned_data['first_name'], form.cleaned_data['surname'])

            person = form.save()
            if user is not None:
                person.user = user
                person.save()

            if spouse is not None:
                person_old_spouse = []
                per_as_spouse = Married.objects.get(person=person)
                for s in per_as_spouse.spouse.all():
                    person_old_spouse.append(s)

                m = Married.objects.get(person=person)
                m.spouse.set(spouse)
                m.save()
                for s in spouse:
                    spou = Married.objects.get(person=s)
                    if person not in spou.spouse.all():
                        spou.spouse.add(person)
                        spou.save()

                person_new_spouse = []
                per_as_spou = Married.objects.get(person=person)
                for s in per_as_spou.spouse.all():
                    person_new_spouse.append(s)

                delete_per_from = set(person_old_spouse) - set(person_new_spouse)
                for s in delete_per_from:
                    sp = Married.objects.get(person=s)
                    sp.spouse.remove(person)
                    sp.save()

            if children is not None:
                p = PersonChildren.objects.get(person=person)
                p.children.set(children)

            if per_father != None or father != None:
                if per_father != father :
                    if per_father != None:
                        rem_child = PersonChildren.objects.get(person=per_father)
                        if person in rem_child.children.all():
                            rem_child.children.remove(person)
                            rem_child.save()

                    per_parent.father = father
                    per_parent.save()

                    try:
                        new_father = PersonChildren.objects.get(person=father)
                        if person not in new_father.children.all():
                            new_father.children.add(person)
                            new_father.save()
                    except:
                        pass

            if per_mother != None or mother != None:
                if per_mother != mother:
                    if per_mother != None:
                        rem_child = PersonChildren.objects.get(person=per_mother)
                        if person in rem_child.children.all():
                            rem_child.children.remove(person)
                            rem_child.save()

                    per_parent.mother = mother
                    per_parent.save()

                    try:
                        new_mother = PersonChildren.objects.get(person=mother)
                        if person not in new_mother.children.all():
                            new_mother.children.add(person)
                            new_mother.save()
                    except:
                        pass
            if not request.user.is_staff:
                return redirect('person-page', pk=f'{person.id}')
            else:
                return redirect('users')

    context = {'form': form,
            'married': married,
            'person_children': person_children,
            'person_parent': person_parent,
            'person': person,
            }

    return render(request, 'web/update.html', context)



# def delete(request):
#     children = Person.objects.all()
#     print(children.count())
#     for child in children:
#         child.delete()
#         print('deleted')
#     return HttpResponse('Deleting...')

@login_required
@admin_only
@verified
def delete_search(request):
    result = list()
    message = ''
    if request.method == 'GET':
        search = request.GET.get('search')
        if search is not '' and search is not None:
            surname_firstname = search.strip().split(' ')
            if len(surname_firstname) != 2 and len(surname_firstname) != 0:
                message = 'Please Enter person\'s First name and Surname'
            if len(surname_firstname) == 2:
                result1 = list(Person.objects.filter(Q(surname__icontains = surname_firstname[0]) & Q(first_name__icontains =surname_firstname[1]) & Q(verified=True)))
                result2 = list(Person.objects.filter(Q(surname__icontains = surname_firstname[1]) & Q(first_name__icontains =surname_firstname[0]) & Q(verified=True)))
                result = result1 + result2
                if len(result)== 0 and '' not in surname_firstname: message = f'No result found for {str(search).upper()}'
            else:
                message = 'You have to ENTER surname and firstname'
        else: pass
    context = {'result': result, 'message': message}
    print(context['result'])
    return render(request, 'web/delete_search.html', context)


@login_required
@admin_only
def delete_confirmation(request, pk):
    person = Person.objects.get(id=pk)
    if request.method == 'POST':
        print('In it')
        person.delete()
        return redirect('delete-search')
    else:
        print('No posts')
    context = {'person': person}
    return render(request, 'web\delete_confirmation.html', context)


@login_required
@verified
def person_page(request, pk):
    context = {}
    try:
        person = Person.objects.get(id=pk, verified=True)
    except:
        person = None

    if request.user.is_authenticated:
        children = PersonChildren.objects.get(person=person).children.all()
        spouse = Married.objects.get(person=person).spouse.all()
        parents = PersonParent.objects.get(person=person)
        context = {
            'person': person,
            'children': children,
            'spouse': spouse,
            'parents': parents
        }
    else:
        return HttpResponse('Sorry you are not allowed to view this page')

    return render(request, 'web/person.html', context)

@login_required
@admin_only
def users(request):
    form = UserCreationpersonForm()
    if request.method == 'POST':
        form = UserCreationpersonForm(request.POST)
        if form.is_valid():
            person = form.cleaned_data['person']
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            print(person.first_name, username, password1, password2)
            if password1 == password2:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1
                )
                person.user = user
                person.save()
                return HttpResponse('success..')
            else:
                raise ValueError('Password does not match.')
    context = {'form': form}
    return render(request, 'web/users.html',  context)


def user_exists(first_name, surname):
    persons = Person.objects.all()
    person_exists = False
    try:
        person = Person.objects.get(first_name=first_name, surname=surname)
        person_exists = True
    except:
        person_exists = False
    return person_exists



def after_signup(request, pk):
    person = Person.objects.get(id=pk)
    user = person.user
    form = PersonForm(instance=person)

    person_as_married = Married.objects.get(person=person)
    married = MarriedForm(instance=person_as_married)

    pers_children = PersonChildren.objects.get(person=person)
    person_children = PersonChildrenForm(instance=pers_children)

    per_parent = PersonParent.objects.get(person=person)
    per_father = per_parent.father
    per_mother = per_parent.mother
    person_parent = PersonParentForm(instance=per_parent)

    if request.method == 'POST':
        form = PersonForm(request.POST, request.FILES, instance=person)
        married = MarriedForm(request.POST, instance=person_as_married)
        person_children = PersonChildrenForm(request.POST, instance=pers_children)
        person_parent = PersonParentForm(request.POST, instance=per_parent)


        if form.is_valid() and married.is_valid() and person_children.is_valid() and person_parent.is_valid():
            image = form.cleaned_data['image']
            first_name = form.cleaned_data['first_name']
            surname = form.cleaned_data['surname']
            spouse = married.cleaned_data['spouse']
            children = person_children.cleaned_data['children']
            father = person_parent.cleaned_data['father']
            mother = person_parent.cleaned_data['mother']

            if user_exists(first_name=first_name, surname=surname):
                Person.objects.get(user=user).delete()
                User.objects.get(id=user.id).delete()
                return HttpResponse('Someone already exists with that surname and firstname. Pls contact admin.')
            else:
                person = form.save()
                if user is not None:
                    person.user = user
                    person.save()

                if person.sex == 'Male' and image == 'female.png':
                    person.image = 'male.png'
                    person.save()
                elif person.sex == 'Female' and image == 'male.png':
                    person.image = 'female.png'
                    person.save()


                if spouse is not None:
                    person_old_spouse = []
                    per_as_spouse = Married.objects.get(person=person)
                    for s in per_as_spouse.spouse.all():
                        person_old_spouse.append(s)

                    m = Married.objects.get(person=person)
                    m.spouse.set(spouse)
                    m.save()
                    for s in spouse:
                        spou = Married.objects.get(person=s)
                        if person not in spou.spouse.all():
                            spou.spouse.add(person)
                            spou.save()

                    person_new_spouse = []
                    per_as_spou = Married.objects.get(person=person)
                    for s in per_as_spou.spouse.all():
                        person_new_spouse.append(s)

                    delete_per_from = set(person_old_spouse) - set(person_new_spouse)
                    for s in delete_per_from:
                        sp = Married.objects.get(person=s)
                        sp.spouse.remove(person)
                        sp.save()

                if children is not None:
                    p = PersonChildren.objects.get(person=person)
                    p.children.set(children)

                if per_father != None or father != None:
                    if per_father != father :
                        if per_father != None:
                            rem_child = PersonChildren.objects.get(person=per_father)
                            if person in rem_child.children.all():
                                rem_child.children.remove(person)
                                rem_child.save()

                        per_parent.father = father
                        per_parent.save()

                        try:
                            new_father = PersonChildren.objects.get(person=father)
                            if person not in new_father.children.all():
                                new_father.children.add(person)
                                new_father.save()
                        except:
                            pass

                if per_mother != None or mother != None:
                    if per_mother != mother:
                        if per_mother != None:
                            rem_child = PersonChildren.objects.get(person=per_mother)
                            if person in rem_child.children.all():
                                rem_child.children.remove(person)
                                rem_child.save()

                        per_parent.mother = mother
                        per_parent.save()

                        try:
                            new_mother = PersonChildren.objects.get(person=mother)
                            if person not in new_mother.children.all():
                                new_mother.children.add(person)
                                new_mother.save()
                        except:
                            pass

                person.init = False
                person.save()
                return redirect('home')

    context = {'form': form,
            'married': married,
            'person_children': person_children,
            'person_parent': person_parent,
            'person': person,
            }
    return render(request, 'web/after_signup.html', context)


@login_required
@verified
def update_for_user(request, pk):
    person = Person.objects.get(id=pk)
    form = PersonUpdate(instance=person)
    if request.method == 'POST':
        form = PersonUpdate(request.POST, request.FILES, instance=person)
        if form.is_valid():
            image = form.cleaned_data['image']
            history = form.cleaned_data['short_history']
            person.image = image
            person.short_history = history
            person.save()
            return redirect('person-page', person.id)
        else:
            print('Form not valid.')
    context = {'form': form}
    return render(request, 'web/update4user.html', context)
