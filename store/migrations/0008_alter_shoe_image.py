# Generated by Django 5.1.4 on 2024-12-26 22:06

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_shoe_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoe',
            name='image',
            field=cloudinary.models.CloudinaryField(default='empty_q2cypk.png', max_length=255, verbose_name='Image'),
        ),
    ]