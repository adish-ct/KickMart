from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

from user_app.models import *
from cart.models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from order.models import *
import razorpay
import datetime
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.cache import never_cache
# module for print pdf
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa


# Create your views here.

@cache_control(no_cache=True, no_store=True)
@login_required(login_url='index')
def order(request):
    user = request.user
    checkout_items = Checkout.objects.get(user=user)
    cart_items = CartItem.objects.filter(customer=user)
    if not cart_items:
        return redirect('index')

    context = {
        'checkout_items': checkout_items,
        'cart_items': cart_items,
    }
    return render(request, 'product/order_confirm.html', context)


@never_cache
@cache_control(no_cache=True, no_store=True)
@login_required(login_url='index')
def order_confirmed(request):
    my_user = request.user
    try:
        cart_items = CartItem.objects.filter(customer=my_user)
    except:
        return redirect('index')
    checkout = Checkout.objects.get(user=my_user)
    if request.method == 'POST':
        total = checkout.grand_total
        my_order = Order()
        my_order.user = my_user
        my_order.address = checkout.address
        my_order.paid_amount = checkout.payable_amount
        my_order.total = checkout.total  # product's total amount.
        my_order.order_total = checkout.grand_total  # total amount including tax and other charges.
        my_order.discount = checkout.discount
        my_order.wallet_amount = checkout.wallet
        my_order.tax = checkout.tax
        my_order.ip = request.META.get('REMOTE_ADDR')
        my_order.is_ordered = True
        my_order.coupon = checkout.coupon

        if float(checkout.grand_total) < float(checkout.wallet):
            my_user.wallet = float(checkout.wallet) - float(checkout.grand_total)
        else:
            my_user.wallet = 0

        my_user.save()
        my_order.save()

        # creating order with current date and order id
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%Y%m%d")
        order_id = current_date + str(my_order.id)  # creating order id
        my_order.order_id = order_id

        my_order.save()

        # creating object for payment.
        payment_type = request.POST.get('paymentMode')
        payment = Payments.objects.create(
            user=my_user,
            total_amount=checkout.grand_total,
            is_paid=False,
        )

        # creating order items
        cart_items = CartItem.objects.filter(customer=my_user)
        for item in cart_items:
            variant = ProductVariant.objects.get(id=item.product.id)
            order_item = OrderProduct.objects.create(
                customer=my_user,
                order_id=my_order,
                payment_id=payment.id,
                variant=variant,
                quandity=item.quantity,
                product_price=item.product.product_price,
                ordered=True,
            )
            variant.stock = variant.stock - item.quantity
            variant.save()
            item.delete()
        try:
            cart_items.delete()
        except:
            pass

        # payment method : cashon delivery
        if payment_type == 'cashonDelivery':
            payment.payment_method = 'Cashon Delivery'  # set current payment method
            payment_id = order_id + "COD"
            payment.payment_id = payment_id
            payment.save()
            my_order.payment = payment
            my_order.save()
            return render(request, 'product/order_confirmed.html')

        payment.payment_method = 'Razor Pay'  # set current payment method
        payment.payment_id = request.POST.get('payment_id')  # check this payment_id
        payment.is_paid = True
        payment.save()
        my_order.payment = payment
        my_order.save()

        return JsonResponse({
            'status': True,
        })

    return render(request, 'product/order_confirmed.html')


@login_required(login_url='user_login')
def proceed_to_pay(request):
    my_user = request.user
    payable_amount = 0
    checkout = Checkout.objects.get(user=my_user.id)
    payable_amount = int(payable_amount + checkout.grand_total)
    return JsonResponse({
        'payable_amount': payable_amount,
    })


@login_required(login_url='user_login')
def order_view(request):
    context = {}
    try:
        if 'user' in request.session:
            my_user = request.user
            orders = OrderProduct.objects.filter(customer=my_user).order_by('-order_id')

            # return HttpResponse(orders)
            context = {
                'orders': orders,
            }
    except Exception as e:
        print(e)
        return redirect('user_profile')

    return render(request, 'user/orders.html', context)


