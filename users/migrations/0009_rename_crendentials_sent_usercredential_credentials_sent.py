# Generated by Django 3.2.5 on 2021-07-23 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20210723_1013'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usercredential',
            old_name='crendentials_sent',
            new_name='credentials_sent',
        ),
    ]
