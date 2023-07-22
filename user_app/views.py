from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from user_app.models import *
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required

# Create your views here.


""" Kick mart main page for every one access """


def index(request):
    return render(request, 'product/index.html')


""" User can create new account, user sign up function"""


def user_signup(request):
    # user is the key, created for normal users
    if 'user' in request.session:
        return redirect('index')
    else:
        if request.method == 'POST':
            first_name = request.POST['firstname']
            last_name = request.POST['lastname']
            username = request.POST['username']
            email = request.POST['email']
            phone = request.POST['phone']
            password = request.POST['password']
            c_password = request.POST['c_password']

            # exist_email will not null if the given email is already in the CustomerUser table.
            exist_email = CustomUser.objects.filter(email=email)

            # check if the email is already exist or not
            if exist_email:
                messages.error(request, "E-mail is already existing")
            else:
                if password == c_password:
                    # Custom user is customised created model inherited by AbstractUser.
                    # create_user is customised created function it save and return user.
                    user = CustomUser.objects.create_user(email, password=password, phone=phone, first_name=first_name)
                    return redirect('user_login')
                else:
                    messages.error(request, "Password didn't match..")
                    return redirect('user_signup')
        else:
            return render(request, 'user/signup.html')


@cache_control(no_cache=True, no_store=True)
def user_login(request):
    if 'user' in request.session:
        return redirect('index')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                request.session['user'] = email
                return redirect('index')
            else:
                messages.error(request, "Invalid credentials, Try again")
                return redirect('user_login')
        return render(request, 'user/login.html')


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='index')
def user_logout(request):
    logout(request)
    request.session.flush()
    return redirect('index')
