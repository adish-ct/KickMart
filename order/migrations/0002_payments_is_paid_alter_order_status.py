# Generated by Django 4.2.3 on 2023-08-08 04:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payments',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Out for delivery', 'Out for delivery'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Order confirmed', 'Order confirmed'), ('Cancelled', 'Cancelled'), ('Returned', 'Returned')], default='Order confirmed', max_length=50),
        ),
    ]