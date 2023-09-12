from django.urls import path, include
from .import views
from user_app.models import *
from shop.models import *
from cart.models import *

urlpatterns = [
    path('', views.order , name="order"),
    path('order-confirmed/', views.order_confirmed , name="order_confirmed"),
    path('orders-view/', views.order_view, name="order_view"),
    path('order-cancelation/<int:order_id>/', views.order_cancel, name="order_cancel"),
    path('order-return/<int:order_id>/', views.order_return, name="order_return"),
    path('proceed-to-pay/', views.proceed_to_pay, name="proceed_to_pay"),
    path('order-success/', views.order_success, name="order_success"),
    path('pdf_view/<int:order_id>/', views.ViewPDF.as_view(), name="pdf_view"),
    path('pdf_download/<int:order_id>/', views.DownloadPDF.as_view(), name="pdf_download"),
]