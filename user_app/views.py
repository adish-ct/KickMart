from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from user_app.models import *
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from .mail import *
import uuid
from django.http import HttpResponse

# Create your views here.


""" Kick mart main page for every one access """


def index(request):
    if 'email' in request.session:
        return redirect('admin_dashboard')
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
            exist_phone = CustomUser.objects.filter(phone=phone)

            # check if the email is already exist or not
            if exist_email:
                messages.error(request, "E-mail is already existing")
            elif exist_phone:
                messages.error(request, "Phone is already existing")
            else:
                if password == c_password:
                    # Custom user is customised created model inherited by AbstractUser.
                    # create_user is customised created function it save and return user.
                    user = CustomUser.objects.create_user(email, password=password, phone=phone, first_name=first_name)
                    user_id = user.id
                    # generate otp
                    otp = get_random_string(length=6, allowed_chars='1234567890')

                    # send mail with generated otp to the user's email from email host , check settings.py
                    subject = 'Verify your account'
                    message = f'Your OTP for account verification is {otp}'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [email, ]
                    send_mail(subject, message, email_from, recipient_list)

                    # save the otp in database,
                    user.otp = otp
                    user.save()
                    return redirect('otp_verification', user_id)
                else:
                    messages.error(request, "Password didn't match..")
                    return redirect('user_signup')
        else:
            return render(request, 'user/signup.html')


def otp_verification(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    context = {
        'user': user
    }
    if request.method == 'POST':
        otp = request.POST['otp']
        if len(otp) == 6:
            if otp == user.otp:
                user.is_verified = True
                user.otp = ''
                user.save()
                messages.success(request, "Account successfully verified, login now.")
                return redirect('user_login')
            else:
                messages.error(request, 'Invalid OTP, try again')
                return redirect('otp_verification', user.id)
        else:
            messages.error(request, 'Please enter a valid OTP....')
    else:
        return render(request, 'user/otp_verification.html', context)




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
                if user.is_verified:
                    login(request, user)
                    request.session['user'] = email
                    return redirect('index')
                else:
                    messages.error(request, "Your account is not verified")
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
