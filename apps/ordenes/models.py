from django.db import models
from django.utils import timezone
from apps.inventario.models import m_inventario, MovimientoInventario
from apps.vehiculo.models import m_vehiculo
from apps.empleado.models import m_empleado


# Create your models here.
#Servicios
class m_servicio(models.Model):
    id_servicio = models.AutoField(primary_key=True, db_column='id_servicio')
    servicio = models.CharField(max_length=250,  null=True, verbose_name="Nombre del servicio")
    descripcion = models.CharField(max_length=250, verbose_name="Descripción del servicio")
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Costo del servicio")

    class Meta:
        db_table = 'servicios'
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"

    def __str__(self):
        return f"{self.servicio}"


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
    mecanico = models.ForeignKey(m_empleado, on_delete=models.SET_NULL, null=True, blank=True,
    verbose_name="Mecánico asignado")
    diagnostico = models.TextField(verbose_name="Diagnóstico inicial")
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='P', verbose_name="Estado de la orden")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Total")

    class Meta:
        db_table = 'ordenes_trabajo'
        verbose_name = "Orden"
        verbose_name_plural = "Órdenes de trabajo"

    def __str__(self):
        return f"Orden #{self.id_orden} - {self.id_vehiculo}"

    def calcular_total(self):
        """Calcula el total sin requerir que la orden esté guardada."""
        total_servicios = 0
        total_refacciones = 0
        # Si la orden ya está guardada, suma las refacciones existentes
        if self.pk:
            total_servicios = sum(
            detalle.costo()
            for detalle in self.servicios_asociados.all()
            )
            total_refacciones = sum(
                detalle.subtotal() 
                for detalle in self.refacciones.all()
            )

        if hasattr(self, '_servicios_temporales'):
            total_servicios += sum(
                detalle.costo()
                for detalle in self._servicios_temporales
            )
        # Si hay refacciones en memoria (no guardadas), súmalas también
        if hasattr(self, '_refacciones_temporales'):
            total_refacciones += sum(
                detalle.subtotal()
                for detalle in self._refacciones_temporales
            )
        return total_servicios + total_refacciones

    def save(self, *args, **kwargs):
        # Calcula el total ANTES de guardar (evitando el doble guardado)
        self.total = self.calcular_total()
        super().save(*args, **kwargs)



#Para las refacciones
class m_refaccion(models.Model):
    orden = models.ForeignKey(m_orden_trabajo, on_delete=models.CASCADE, related_name='refacciones')
    producto = models.ForeignKey(m_inventario, on_delete=models.PROTECT, verbose_name="Refacción utilizada")
    cantidad = models.PositiveIntegerField(default=1, verbose_name="Cantidad")

    class Meta:
        db_table = 'detalle_refacciones'
        verbose_name = "Detalle de refacción"
        verbose_name_plural = "Detalles de refacciones"

    def save(self, *args, **kwargs):
        is_new = not self.pk  # ¿Es una nueva refacción?
        if is_new:
            # Restar del inventario solo si la orden está guardada
            if self.orden.pk:
                self.producto.stock -= self.cantidad
                self.producto.save()
                MovimientoInventario.objects.create(
                producto=self.producto,
                tipo='salida',
                cantidad=self.cantidad,
                fecha=timezone.now())
            else:
                # Si la orden no está guardada, guarda la refacción en memoria
                if not hasattr(self.orden, '_refacciones_temporales'):
                    self.orden._refacciones_temporales = []
                self.orden._refacciones_temporales.append(self)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Si se elimina una refacción, regresa el stock al inventario
        producto = self.producto
        producto.stock += self.cantidad
        producto.save()
        MovimientoInventario.objects.create(
        producto=producto,
        tipo='entrada',
        cantidad=self.cantidad,
        fecha=timezone.now())
        super().delete(*args, **kwargs)

    def subtotal(self):
        return self.producto.precio * self.cantidad

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre_p} para OT#{self.orden.id_orden}"

class DetalleServicio(models.Model):
    orden = models.ForeignKey('m_orden_trabajo', on_delete=models.CASCADE, related_name='servicios_asociados')
    servicio = models.ForeignKey('m_servicio', on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        is_new = not self.pk
        if is_new:
            if self.orden.pk:  # Si la orden ya está guardada
                super().save(*args, **kwargs)  # Guarda primero el detalle
            else:
                # Si la orden no está guardada, guarda en memoria
                if not hasattr(self.orden, '_servicios_temporales'):
                    self.orden._servicios_temporales = []
                self.orden._servicios_temporales.append(self)
        else:
            super().save(*args, **kwargs)

    def costo(self):
        return self.servicio.costo

    def __str__(self):
        return f"{self.servicio.nombre} (Orden #{self.orden.id_orden})"
