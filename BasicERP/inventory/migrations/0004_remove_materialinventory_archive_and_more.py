# Generated by Django 4.0.1 on 2022-03-23 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_materialsonorder_units_on_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='materialinventory',
            name='archive',
        ),
        migrations.RemoveField(
            model_name='materialinventory',
            name='material_id',
        ),
        migrations.RemoveField(
            model_name='materialsonorder',
            name='material_id',
        ),
        migrations.AddField(
            model_name='material',
            name='material_id',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='inventory.materialinventory'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='materialsonorder',
            name='MaterialsOnOrder',
            field=models.ManyToManyField(to='inventory.MerchantMaterials'),
        ),
    ]
