# Generated by Django 5.2 on 2025-06-02 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehiculo', '0003_m_vehiculo_kilometraje_m_vehiculo_observaciones_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='m_vehiculo',
            name='color',
            field=models.CharField(max_length=30, null=True, verbose_name='Color'),
        ),
    ]
