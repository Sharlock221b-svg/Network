# Generated by Django 4.0.5 on 2022-07-13 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_following'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Posts',
            new_name='Post',
        ),
    ]