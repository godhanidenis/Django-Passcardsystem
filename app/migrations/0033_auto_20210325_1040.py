# Generated by Django 3.1.7 on 2021-03-25 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_auto_20210324_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='isEnable',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='visitor',
            name='isPermanent',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='resident',
            name='passcode',
            field=models.CharField(blank=True, default=8074, max_length=120, unique=True),
        ),
    ]
