# Generated by Django 3.2.9 on 2022-01-17 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20220117_0827'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='init',
            field=models.BooleanField(default=True),
        ),
    ]
