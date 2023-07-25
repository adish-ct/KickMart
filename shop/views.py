from django.shortcuts import render, redirect
from .models import *
from django.db.models import QuerySet
from itertools import chain


# app : shop

# Create your views here.
def products(request):
    if 'email' in request.session:
        return redirect('admin_dashboard')
    category = Category.objects.all()
    all_brands = ProductBrand.objects.all()
    all_products = Product.objects.all()
    context = {
        'category': category,
        'products': all_products,
        'brands': all_brands,
    }
    return render(request, 'product/product.html', context)


def detail_view(request, product_id):
    all_products = Product.objects.all()
    product = Product.objects.filter(id=product_id)
    variant = ProductVariant.objects.filter(product_id=product_id)
    context = {
        'product': product,
        'variant': variant,
        'products': all_products,
    }

    return render(request, 'product/viewproduct.html', context)
