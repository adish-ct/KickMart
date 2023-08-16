from django.urls import path, include
from .import views
from user_app.models import *
from shop.models import *
from cart.models import *

urlpatterns = [
    path('', views.order , name="order"),
    path('order-confirmed/', views.order_confirmed , name="order_confirmed"),
    path('orders-view/', views.order_view, name="order_view"),
    path('orders-details/<int:order_id>/', views.order_details, name="order_details"),
    path('order-cancelation/<int:order_id>/', views.order_cancel, name="order_cancel"),
    path('order-return/<int:order_id>/', views.order_return, name="order_return"),
]