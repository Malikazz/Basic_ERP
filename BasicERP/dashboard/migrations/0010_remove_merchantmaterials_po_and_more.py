# Generated by Django 4.0.1 on 2022-04-11 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_merchantmaterials_archived'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='merchantmaterials',
            name='po',
        ),
        migrations.RemoveField(
            model_name='merchantmaterials',
            name='purchase_date',
        ),
        migrations.AddField(
            model_name='merchantmaterials',
            name='minimum_units_on_purchase',
            field=models.IntegerField(default=0),
        ),
    ]
