# Generated by Django 4.2.3 on 2023-07-29 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_remove_cartitem_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='quandity',
            new_name='quantity',
        ),
    ]