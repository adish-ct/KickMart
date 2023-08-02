from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db.models import QuerySet, Q
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.http import HttpResponse
from shop.models import *
from django.contrib import messages



# app : shop

# Create your views here.
def products(request, category_slug=None):
    if 'email' in request.session:
        return redirect('admin_dashboard')
    
    categories = None
    all_products = None

    if category_slug !=None:
        category = Category.objects.get(slug=category_slug)
        all_products = Product.objects.filter(category=category, is_available=True)
        paginator = Paginator(all_products, 9)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = all_products.count()

    else:    
        all_products = Product.objects.all()
        paginator = Paginator(all_products, 9)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = all_products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'product/product.html', context)


def detail_view(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    current_user = request.user
    user_id = current_user.id
    product_id = single_product.id
    all_products = Product.objects.all()
    variant = ProductVariant.objects.filter(product=product_id)
    multiple_images = MultipleImages.objects.filter(product=product_id)
    context = {
        'product': single_product,
        'variant': variant,
        'products': all_products,
        'multiple_images': multiple_images,
        'user_id': user_id,
    }

    return render(request, 'product/viewproduct.html', context)



def search(request):
    if 'search' in request.GET:
        keyword = request.GET['search']
        if keyword:
            products = Product.objects.order_by('created_date').filter(
                Q(product_name__icontains = keyword) |
                Q(product_description__icontains = keyword) |
                Q(category__category_name__icontains = keyword)
            ).filter(is_available=True)
            products_count = products.count()
        else:
            return redirect('products')
        context = {
            'products': products,
            'product_count': products_count,
        }
    return render(request, 'product/product.html', context)



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
