# Generated by Django 4.2.3 on 2023-08-02 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_alter_coupons_discount_alter_coupons_discount_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupons',
            name='active',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='coupons',
            name='free_shipping',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='coupons',
            name='one_time_use_per_user',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
