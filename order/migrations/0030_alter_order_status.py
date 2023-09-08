# Generated by Django 4.2.3 on 2023-09-08 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0029_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Return processing', 'Return processing'), ('Order confirmed', 'Order confirmed'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Out for delivery', 'Out for delivery'), ('Return requested', 'Return requested'), ('Cancelled', 'Cancelled'), ('Returned', 'Returned')], default='Order confirmed', max_length=50),
        ),
    ]
