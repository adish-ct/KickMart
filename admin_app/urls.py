from django.urls import path
from admin_app import views

urlpatterns = [
    path('', views.admin_login, name="admin_login"),
    path('admin_dashboard/', views.admin_dashboard, name="admin_dashboard"),
    path('admin_product/', views.admin_product, name="admin_product"),
    path('admin_product_variant/<str:id>/', views.admin_product_variant, name="admin_product_variant"),
    path('admin_users/', views.admin_users, name="admin_users"),
    path('admin_logout/', views.admin_logout, name="admin_logout"),
]