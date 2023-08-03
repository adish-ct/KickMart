from .models import * 

# app : shop

def category_link(request):
    categories = Category.objects.all().order_by('id')
    return dict(category_link=categories)


def product_link(request):
    products = Product.objects.all().order_by('id')
    return dict(products=products)


def brand_link(requset):
    brands = ProductBrand.objects.all().order_by('id')
    return dict(brands=brands)