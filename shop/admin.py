from django.contrib import admin
from shop.models import *

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name', )}
    list_display = ('category_name', 'slug')


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('product_name', )}
    list_display = ('product_name', 'slug', 'product_image', 'category', 'selling_price')

class BrandAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('brand_name', )}
    list_display = ('brand_name', 'slug')

class VariantAdmin(admin.ModelAdmin):
    list_display = ('id', 'product',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating',)

class SizeAdmin(admin.ModelAdmin):
    list_display = ('id', 'size')


admin.site.register(Category, CategoryAdmin)
admin.site.register(ProductBrand, BrandAdmin)
admin.site.register(ProductSize, SizeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariant, VariantAdmin)
admin.site.register(MultipleImages)
admin.site.register(Review, ReviewAdmin)
