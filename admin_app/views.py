from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.shortcuts import render, redirect
from user_app.models import *
from shop.models import *


# Create your views here.


@cache_control(no_cache=True, no_store=True)
def admin_login(request):
    if 'email' in request.session:
        return redirect('admin_dashboard')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # authenticating user, checking user is valid or not
        admin = authenticate(email=email, password=password)
        if admin:
            # checking if the admin has is_superuser is true or not.
            if admin.is_superuser:
                login(request, admin)
                request.session['email'] = email
                return redirect('admin_dashboard')
            else:
                messages.error(request, "You can't access this session with user credentials.")
        else:
            messages.error(request, "Invalid credentials, try again with valid credentials.")
    return render(request, 'admin/admin_login.html')


@login_required(login_url='admin_login')
def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')


@login_required(login_url='admin_login')
def admin_product(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'admin/admin_product.html', context)


@login_required(login_url='admin_login')
def admin_product_variant(request, product_id):
    variant = ProductVariant.objects.filter(product=product_id)
    context = {
        'variants': variant,
    }
    return render(request, 'admin/admin_variant_product.html', context)


@login_required(login_url='admin_login')
def admin_users(request):
    users = CustomUser.objects.all()
    context = {
        'users': users,
    }
    return render(request, 'admin/admin_users.html', context)


# @cache_control(no_cache=True, no_store=True)
@login_required(login_url='admin_login')
def admin_logout(request):
    logout(request)
    request.session.flush()
    return redirect('admin_login')


def admin_category(request):
    return render(request, 'admin/admin_category.html')
