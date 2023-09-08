# Generated by Django 4.2.3 on 2023-09-03 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0024_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='item_cancel',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Return processing', 'Return processing'), ('Shipped', 'Shipped'), ('Out for delivery', 'Out for delivery'), ('Delivered', 'Delivered'), ('Order confirmed', 'Order confirmed'), ('Return requested', 'Return requested'), ('Cancelled', 'Cancelled'), ('Returned', 'Returned')], default='Order confirmed', max_length=50),
        ),
    ]
