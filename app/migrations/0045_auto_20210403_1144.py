# Generated by Django 3.1.7 on 2021-04-03 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0044_auto_20210402_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resident',
            name='passcode',
            field=models.CharField(blank=True, default=2915, max_length=120, unique=True),
        ),
    ]
