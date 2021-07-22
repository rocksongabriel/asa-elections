# Generated by Django 3.2.5 on 2021-07-21 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote_app', '0003_alter_candidate_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='no',
            field=models.PositiveIntegerField(default=0, verbose_name='Number of Nos'),
        ),
        migrations.AddField(
            model_name='candidate',
            name='yes',
            field=models.PositiveBigIntegerField(default=0, verbose_name='Number of Yes'),
        ),
    ]
