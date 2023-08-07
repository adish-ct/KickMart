# from django.db import models
# from user_app.models import *
# from shop.models import *
# from cart.models import *

# # Create your models here.

# class Order(models.Model):
#     STATUS = {
#         ('Order confirmed', 'Order confirmed'),
#         ('Shipped', 'Shipped'),
#         ('Out for delivery', 'Out for delivery'),
#         ('Delivered', 'Delivered'),
#         ('Cancelled', 'Cancelled'),
#         ('Returned', 'Returned'),
#     }
#     user = models.ForeignKey(on_delete=models.CASCADE, null=True, blank=True)
#     address = models.ForeignKey(on_delete=models.SET_NULL, null=True, blank=True)
#     order_id = models.CharField(max_length=200, blank=True)
#     total_amount = models.FloatField(blank=True)
#     discount = models.FloatField(default=0, blank=True)
#     paid_amount = models.FloatField(blank=True)

