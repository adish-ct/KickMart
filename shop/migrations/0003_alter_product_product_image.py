# Generated by Django 4.2.3 on 2023-07-24 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_productvariant_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image',
            field=models.ImageField(blank=True, upload_to='product_images/'),
        ),
    ]
