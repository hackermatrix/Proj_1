# Generated by Django 4.1.5 on 2023-05-04 05:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0007_zapscan'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nucleiscan',
            fields=[
                ('endpoint_id', models.AutoField(primary_key=True, serialize=False)),
                ('endpoint_name', models.CharField(max_length=100)),
                ('severity', models.CharField(max_length=50)),
                ('vulnerability', models.CharField(max_length=100)),
                ('vulnerable_url', models.CharField(max_length=100)),
                ('param', models.JSONField(max_length=30)),
                ('subdomain_name', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
