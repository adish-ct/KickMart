from .models import * 


def category_link(request):
    categories = Category.objects.all()
    return dict(category_link=categories)


def product_link(request):
    products = Product.objects.all()
    return dict(products=products)