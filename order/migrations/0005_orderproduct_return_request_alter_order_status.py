# Generated by Django 4.2.3 on 2023-08-13 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_remove_orderproduct_product_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='return_request',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Return requested', 'Return requested'), ('Return processing', 'Return processing'), ('Cancelled', 'Cancelled'), ('Delivered', 'Delivered'), ('Shipped', 'Shipped'), ('Out for delivery', 'Out for delivery'), ('Returned', 'Returned'), ('Order confirmed', 'Order confirmed')], default='Order confirmed', max_length=50),
        ),
    ]
