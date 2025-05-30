# Generated by Django 5.2 on 2025-05-17 01:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id_categoria', models.AutoField(db_column='id_categoria', primary_key=True, serialize=False)),
                ('categoria', models.CharField(max_length=250, unique=True, verbose_name='Categoría')),
            ],
            options={
                'verbose_name': 'Categoría',
                'verbose_name_plural': 'Categorías',
                'db_table': 'categorias',
            },
        ),
        migrations.CreateModel(
            name='m_inventario',
            fields=[
                ('id_producto', models.AutoField(db_column='id_producto', primary_key=True, serialize=False)),
                ('nombre_p', models.CharField(max_length=250, null=True, verbose_name='Producto')),
                ('descripcion', models.CharField(max_length=250, null=True, verbose_name='Descripción')),
                ('stock', models.IntegerField(null=True, verbose_name='Stock')),
                ('precio', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Precio')),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventario.categoria', verbose_name='Categoría')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'db_table': 'inventario',
            },
        ),
    ]
