# Generated by Django 4.2.3 on 2023-08-30 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0022_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Delivered', 'Delivered'), ('Order confirmed', 'Order confirmed'), ('Cancelled', 'Cancelled'), ('Out for delivery', 'Out for delivery'), ('Return requested', 'Return requested'), ('Returned', 'Returned'), ('Shipped', 'Shipped'), ('Return processing', 'Return processing')], default='Order confirmed', max_length=50),
        ),
    ]
