from django.core.mail import send_mail
from django.conf import settings


def send_otp(email, otp):
    subject = "Verify your account"
    message = f'Your OTP for account verification is {otp}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list)
    return True


def send_forgot_password_mail(email, token):
    subject = "Forgot password"
    message = f'Hi, click the link to reset your password http://127.0.0.1:8000/reset-password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list)
    return True
