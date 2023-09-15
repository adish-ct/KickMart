from django.contrib import admin
from .models import *


# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order_id', 'created', 'status']


class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'payment_method', 'total_amount', 'status', 'is_paid', ]
    list_editable = ['payment_method', 'total_amount', 'is_paid', 'status', ]


admin.site.register(Payments, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
