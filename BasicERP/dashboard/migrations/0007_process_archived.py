# Generated by Django 4.0.1 on 2022-04-10 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_material_archived'),
    ]

    operations = [
        migrations.AddField(
            model_name='process',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]
