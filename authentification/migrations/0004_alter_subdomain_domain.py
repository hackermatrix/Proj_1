# Generated by Django 4.1.5 on 2023-04-28 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0003_subdomain'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subdomain',
            name='domain',
            field=models.CharField(max_length=100),
        ),
    ]