from django.contrib import admin
from .models import *

# Register your models here.

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'payment_method', 'total_amount', 'status', 'is_paid',]
    list_editable = ['payment_method', 'total_amount', 'is_paid', 'status',]

admin.site.register(Payments, PaymentAdmin)
admin.site.register(Order)
admin.site.register(OrderProduct)
