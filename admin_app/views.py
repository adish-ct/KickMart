from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from user_app.models import *
from shop.models import *


# Create your views here.
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


def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')


def admin_product(request):

    return render(request, 'admin/admin_product.html')
