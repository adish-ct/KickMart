from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from user_app.models import *
from cart.models import *
from shop.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from order.models import *
from django.http import JsonResponse
from django.utils import timezone


# Create your views here.


@cache_control(no_cache=True)
def cart(request, quantity=0, total=0, cart_items=None, tax=0, grand_total=0, coupon=None):
    if 'email' in request.session:
        return redirect('admin_dashboard')
    coupons = Coupons.objects.filter(valid_to__gte=timezone.now()).order_by('id')
    delivery_charge = 99
    total = 0
    quantity = 0
    discount = 0

    if 'user' in request.session:
        my_user = request.user
        checkout_user = request.user.id
        try:  # new change 10-08-23
            if Checkout.objects.get(user=checkout_user):
                checkout = Checkout.objects.get(user=checkout_user)
        except:
            checkout = Checkout()
            checkout.user = CustomUser.objects.get(id=checkout_user)  # checkout user saving

        checkout.discount = discount  # initially discount should be zero
        checkout.coupon = None

        try:
            cart_items = CartItem.objects.filter(customer=my_user).order_by(
                'id')  # fetch every cart items related with the cart
            for item in cart_items:
                total += (item.product.product_price * item.quantity)
                quantity += item.quantity
            checkout.total = total  # checkout saving total

            if total > 2500:
                delivery_charge = 0
            checkout.shipping = delivery_charge  # checkout saving delivery charge

            tax = (total * 3) // 100
            checkout.tax = tax  # checkout saving tax

            # after submitting the coupon form. Coupon handling logic

            if request.method == 'POST':
                arr = []  # for storing used coupon
                orders = Order.objects.filter(user=checkout_user)
                if orders:
                    for order in orders:
                        if order.coupon:
                            arr.append(order.coupon.coupon_code)
                        else:
                            pass
                coupon_code = request.POST['coupon']
                coupon = Coupons.objects.get(coupon_code__exact=coupon_code)

                if coupon_code in arr:
                    messages.error(request, "Coupon already taken")
                    return redirect('cart')
                else:
                    if coupon.active and coupon in coupons:
                        minimum_amount = coupon.minimum_order_amount
                        if total > minimum_amount:
                            if coupon.discount_amount:
                                discount = coupon.discount_amount
                            elif coupon.discount:
                                discount = (total * coupon.discount) / 100
                            else:
                                discount = 0
                            checkout.discount = discount  # checkout saving
                            checkout.coupon = coupon
                            messages.success(request, "coupon applied")
                        else:
                            messages.error(request, f"minimum purchase amount : Rs. {minimum_amount}")
                            return redirect('cart')
                    else:
                        messages.error(request, "coupon expired")
                        return redirect('cart')
                checkout.save()

            grand_total = (total + tax + delivery_charge) - discount  # calculating grand total.
            checkout.grand_total = grand_total  # checkout saving grand total.

        except ObjectDoesNotExist:
            pass

        checkout.save()

    # anonymous user handling
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))  # fetching the cart id
            cart_items = CartItem.objects.filter(cart=cart)  # fetch every cart items related with the cart
            for item in cart_items:
                total += (item.product.product_price * item.quantity)
                quantity += item.quantity
            if total > 2500:
                delivery_charge = 0

            tax = (total * 3) / 100

            if request.method == 'POST':
                coupon_code = request.POST['coupon']
                coupon = Coupons.objects.get(coupon_code__exact=coupon_code)
                if coupon.active == True:
                    minimum_amount = coupon.minimum_order_amount
                    if total > minimum_amount:
                        if coupon.discount_amount:
                            discount = coupon.discount_amount
                        elif coupon.discount:
                            discount = (total * coupon.discount) / 100
                        else:
                            discount = 0
                        messages.success(request, "coupon applied")
                    else:
                        messages.error(request, f"minimum purchase amount : Rs. {minimum_amount}")
                else:
                    messages.error(request, "coupon expired")

            grand_total = (total + delivery_charge + tax) - discount
        except ObjectDoesNotExist:
            pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'delivery_charge': delivery_charge,
        'tax': tax,
        'grand_total': grand_total,
        'coupons': coupons,
        'coupon_discount': discount,
        'coupon': coupon,
    }

    return render(request, 'product/cart.html', context)


def _cart_id(request):
    cart = request.session.session_key  # checking for current session
    if not cart:
        cart = request.session.create()  # if there is no session create a new session
    return cart


