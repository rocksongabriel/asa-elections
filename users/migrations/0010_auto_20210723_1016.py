# Generated by Django 3.2.5 on 2021-07-23 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_rename_crendentials_sent_usercredential_credentials_sent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercredential',
            name='credentials_sent',
        ),
        migrations.AddField(
            model_name='user',
            name='credentials_sent',
            field=models.BooleanField(default=False, verbose_name='Credentials Sent'),
        ),
    ]
