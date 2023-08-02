from django.db import models
from shop.models import *
from user_app.models import CustomUser
# Create your models here.


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id



class CartItem(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True)
    single_product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    created_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['created_date']

    def sub_total(self):
        return self.product.product_price * self.quantity

    def __str__(self):
        return f"self.product.variant_name"
