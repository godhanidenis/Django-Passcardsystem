# Generated by Django 3.1.7 on 2021-03-24 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_auto_20210323_2232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resident',
            name='passcode',
            field=models.CharField(blank=True, default=3982, max_length=120, unique=True),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='profiles'),
        ),
    ]
