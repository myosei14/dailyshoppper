# Generated by Django 4.0.6 on 2024-01-24 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0005_alter_customer_deviceid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='deviceId',
        ),
        migrations.AddField(
            model_name='accountinfo',
            name='deviceId',
            field=models.CharField(max_length=200, null=True, verbose_name='Device Id'),
        ),
    ]
