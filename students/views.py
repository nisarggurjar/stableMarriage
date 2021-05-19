from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import *
from .models import Preferences as Choices
from datetime import datetime
from django.http import HttpResponse


def Home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'index.html')


def Login(request):
    if request.method == 'POST':
        un = request.POST["username"]
        pwd = request.POST['password']
        user = authenticate(username=un, password=pwd)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')


def Logout(request):
    logout(request)
    return redirect('login')


def Signup(request):
    err = False
    if request.method == 'POST':
        n = request.POST['name']
        un = request.POST['username']
        e = request.POST['email']
        ty = request.POST['type']
        pwd = request.POST['password']
        check = User.objects.filter(username=un)
        if check:
            err = True
        else:
            if ty == '1':
                User.objects.create_user(
                    username=un, email=e, password=pwd, first_name=n, is_staff=True)
                user = authenticate(username=un, password=pwd)
                login(request, user)
            else:
                User.objects.create_user(
                    username=un, email=e, password=pwd, first_name=n, is_staff=False)
                user = authenticate(username=un, password=pwd)
                login(request, user)
            return redirect('home')
    return render(request, 'signup.html', {'err': err})


def Rooms(request):
    return render(request, 'rooms.html')


def Mess(request):
    return render(request, 'mess.html')


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        desc = request.POST['desc']
        Contact.objects.create(name=name, email=email,
                               phone=phone, desc=desc, date=datetime.today())
        return redirect('home')
    return render(request, 'contact.html')


def Preferences(request):
    if request.method == 'POST':
        data = request.POST
        ch1 = User.objects.get(id=data['ch1'])
        ch2 = User.objects.get(id=data['ch2'])
        ch3 = User.objects.get(id=data['ch3'])
        ch4 = User.objects.get(id=data['ch4'])
        ch5 = User.objects.get(id=data['ch5'])
        Choices.objects.create(user=request.user, choice1=ch1,
                               choice2=ch2, choice3=ch3, choice4=ch4, choice5=ch5)
        return redirect('results')
    if request.user.is_staff:
        students = User.objects.filter(is_staff=False)
    else:
        students = User.objects.filter(is_staff=True)
    d = {'students': students}
    return render(request, 'preferences.html', d)


def Results(request):
    return render(request, 'results.html')
