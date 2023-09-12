# Generated by Django 4.2.3 on 2023-09-08 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0018_alter_customuser_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='test')),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]