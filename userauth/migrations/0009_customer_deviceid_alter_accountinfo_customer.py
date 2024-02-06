# Generated by Django 4.0.6 on 2024-01-26 01:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0008_alter_accountinfo_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='deviceId',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Device Id'),
        ),
        migrations.AlterField(
            model_name='accountinfo',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
