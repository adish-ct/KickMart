import os
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.shortcuts import render, redirect, get_object_or_404
from user_app.models import *
from shop.models import *
from order.models import *
from django.http import HttpResponse
from django.db.models import Sum
from django.utils import timezone
from datetime import date, datetime



# Create your views here.

@cache_control(no_cache=True, no_store=True)
def admin_login(request):
    if 'email' in request.session:
        return redirect('admin_dashboard')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        admin = authenticate(email=email, password=password)            # authenticating user, checking user is valid or not   
        if admin:
            if admin.is_superuser:                                      # checking if the admin is super user or not.
                login(request, admin)
                request.session['email'] = email
                return redirect('admin_dashboard')
            else:
                messages.error(request, "You can't access this session with user credentials.")
        else:
            messages.error(request, "Invalid credentials, try again with valid credentials.")
    return render(request, 'admin/admin_login.html')



@staff_member_required(login_url='admin_login')
def admin_dashboard(request):
    orders = Order.objects.all().order_by('-id')
    order_count = orders.count()
    order_total = Order.objects.aggregate(total=Sum('order_total'))['total']
    today = date.today()
    today_count = Order.objects.filter(created__date=today).count()
    today_revenue = Order.objects.filter(created__date=today).aggregate(total=Sum('order_total'))['total']
    cash_on_delivery = Order.objects.filter(payment__payment_method='Cashon Delivery').count()
    razor_pay = Order.objects.filter(payment__payment_method='Razor Pay').count()
    # paypal = Order.objects.filter(payment__payment_method='Paypal').count()

    if request.method == 'POST':
        try:
            date_from = request.POST.get('startDate')
            date_to = request.POST.get('endDate')
            orders = Order.objects.filter(created__range=(date_from, date_to))
        except:
            pass

    ar = [2020,2021,2022, 2023]
    sales =[10000 ,2500,1200, 3500]

    payment_count = [cash_on_delivery, razor_pay]
    payment_method = ['Cash on Delivery', 'Razor Pay']

    month = ['June', 'July', 'Aug', 'Oct', 'Nov', 'Dec']
    order = [0, 0, order_count, 0, 0]
    context = {
        'year': ar,
        'sales': sales,
        'month': month,
        'order': order,
        'orders': orders,
        'order_count': order_count,
        'order_total': order_total,
        'today_count': today_count,
        'today_revenue': today_revenue,
        'payment_count': payment_count,
        'payment_method': payment_method,
    }
    return render(request, 'admin/admin_dashboard.html', context)



# Product section -----------------------------------------------


@staff_member_required(login_url='admin_login')
def admin_product(request):
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'admin/admin_product.html', context)


@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def admin_edit_product(request, id):
    product = Product.objects.get(id=id)
    product_category = product.category
    product_brand = product.brand
    # fetch the images from multiple images table related with that product
    object_image = MultipleImages.objects.filter(product=id)
    brands = ProductBrand.objects.exclude(brand_name=product_brand)
    categories = Category.objects.exclude(category_name=product_category)
    context = {
        'product': product,
        'categories': categories,
        'brands': brands,
        'product_category': product_category,
        'product_brand': product_brand,
        'multiple_images': object_image,
    }

    if request.method == 'POST':
        product_name = request.POST['product_name']
        category = request.POST['selectOption']
        brand = request.POST['selectBrandOption']
        original_price = request.POST['originalPrice']
        selling_price = request.POST['sellingPrice']
        # condition for checking is there any file is present in the request.
        single_image = request.FILES.get('image', None)
    
        multiple_images = request.FILES.getlist('multipleImage')
            # we want to remove the image that already stored in the database.
            # first of all we have to check if there is any image exist on product object.
        if single_image:
            if product.product_image:
                os.remove(product.product_image.path)
            product.product_image = single_image  

        if multiple_images:
            if object_image:
                for i in object_image:
                    os.remove(i.images.path)
                    i.delete()
                for image in multiple_images:
                    photo = MultipleImages.objects.create(
                        product = product,
                        images = image,
                    )
            else:
                for image in multiple_images:
                    photo = MultipleImages.objects.create(
                        product = product,
                        images = image,
                    )
                
        product.product_name = product_name
        product.category = Category.objects.get(id=category)
        product.brand = ProductBrand.objects.get(id=brand)
        product.original_price = original_price
        product.selling_price = selling_price

        product.save()
        # Multi_image.save()
        messages.success(request, "Product updated successfully")
        return redirect('admin_product')

    return render(request, 'admin/admin_edit_product.html', context)


