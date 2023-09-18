# cart quandity update function logic by ajax.

# def remove_cart_quandity(request):
#     # ajax request
#     if request.method == 'POST':
#         grant_total, total_amount, total, tax = 0, 0, 0, 0
#         delivery_charge = 99
#
#         variant_id = request.POST.get('product_id')
#         product_quantity = request.POST.get('product_quandity')
#         product_stock = request.POST.get('product_stock')
#
#         variant = ProductVariant.objects.get(id=variant_id)
#
#         if 'user' in request.session:
#             my_user = request.user.id
#             try:
#                 cart_item = CartItem.objects.get(product=variant, customer=my_user)
#
#                 if cart_item.quantity > 1:
#                     cart_item.quantity -= 1
#                 cart_item.save()
#                 # deleted else case
#
#                 # single product total is total
#                 product_quantity = cart_item.quantity
#                 total = cart_item.product.product_price * cart_item.quantity
#
#                 # Total of every product in cart is grant_total
#                 cart_items = CartItem.objects.filter(customer=my_user).order_by('id')
#
#                 for item in cart_items:
#                     grant_total += (item.product.product_price * item.quantity)
#
#             except CartItem.DoesNotExist:
#                 pass
#
#             try:
#                 # check out handling
#                 checkout = Checkout.objects.get(user=my_user)
#
#                 checkout.total = grant_total
#                 if grant_total > 2500:
#                     delivery_charge = 0
#                 checkout.shipping = delivery_charge  # checkout saving delivery charge
#
#                 tax = (grant_total * 3) // 100
#                 checkout.tax = tax
#                 total_amount = (grant_total + tax + delivery_charge)  # calculating grand total.
#                 checkout.grand_total = total_amount
#
#                 checkout.save()
#             except Checkout.DoesNotExist:
#                 pass
#
#         else:
#             cart = Cart.objects.get(
#                 cart_id=_cart_id(request))  # fetch the current cart, cart will be present in this case.
#             try:
#                 cart_item = CartItem.objects.get(product=variant, cart=cart)  # fetch the cart item
#                 if cart_item.quantity > 1:
#                     cart_item.quantity = cart_item.quantity - 1
#                     cart_item.save()
#                 else:
#                     cart_item.delete()
#                 product_quantity = cart_item.quantity
#             except CartItem.DoesNotExist:
#                 pass
#
#             return redirect('cart')
#
#         return JsonResponse({
#             'quantity': cart_item.quantity,
#             'total': total,
#             'delivery_charge': delivery_charge,
#             'tax': tax,
#             'grant_total': grant_total,
#             'total_amount': checkout.grand_total,
#         })
#     else:
#         return redirect('cart')


#  cart item quandity update without using ajax

# @cache_control(no_cache=True, no_store=True)
# def remove_cart(request, variant_id):
#     if request.method == 'POST':
#         variant = get_object_or_404(ProductVariant, id=variant_id)
#         if 'user' in request.session:
#             my_user = request.user.id
#             try:
#                 cart_item = CartItem.objects.get(product=variant, customer=my_user)
#                 if cart_item.quantity > 1:
#                     cart_item.quantity -= 1
#                     cart_item.save()
#                 else:
#                     cart_item.delete()
#             except CartItem.DoesNotExist:
#                 pass
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))         # fetch the current cart, cart will be present in this case.
#             try:
#                 cart_item = CartItem.objects.get(product=variant, cart=cart)    # fetch the cart item
#                 if cart_item.quantity > 1:
#                     cart_item.quantity = cart_item.quantity - 1
#                     cart_item.save()
#                 else:
#                     cart_item.delete()
#             except CartItem.DoesNotExist:
#                 pass
#         return redirect('cart')
#     else:
#         return redirect('cart')


# @cache_control(no_cache=True, no_store=True)
# def add_cart_quandity(request, variant_id):
#     if request.method == 'POST':
#         variant = ProductVariant.objects.get(id=variant_id)
#         if 'user' in request.session:
#             my_user = request.user

#             try:
#                 cart_item = CartItem.objects.get(customer=my_user, product=variant)
#                 if variant.stock > cart_item.quantity:
#                     cart_item.quantity += 1
#                 else:
#                     messages.error(request, "No more products available in the current variant")
#                 cart_item.save()
#             except CartItem.DoesNotExist:
#                 pass
#         else:
#             try:
#                 cart = Cart.objects.get(cart_id=_cart_id(request))
#                 cart_item = CartItem.objects.get(cart=cart, product=variant)
#                 if variant.stock > cart_item.quantity:
#                     cart_item.quantity += 1
#                 else:
#                     messages.error(request, "No more products available in the current variant")
#                 cart_item.save()
#             except CartItem.DoesNotExist:
#                 pass
#         return redirect('cart')
#     else:
#         return redirect('cart')