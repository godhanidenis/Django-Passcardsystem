# Generated by Django 3.1.7 on 2021-03-27 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0035_auto_20210325_1805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resident',
            name='passcode',
            field=models.CharField(blank=True, default=4063, max_length=120, unique=True),
        ),
    ]
