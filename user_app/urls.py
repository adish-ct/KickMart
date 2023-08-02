from django.urls import path
from user_app import views

urlpatterns = [
    path('', views.index, name="index"),
    path('user_signup/', views.user_signup, name="user_signup"),
    path('otp_verification/<int:user_id>/', views.otp_verification, name="otp_verification"),
    path('regenerate-otp/<int:id>/', views.regenerate_otp, name="regenerate_otp"),
    path('user_login/', views.user_login, name="user_login"),
    path('user_logout/', views.user_logout, name="user_logout"),
    path('user-profile/<int:user_id>', views.user_profile, name="user_profile"),
    path('address-book/<int:user_id>', views.address_book, name="address_book"),
    path('add-address/<int:user_id>', views.add_address, name="add_address"),
    path('delete-address/<int:address_id>', views.delete_address, name="delete_address"),
]