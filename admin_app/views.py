import os

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
def admin_edit_product(request, id):
    product = Product.objects.get(id=id)
    product_category = product.category
    product_brand = product.brand
    brands = ProductBrand.objects.exclude(brand_name=product_brand)
    categories = Category.objects.exclude(category_name=product_category)
    context = {
        'product': product,
        'categories': categories,
        'brands': brands,
        'product_category': product_category,
        'product_brand': product_brand,
    }
    if request.method == 'POST':
        product_name = request.POST['product_name']
        category = request.POST['selectOption']
        brand = request.POST['selectBrandOption']
        original_price = request.POST['originalPrice']
        selling_price = request.POST['sellingPrice']

        # condition for checking is there any file is present in the request.
        if len(request.FILES) != 0:
            # we want to remove the image that already stored in the database.
            # first of all we have to check if there is any image exist on product object.
            if product.product_image:
                if len(product.product_image) > 0:
                    os.remove(product.product_image.path)
            product_image = request.FILES['image']
        product.product_name = product_name
        product.category = Category.objects.get(id=category)
        product.brand = ProductBrand.objects.get(id=brand)
        product.original_price = original_price
        product.selling_price = selling_price
        # condition for checking image is present or not.
        if product_image:
            product.product_image = product_image
        product.save()
        messages.success(request, "Product updated successfully")
        return redirect('admin_product')

    return render(request, 'admin/admin_edit_product.html', context)


@login_required(login_url='admin_login')
def admin_add_product(request):
    categories = Category.objects.all()
    print(categories)
    brands = ProductBrand.objects.all()
    context = {
        'categories': categories,
        'brands': brands,
    }
    if request.method == 'POST':
        product = Product()
        product_name = request.POST['name']
        category = request.POST['selectOption']
        brand = request.POST['selectBrand']
        original_price = request.POST['originalPrice']
        selling_price = request.POST['sellingPrice']
        product_description = request.POST['description']

        if len(request.FILES) != 0:
            product_image = request.FILES['image']
            product.product_image = product_image

        product.product_name = product_name
        product.category = Category.objects.get(id=category)
        product.brand = ProductBrand.objects.get(id=brand)
        product.original_price = original_price
        product.selling_price = selling_price
        product.product_description = product_description
        product.save()
        messages.success(request, "Product added successfully")
        return redirect('admin_product')

    return render(request, 'admin/admin_add_product.html', context)


@cache_control(no_store=True, no_cache=True)
@login_required(login_url='admin_login')
def admin_delete_product(request, id):
    prod = Product.objects.get(id=id)
    if prod.product_image:
        if len(prod.product_image) != 0:
            os.remove(prod.product_image.path)
    prod.delete()
    messages.success(request, "Product deleted successfully")
    return redirect('admin_product')


@login_required(login_url='admin_login')
def admin_product_variant(request, id):
    variant = ProductVariant.objects.filter(product=id)
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


def admin_user_manage(request, id):
    user = CustomUser.objects.get(id=id)
    if user.is_active:
        user.is_active = False
        user.save()
    else:
        user.is_active = True
        user.save()
    return redirect('admin_users')


def admin_category(request):
    return render(request, 'admin/admin_category.html')


# @cache_control(no_cache=True, no_store=True)
@login_required(login_url='admin_login')
def admin_logout(request):
    logout(request)
    request.session.flush()
    return redirect('admin_login')
