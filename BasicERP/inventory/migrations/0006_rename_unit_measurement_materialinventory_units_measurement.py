# Generated by Django 4.0.1 on 2022-03-25 20:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_materialinventory_archive_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='materialinventory',
            old_name='unit_measurement',
            new_name='units_measurement',
        ),
    ]
