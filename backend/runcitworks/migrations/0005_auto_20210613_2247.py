# Generated by Django 3.1.5 on 2021-06-13 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('runcitworks', '0004_auto_20210613_2221'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='sales_target',
            new_name='account',
        ),
    ]
