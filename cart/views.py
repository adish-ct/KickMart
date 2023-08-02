from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from user_app.models import CustomUser
from cart.models import *
from shop.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

# Create your views here.


def cart(request, quantity=0, total=0, cart_items=None, tax=0, grand_total=0):
    delivery_charge = 99
    if 'user' in request.session:
        my_user = request.user.id
        try:
            cart_items = CartItem.objects.filter(customer=my_user).order_by('id') # fetch every cart items related with the cart
            for item in cart_items: 
                total += (item.product.product_price * item.quantity)
                quantity += item.quantity
            if total > 2500:
                delivery_charge = 0
            else:
                delivery_charge 
            tax = (total * 3) / 100
            grand_total = total + tax
        except ObjectDoesNotExist:
            pass
    else:        
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
            grand_total = total + tax
        except ObjectDoesNotExist:
            pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'delivery_charge': delivery_charge,
        'tax': tax,
        'grand_total': grand_total,
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
        # cart_item = CartItem.objects.get(product=variant, cart=cart)
        # cart_item.quantity += 1
        # cart_item.save()
        if 'user' in request.session:
            my_user = request.user
            cart_item = CartItem.objects.get(product=variant, customer=my_user)
            cart_item.quantity += 1
        else:
            cart_item = CartItem.objects.get(product=variant, cart=cart)
            cart_item.quantity += 1
        cart_item.save()


    except CartItem.DoesNotExist:
        # cart_item = CartItem.objects.create(single_product=product, quantity=1, cart=cart)
        if 'user' in request.session:
            my_user = request.user
            cart_item = CartItem.objects.create(product=variant, quantity=1, cart=cart, customer=my_user)
        else:
            cart_item = CartItem.objects.create(product=variant, quantity=1, cart=cart)
        cart.save()
        pass

    return redirect('cart')



def remove_cart(request, variant_id):
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


def add_cart_quandity(request, variant_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    variant = ProductVariant.objects.get(id=variant_id)
    try:
        cart_item = CartItem.objects.get(cart=cart, product=variant)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart')


def delete_cart(request, variant_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    variant = get_object_or_404(ProductVariant, id=variant_id)
    cart_item = CartItem.objects.filter(cart=cart, product=variant)
    cart_item.delete()
    return redirect('cart')


