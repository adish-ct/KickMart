from django.shortcuts import render, redirect
from django.http import HttpResponse
from user_app.models import *
from cart.models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from order.models import *
import razorpay

# Create your views here.

@cache_control(no_cache=True, no_store=True)
@login_required(login_url='index')
def order(request):
    user = request.user
    checkout_items = Checkout.objects.get(user=user)
    cart_items = CartItem.objects.filter(customer=user)
    
    context = {
        'checkout_items': checkout_items,
        'cart_items': cart_items,
    }

    return render(request, 'product/order_confirm.html', context)


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='index')
def order_confirmed(request):
    my_user = request.user
    order = Checkout.objects.get(user=my_user)
    if request.method == 'POST':
        payment = request.POST['paymentMethod']
        if payment == 'cashonDelivery':
            return redirect('order_confirmed')
        # if payment == 'razorpayMethod':
        #     client = razorpay.Client(auth=("rzp_test_XvQRlmJZvpy445", "SZOVtWybr8PrIJLUnMmSaweY"))
    
    return render(request, 'product/order_confirmed.html')