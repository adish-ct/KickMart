# Generated by Django 4.2.3 on 2023-08-17 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0013_customuser_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='wallet',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]