from django.db import models
from apps.cliente.models import m_cliente


# Create your models here.
class m_vehiculo(models.Model):
    # Primary Key
    id_vehiculo = models.AutoField(primary_key=True, db_column='id_vehiculo')

    # Campos de la tabla
    marca = models.CharField(max_length=50, null=True, verbose_name="Marca")
    modelo = models.CharField(max_length=50, null=True, verbose_name="Modelo")
    anio = models.PositiveIntegerField(null=True, verbose_name="Año")
    color = models.CharField(max_length=30, null=True, verbose_name="Color")
    kilometraje = models.PositiveIntegerField(null=True, verbose_name="Kilometraje")
    TRANSMISION_CHOICES = [('', 'Selecciona una opción'),('Manual', 'Manual'),('Automatica', 'Automática'),]
    transmision = models.CharField(max_length=10, null=True, choices=TRANSMISION_CHOICES)
    numero_serie = models.CharField(max_length=100, unique=True, verbose_name="Número de Serie")
    placas = models.CharField(max_length=20, unique=True, verbose_name="Placas")
    
    cliente = models.ForeignKey(m_cliente, on_delete=models.CASCADE, related_name='vehiculos', verbose_name="Cliente")
    observaciones = models.TextField(null=True, verbose_name="Observaciones")

    date_created = models.DateTimeField(auto_now=True, null=True, verbose_name="Creación")

    class Meta:
        # Tabla en la base de datos
        db_table = 'vehiculo'
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"

    def __str__(self):
        return f'{self.marca} {self.modelo}'