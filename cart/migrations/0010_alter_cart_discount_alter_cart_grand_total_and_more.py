# Generated by Django 4.2.3 on 2023-08-05 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0009_cart_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='discount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='grand_total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='shipping',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='tax',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]