# Generated by Django 4.1.5 on 2023-05-04 16:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0008_nucleiscan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nucleiscan',
            name='param',
        ),
    ]
