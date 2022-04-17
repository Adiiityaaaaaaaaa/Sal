from email import message
import email
from http.client import HTTPResponse
from pyexpat.errors import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User, Group
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.

    
                    # save this new group for this example
def is_member(user,name):
    return user.groups.filter(name).exists()

def home(request):
    return render(request, "patientdoc/index.html")

def signup(request):
    group3, created = Group.objects.get_or_create(name = 'Doctor')
    group4, created = Group.objects.get_or_create(name = 'Patient')

    if request.method == "POST":
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]
        types = request.POST["users"]

        if pass2 != pass1:
            messages.error(request, "password didnt match")
            return redirect('home')
        else:
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            if types == "Doctor":  
                myuser.groups.add(group3)
            else:
                myuser.groups.add(group4)

            myuser.save()

            messages.success(request, "Success")

            return redirect('signin')



    return render(request, "patientdoc/signup.html")

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass']

        user = authenticate(username=username, password =pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            lname = user.last_name
            email = user.email

            if user.groups.filter(name = 'Doctor').exists():
                users = "Doctor"
            else:
                users = "Patient"
            
            return render(request, "patientdoc/index.html", {'fname':fname,'username':username, 'users':users, 'lname':lname, 'email':email})
            
        else:
            messages.error(request, "ERROR")
            return redirect('home')


    return render(request, "patientdoc/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out")
    return redirect('home')