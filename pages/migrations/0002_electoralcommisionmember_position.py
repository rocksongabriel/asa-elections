# Generated by Django 3.2.5 on 2021-07-22 00:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='electoralcommisionmember',
            name='position',
            field=models.CharField(default='', help_text='Enter the position held by this member', max_length=100, verbose_name='Position of Board Member'),
        ),
    ]