@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def admin_add_product(request):
    categories = Category.objects.all()
    brands = ProductBrand.objects.all()
    context = {
        'categories': categories,
        'brands': brands,
    }
    if request.method == 'POST':
        product = Product()
        category = request.POST['selectOption']
        brand = request.POST['selectBrand']
        original_price = request.POST['originalPrice']
        selling_price = request.POST['sellingPrice']
        product_offer = request.POST['productOffer']
        if product_offer != 0:
            off_amount = (original_price * product_offer) / 100
            selling_price = original_price - off_amount
        if category.offer != 0:
            discount_amount = (selling_price * category.offer) / 100
            selling_price = selling_price - discount_amount
        
        # single image fetching
        product_image = request.FILES.get('image', None)
        if product_image:
            product.product_image = product_image
  
        product.product_name = request.POST['name']
        product.category = Category.objects.get(id=category)
        product.brand = ProductBrand.objects.get(id=brand)
        product.original_price = original_price
        product.selling_price = selling_price
        product.product_description = request.POST['description']
        product.offer = product_offer
        product.save()

        # multiple image fetching
        multiple_images = request.FILES.getlist('multipleImage', None)
        if multiple_images:            
            for image in multiple_images:
                photo = MultipleImages.objects.create(
                    product = product,
                    images = image,
                )
            
        messages.success(request, "Product added successfully")

        return redirect('admin_product')

    return render(request, 'admin/admin_add_product.html', context)



@cache_control(no_store=True, no_cache=True)
@staff_member_required(login_url='admin_login')
def admin_delete_product(request, id):
    prod = Product.objects.get(id=id)
    if prod.product_image:
        if len(prod.product_image) != 0:
            os.remove(prod.product_image.path)
    prod.delete()
    messages.success(request, "Product deleted successfully")

    return redirect('admin_product')



@staff_member_required(login_url='admin_login')
def admin_product_variant(request, product_id):
    variant = ProductVariant.objects.filter(product=product_id)
    context = {
        'variants': variant,
        'product_id': product_id,
    }

    return render(request, 'admin/admin_variant_product.html', context)



