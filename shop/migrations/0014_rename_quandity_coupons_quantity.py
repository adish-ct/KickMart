# Generated by Django 4.2.3 on 2023-08-02 04:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_coupons_coupon_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coupons',
            old_name='Quandity',
            new_name='Quantity',
        ),
    ]