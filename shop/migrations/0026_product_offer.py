# Generated by Django 4.2.3 on 2023-08-30 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0025_category_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='offer',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]