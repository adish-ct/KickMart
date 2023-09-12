# Generated by Django 4.2.3 on 2023-08-16 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Return processing', 'Return processing'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled'), ('Order confirmed', 'Order confirmed'), ('Delivered', 'Delivered'), ('Out for delivery', 'Out for delivery'), ('Returned', 'Returned'), ('Return requested', 'Return requested')], default='Order confirmed', max_length=50),
        ),
    ]