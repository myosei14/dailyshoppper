# Generated by Django 4.0.6 on 2024-01-24 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0003_alter_customer_device'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='device',
            new_name='deviceId',
        ),
    ]
