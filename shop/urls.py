from django.urls import path
from shop import views


# app : shop

urlpatterns = [
    path('', views.products, name="products"),
    path('detail_view/<str:product_id>/', views.detail_view, name="detail_view"),
]

