# Generated by Django 4.0.3 on 2022-04-07 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_friends_alter_profile_image_friendrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='mobile_number',
            field=models.CharField(default='', max_length=10),
        ),
    ]