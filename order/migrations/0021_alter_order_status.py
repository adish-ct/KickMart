# Generated by Django 4.2.3 on 2023-08-30 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0020_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Cancelled', 'Cancelled'), ('Return processing', 'Return processing'), ('Delivered', 'Delivered'), ('Out for delivery', 'Out for delivery'), ('Return requested', 'Return requested'), ('Returned', 'Returned'), ('Shipped', 'Shipped'), ('Order confirmed', 'Order confirmed')], default='Order confirmed', max_length=50),
        ),
    ]
