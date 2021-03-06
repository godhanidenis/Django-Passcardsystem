# Generated by Django 3.1.7 on 2021-04-02 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0042_auto_20210331_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resident',
            name='passcode',
            field=models.CharField(blank=True, default=8204, max_length=120, unique=True),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='profile_image',
            field=models.ImageField(blank=True, default='/media/profiles/profile-placeholder.png', null=True, upload_to='profiles'),
        ),
    ]
