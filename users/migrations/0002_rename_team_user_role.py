# Generated by Django 4.1 on 2022-08-08 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='team',
            new_name='role',
        ),
    ]
