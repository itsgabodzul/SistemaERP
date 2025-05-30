# Generated by Django 5.2 on 2025-05-25 22:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0003_alter_m_orden_trabajo_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetalleServicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='servicios_asociados', to='ordenes.m_orden_trabajo')),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ordenes.m_servicio')),
            ],
        ),
        migrations.DeleteModel(
            name='DetalleServicioOrden',
        ),
    ]
