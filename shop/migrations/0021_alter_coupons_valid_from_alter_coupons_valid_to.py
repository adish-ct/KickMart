# Generated by Django 4.2.3 on 2023-08-02 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0020_remove_coupons_free_shipping_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupons',
            name='valid_from',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='coupons',
            name='valid_to',
            field=models.DateField(null=True),
        ),
    ]