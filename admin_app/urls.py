from django.urls import path
from admin_app import views

urlpatterns = [
    path('', views.admin_login, name="admin_login"),
    path('admin_dashboard/', views.admin_dashboard, name="admin_dashboard"),
    path('admin_product/', views.admin_product, name="admin_product"),
]