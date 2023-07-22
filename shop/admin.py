from django.contrib import admin
from shop.models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(ProductBrand)
admin.site.register(ProductSize)
admin.site.register(Product)
admin.site.register(ProductVariant)