@login_required(login_url='user_login')
def order_cancel(requset, order_id):
    try:
        order_product = OrderProduct.objects.get(id=order_id)
        variant = ProductVariant.objects.get(id=order_product.variant.id)
        order = order_product.order_id
        payment = order.payment
        coupon = order.coupon
        user = order.user
        deduct_discount = order.discount

        if requset.method == 'POST':
            reason = requset.POST['cancelReason']
            if reason:
                order_product.return_reason = reason

            order.status = "Cancelled"
            payment.status = 'Order cancelled'
            order_product.item_cancel = True
            variant.stock += order_product.quandity

            if payment.payment_method != "Cashon Delivery":
                # cash back logic should be handle here.

                if order.total < 2500:  # delivery charge logic.
                    delivery_charge = 99
                else:
                    delivery_charge = 0
                amount = variant.product_price * order_product.quandity
                if coupon:
                    if order.total - amount >= coupon.minimum_order_amount:
                        deduct_discount = 0
                    else:
                        order.discount = 0

                refund_amount = (float(amount) + float(delivery_charge)) - float(
                    deduct_discount)  # calculating refund amount.
                user.wallet = float(user.wallet) + float(refund_amount)
                user.save()

            order.save()
            order_product.save()
            variant.save()
            payment.save()
        return redirect('order_view')
    except Exception as e:
        print(e)
    return redirect('order_view')


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='user_login')
def order_return(request, order_id):
    order_item = OrderProduct.objects.get(id=order_id)
    try:
        if request.method == 'POST':
            return_reason = request.POST.get('returnReason', None)
            if return_reason:
                order_item.return_reason = return_reason
            order_item.return_request = True
        order_item.save()
        return redirect('order_view')
    except Exception as e:
        print(e)

    return redirect('order_view')


def order_success(request):
    return render(request, 'product/success.html')


# print invoice in pdf

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


# Opens up page as PDF
class ViewPDF(View):
    def get(self, request, order_id, *args, **kwargs):
        user = request.user
        try:
            id = OrderProduct.objects.get(id=order_id).order_id.id
            order = Order.objects.get(id=id)
            order_products = OrderProduct.objects.filter(order_id=order)
            data = {
                "company": "Kick Mart",
                "address": "AC Market, 123 Street",
                "city": "Kannur",
                "state": "Kerala",
                "zipcode": "685256",

                "phone": "+91 860635952",
                "email": "kickmart@yahoo.com",
                "website": "kickmart.com",
                "user": order.address.name,
                "customer_address": order.address.address,
                "town": order.address.town,
                "customer_email": user.email,
                "nearby_location": order.address.nearby_location,
                "district": order.address.district,
                "zip_code": order.address.zip_code,
                "customer_phone": user.phone,
                "order_products": order_products,
                "order": order,

            }

        except Exception as e:
            print(e)
            return HttpResponse(False)
        pdf = render_to_pdf('user/order_invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


# Automaticly downloads to PDF file
class DownloadPDF(View):
    def get(self, request, order_id, *args, **kwargs):
        user = request.user
        try:
            id = OrderProduct.objects.get(id=order_id).order_id.id
            order = Order.objects.get(id=id)
            order_products = OrderProduct.objects.filter(order_id=order)
            data = {
                "company": "Kick Mart",
                "address": "AC Market, 123 Street",
                "city": "Kannur",
                "state": "Kerala",
                "zipcode": "685256",

                "phone": "+91 860635952",
                "email": "kickmart@yahoo.com",
                "website": "kickmart.com",
                "user": order.address.name,
                "customer_address": order.address.address,
                "town": order.address.town,
                "customer_email": user.email,
                "nearby_location": order.address.nearby_location,
                "district": order.address.district,
                "zip_code": order.address.zip_code,
                "customer_phone": user.phone,
                "order_products": order_products,
                "order": order,

            }
        except Exception as e:
            print(e)

        pdf = render_to_pdf('user/order_invoice.html', data)

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % ("12341231")
        content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
