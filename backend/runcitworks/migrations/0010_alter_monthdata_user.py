# Generated by Django 3.2.8 on 2022-01-02 16:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('runcitworks', '0009_expense'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthdata',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, unique_for_date='month'),
        ),
    ]
