# Generated by Django 5.1.4 on 2025-03-02 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_rename_status_client_verificaton_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='date',
            field=models.CharField(default='', max_length=100),
        ),
    ]
