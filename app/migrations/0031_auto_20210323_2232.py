# Generated by Django 3.1.7 on 2021-03-23 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0030_auto_20210323_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resident',
            name='passcode',
            field=models.CharField(blank=True, default=6804, max_length=120, unique=True),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='timedatefrom',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='timedateto',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
