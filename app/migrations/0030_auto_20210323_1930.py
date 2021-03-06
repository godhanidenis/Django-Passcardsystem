# Generated by Django 3.1.7 on 2021-03-23 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_auto_20210323_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='Profiles/'),
        ),
        migrations.AlterField(
            model_name='resident',
            name='passcode',
            field=models.CharField(blank=True, default=6154, max_length=120, unique=True),
        ),
    ]
