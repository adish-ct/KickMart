# Generated by Django 4.2.3 on 2023-09-08 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0017_alter_customuser_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='image',
            field=models.ImageField(blank=True, default="{% static 'img/none_user.jpg' %}", null=True, upload_to='profile_images'),
        ),
    ]