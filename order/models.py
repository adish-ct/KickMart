from django.db import models
from user_app.models import *
from shop.models import *
from cart.models import *

# Create your models here.


class Payments(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=200)
    payment_method = models.CharField(max_length=100)
    total_amount = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.payment_id
     



class Order(models.Model):
    STATUS = {
        ('Order confirmed', 'Order confirmed'),
        ('Shipped', 'Shipped'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Return requested', 'Return requested'),
        ('Return processing', 'Return processing'),
        ('Returned', 'Returned'),
    }
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    payment = models.ForeignKey(Payments, on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey(UserAddress, on_delete=models.SET_NULL, null=True, blank=True)
    order_id = models.CharField(max_length=200, blank=True)
    paid_amount = models.FloatField(blank=True)
    order_note = models.CharField(max_length=150, blank=True)
    total = models.FloatField()
    order_total = models.FloatField()
    discount = models.FloatField(default=0, blank=True)
    wallet_amount = models.FloatField(default=0, blank=True, null=True)
    tax = models.FloatField()
    status = models.CharField(max_length=50, choices=STATUS, default="Order confirmed")
    ip = models.CharField(null=True, blank=True)
    is_ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    coupon = models.ForeignKey(Coupons, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.order_id
    

class OrderProduct(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payments, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True)
    quandity = models.IntegerField(default=0)
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    return_request = models.BooleanField(default=False)
    return_accept = models.BooleanField(default=False)
    is_returned = models.BooleanField(default=False)
    return_reason = models.TextField(blank=True)
    item_cancel = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return f"{self.customer.email} - {self.variant.product.product_name}" 
    