@staff_member_required(login_url='admin_login')
@cache_control(no_store=True, no_cache=True)
def add_product_variant(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variants = ProductVariant.objects.filter(product=product)
    sizes = ProductSize.objects.all().order_by('id')
    
    if request.method == 'POST':
        size = request.POST['selectSize']
        stock = request.POST['stock']
        productPrice = request.POST['productPrice']
        try:
            variant = ProductVariant.objects.get(product=product, product_size=size)
            variant.stock = variant.stock + int(stock)
        except ProductVariant.DoesNotExist:
            variant = ProductVariant.objects.create(
                product=product,
                product_size=size,
                stock=stock,
            )
        if productPrice:
            variant.product_price = productPrice
        variant.save()

        return redirect('admin_product_variant', product_id)

    context = {
        'product': product,
        'sizes': sizes,
        'product_variants': product_variants,
    }

    return render(request, 'admin/admin_add_variant.html', context)



@staff_member_required(login_url='admin_login')
@cache_control(no_store=True, no_cache=True)
def product_variant_update(request):
    if request.method == 'POST':
        id = request.POST['id']
        price = request.POST['price']
        stock = request.POST['stock']
        variant = ProductVariant.objects.get(id=id)
        product_id = variant.product
        variant.product_price = price
        variant.stock = stock
        variant.save()

        return redirect('admin_product_variant', product_id.id)



@staff_member_required(login_url='admin_login')
@cache_control(no_store=True, no_cache=True)
def product_variant_control(request, variant_id):
    variant = ProductVariant.objects.get(id=variant_id)
    product_id = variant.product.id
    if variant.is_active:
        variant.is_active = False
    else:
        variant.is_active = True
    variant.save()
    
    return redirect('admin_product_variant', product_id)



def product_variant_delete(request, variant_id):

    if request.method == 'POST':
        variant = ProductVariant.objects.get(id=variant_id)
        product = variant.product
        if variant:
            variant.delete()
        return redirect('admin_product_variant', product.id)
    else:
        return redirect('admin_dashboard')

# Product section end -------------------------------------------------


# admin user section --------------------------------------------------


@staff_member_required(login_url='admin_login')
def admin_users(request):
    users = CustomUser.objects.all()
    context = {
        'users': users,
    }

    return render(request, 'admin/admin_users.html', context)



@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def admin_user_manage(request, id):
    user = CustomUser.objects.get(id=id)
    if user.is_active:
        user.is_active = False
        user.save()
    else:
        user.is_active = True
        user.save()

    return redirect('admin_users')






# admin user section ended ------------------------------------------


# admin category section --------------------------------------------


@staff_member_required(login_url='admin_login')
def admin_category(request):
    categories = Category.objects.all().order_by('id')
    context = {
        'categories': categories
    }

    return render(request, 'admin/admin_category.html', context)



@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def admin_add_category(request):
    if request.method == 'POST':
        category_name = request.POST['category_name']
        exist_category = Category.objects.filter(category_name__iexact=category_name)
        if exist_category.exists():
            messages.error(request, "This is an existing category")
            return redirect('admin_add_category')
        if len(request.FILES['image']):
            category_image = request.FILES['image']
        category = Category(
            category_name = category_name,
            category_image = category_image,
            category_description = request.POST['description'],
            offer = request.POST['category_offer'],
            )
        category.save()
        messages.success(request, "Successfully added new category")

        return redirect('admin_category')
    
    return render(request, 'admin/admin_add_category.html')



@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def admin_edit_category(request, id):
    category = Category.objects.get(id=id)
    context = {
        'category': category,
    }
    if request.method == 'POST':
        if len(request.FILES) != 0:
            if category.category_image:
                if len(category.category_image) > 0:
                    os.remove(category.category_image.path)
            category.category_image = request.FILES['image']
        category.category_name = request.POST['name']
        category.category_description = request.POST['description']
        category.offer = request.POST['category_offer']
        category.save()
        messages.success(request, "Category updated successfully")

        return redirect('admin_category')
    
    return render(request, 'admin/admin_edit_category.html', context)



@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def admin_delete_category(request, id):
    category = Category.objects.get(id=id)
    if category.category_image:
        if len(category.category_image) > 0:
            os.remove(category.category_image.path)
    category.delete()

    return redirect('admin_category')


# admin category section end ---------------------------------------

# coupon section start ----------------------------------------------

@staff_member_required(login_url='admin_login')
def admin_coupon_management(request):
    coupons = Coupons.objects.all().order_by('id')
    context = {
        'coupons': coupons,
    }
    return render(request, 'admin/admin_coupon.html', context)



@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def add_coupon(request):
    if request.method == 'POST':
        description = request.POST['description']
        coupon_code = request.POST['coupon_code']
        coupon_title = request.POST['coupon_title']
        discount_amount = request.POST['discount_amount']
        discount = request.POST['discount'] 
        valid_from = request.POST['valid_from']
        valid_to = request.POST['valid_to'] 
        quantity = request.POST['quantity'] 
        minimum_order_amount = request.POST['minimum_amount'] 

        coupon = Coupons.objects.create(
            description = description,
            coupon_code = coupon_code,
            coupon_title = coupon_title,
            valid_from = valid_from,
            valid_to = valid_to,
            quantity = quantity,
            minimum_order_amount = minimum_order_amount,
        )
        if discount_amount:
            coupon.discount_amount = discount_amount
        if discount:
            coupon.discount = discount
    
        coupon.save()

        return redirect('admin_coupon_management')
    return render(request, 'admin/admin_add_coupon.html')



@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def delete_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupons, id=coupon_id)
    if coupon:
        coupon.delete()
    return redirect ('admin_coupon_management')



@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def edit_coupon(request, coupon_id):
    coupon = Coupons.objects.get(id=coupon_id)
    if request.method == 'POST':
        description = request.POST['description']
        coupon_code = request.POST['coupon_code']
        coupon_title = request.POST['coupon_title']
        discount_amount = request.POST['discount_amount']
        discount = request.POST['discount'] 
        valid_from = request.POST['valid_from']
        valid_to = request.POST['valid_to'] 
        quantity = request.POST['quantity'] 
        minimum_order_amount = request.POST['minimum_amount'] 

        coupon.id = coupon_id
        coupon.description = description
        coupon.coupon_code = coupon_code
        coupon.coupon_title = coupon_title
        coupon.quantity = quantity
        coupon.minimum_order_amount = minimum_order_amount

        if valid_from:
            coupon.valid_from = valid_from
        if valid_to:
            coupon.valid_to = valid_to
        if discount_amount:
            coupon.discount_amount = discount_amount
            if discount:
                discount = None
        if discount:
            if discount_amount:
                discount_amount = None
                coupon.discount = discount   

        coupon.save()

        return redirect('admin_coupon_management')
    context = {
        'coupon': coupon,
    }
    return render(request, 'admin/admin_edit_coupon.html', context)



