from django.urls import path
from cart import views

urlpatterns = [
    path('', views.cart, name="cart"),
    path('user-cart/', views.cart, name="user_cart"),
    path('add-cart/<int:product_id>/', views.add_cart, name="add_cart"),
    path('add-cart-quandity/<int:variant_id>/', views.add_cart_quandity, name="add_cart_quandity"),
    path('remove-cart/<int:variant_id>/', views.remove_cart, name="remove_cart"),
    path('delete-cart/<int:variant_id>/', views.delete_cart, name="delete_cart"),
 
]