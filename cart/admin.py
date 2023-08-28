from django.contrib import admin
from .models import *

class CartAdmin(admin.ModelAdmin):
    list_display = ['cart_id', 'date_added']


class CartItemAdmin(admin.ModelAdmin):
    list_display = ['customer', 'product', 'single_product', 'cart', 'quantity', 'active']

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
admin.site.register(Checkout)