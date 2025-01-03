# Generated by Django 5.1.4 on 2024-12-29 00:30

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_shoe_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='pant',
            name='image1',
            field=cloudinary.models.CloudinaryField(default='empty_q2cypk.png', max_length=255, verbose_name='Image1'),
        ),
        migrations.AddField(
            model_name='pant',
            name='image2',
            field=cloudinary.models.CloudinaryField(default='empty_q2cypk.png', max_length=255, verbose_name='Image2'),
        ),
        migrations.AddField(
            model_name='pant',
            name='image3',
            field=cloudinary.models.CloudinaryField(default='empty_q2cypk.png', max_length=255, verbose_name='Image3'),
        ),
        migrations.AddField(
            model_name='pant',
            name='image4',
            field=cloudinary.models.CloudinaryField(default='empty_q2cypk.png', max_length=255, verbose_name='Image4'),
        ),
        migrations.AddField(
            model_name='sandal',
            name='image1',
            field=cloudinary.models.CloudinaryField(default='empty_q2cypk.png', max_length=255, verbose_name='Image1'),
        ),
        migrations.AddField(
            model_name='sandal',
            name='image2',
            field=cloudinary.models.CloudinaryField(default='empty_q2cypk.png', max_length=255, verbose_name='Image2'),
        ),
        migrations.AddField(
            model_name='sandal',
            name='image3',
            field=cloudinary.models.CloudinaryField(default='empty_q2cypk.png', max_length=255, verbose_name='Image3'),
        ),
        migrations.AddField(
            model_name='sandal',
            name='image4',
            field=cloudinary.models.CloudinaryField(default='empty_q2cypk.png', max_length=255, verbose_name='Image4'),
        ),
        migrations.AddField(
            model_name='shirt',
            name='image1',
            field=cloudinary.models.CloudinaryField(default='empty_q2cypk.png', max_length=255, verbose_name='Image1'),
        ),
        migrations.AddField(
            model_name='shirt',
            name='image2',
            field=cloudinary.models.CloudinaryField(default='empty_q2cypk.png', max_length=255, verbose_name='Image2'),
        ),
        migrations.AddField(
            model_name='shirt',
            name='image3',
            field=cloudinary.models.CloudinaryField(default='empty_q2cypk.png', max_length=255, verbose_name='Image3'),
        ),
        migrations.AddField(
            model_name='shirt',
            name='image4',
            field=cloudinary.models.CloudinaryField(default='empty_q2cypk.png', max_length=255, verbose_name='Image4'),
        ),
        migrations.AlterField(
            model_name='pant',
            name='image',
            field=cloudinary.models.CloudinaryField(default='empty_q2cypk.png', max_length=255, verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='sandal',
            name='image',
            field=cloudinary.models.CloudinaryField(default='empty_q2cypk.png', max_length=255, verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='shirt',
            name='image',
            field=cloudinary.models.CloudinaryField(default='empty_q2cypk.png', max_length=255, verbose_name='Image'),
        ),
        migrations.AlterField(
            model_name='shirtdetail',
            name='size',
            field=models.PositiveIntegerField(),
        ),
    ]
