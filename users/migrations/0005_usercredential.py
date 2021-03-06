# Generated by Django 3.2.5 on 2021-07-22 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_campus'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCredential',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(help_text='Enter the Student ID of the student', max_length=20, verbose_name='Student ID')),
                ('email', models.URLField(help_text='Enter the email address of the student', max_length=300, verbose_name='Email of Student')),
                ('campus', models.CharField(choices=[('MC', 'Main Campus'), ('CC', 'City Campus')], default='MC', help_text='Select the campus the student is on', max_length=20, verbose_name='Campus')),
            ],
            options={
                'verbose_name': 'User Credential',
                'verbose_name_plural': 'User Credentials',
            },
        ),
    ]
