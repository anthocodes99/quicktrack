# Generated by Django 3.2.8 on 2021-11-29 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quicktrack', '0003_auto_20210626_1219'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]