def add_cart(request, product_id):
    if 'email' in request.session:
        return redirect('admin_dashboard')
    product = Product.objects.get(id=product_id)

    # getting variant of product
    if request.method == 'POST':
        try:
            product = Product.objects.get(id=product_id)
            category_slug = product.category.slug
            product_slug = product.slug
            size = request.POST['selectedValue']
            if size:
                variant = ProductVariant.objects.get(Q(product=product), Q(product_size__size=size))
            else:
                messages.error(request, 'choose a size')
                return redirect('detail_view', category_slug, product_slug)
        except ProductVariant.DoesNotExist:
            return redirect('detail_view', category_slug, product_slug)

    # getting cart    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    # getting cart items
    try:
        if 'user' in request.session:
            my_user = request.user
            cart_item = CartItem.objects.get(product=variant, customer=my_user)
            if variant.stock > cart_item.quantity:
                cart_item.quantity += 1
            else:
                messages.error(request, "stock exhausted")
        else:
            cart_item = CartItem.objects.get(product=variant, cart=cart)
            if variant.stock > cart_item.quantity:
                cart_item.quantity += 1
            else:
                messages.error(request, "stock exhausted")
        cart_item.save()


    except CartItem.DoesNotExist:
        if 'user' in request.session:
            my_user = request.user
            cart_item = CartItem.objects.create(product=variant, quantity=1, cart=cart, customer=my_user)
        else:
            cart_item = CartItem.objects.create(product=variant, quantity=1, cart=cart)
        cart.save()

    return redirect('cart')


@cache_control(no_cache=True, no_store=True)
def remove_cart_quandity(request):
    if 'email' in request.session:
        return redirect('admin_dashboard')
    if request.method == 'POST':
        grant_total, total_amount, total, tax = 0, 0, 0, 0
        delivery_charge = 99

        variant_id = request.POST.get('product_id')
        product_quantity = request.POST.get('product_quandity')
        product_stock = request.POST.get('productStock')

        variant = ProductVariant.objects.get(id=variant_id)

        if 'user' in request.session:
            my_user = request.user
            print("---------------------------")
            print(my_user)
            try:
                cart_item = CartItem.objects.get(customer=my_user, product=variant)
                print("---------------------------")
                print(variant)
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1

                cart_item.save()

                product_quantity = cart_item.quantity
                total = cart_item.product.product_price * cart_item.quantity
                cart_items = CartItem.objects.filter(customer=my_user)

                for item in cart_items:
                    grant_total += (item.product.product_price * item.quantity)

            except CartItem.DoesNotExist:
                pass

            try:
                # check out handling
                checkout = Checkout.objects.get(user=my_user.id)

                checkout.total = grant_total
                if grant_total > 2500:
                    delivery_charge = 0
                checkout.shipping = delivery_charge  # checkout saving delivery charge
                tax = (grant_total * 3) // 100  # tax logic
                checkout.tax = tax
                total_amount = (grant_total + tax + delivery_charge)  # calculating grand total.
                checkout.grand_total = total_amount

                checkout.save()

            except Checkout.DoesNotExist:
                pass

        else:

            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_item = CartItem.objects.get(cart=cart, product=variant)
                if variant.stock > cart_item.quantity:
                    cart_item.quantity += 1
                    product_quantity += 1
                else:
                    messages.error(request, "No more products available in the current variant")
                cart_item.save()
                total = cart_item.product.product_price * cart_item.quantity

            except CartItem.DoesNotExist:
                pass

        return JsonResponse({
            'quantity': product_quantity,
            'total': total,
            'grant_total': grant_total,
            'tax': tax,
            'total_amount': total_amount,
            'delivery_charge': delivery_charge,
        })
    else:
        return redirect('cart')




