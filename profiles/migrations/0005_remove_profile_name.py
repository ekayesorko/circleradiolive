# Generated by Django 3.1.7 on 2021-05-13 20:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_profile_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='name',
        ),
    ]