from django.db import models
from shop.models import *
from user_app.models import *
# Create your models here.


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)  
    #user = onetoonefield()
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
    

class Checkout(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    tax = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0, null=True)
    coupon = models.ForeignKey(Coupons ,on_delete=models.SET_NULL, blank=True, null=True)
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, null=True, blank=True)
    payable_amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    payment = models.CharField(max_length=100, null=True, blank=True)
    wallet = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)


    class Meta:
        ordering = ['user']
        

    def __str__(self):
        return self.user.email



