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
from django.db.models import Sum, Count
from django.db.models.functions import ExtractMonth, ExtractYear


# Create your views here.

@cache_control(no_cache=True, no_store=True)
def admin_login(request):
    if 'email' in request.session:
        return redirect('admin_dashboard')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        admin = authenticate(email=email, password=password)  # authenticating user, checking user is valid or not
        if admin:
            if admin.is_superuser:  # checking if the admin is super user or not.
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
    context = {}
    order = [0] * 12
    order_count = [0] * 12
    year = [0]
    payment_count = []
    payment_method = []

    try:
        orders = Order.objects.all().order_by('-id')
        order_count = orders.count()
        order_total = Order.objects.aggregate(total=Sum('order_total'))['total']
        today = date.today()
        today_count = Order.objects.filter(created__date=today).count()
        today_revenue = Order.objects.filter(created__date=today).aggregate(total=Sum('order_total'))['total']
        cash_on_delivery = Order.objects.filter(payment__payment_method='Cashon Delivery').count()
        razor_pay = Order.objects.filter(payment__payment_method='Razor Pay').count()

        payment_count = [cash_on_delivery, razor_pay]
        payment_method = ['Cash on Delivery', 'Razor Pay']

        # -------------------- month order section revenue ---------------------------

        monthly_sales = (
            Order.objects.annotate(month=ExtractMonth('created'))
            .values('month')
            .annotate(total_sales=Sum('order_total'))
            .order_by('month')
        )

        months_sales = [item['month'] for item in monthly_sales]
        total_sales = [item['total_sales'] for item in monthly_sales]

        i = 0
        while i < len(order):
            try:
                if i == monthly_sales[0]['month']:
                    order[i] = int(monthly_sales[0]['total_sales'])
            except Exception as e:
                print(e)
            i += 1

        # ----------------------- revenue ended -------------------------

        # -------------------- monthly orders count ----------------------

        monthly_order_count = (
            Order.objects
            .annotate(month=ExtractMonth('created'))
            .values('month')
            .annotate(order_count=Count('id'))
            .order_by('month')
        )

        months_in_order = [item['month'] for item in monthly_order_count]
        order_counts = [item['order_count'] for item in monthly_order_count]

        j = 0
        monthly_order_count_list = [0] * 12
        while j < len(monthly_order_count_list):
            try:
                if j == monthly_order_count[0]['month']:
                    monthly_order_count_list[j] = int(monthly_order_count[0]['order_count'])
            except Exception as e:
                print(e)
            j += 1

        months = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr',
                  5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug',
                  9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
                  }

        # -------------------- monthly orders count end ----------------

        # ----------------- Date filter ------------------------------

        if request.method == 'POST':
            try:
                date_from = request.POST.get('startDate')
                date_to = request.POST.get('endDate')
                orders = Order.objects.filter(created__range=(date_from, date_to))
            except:
                pass

        # ------------------ Date filter end -----------------

        # ----------------- yearly sales section ----------------

        yearly_sales = (
            Order.objects
            .annotate(year=ExtractYear('created'))
            .values('year')
            .annotate(year_total=Sum('order_total'))
            .order_by('year')
        )

        # calculate yearly orders

        yearly_orders = (
            Order.objects
            .annotate(year=ExtractYear('created'))
            .values('year')
            .annotate(total_orders=Count('id'))
            .order_by('year')
        )

        # Create lists to store the yearly data

        years = [0]  # To store the years
        yearly_sales_totals = [0]  # To store the yearly sales totals
        yearly_orders_counts = [0]  # To store the yearly order counts

        for sales_entry, orders_entry in zip(yearly_sales, yearly_orders):
            year = sales_entry['year']
            sales_total = sales_entry['year_total']
            orders_count = orders_entry['total_orders']

            years.append(year)
            yearly_sales_totals.append(sales_total)
            yearly_orders_counts.append(orders_count)

        # ----------------- yearly sales section ended ----------------

        context = {
            'orders': orders,

            'year': years,
            'sales': yearly_sales_totals,

            'months': months.values(),
            'order': order,
            'monthly_order_count_list': monthly_order_count_list,

            'order_count': order_count,
            'order_total': int(order_total),
            'today_count': today_count,
            'today_revenue': today_revenue,

            'payment_count': payment_count,
            'payment_method': payment_method,

        }
    except Exception as e:
        print(e)
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
    try:
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
                            product=product,
                            images=image,
                        )
                else:
                    for image in multiple_images:
                        photo = MultipleImages.objects.create(
                            product=product,
                            images=image,
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
    except Exception as e:
        print(e)

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
    try:
        if request.method == 'POST':

            product = Product()
            category = request.POST['selectOption']
            brand = request.POST['selectBrand']
            original_price = int(request.POST['originalPrice'])
            selling_price = int(request.POST['sellingPrice'])
            try:
                product_offer = int(request.POST['productOffer'])
                if int(product_offer) > 0:
                    product.offer = product_offer
                    off_amount = (original_price * product_offer) // 100
                    if (original_price - off_amount) < selling_price:
                        selling_price = original_price - off_amount
            except Exception as e:
                print(e)
            try:
                if category.offer > 0:
                    discount_amount = (selling_price * category.offer) // 100
                    if (original_price - discount_amount) < selling_price:
                        selling_price = original_price - discount_amount
            except Exception as e:
                print(e)

            # single image fetching
            try:
                product_image = request.FILES.get('image', None)
                if product_image:
                    product.product_image = product_image
            except Exception as e:
                print(e)

            product_name = request.POST['name']
            product.product_name = product_name
            product_slug = product_name.replace(" ", "-")
            product.category = Category.objects.get(id=category)
            product.brand = ProductBrand.objects.get(id=brand)
            product.original_price = original_price
            product.selling_price = selling_price
            product.product_description = request.POST['description']
            product.slug = product_slug
            product.save()

            # multiple image fetching
            try:
                multiple_images = request.FILES.getlist('multipleImage', None)
                if multiple_images:
                    for image in multiple_images:
                        photo = MultipleImages.objects.create(
                            product=product,
                            images=image,
                        )
            except Exception as e:
                print(e)

            messages.success(request, "Product Created")

            return redirect('admin_product')
    except Exception as e:
        messages.error(request, "Product Exist")
        print(e)

    return render(request, 'admin/admin_add_product.html', context)


# @cache_control(no_store=True, no_cache=True)
# @staff_member_required(login_url='admin_login')
# def admin_delete_product(request, id):
#     prod = Product.objects.get(id=id)
#     if prod.product_image:
#         if len(prod.product_image) != 0:
#             os.remove(prod.product_image.path)
#     prod.delete()
#     messages.success(request, "Product deleted successfully")
#
#     return redirect('admin_product')


# Product list and un list

@cache_control(no_store=True, no_cache=True)
@staff_member_required(login_url='admin_login')
def admin_delete_product(request, id):
    try:
        prod = Product.objects.get(id=id)
        if prod.is_available:
            prod.is_available = False
            messages.success(request, "Product unlisted")
        else:
            prod.is_available = True
            messages.success(request, "Product listed")
        prod.save()
    except Exception as e:
        print(e)
    return redirect('admin_product')



#   verified
@staff_member_required(login_url='admin_login')
def admin_product_variant(request, product_id):
    context = {}
    try:
        variant = ProductVariant.objects.filter(product=product_id)
        context = {
            'variants': variant,
            'product_id': product_id,
        }
        return render(request, 'admin/admin_variant_product.html', context)
    except Exception as e:
        print(e)
        return redirect('admin_product')


#   verified
@staff_member_required(login_url='admin_login')
@cache_control(no_store=True, no_cache=True)
def add_product_variant(request, product_id):
    context = {}
    try:
        product = Product.objects.get(id=product_id)
        product_variants = ProductVariant.objects.filter(product=product)
        sizes = ProductSize.objects.all().order_by('id')

        if request.method == 'POST':
            size_id = request.POST['selectSize']
            stock = request.POST['stock']
            productPrice = request.POST['productPrice']
            variant_size = ProductSize.objects.get(id=size_id)

            try:
                variant = ProductVariant.objects.get(product=product_id, product_size=variant_size)

                if variant:
                    print("existing variant")
                    variant.stock = variant.stock + int(stock)
            except:
                variant = ProductVariant.objects.create(
                    product=product,
                    product_size=variant_size,
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
    except Exception as e:
        print(e)
        return redirect('admin_product')


#   verified
@staff_member_required(login_url='admin_login')
@cache_control(no_store=True, no_cache=True)
def product_variant_update(request):
    try:
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
    except Exception as e:
        print(e)
        return redirect('admin_product')


# verified
@staff_member_required(login_url='admin_login')
@cache_control(no_store=True, no_cache=True)
def product_variant_control(request, variant_id):
    try:
        variant = ProductVariant.objects.get(id=variant_id)
        product_id = variant.product.id
        if variant.is_active:
            variant.is_active = False
        else:
            variant.is_active = True
        variant.save()
        return redirect('admin_product_variant', product_id)
    except Exception as e:
        print(e)
        return redirect('admin_product')



#   verified
@staff_member_required(login_url='admin_login')
@cache_control(no_store=True, no_cache=True)
def product_variant_delete(request, variant_id):
    try:
        if request.method == 'POST':
            variant = ProductVariant.objects.get(id=variant_id)
            product = variant.product
            if variant:
                variant.delete()
            return redirect('admin_product_variant', product.id)
    except Exception as e:
        print(e)
    return redirect('admin_dashboard')


# Product section end -------------------------------------------------


# admin user section --------------------------------------------------


# verified

@staff_member_required(login_url='admin_login')
def admin_users(request):
    context = {}
    try:
        users = CustomUser.objects.all()
        context = {
            'users': users,
        }
    except Exception as e:
        print(e)

    return render(request, 'admin/admin_users.html', context)


#   verified
@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def admin_user_manage(request, id):
    try:
        user = CustomUser.objects.get(id=id)
        if user.is_active:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
    except Exception as e:
        print(e)

    return redirect('admin_users')


# admin user section ended ------------------------------------------


# admin category section --------------------------------------------


#   verified
@staff_member_required(login_url='admin_login')
def admin_category(request):
    context = {}
    try:
        categories = Category.objects.all().order_by('id')
        context = {
            'categories': categories
        }
    except Exception as e:
        print(e)

    return render(request, 'admin/admin_category.html', context)


#   verified
@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def admin_add_category(request):
    try:
        if request.method == 'POST':
            category_name = request.POST['category_name']
            category_slug = category_name.replace("-", " ")
            exist_category = Category.objects.filter(category_name__iexact=category_name)
            if exist_category.exists():
                messages.error(request, "Category Exist")
                return redirect('admin_add_category')
            category = Category(
                category_name=category_name,
                category_description=request.POST['description'],
                slug=category_slug,
            )
            if request.FILES:
                category.category_image = request.FILES['image']

            if request.POST['category_offer']:
                category.offer = request.POST['category_offer']

            category.save()
            messages.success(request, "Category Added")
            return redirect('admin_category')
    except Exception as e:
        print(e)

    return render(request, 'admin/admin_add_category.html')


#   verify
@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def admin_edit_category(request, id):
    context = {}
    try:
        category = Category.objects.get(id=id)
        context = {
            'category': category,
        }
        if request.method == 'POST':
            if request.FILES:
                if category.category_image:
                    os.remove(category.category_image.path)
                category.category_image = request.FILES['image']
            category.category_name = request.POST['name']
            category.category_description = request.POST['description']
            if request.POST['category_offer']:
                category.offer = request.POST['category_offer']
            category.save()

            messages.success(request, "Category Updated")
            return redirect('admin_category')
        return render(request, 'admin/admin_edit_category.html', context)
    except Exception as e:
        print(e)
        return redirect('admin_category')


#  Logic for category deletion
#   verified
# @cache_control(no_cache=True, no_store=True)
# @staff_member_required(login_url='admin_login')
# def admin_delete_category(request, id):
#     try:
#         category = Category.objects.get(id=id)
#         if category.category_image:
#             os.remove(category.category_image.path)
#         category.delete()
#         messages.success(request, "Category Deleted")
#     except Exception as e:
#         print(e)
#
#     return redirect('admin_category')


#  Logic for category list and unlisted

#   verified
@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def admin_delete_category(request, id):
    try:
        category = Category.objects.get(id=id)
        if category.is_active:
            category.is_active = False
            messages.success(request, "Category unlisted")
        else:
            category.is_active = True
            messages.success(request, "Category listed")
    except Exception as e:
        print(e)

    return redirect('admin_category')


# admin category section end ---------------------------------------

# admin brand section  ---------------------------------------


# verified
@staff_member_required(login_url='admin_login')
def brand(request):
    context = {}
    try:
        brands = ProductBrand.objects.all()
        context = {
            'brands': brands,
        }
        return render(request, 'admin/admin_brand.html', context)
    except Exception as e:
        print(e)
        return redirect('admin_dashboard')


# verified
@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def admin_add_brand(request):
    try:
        if request.method == 'POST':
            brand_name = request.POST['brand_name']
            slug = brand_name.replace("-", " ")
            brand = ProductBrand(
                brand_name=brand_name,
                brand_description=request.POST['brand_description'],
                slug=slug,
            )
            if request.FILES:
                brand.brand_image = request.FILES['brand_image']
            brand.save()
            messages.success(request, "Brand added.")
            return redirect('admin_brand')
        return render(request, 'admin/admin_add_brand.html')
    except Exception as e:
        messages.error(request, "Provide the fields")
        print(e)
        return redirect('admin_add_brand')


# verified
@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def admin_edit_brand(request, id):
    context = {}
    try:
        brand = ProductBrand.objects.get(id=id)
        if request.method == 'POST':
            brand_name = request.POST['brand_name']
            brand.brand_name = brand_name
            brand.brand_description = request.POST['brand_description']
            slug = brand_name.replace("-", " ")
            brand.slug = slug
            if request.FILES:
                if brand.brand_image:
                    os.remove(brand.brand_image.path)
                brand.brand_image = request.FILES['brand_image']
            brand.save()
            messages.success(request, "Brand updated")
            return redirect('admin_brand')
        context = {
            'brand': brand,
        }
        return render(request, 'admin/admin_edit_brand.html', context)
    except Exception as e:
        print(e)
        return redirect('admin_brand')


#   verified
@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def admin_delete_brand(request, id):
    try:
        brand = ProductBrand.objects.get(id=id)
        if brand.brand_image:
            os.remove(brand.brand_image.path)
        brand.delete()
        messages.success(request, "Brand deleted")
        return redirect('admin_brand')
    except Exception as e:
        print(e)
    return redirect('admin_brand')


# admin brand section end ---------------------------------------

# coupon section start ----------------------------------------------

# verified
@staff_member_required(login_url='admin_login')
def admin_coupon_management(request):
    context = {}
    try:
        coupons = Coupons.objects.all().order_by('-id')
        context = {
            'coupons': coupons,
        }
    except Exception as e:
        print(e)
    return render(request, 'admin/admin_coupon.html', context)


#  verified
@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def add_coupon(request):
    try:
        if request.method == 'POST':
            coupon = Coupons.objects.create(
                description=request.POST['description'],
                coupon_code=request.POST['coupon_code'],
                coupon_title=request.POST['coupon_title'],
                valid_from=request.POST['valid_from'],
                valid_to=request.POST['valid_to'],
                minimum_order_amount=request.POST['minimum_amount'],
            )
            if request.POST['discount_amount']:
                coupon.discount_amount = request.POST['discount_amount']

            if request.POST['discount']:
                coupon.discount = request.POST['discount']
            if request.POST['quantity']:
                coupon.quantity = request.POST['quantity']

            coupon.save()
            messages.success(request, "Coupon created")
            return redirect('admin_coupon_management')
        return render(request, 'admin/admin_add_coupon.html')
    except Exception as e:
        print(e)
        return redirect('admin_coupon_management')


# verified
@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def edit_coupon(request, coupon_id):
    context = {}
    try:
        coupon = Coupons.objects.get(id=coupon_id)
        if request.method == 'POST':
            coupon.id = coupon_id
            coupon.description = request.POST['description']
            coupon.coupon_code = request.POST['coupon_code']
            coupon.coupon_title = request.POST['coupon_title']
            coupon.minimum_order_amount = request.POST['minimum_amount']

            if request.POST['valid_from']:
                coupon.valid_from = request.POST['valid_from']
            if request.POST['valid_to']:
                coupon.valid_to = request.POST['valid_to']

            if request.POST['discount_amount']:
                coupon.discount_amount = request.POST['discount_amount']

            if request.POST['discount']:
                coupon.discount = request.POST['discount']

            if request.POST['quantity']:
                coupon.quantity = request.POST['quantity']

            coupon.save()
            messages.success(request, "Coupon updated")
            return redirect('admin_coupon_management')

        context = {
            'coupon': coupon,
        }
        return render(request, 'admin/admin_edit_coupon.html', context)
    except Exception as e:
        print(e)
        return redirect('admin_coupon_management')


# verified
@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def delete_coupon(request, coupon_id):
    try:
        coupon = get_object_or_404(Coupons, id=coupon_id)
        if coupon:
            coupon.delete()
            messages.success(request, "Coupon deleted")
    except Exception as e:
        print(e)
        pass
    return redirect('admin_coupon_management')


@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def activate_coupon(requset, coupon_id):
    try:
        coupon = Coupons.objects.get(id=coupon_id)
        if coupon.active:
            coupon.active = False
            messages.success(requset, "Coupon deactivated")
        else:
            coupon.active = True
            messages.success(requset, "Coupon activated")
        coupon.save()
    except Exception as e:
        print(e)
    return redirect('admin_coupon_management')


# coupon section end ----------------------------------------------


# order management section ----------------------------------------

@staff_member_required(login_url='admin_login')
def order_management(request):
    context = {}
    try:
        orders = Order.objects.all().order_by('-order_id')
        context = {
            'orders': orders,
        }
    except Exception as e:
        print(e)
    return render(request, 'admin/admin_order_management.html', context)


#   verified
@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def order_update(request, order_id):
    context = {}
    try:
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
    except Exception as e:
        print(e)
        return redirect('admin_order_management')


@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def return_request(request, item_id):
    try:
        order_item = OrderProduct.objects.get(id=item_id)
        variant = order_item.variant
        order = order_item.order_id
        order_id = order.id
        coupon = order.coupon
        user = order.user
        deduct_discount = order.discount

        if order.total < 2500:  # delivery charge logic.
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

            refund_amount = (float(amount) + float(delivery_charge)) - float(
                deduct_discount)  # calculating refund amount.
            user.wallet = float(user.wallet) + float(refund_amount)
            order_item.save()
            variant.save()
            user.save()
            order.save()
        return redirect('order_update', order_id)
    except Exception as e:
        print(e)
        return redirect('admin_order_management')


# -------------------------- Banner Management --------------------------


@staff_member_required(login_url='admin_login')
def banner_management(request):
    context = {}
    try:
        banners = Banner.objects.all().order_by('id')
        context = {
            'banners': banners,
        }
    except Exception as e:
        print(e)
    return render(request, 'admin/admin_banner.html', context)


#   verified
@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def create_banner(request):
    try:
        if request.method == 'POST':
            banner = Banner()
            fields_to_update = ['section', 'identifier', 'description', 'offer', 'title', 'notes']
            for field_name in fields_to_update:
                setattr(banner, field_name, request.POST.get(field_name))
            if request.FILES:
                banner.image = request.FILES['image']
            banner.save()

            messages.success(request, "Banner created")
            return redirect('banner_management')
        return render(request, 'admin/admin_add_banner.html')
    except Exception as e:
        messages.error(request, "provide values")
        print(e)
        return redirect('banner_management')


#   verified
@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def update_banner(request, banner_id):
    context = {}
    try:
        banner = Banner.objects.get(id=banner_id)
        if request.method == 'POST':
            fields_to_update = ['section', 'identifier', 'description', 'offer', 'title', 'notes']

            for field_name in fields_to_update:
                setattr(banner, field_name, request.POST.get(field_name))

            if request.FILES:
                if banner.image:
                    os.remove(banner.image.path)
                banner.image = request.FILES.get('image')

            banner.save()
            messages.success(request, "Banner Updated")
            return redirect('banner_management')

        context = {
            'banner': banner,
        }
        return render(request, 'admin/admin_edit_banner.html', context)
    except Exception as e:
        messages.error(request, "Provide the details.")
        print(e)
        return redirect('banner_management')


#   verified
@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def delete_banner(request, banner_id):
    try:
        banner = Banner.objects.get(id=banner_id)
        banner.delete()
        messages.success(request, "Banner deleted.")
    except Exception as e:
        print(e)
    return redirect('banner_management')


@staff_member_required(login_url='admin_login')
def reports(request):
    context = {}
    try:
        variants = ProductVariant.objects.all()
        cancel_orders = OrderProduct.objects.filter(item_cancel=True)

        context = {
            'variants': variants,
            'cancel_orders': cancel_orders,
        }
    except Exception as e:
        print(e)

    return render(request, 'admin/admin_reports.html', context)


# -------------------------- Admin Logout --------------------------

@cache_control(no_cache=True, no_store=True)
@staff_member_required(login_url='admin_login')
def admin_logout(request):
    logout(request)
    request.session.flush()
    return redirect('admin_login')


def page_not_found(request):
    return render(request, 'error.html')
