from django.urls import path
from shop import views


# app : shop

urlpatterns = [
    path('', views.products, name="products"),
    path('category/<slug:category_slug>/', views.products, name="products_by_category"),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.detail_view, name="detail_view"),
    path('search/', views.search, name="search"),
    path('search-by-name/', views.search_by_name, name="search_by_name"),
]

