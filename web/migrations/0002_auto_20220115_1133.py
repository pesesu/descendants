# Generated by Django 3.2.9 on 2022-01-15 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='first_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='surname',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
