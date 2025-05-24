from django.db import models
from apps.inventario.models import m_inventario
from apps.vehiculo.models import m_vehiculo
from apps.empleado.models import m_empleado


# Create your models here.
#Servicios
class m_servicio(models.Model):
    id_servicio = models.AutoField(primary_key=True, db_column='id_servicio')
    descripcion = models.CharField(max_length=250, verbose_name="Descripción del servicio")
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Costo del servicio")

    class Meta:
        db_table = 'servicios'
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"


#Ordenes de Trabajo
class m_orden_trabajo(models.Model):
    ESTADO_CHOICES = [
        ('P', 'Pendiente'),
        ('E', 'En proceso'),
        ('T', 'Terminado'),
        ('C', 'Cancelado'),
    ]

    id_orden = models.AutoField(primary_key=True, db_column='id_orden')
    id_vehiculo = models.ForeignKey(m_vehiculo, on_delete=models.PROTECT, verbose_name="Vehículo")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    entrega_estimada = models.DateTimeField(null=True, blank=True, verbose_name="Fecha estimada de entrega")
    servicio = models.ForeignKey(m_servicio, on_delete=models.PROTECT, verbose_name="Servicio solicitado")
    mecanico = models.ForeignKey(m_empleado, on_delete=models.SET_NULL, null=True, blank=True,
    verbose_name="Mecánico asignado")
    diagnostico = models.TextField(verbose_name="Diagnóstico inicial")
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='P', verbose_name="Estado de la orden")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Total")

    class Meta:
        db_table = 'ordenes_trabajo'
        verbose_name = "Orden de trabajo"
        verbose_name_plural = "Órdenes de trabajo"

    def __str__(self):
        return f"Orden #{self.id_orden} - {self.id_vehiculo}"

    def calcular_total(self):
        """Calcula el total sumando servicio y refacciones"""
        total_refacciones = sum(detalle.subtotal() for detalle in self.detallerefaccion_set.all())
        return self.servicio.costo + total_refacciones

    def save(self, *args, **kwargs):
        self.total = self.calcular_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.descripcion} - ${self.costo}"


#Para las refacciones
class m_refaccion(models.Model):
    orden = models.ForeignKey(m_orden_trabajo, on_delete=models.CASCADE)
    producto = models.ForeignKey(m_inventario, on_delete=models.PROTECT, verbose_name="Refacción utilizada")
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad")

    class Meta:
        db_table = 'detalle_refacciones'
        verbose_name = "Detalle de refacción"
        verbose_name_plural = "Detalles de refacciones"

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre_p} para OT#{self.orden.id_orden}"