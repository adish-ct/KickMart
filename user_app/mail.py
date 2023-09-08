# import pyotp
# from django.core.mail import send_mail
# import random
# from django.conf import settings
# from .models import *


# def send_otp_via_mail(email):
#     subject = f'Verify your account with KickMart'
#     otp = pyotp.TOTP(pyotp.random_base32(length=6))
#     otp_value = otp.now()
#     message = f'Use this as your OTP {otp_value} do not share with others'
#     email_from = settings.EMAIL_HOST
#     send_mail(subject, message, email_from, [email])
#     user = CustomUser.objects.get(email=email)
#     user.otp = otp
#     user.save()
#     return otp_value

#
#
# path('register/', views.register, name='register'),
#     path('verifyotp/<int:user_id>/', views.verify_otp, name='verifyotp'),
#     path('resend-otp/<int:user_id>/', views.resend_otp, name='resend_otp'),
#
#
#     path('login/',views.user_login,name="login"),
#     path('resetpass/<int:user_id>/', views.reset_password, name='resetpass'),
#     path('forgotpass/', views.forgot_password, name='forgotpass'),
#
#
#     path('logout/',views.user_logout,name="logout_user"),
