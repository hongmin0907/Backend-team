# Generated by Django 2.1 on 2019-07-17 01:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stay', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='MaximumPersonnel',
            new_name='maximumPersonnel',
        ),
    ]
