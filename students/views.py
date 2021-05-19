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
    
    prefGrid = dict()
    pref = Choices.objects.all()
    toppers = [i.user.id for i in User.objects.filter(is_staff=True)]
    avgStudents = [
        i.user.id for i in User.objects.filter(is_staff=False)]

    topPref = dict()
    avgPref = dict()
    for i in pref:
        prefGrid.update({i.user.id: [
                        i.choice1.id, i.choice2.id, i.choice3.id, i.choice4.id, i.choice5.id]})
    for i in toppers:
        topPref.update({i: prefGrid[i]})
    for i in avgStudents:
        avgPref.update({i: prefGrid[i]})

    tentative_engagements = []

    free_toppers = []

    def init_free_topper():
        '''Initialize the arrays of women and men to represent 
            that they're all initially free and not engaged'''
        for top in topPref:
            free_toppers.append(top)

    def begin_matching(top):  # (man)
        '''Find the first free woman available to a man at
                any given time'''

        for avg in topPref[top]:

            # Boolean for whether woman is taken or not
            taken_match = [
                mate for mate in tentative_engagements if avg in mate]

            if (len(taken_match) == 0):
                # tentatively engage the man and woman
                tentative_engagements.append([top, avg])
                free_toppers.remove(top)

                break

            elif (len(taken_match) > 0):

                # Check ranking of the current dude and the ranking of the   'to-be' dude
                current_mate = avgPref[avg].index(taken_match[0][0])
                potential_mate = avgPref[avg].index(top)

                if (current_mate < potential_mate):
                    pass
                else:
                    # The new guy is engaged
                    free_toppers.remove(top)

                    # The old guy is now single
                    free_toppers.append(taken_match[0][0])

                    # Update the fiance of the woman (tentatively)
                    taken_match[0][0] = top
                    break

    def stable_matching():
        '''Matching algorithm until stable match terminates'''
        while (len(free_toppers) > 0):
            for top in free_toppers:
                begin_matching(top)

    def main():
        init_free_topper()
        print(free_toppers)
        stable_matching()
        return tentative_engagements

    RoomMates = main()
    print(RoomMates)
    Roomies = list()
    for i in RoomMates:
        p1 = User.objects.get(id=i[0])
        p2 = User.objects.get(id=i[1])
        Roomies.append([p1.username, p2.username])
    print(Roomies)
    return render(request, 'results.html')
