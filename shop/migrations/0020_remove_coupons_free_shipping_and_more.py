# Generated by Django 4.2.3 on 2023-08-02 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_alter_coupons_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupons',
            name='free_shipping',
        ),
        migrations.RemoveField(
            model_name='coupons',
            name='one_time_use_per_user',
        ),
    ]
