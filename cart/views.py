from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from user_app.models import *
from cart.models import *
from shop.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required

# Create your views here.


@cache_control(no_cache=True)
def cart(request, quantity=0, total=0, cart_items=None, tax=0, grand_total=0, coupon=None):
    coupons = Coupons.objects.all().order_by('id')
    delivery_charge = 99

    if 'user' in request.session:
        discount = 0
        my_user = request.user
        checkout_user = request.user.id
        if Checkout.objects.get(user=checkout_user):
            checkout = Checkout.objects.get(user=checkout_user)   
        else:
            checkout = Checkout()
        checkout.user = CustomUser.objects.get(id=checkout_user)  # checkout user saving
        checkout.discount = 0       # initially discount should be zero
        checkout.coupon = None
        
        try:
            cart_items = CartItem.objects.filter(customer=my_user).order_by('id') # fetch every cart items related with the cart
            for item in cart_items: 
                total += (item.product.product_price * item.quantity)
                quantity += item.quantity
            checkout.total = total  # checkout saving 
            if total > 2500:
                delivery_charge = 0
            checkout.shipping = delivery_charge     # checkout saving 
             
            tax = (total * 3) // 100
            checkout.tax = tax      # checkout saving 

            if request.method == 'POST':
                coupon_code = request.POST['coupon']
                coupon = Coupons.objects.get(coupon_code__exact=coupon_code)
                if coupon.active == True:
                    minimum_amount = coupon.minimum_order_amount
                    if total > minimum_amount:
                        if coupon.discount_amount:
                            discount = coupon.discount_amount
                            checkout.discount = discount
                        elif coupon.discount:
                            discount = ( total * coupon.discount ) / 100
                            checkout.discount = discount
                        else:
                            discount = 0
                            checkout.discount = discount        # checkout saving 
                        checkout.coupon = coupon
                        messages.success(request, "coupon applied")
                    else:
                        messages.error(request, f"minimum purchase amount : Rs. {minimum_amount}")
                else:
                    messages.error(request, "coupon expired")
            grand_total = total + tax - discount
            checkout.grand_total = grand_total          # checkout saving 
            
        except ObjectDoesNotExist:
            pass

        checkout.save()
 
    else:
        discount = 0        
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) # fetching the cart id 
            cart_items = CartItem.objects.filter(cart=cart) # fetch every cart items related with the cart
            for item in cart_items: 
                total += (item.product.product_price * item.quantity)
                quantity += item.quantity
            if total > 2500:
                delivery_charge = 0
            else:
                delivery_charge 
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
                            discount = ( total * coupon.discount ) / 100
                        else:
                            discount = 0
                        messages.success(request, "coupon applied")
                    else:
                        messages.error(request, f"minimum purchase amount : Rs. {minimum_amount}")
                else:
                    messages.error(request, "coupon expired")

            grand_total = total + tax - discount
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
    cart = request.session.session_key # checking for current session
    if not cart:
        cart = request.session.create() # if there is no session create a new session
    return cart




def add_cart(request, product_id):
    
    product = Product.objects.get(id=product_id)

    # getting variant of product
    if request.method == 'POST':
        product = Product.objects.get(id=product_id)
        size = request.POST['selectedValue']
        variant = ProductVariant.objects.get(Q(product=product), Q(product_size__size=size))

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
def remove_cart(request, variant_id):
    if request.method == 'POST':
        variant = get_object_or_404(ProductVariant, id=variant_id)
        if 'user' in request.session:
            my_user = request.user.id
            try:
                cart_item = CartItem.objects.get(product=variant, customer=my_user)
                if cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                else:
                    cart_item.delete()
            except CartItem.DoesNotExist:
                pass
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))         # fetch the current cart, cart will be present in this case.
            try:
                cart_item = CartItem.objects.get(product=variant, cart=cart)    # fetch the cart item 
                if cart_item.quantity > 1:
                    cart_item.quantity = cart_item.quantity - 1
                    cart_item.save()
                else:
                    cart_item.delete()
            except CartItem.DoesNotExist:
                pass
        return redirect('cart')
    else:
        return redirect('cart')


@cache_control(no_cache=True, no_store=True)
def add_cart_quandity(request, variant_id):
    if request.method == 'POST':
        variant = ProductVariant.objects.get(id=variant_id)
        cart = Cart.objects.get(cart_id=_cart_id(request))
        if 'user' in request.session:
            my_user = request.user

            try:
                cart_item = CartItem.objects.get(customer=my_user, product=variant)
                if variant.stock > cart_item.quantity:
                    cart_item.quantity += 1
                else:
                    messages.error(request, "No more products available in the current variant")
                cart_item.save()
            except CartItem.DoesNotExist:
                pass
        else:
            try:
                cart_item = CartItem.objects.get(cart=cart, product=variant)
                if variant.stock > cart_item.quantity:
                    cart_item.quantity += 1
                else:
                    messages.error(request, "No more products available in the current variant")
                cart_item.save()
            except CartItem.DoesNotExist:
                pass
        return redirect('cart')
    else:
        return redirect('cart')


@cache_control(no_cache=True, no_store=True)
def delete_cart(request, variant_id):
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


@login_required(login_url='user_login')
def checkout(request):
    if 'user' in request.session:
        my_user = request.user
        checkout_user = my_user.id
        try:
            checkout_items = Checkout.objects.get(user=checkout_user)
        except Checkout.DoesNotExist:
            checkout_items = None
        address = UserAddress.objects.filter(user=my_user)
        
        context = {
            'addresses': address,
            'checkout_items': checkout_items,
        }
        # return HttpResponse(context['addresses'])

        if request.method == 'POST':
            delivery_address = UserAddress.objects.get(id=request.POST['selectAddress'])
            payment = request.POST['paymentMethod']
            checkout_items.address = delivery_address
            checkout_items.payment = payment
            checkout_items.save()

            return redirect('order')        
        return render(request, "product/checkout.html", context)
        

