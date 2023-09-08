import os
import requests
import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from user_app.models import *
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from .mail import *
from .sendMail import *
from shop.models import *
from django.http import HttpResponse
from urllib.parse import urlparse
from order.models import *
from django.core.mail import send_mail

# Create your views here.


""" Kick mart main page for every one access """


def index(request):
    if 'email' in request.session:
        return redirect('admin_dashboard')

    categories = Category.objects.all().order_by('id')
    products = Product.objects.all()[:4]
    latest_product = Product.objects.all().order_by('created_date')[:4:-1]
    brands = ProductBrand.objects.all().order_by('id')
    main_banner = Banner.objects.filter(section='index', identifier='main')
    sub_banner_left = Banner.objects.filter(section='index', identifier='first').order_by('-id')
    sub_banner_right = Banner.objects.filter(section='index', identifier='second').order_by('-id')

    context = {
        'categories': categories,
        'products': products,
        'latest_poduct': latest_product,
        'brands': brands,
        'main_banner': main_banner,
        'sub_banner_left': sub_banner_left[0],
        'sub_banner_right': sub_banner_right[0],
    }

    return render(request, 'product/index.html', context)


""" User can create new account, user sign up function"""


# def user_signup(request, *args, **kwargs):
#     if 'email' in request.session:
#         return redirect('admin_dashboard')
#     if 'user' in request.session:
#         return redirect('index')
#     else:
#         try:
#             code = kwargs.get('referal_code')
#             try:
#                 profile = Profile.objects.get(referal_code=code)
#                 request.session['referal'] = profile.id
#                 print('id', profile.id)
#             except Exception as e:
#                 print(e)
#
#             if request.method == 'POST':
#                 first_name = request.POST['firstname']
#                 last_name = request.POST['lastname']
#                 username = request.POST['username']
#                 email = request.POST['email']
#                 phone = request.POST['phone']
#                 password = request.POST['password']
#                 c_password = request.POST['c_password']
#
#                 # exist_email will not null if the given email is already in the CustomerUser table.
#                 exist_email = CustomUser.objects.filter(email=email)
#                 exist_phone = CustomUser.objects.filter(phone=phone)
#
#                 # check if the email is already exist or not
#                 if exist_email:
#                     messages.error(request, "E-mail is already taken.")
#                 elif exist_phone:
#                     messages.error(request, "Phone number is already taken.")
#                 else:
#                     if password == c_password:
#                         # Custom user is customised created model inherited by AbstractUser.
#                         # create_user is customised created function it save and return user.
#                         user = CustomUser.objects.create_user(email, password=password, phone=phone, first_name=first_name)
#
#                         # generate otp
#                         otp = get_random_string(length=6, allowed_chars='1234567890')
#
#                         send_otp(email, otp)
#                         user.otp = otp
#                         user.save()
#
#                         return redirect('otp_verification', user.id)
#                     else:
#                         messages.error(request, "Password didn't match.")
#
#                         return redirect('user_signup')
#                 return redirect('user_signup')
#             else:
#
#                 return render(request, 'user/signup.html')
#         except Exception as e:
#             print(e)

def user_signup(request):
    if 'email' in request.session:
        return redirect('admin_dashboard')
    if 'user' in request.session:
        return redirect('index')
    else:
        try:
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
                    messages.error(request, "E-mail is already taken.")
                elif exist_phone:
                    messages.error(request, "Phone number is already taken.")
                else:
                    if password == c_password:
                        # Custom user is customised created model inherited by AbstractUser.
                        # create_user is customised created function it save and return user.
                        user = CustomUser.objects.create_user(email, password=password, phone=phone,
                                                              first_name=first_name)

                        # generate otp
                        otp = get_random_string(length=6, allowed_chars='1234567890')

                        send_otp(email, otp)
                        user.otp = otp
                        user.save()

                        return redirect('otp_verification', user.id)
                    else:
                        messages.error(request, "Password didn't match.")

                        return redirect('user_signup')
                return redirect('user_signup')
            else:

                return render(request, 'user/signup.html')
        except Exception as e:
            print(e)


@cache_control(no_store=True, no_cache=True)
def otp_verification(request, user_id):
    if 'email' in request.session:
        return redirect('admin_dashboard')
    if 'user' in request.session:
        return redirect('index')
    user = CustomUser.objects.get(id=user_id)
    context = {
        'user': user,
    }
    if request.method == 'POST':
        otp = request.POST['otp']

        if len(otp) == 6:
            if otp == user.otp:
                user.is_verified = True
                user.otp = ''
                user.save()
                messages.success(request, "Account verified.")
                return redirect('user_login')
            else:
                messages.error(request, 'Invalid OTP.')
                return redirect('otp_verification', user.id)
        else:
            messages.error(request, "Invalid OTP")
            return redirect('otp_verification', user.id)

    return render(request, 'user/otp_verification.html', context)


@cache_control(no_store=True, no_cache=True)
def regenerate_otp(request, id):
    user = CustomUser.objects.get(id=id)
    email = user.email
    user.otp = ''
    otp = get_random_string(length=6, allowed_chars='1234567890')

    subject = 'Verify your account'
    message = f'Your OTP for account verification is {otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list)

    user.otp = otp
    user.save()
    return redirect('otp_verification', id)


