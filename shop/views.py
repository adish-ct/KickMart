from django.shortcuts import render
from .models import *
from django.db.models import QuerySet
from itertools import chain


# app : shop

# Create your views here.
def products(request):
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
    product = Product.objects.filter(id=product_id)
    variant = ProductVariant.objects.filter(product_id=product_id)
    context = {
        'product': product,
        'variant': variant,
    }

    return render(request, 'product/viewproduct.html', context)
