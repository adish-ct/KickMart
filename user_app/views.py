import os
import requests
import uuid
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
from django.http import HttpResponse, JsonResponse
from urllib.parse import urlparse
from order.models import *
from django.core.mail import send_mail
from .forms import ImageForm
from datetime import datetime, timedelta

# Create your views here.


""" Kick mart main page for every one access """


def index(request):
    context = {}
    if 'email' in request.session:
        return redirect('admin_dashboard')
    try:
        categories = Category.objects.all().order_by('id')
        products = Product.objects.all()[:4]
        latest_product = Product.objects.all().order_by('created_date')[:4:-1]
        brands = ProductBrand.objects.all().order_by('id')
        try:
            main_banner = Banner.objects.filter(section='index', identifier='main')
        except:
            main_banner = None
        try:
            sub_banner_left = Banner.objects.filter(section='index', identifier='first').order_by('-id')[0]
        except:
            sub_banner_left = None
        try:
            sub_banner_right = Banner.objects.filter(section='index', identifier='second').order_by('-id')[0]
        except:
            sub_banner_right = None

        context = {
            'categories': categories,
            'products': products,
            'latest_poduct': latest_product,
            'brands': brands,
            'main_banner': main_banner,
            'sub_banner_left': sub_banner_left,
            'sub_banner_right': sub_banner_right,
        }
    except Exception as e:
        print(e)

    return render(request, 'product/index.html', context)


def user_signup(request):
    if 'email' in request.session:
        return redirect('admin_dashboard')
    if 'user' in request.session:
        return redirect('index')
    try:
        if request.method == 'POST':
            field_names = ['first_name', 'last_name', 'username', 'email', 'phone', 'password', 'c_password',
                           'referral_code']
            user_data = {field: request.POST.get(field, '') for field in field_names}

            exist_email = CustomUser.objects.filter(email=user_data['email'])
            exist_phone = CustomUser.objects.filter(phone=user_data['phone'])

            # check if the email is already exist or not
            if exist_email:
                messages.error(request, "E-mail is already taken.")
            elif exist_phone:
                messages.error(request, "Phone number is already taken.")
            else:
                if user_data['password'] == user_data['c_password']:
                    # Custom user is customised created model inherited by AbstractUser.
                    # create_user is customised created function it save and return user.
                    user = CustomUser.objects.create_user(user_data['email'], password=user_data['password'], phone=user_data['phone'],
                                                          first_name=user_data['first_name'])
                    # generate otp
                    otp = get_random_string(length=6, allowed_chars='1234567890')
                    code = generate_referral_code()

                    send_otp(user_data['email'], otp)
                    # send_otp(email, otp)
                    user.otp = otp
                    user.referral_code = code
                    try:
                        if user_data['referral_code']:
                            ref_user = CustomUser.objects.filter(referral_code=user_data['referral_code']).first()
                            if ref_user:
                                referred_user = CustomUser.objects.get(id=ref_user.id)
                                referred_user.wallet = 200
                                user.wallet = 50
                                user.referred_by = referred_user.email
                                referred_user.save()
                                messages.success(request, "Referral code verified")
                            else:
                                messages.error(request, "Invalid Referral code.")
                    except Exception as e:
                        print(e)
                    user.save()

                    return redirect('otp_verification', user.id)
                else:
                    messages.error(request, "Password didn't match.")

                    return redirect('user_signup')
            return redirect('user_signup')

        return render(request, 'user/signup.html')
    except Exception as e:
        print(e)
        return redirect('user_signup')


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
    try:
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
    except Exception as e:
        print(e)

    return render(request, 'user/otp_verification.html', context)


@cache_control(no_store=True, no_cache=True)
def regenerate_otp(request, id):
    if 'email' in request.session:
        return redirect('admin_dashboard')
    try:
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
        messages.success(request, "OTP sent to your mail")
    except Exception as e:
        print(e)
    return redirect('otp_verification', id)


@cache_control(no_cache=True, no_store=True)
def user_login(request):
    if 'email' in request.session:
        return redirect('admin_dashboard')
    if 'user' in request.session:
        return redirect('index')
    else:
        try:
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
                        if not user.is_verified:
                            messages.success(request, "Verify your account.")
                            return redirect('otp_verification', user.id)
                        messages.error(request, "invalid credentials.")
                else:
                    messages.error(request, "Invalid credentials.")
                    return redirect('user_login')
        except Exception as e:
            print(e)
        return render(request, 'user/login.html')


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='index')
def user_logout(request):
    if 'email' in request.session:
        return redirect('admin_dashboard')
    try:
        if 'user' in request.session:
            logout(request)
            request.session.flush()
            messages.success(request, 'Logout successfully.')
            return redirect('index')
    except Exception as e:
        print(e)
        return redirect('index')


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='index')
def user_profile(request):
    if 'email' in request.session:
        return redirect('admin_dashboard')
    context = {}
    if 'user' in request.session:
        user = request.user
    if user:
        try:
            order = Order.objects.filter(user=user)
            order_count = order.count()
            context = {
                'order': order,
                'order_count': order_count,
            }
        except Exception as e:
            print(e)
        try:
            if request.method == 'POST':
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                date_of_birth = request.POST.get('date_of_birth', None)
                if date_of_birth:
                    user.date_of_birth = date_of_birth

                phone = request.POST['phone']
                if len(phone) != 10:
                    messages.error(request, "must be 10 digits")
                    return redirect('user_profile')
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
        except Exception as e:
            messages.success(request, "Updated")

            print(e)

    return render(request, 'user/user_profile.html', context)


@login_required(login_url='index')
def address_book(request):
    if 'email' in request.session:
        return redirect('admin_dashboard')
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
    if 'email' in request.session:
        return redirect('admin_dashboard')
    try:
        if 'user' in request.session:
            user = request.user
        if request.method == 'POST':
            name = request.POST['first_name']
            if len(request.POST['phone']) == 10:
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
                messages.success(request, "Address created")
                return redirect('checkout')
            else:
                messages.success(request, "New address added.")
                return redirect('address_book')
    except Exception as e:
        print(e)
    return render(request, 'user/add_address.html')


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='index')
def forgot_password(request):
    if 'email' in request.session:
        return redirect('admin_dashboard')
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
    if 'email' in request.session:
        return redirect('admin_dashboard')
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
    if 'email' in request.session:
        return redirect('admin_dashboard')
    try:
        user = request.user
        address = UserAddress.objects.get(id=address_id)
        address.delete()
        messages.success(request, "Address deleted.")
    except Exception as e:
        print(e)
    return redirect('address_book')


@login_required(login_url='index')
def wallet_book(request):
    context = {}
    if 'email' in request.session:
        return redirect('admin_dashboard')
    if 'user' in request.session:
        user = request.user
        try:
            reports = WalletBook.objects.filter(customer=user.id)
            context = {
                'reports': reports,
            }
            return render(request, "user/wallet_book.html", context)
        except Exception as e:
            print(e)
            return redirect('user_profile')
    return redirect('index')


@cache_control(no_cache=True, no_store=True)
def subscribe(request):
    if 'email' in request.session:
        return redirect('admin_dashboard')
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


def test(request):
    form = ImageForm(request.POST or None, request.FILES or None)
    images = Image.objects.all()
    if form.is_valid():
        form.save()
        return JsonResponse({'message': 'works'})
    context = {
        'form': form,
        'image': images,
    }

    return render(request, 'main.html', context)
