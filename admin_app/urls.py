from django.urls import path
from admin_app import views


urlpatterns = [

    path('', views.admin_login, name="admin_login"),
    path('admin_dashboard/', views.admin_dashboard, name="admin_dashboard"),

    path('admin_product/', views.admin_product, name="admin_product"),
    path('admin_edit_product/<int:id>/', views.admin_edit_product, name="admin_edit_product"),
    path('admin_add_product/', views.admin_add_product, name="admin_add_product"),
    path('admin_delete_product/<int:id>', views.admin_delete_product, name="admin_delete_product"),

    path('admin-product-variant/<int:product_id>/', views.admin_product_variant, name="admin_product_variant"),
    path('product-variant-update/', views.product_variant_update, name="product_variant_update"),
    path('product-variant-control/<str:variant_id>/', views.product_variant_control, name="product_variant_control"),
    path('add-product-variant/<int:product_id>/', views.add_product_variant, name="add_product_variant"),
    path('product-variant-delete/<int:variant_id>/', views.product_variant_delete, name="product_variant_delete"),

    path('admin_users/', views.admin_users, name="admin_users"),
    path('admin_user_manage/<int:id>/', views.admin_user_manage, name="admin_user_manage"),

    path('admin-category/', views.admin_category, name="admin_category"),
    path('admin-add-category/', views.admin_add_category, name="admin_add_category"),
    path('admin-edit-category/<int:id>', views.admin_edit_category, name="admin_edit_category"),
    path('admin-delete-category/<int:id>', views.admin_delete_category, name="admin_delete_category"),

    path('admin-coupon-management', views.admin_coupon_management, name="admin_coupon_management"),
    path('add-coupon', views.add_coupon, name="add_coupon"),
    path('delete-coupon/<int:coupon_id>/', views.delete_coupon, name="delete_coupon"),
    path('edit-coupon/<int:coupon_id>/', views.edit_coupon, name="edit_coupon"),
    path('activate-coupon/<int:coupon_id>/', views.activate_coupon, name="activate_coupon"),

    path('admin-order-management/', views.order_management, name="admin_order_management"),
    path('order-update/<int:order_id>', views.order_update, name="order_update"),
    path('return-request/<int:item_id>/', views.return_request, name="return_request"),

    path('banner-management/', views.banner_management, name="banner_management"),
    path('create-banner/', views.create_banner, name="create_banner"),
    path('update-banner/<int:banner_id>/', views.update_banner, name="update_banner"),
    path('delete-banner/<int:banner_id>/', views.delete_banner, name="delete_banner"),

    path('reports/', views.reports, name="reports"),

    path('admin_logout/', views.admin_logout, name="admin_logout"),
]
