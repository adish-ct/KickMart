from django.urls import path, include
from .import views
from user_app.models import *
from shop.models import *
from cart.models import *

urlpatterns = [
    path('', views.order , name="order"),
    path('order-confirmed/', views.order_confirmed , name="order_confirmed"),
]