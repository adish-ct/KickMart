# Generated by Django 4.2.3 on 2023-09-11 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0019_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='referral_code',
            field=models.CharField(blank=True, default='KickMartShoe', max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='referred_by',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]