# Generated by Django 4.2.3 on 2023-09-06 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0026_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Shipped', 'Shipped'), ('Cancelled', 'Cancelled'), ('Delivered', 'Delivered'), ('Return processing', 'Return processing'), ('Out for delivery', 'Out for delivery'), ('Return requested', 'Return requested'), ('Order confirmed', 'Order confirmed'), ('Returned', 'Returned')], default='Order confirmed', max_length=50),
        ),
    ]
