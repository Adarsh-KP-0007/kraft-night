# Generated by Django 4.2.6 on 2024-04-20 21:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0002_alter_user_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='lifestyle',
        ),
        migrations.RemoveField(
            model_name='user',
            name='politics',
        ),
        migrations.RemoveField(
            model_name='user',
            name='world',
        ),
    ]