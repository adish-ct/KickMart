from django.shortcuts import render, redirect
from django.http import HttpResponse
from user_app.models import *
from cart.models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from order.models import *
import razorpay
import datetime
from decimal import Decimal
from django.http import JsonResponse

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
    checkout = Checkout.objects.get(user=my_user)
    if request.method == 'POST':
        total = checkout.grand_total
        my_order = Order()
        my_order.user = my_user
        my_order.address = checkout.address
        my_order.paid_amount = checkout.payable_amount
        my_order.total = checkout.total                     # product's total amount. 
        my_order.order_total = checkout.grand_total         # total amount including tax and other charges.
        my_order.discount = checkout.discount
        my_order.wallet_amount = checkout.wallet
        my_order.tax = checkout.tax
        my_order.ip = request.META.get('REMOTE_ADDR')
        my_order.is_ordered = True
        my_order.coupon = checkout.coupon

        my_order.save()

        # creating order with current date and order id
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%Y%m%d")
        order_id = current_date + str(my_order.id)          # creating order id
        my_order.order_id = order_id

        my_order.save()

        # creating object for payment.
        payment_type = request.POST.get('paymentMode')
        payment = Payments.objects.create(
            user = my_user,
            total_amount = checkout.grand_total,
            is_paid = False,
        )
        
        # creating order items
        cart_items = CartItem.objects.filter(customer=my_user)
        for item in cart_items:
            variant = ProductVariant.objects.get(id=item.product.id)
            order_item = OrderProduct.objects.create(
                customer = my_user,
                order_id = my_order,
                payment_id = payment.id,
                variant = variant,
                quandity = item.quantity,
                product_price = item.product.product_price,
                ordered = True,
            )
            variant.stock = variant.stock - item.quantity
            variant.save()
            item.delete()

        # payment method : cashon delivery
        if payment_type == 'cashonDelivery':
            payment.payment_method = 'Cashon Delivery'      # set current payment method
            payment_id = order_id + "COD"
            payment.payment_id = payment_id
            payment.save()

        # payment method : razor pay
        if payment_type == 'razorpayMethod':
            payment.payment_method = 'Razor Pay'      # set current payment method
            payment.payment_id = payment_id           # check this payment_id
            # this is the error occuring portion
            payment.is_paid = True
            payment.save()
            return JsonResponse({'status': "Transaction has been successfully completed"})
        
        # payment method : paypal pay
        else:
            pass
        
        my_order.payment = payment
        my_order.save()
                      
        return redirect('order_confirmed')
  
    return render(request, 'product/order_confirmed.html')


@login_required(login_url='user_login')
def proceed_to_pay(request):
    my_user = request.user
    payable_amount = 0
    checkout = Checkout.objects.get(user=my_user)
    payable_amount = payable_amount + checkout.payable_amount
    return JsonResponse({
        'payable_amount': payable_amount,
    })


@login_required(login_url='user_login')
def order_view(request):
    if 'user' in request.session:
        my_user = request.user
        orders = OrderProduct.objects.filter(customer=my_user).order_by('-order_id')
        
        # return HttpResponse(orders)
        context = {
            'orders': orders,
        }

    return render(request, 'user/orders.html', context)


@login_required(login_url='user_login')
def order_details(request, order_id):
    order = Order.objects.get()
    return render(request, 'user/order_details.html')



@login_required(login_url='user_login')
def order_cancel(requset, order_id):
    order_product = OrderProduct.objects.get(id=order_id)
    variant = order_product.variant
    order = order_product.order_id
    payment = order.payment

    if requset.method == 'POST':
        reason = requset.POST['cancelReason']
        if reason:
            order_product.return_reason = reason
        order.status = "Cancelled"
        payment.status = 'Order cancelled'
        variant.stock += order_product.quandity
        if payment.payment_method != "Cashon Delivery":
            #cash back logic should be handle here.
            pass
        order.save()
        order_product.save()
        variant.save()
        payment.save()
    return redirect('order_view' )


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='user_login')
def order_return(request, order_id):
    order_item = OrderProduct.objects.get(id=order_id)
    if request.method == 'POST':
        return_reason = request.POST.get('returnReason', None)
        if return_reason:
            order_item.return_reason = return_reason
        order_item.return_request = True
    order_item.save()

    return redirect('order_view')