@cache_control(no_cache=True, no_store=True)
def add_cart_quandity(request):
    if 'email' in request.session:
        return redirect('admin_dashboard')
    if request.method == 'POST':
        grant_total, total_amount, total, tax = 0, 0, 0, 0
        delivery_charge = 99

        variant_id = request.POST.get('product_id')
        product_quantity = request.POST.get('product_quandity')
        product_stock = request.POST.get('productStock')

        variant = ProductVariant.objects.get(id=variant_id)

        if 'user' in request.session:
            my_user = request.user
            print("---------------------------")
            print(my_user)
            try:
                cart_item = CartItem.objects.get(customer=my_user, product=variant)
                print("---------------------------")
                print(variant)
                if variant.stock > cart_item.quantity:
                    cart_item.quantity += 1

                cart_item.save()

                product_quantity = cart_item.quantity
                total = cart_item.product.product_price * cart_item.quantity
                cart_items = CartItem.objects.filter(customer=my_user)

                for item in cart_items:
                    grant_total += (item.product.product_price * item.quantity)

            except CartItem.DoesNotExist:
                pass

            try:
                # check out handling
                checkout = Checkout.objects.get(user=my_user.id)

                checkout.total = grant_total
                if grant_total > 2500:
                    delivery_charge = 0
                checkout.shipping = delivery_charge  # checkout saving delivery charge
                tax = (grant_total * 3) // 100  # tax logic
                checkout.tax = tax
                total_amount = (grant_total + tax + delivery_charge)  # calculating grand total.
                checkout.grand_total = total_amount

                checkout.save()

            except Checkout.DoesNotExist:
                pass

        else:

            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_item = CartItem.objects.get(cart=cart, product=variant)
                if variant.stock > cart_item.quantity:
                    cart_item.quantity += 1
                    product_quantity += 1
                else:
                    messages.error(request, "No more products available in the current variant")
                cart_item.save()
                total = cart_item.product.product_price * cart_item.quantity

            except CartItem.DoesNotExist:
                pass

        return JsonResponse({
            'quantity': product_quantity,
            'total': total,
            'grant_total': grant_total,
            'tax': tax,
            'total_amount': total_amount,
            'delivery_charge': delivery_charge,
            'product_stock': product_stock,
        })
    else:
        return redirect('cart')


@cache_control(no_cache=True, no_store=True)
def delete_cart(request, variant_id):
    if 'email' in request.session:
        return redirect('admin_dashboard')
    variant = get_object_or_404(ProductVariant, id=variant_id)
    if 'user' in request.session:
        my_user = request.user
        cart_item = CartItem.objects.filter(customer=my_user, product=variant)
        if cart_item:
            cart_item.delete()
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))

        cart_item = CartItem.objects.filter(cart=cart, product=variant)
        cart_item.delete()
    return redirect('cart')


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='user_login')
def coupon_remove(request):
    if 'email' in request.session:
        return redirect('admin_dashboard')
    my_user = request.user
    checkout = Checkout.objects.get(user=my_user)
    checkout.coupon = None
    checkout.discount = 0
    checkout.save()
    return redirect('cart')


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='user_login')
def checkout(request):
    if 'email' in request.session:
        return redirect('admin_dashboard')
    if 'user' in request.session:
        my_user = request.user
        cart_items = CartItem.objects.filter(customer=my_user)
        if not cart_items:
            return redirect('index')
        checkout_user = my_user.id
        try:
            checkout_items = Checkout.objects.get(user=checkout_user)
        except Checkout.DoesNotExist:
            checkout_items = None
        try:
            address = UserAddress.objects.filter(user=my_user)
        except Exception as e:
            print(e)
            messages.error(request, "choose address")
            return redirect('checkout')
        context = {
            'addresses': address,
            'checkout_items': checkout_items,
        }

        # place holder handling logic after form submission.
        if request.method == 'POST':
            try:
                delivery_address = UserAddress.objects.get(id=request.POST['selectAddress'])
                payment = request.POST['paymentMethod']
            except Exception as e:
                messages.error(request, "Choose delivery address")
                return redirect('checkout')

            # wallet is selected or not.
            try:
                wallet = request.POST['selectWallet']
            except:
                wallet = 0
            checkout_items.wallet = wallet
            checkout_items.address = delivery_address
            checkout_items.payment = payment

            checkout_items.save()

            # wallet handling must accept this condition on the time of order submit.
            if float(checkout_items.grand_total) > float(checkout_items.wallet):
                checkout_items.payable_amount = float(checkout_items.grand_total) - float(checkout_items.wallet)
                # my_user.wallet = float(my_user.wallet) - float(checkout_items.wallet)

            elif float(checkout_items.grand_total) < float(checkout_items.wallet):
                checkout_items.payable_amount = 0
                # my_user.wallet = float(checkout_items.wallet) - float(checkout_items.grand_total)

            else:
                checkout_items.payable_amount = 0
                # my_user.wallet = float(my_user.wallet) - float(checkout_items.grand_total)

            checkout_items.save()

            my_user.save()

            return redirect('order')

        return render(request, "product/checkout.html", context)
