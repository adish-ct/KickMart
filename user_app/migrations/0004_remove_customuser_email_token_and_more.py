# Generated by Django 4.2.3 on 2023-07-24 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0003_customuser_forgot_password_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='email_token',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='forgot_password_token',
        ),
        migrations.AddField(
            model_name='customuser',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
