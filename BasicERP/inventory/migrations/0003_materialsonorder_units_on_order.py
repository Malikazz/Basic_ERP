# Generated by Django 4.0.1 on 2022-03-17 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_remove_material_status_remove_merchant_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='materialsonorder',
            name='units_on_order',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]