@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def activate_coupon(requset, coupon_id):
    coupon = Coupons.objects.get(id=coupon_id)
    if coupon.active:
        coupon.active = False
    else:
        coupon.active = True
    coupon.save()
    return redirect('admin_coupon_management')


# coupon section end ----------------------------------------------


# order management section ----------------------------------------

@staff_member_required(login_url='admin_login')
def order_management(request):
    orders = Order.objects.all().order_by('-order_id')
    context = {
        'orders': orders,
    }
    return render(request, 'admin/admin_order_management.html', context)




@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def order_update(request, order_id):
    order = Order.objects.get(id=order_id)
    order_items = OrderProduct.objects.filter(order_id=order_id)
    payment = order.payment
    if request.method == 'POST':
        order_status = request.POST.get('orderStatus', None)
        if order_status:
            order.status = order_status
            order.save()
        if order_status == 'Delivered':
            payment.is_paid = True
        
        payment.save()
        messages.success(request, 'Status updated')
        return redirect('order_update', order_id)
    context = {
        'order': order,
        'order_items': order_items,
    }

    return render(request, 'admin/admin_order_update.html', context)



@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def return_request(request, item_id):
    order_item = OrderProduct.objects.get(id=item_id)
    variant = order_item.variant
    order = order_item.order_id
    order_id = order.id
    coupon = order.coupon
    user = order.user
    deduct_discount = order.discount

    if order.total < 2500:                      # delivery charge logic.
        delivery_charge = 99
    else:
        delivery_charge = 0

    if request.method == 'POST':
        order_item.is_returned = True
        variant.stock += order_item.quandity
        amount = variant.product_price * order_item.quandity
        if coupon:
            if float(order.total) - float(amount) >= float(coupon.minimum_order_amount):
                deduct_discount = 0
            else:
                order.discount = 0

        refund_amount = (float(amount) + float(delivery_charge)) - float(deduct_discount)           # calculating refund amount.
        user.wallet = float(user.wallet) + float(refund_amount) 
        order_item.save()
        variant.save()
        user.save()
        order.save()
        
    return redirect('order_update', order_id)


# -------------------------- Banner Management --------------------------


@staff_member_required(login_url='admin_login')
def banner_management(request):
    banners = Banner.objects.all().order_by('id')
    context = {
        'banners': banners,
    }
    return render(request, 'admin/admin_banner.html', context)



@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def create_banner(request):
    if request.method == 'POST':
        banner = Banner.objects.create(
            section = request.POST.get('section', None), 
            identifier = request.POST.get('identifier', None),
            description = request.POST.get('description', None),
            offer_detail = request.POST.get('offer', None),
            title = request.POST.get('title', None) ,
            notes = request.POST.get('notes', None) ,
        )
        if request.FILES['image']:
            image = request.FILES['image']
            banner.image = image
        banner.save() 

        return redirect('banner_management')

    return render(request, 'admin/admin_add_banner.html')



@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def update_banner(request, banner_id):
    banner = Banner.objects.get(id=banner_id)
    
    if request.method == 'POST':
        banner.section = request.POST['section']        
        banner.identifier = request.POST['identifier']
        banner.description = request.POST['description']
        banner.offer_detail = request.POST['offer']
        banner.title = request.POST.get('title', None)
        banner.notes = request.POST['notes']
        if len(request.FILES) != 0:
            if banner.image:
                os.remove(banner.image.path)
            banner.image = request.FILES['image']
        banner.save()

        return redirect('banner_management')
    
    context = {
        'banner': banner,
    }

    return render(request, 'admin/admin_edit_banner.html', context)



@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def delete_banner(request, banner_id):
    banner = Banner.objects.get(id=banner_id)
    banner.delete()
    return redirect('banner_management')



@staff_member_required(login_url='admin_login')
def reports(request):
    variants = ProductVariant.objects.all()
    cancel_orders = OrderProduct.objects.filter(item_cancel=True)

    context = {
        'variants': variants,
        'cancel_orders': cancel_orders,
    }

    return render(request, 'admin/admin_reports.html', context)


# -------------------------- Admin Logout --------------------------

@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def admin_logout(request):
    logout(request)
    request.session.flush()
    return redirect('admin_login')



