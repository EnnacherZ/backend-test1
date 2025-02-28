# Generated by Django 5.1.4 on 2025-02-24 15:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_alter_pantdetail_size_alter_shirtdetail_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductReviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_type', models.CharField(max_length=10)),
                ('product_id', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('review', models.CharField(max_length=150)),
                ('stars', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('date', models.DateTimeField()),
            ],
        ),
    ]
