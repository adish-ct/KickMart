# Generated by Django 4.2.3 on 2023-08-28 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0017_alter_order_coupon_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Delivered', 'Delivered'), ('Return processing', 'Return processing'), ('Order confirmed', 'Order confirmed'), ('Returned', 'Returned'), ('Return requested', 'Return requested'), ('Shipped', 'Shipped'), ('Out for delivery', 'Out for delivery'), ('Cancelled', 'Cancelled')], default='Order confirmed', max_length=50),
        ),
    ]
