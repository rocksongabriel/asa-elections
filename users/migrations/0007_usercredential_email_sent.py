# Generated by Django 3.2.5 on 2021-07-23 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_usercredential_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercredential',
            name='email_sent',
            field=models.BooleanField(default=False, verbose_name='Email Sent'),
        ),
    ]