# Generated by Django 5.0.1 on 2024-02-26 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_profile_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, default='profile/user-default.png', null=True, upload_to='profile/'),
        ),
    ]
