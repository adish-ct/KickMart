# Generated by Django 4.2.3 on 2023-08-07 12:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_app', '0012_alter_useraddress_alternative_mobile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0021_alter_coupons_valid_from_alter_coupons_valid_to'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=200)),
                ('paid_amount', models.FloatField(blank=True)),
                ('order_note', models.CharField(blank=True, max_length=150)),
                ('total', models.FloatField()),
                ('order_total', models.FloatField()),
                ('discount', models.FloatField(blank=True, default=0)),
                ('tax', models.FloatField()),
                ('status', models.CharField(choices=[('Order confirmed', 'Order confirmed'), ('Delivered', 'Delivered'), ('Shipped', 'Shipped'), ('Cancelled', 'Cancelled'), ('Returned', 'Returned'), ('Out for delivery', 'Out for delivery')], default='Order confirmed', max_length=50)),
                ('ip', models.CharField(blank=True, null=True)),
                ('is_ordered', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_app.useraddress')),
            ],
        ),
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=200)),
                ('payment_method', models.CharField(max_length=100)),
                ('total_amount', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quandity', models.IntegerField(default=0)),
                ('product_price', models.FloatField()),
                ('ordered', models.BooleanField(default=False)),
                ('is_returned', models.BooleanField(default=False)),
                ('return_reason', models.TextField(blank=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('order_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.order')),
                ('payment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.payments')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.product')),
                ('variant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.productvariant')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.payments'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
