# Generated by Django 2.1.4 on 2020-03-12 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20200312_1700'),
    ]

    operations = [
        migrations.RenameField(
            model_name='articlepost',
            old_name='user',
            new_name='author',
        ),
    ]
