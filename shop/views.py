from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from shop.models import *
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import *
from order.models import *
from django.core.mail import send_mail
from django.conf import settings


# app : shop

# Create your views here.
def products(request, category_slug=None, categories=None, all_products=None):
    if 'email' in request.session:
        return redirect('admin_dashboard')
    context = {}
    try:
        brands, sizes = ProductBrand.objects.all(), ProductSize.objects.all().order_by('size')

        if category_slug is not None:
            category = Category.objects.get(slug=category_slug)
            all_products = Product.objects.filter(category=category, is_available=True)
        else:
            all_products = Product.objects.filter(is_available=True)
        paginator = Paginator(all_products, 9)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = all_products.count()

        try:
            if request.method == "POST":
                filter_products = Product.objects.all()
                try:
                    selected_category = request.POST.getlist('checkboxCategory')
                    selected_brand = request.POST.getlist('checkboxBrand')
                    selected_size = request.POST.getlist('checkboxSize')
                    selected_rating = request.POST.getlist('checkboxRating')

                    if selected_category:
                        filter_products = filter_products.filter(category__category_name__in=selected_category)
                    if selected_brand:
                        filter_products = filter_products.filter(brand__brand_name__in=selected_brand)
                    if selected_size:
                        product_variants = ProductVariant.objects.filter(product_size__id__in=selected_size)
                        filtered_products_id = filter_products.values_list('id', flat=True)
                        filter_variants = product_variants.filter(product__id__in=filtered_products_id)
                        filter_products = [variant.product for variant in filter_variants]
                    if selected_rating:
                        filter_products = filter_products.filter(rating__in=selected_rating)

                    minimum_price = request.POST['minPrice']
                    if not minimum_price:
                        minimum_price = 0
                    maximum_price = request.POST['maxPrice']
                    if not maximum_price:
                        maximum_price = 10000
                    if minimum_price and maximum_price:
                        filter_products = filter_products.filter(selling_price__gte=minimum_price,
                                                                 selling_price__lte=maximum_price)

                except Exception as e:
                    print(e)

                paginator = Paginator(filter_products, 9)
                page = request.GET.get('page')
                paged_products = paginator.get_page(page)
                try:
                    product_count = len(filter_products)
                except:
                    product_count = 0

        except Exception as e:
            print(e)

        context = {
            'products': paged_products,
            'product_count': product_count,
            'brands': brands,
            'sizes': sizes,
        }

    except Exception as e:
        print(e)
    return render(request, 'product/product.html', context)


def detail_view(request, category_slug, product_slug):
    rating = [1, 2, 3, 4, 5]
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        average_rating = Review.objects.filter(product=single_product).aggregate(avg_rating=Avg('rating'))
        rating_avg = average_rating['avg_rating']
        try:
            if rating_avg > 0:
                single_product.rating = rating_avg
                single_product.save()
        except Exception as e:
            print(e)
    except Exception as e:
        raise e

    reviews = Review.objects.filter(product=single_product)
    product_id = single_product.id
    variant = ProductVariant.objects.filter(product=product_id)
    multiple_images = MultipleImages.objects.filter(product=product_id).order_by('-id')[:4]

    context = {
        'product': single_product,
        'variant': variant,
        'products': Product.objects.all(),
        'multiple_images': multiple_images,
        'user_id': request.user.id,
        'reviews': reviews,
        'rating': rating,
        'reviews_count': reviews.count(),
        'avarage_rating': single_product.rating,
    }

    return render(request, 'product/viewproduct.html', context)


def search(request):
    context = {}
    if 'search' in request.GET:
        keyword = request.GET['search']
        if keyword:
            products = Product.objects.order_by('created_date').filter(
                Q(product_name__icontains=keyword) |
                Q(product_description__icontains=keyword) |
                Q(category__category_name__icontains=keyword)
            ).filter(is_available=True)
            products_count = products.count()
        else:
            return redirect('products')
        context = {
            'products': products,
            'product_count': products_count,
        }
    return render(request, 'product/product.html', context)


def get_names(request):
    search = request.GET.get('search')
    payload = []

    if search:
        products = Product.objects.filter(Q(product_name__istartswith=search) | Q(category__category_name__istartswith=search))
        for product in products:
            payload.append(product.product_name)

    return JsonResponse({
        'status': True,
        'payload': payload,
    })


def search_by_name(request):
    if 'search_by_name' in request.GET:
        keyword = request.GET['search_by_name']
        if keyword:
            products = Product.objects.order_by('created_date').filter(product_name__icontains=keyword)
            product_count = products.count()
        else:
            products = Product.objects.all()
            product_count = products.count()
        context = {
            'products': products,
            'product_count': product_count,
        }

    return render(request, 'product/product.html', context)


@cache_control(no_cache=True, no_store=True)
@login_required(login_url='user_login')
def review(request):
    my_user = request.user
    try:
        orders = OrderProduct.objects.filter(customer=my_user)
        order_items = []
        for i in orders:
            order_items.append(i.variant.product.id)
        if request.method == 'POST':
            product = Product.objects.get(id=request.POST['product'])
            category_slug = product.category.slug
            product_slug = product.slug
            if product.id in order_items:
                product_review = Review.objects.create(
                    user=my_user,
                    product=product,
                    rating=request.POST['rating'],
                    review=request.POST['review'],
                )
            else:
                messages.error(request, "You are not purchsed these item!")
    except Exception as e:
        print(e)

    return redirect(detail_view, category_slug, product_slug)


@cache_control(no_cache=True, no_store=True)
def contact(request):
    try:
        if request.method == 'GET':
            name = request.GET['name']
            email = request.GET['email']
            message = request.GET['message']
            head = 'ceetey1997@gmail.com'

            subject = f"Queries from {name} "
            message = f'email {email}\n messaage : {message}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [head, ]
            send_mail(subject, message, email_from, recipient_list)

            messages.success(request, "Message sent successfully")
            return redirect('contact')
    except Exception as e:
        print(e)
    return render(request, 'product/contact.html')


def for_help(request):
    return render(request, 'product/help.html')


def error_404(request, exception):
    return render(request, "error.html")
