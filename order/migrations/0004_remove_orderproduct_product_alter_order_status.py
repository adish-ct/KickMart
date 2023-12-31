# Generated by Django 4.2.3 on 2023-08-10 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_order_coupon_alter_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='product',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Delivered', 'Delivered'), ('Shipped', 'Shipped'), ('Order confirmed', 'Order confirmed'), ('Out for delivery', 'Out for delivery'), ('Cancelled', 'Cancelled'), ('Returned', 'Returned')], default='Order confirmed', max_length=50),
        ),
    ]
