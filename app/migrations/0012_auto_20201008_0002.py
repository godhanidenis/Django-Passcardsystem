# Generated by Django 3.1.1 on 2020-10-07 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20201007_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resident',
            name='passcode',
            field=models.CharField(blank=True, default=9705, max_length=120, unique=True),
        ),
    ]
