# Generated by Django 5.2 on 2025-05-11 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0003_alter_m_cliente_options_alter_m_cliente_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='m_cliente',
            name='direccion',
            field=models.CharField(max_length=250, null=True, verbose_name='direccion'),
        ),
        migrations.AddField(
            model_name='m_cliente',
            name='email',
            field=models.CharField(max_length=250, null=True, verbose_name='Email'),
        ),
        migrations.AddField(
            model_name='m_cliente',
            name='telefono',
            field=models.CharField(max_length=10, null=True, verbose_name='Telefono'),
        ),
    ]