@cache_control(no_cache=True, no_store=True)
def user_login(request):
    if 'email' in request.session:
        return redirect('admin_dashboard')
    if 'user' in request.session:
        return redirect('index')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(request, email=email, password=password)
            if user:
                if user.is_verified and user.is_superuser == False:
                    login(request, user)
                    request.session['user'] = email
                    messages.success(request, "logged in successfully")

                    # if the request is come from cart page we have to redirect the user into checkout page thats handle here
                    url = request.META.get('HTTP-REFERER')
                    try:
                        query = requests.utils.urlparse(url).query

                        params = dict(x.split('=') for x in query.split('&'))

                        if 'next' in params:
                            nextPage = params['next']
                            return redirect(nextPage)
                    except:
                        return redirect('index')
                    # section end 
                else:
                    messages.error(request, "invalid credentials.")
            else:
                messages.error(request, "Invalid credentials.")
                return redirect('user_login')
        return render(request, 'user/login.html')


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='index')
def user_logout(request):
    if 'email' in request.session:
        return redirect('admin_dashboard')
    if 'user' in request.session:
        logout(request)
        request.session.flush()
        messages.success(request, 'Logout successfully.')
        return redirect('index')
    else:
        return redirect('index')


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='index')
def user_profile(request):
    if 'user' in request.session:
        user = request.user
    if user:
        order = Order.objects.filter(user=user)
        order_count = order.count()
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        date_of_birth = request.POST.get('date_of_birth', None)
        if date_of_birth:
            user.date_of_birth = date_of_birth

        phone = request.POST['phone']
        if request.FILES:
            if user.image:
                os.remove(user.image.path)
            image = request.FILES.get('pic', None)
            if image:
                user.image = image
        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        user.save()
        messages.success(request, "profile updated")
        return redirect('user_profile')

    context = {
        'order': order,
        'order_count': order_count,
    }

    return render(request, 'user/user_profile.html', context)


@login_required(login_url='index')
def address_book(request):
    if 'user' in request.session:
        user = request.user
    address = UserAddress.objects.filter(user=user)
    context = {
        'address': address,
    }
    return render(request, 'user/address_book.html', context)


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='index')
def add_address(request, id):
    if 'user' in request.session:
        user = request.user
    if request.method == 'POST':
        name = request.POST['first_name']
        phone = request.POST['phone']
        address = request.POST['address']
        town = request.POST['town']
        zip = request.POST['zip']
        location = request.POST['location']
        district = request.POST['district']
        if not name:
            name = user.first_name

        user_address = UserAddress(user=user, name=name, alternative_mobile=phone, address=address, town=town,
                                   zip_code=zip, nearby_location=location, district=district, )
        user_address.save()

        if id == 1:
            return redirect('checkout')
        else:
            messages.success(request, "Address added successfully.")
            return redirect('address_book')
    return render(request, 'user/add_address.html')


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='index')
def forgot_password(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email', None)
            my_user = CustomUser.objects.get(email=email)
            token = str(uuid.uuid4())
            try:
                profile_token = PasswordControl.objects.get(user=my_user.id)
            except:
                profile_token = PasswordControl.objects.create(user=my_user)
            profile_token.forgot_password_token = token
            profile_token.save()

            send_forgot_password_mail(email, token)

            messages.success(request, "Password reset link sent to the email.")
            return redirect('user_login')

    except Exception as e:
        messages.error(request, "User not found")
        print(e)
    return render(request, 'user/forgot_password.html')



@cache_control(no_cache=True, no_store=True)
@login_required(login_url='index')
def change_password(request, token):
    context = {}
    try:
        profile = PasswordControl.objects.get(forgot_password_token=token)

        if request.method == 'POST':
            try:
                password = request.POST['password']
                c_password = request.POST['cpassword']
                user_id = request.POST['user_id']

                token_id = PasswordControl.objects.filter(forgot_password_token=token).first()

                if password != c_password:
                    messages.error(request, "Password is not matching.")
                    return redirect('reset_password', token)

                user = token_id.user
                user.set_password(password)
                user.save()
                messages.success(request, "password changed")
            except Exception as e:
                print(e)
                messages.error(request, "Invalid credentials.")
            return redirect('user_login')

        context = {
            'user_id': profile.user.id,
            'token': token,
        }
    except Exception as e:
        messages.error(request, "something went wrong.")
        print(e)

    return render(request, 'user/reset_password.html', context)



@cache_control(no_cache=True, no_store=True)
@login_required(login_url='index')
def delete_address(request, address_id):
    user = request.user
    address = UserAddress.objects.get(id=address_id)
    address.delete()
    messages.success(request, "Address deleted successfully.")
    return redirect('address_book')


@cache_control(no_cache=True, no_store=True)
def subscribe(request):
    try:
        if request.method == 'GET':
            name = request.GET['name']
            email = request.GET['email']

            subject = f"Kick Mart subscription successfully"
            message = (f' Dear {name}, We are excited to have you as our new subscriber!\n you will receive exclusive '
                       f'discounts and offers on our products. \nYou will also be the first to know about our new '
                       f'arrivals and sales.To complete your subscription, please click on the link below:\nIf you '
                       f'have any questions or concerns, please feel free to contact us at ['
                       f'kickmart@gmail.com].\nThank you again for subscribing!\nBest regards, Kick Mart Team\nI hope '
                       f'this helps! Let me know if there’s anything else I can help you with.')
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail(subject, message, email_from, recipient_list)

            messages.success(request, "Subscribed you will get a mail from Kick mart")
            return redirect('index')

    except Exception as e:
        print(e)
        messages.error(request, "Something went wrong.")
    return redirect('index')
