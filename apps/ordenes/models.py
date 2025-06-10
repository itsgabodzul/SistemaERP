from django.db import models
from django.utils import timezone
from apps.inventario.models import m_inventario, MovimientoInventario
from apps.vehiculo.models import m_vehiculo
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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
    fecha_creacion = models.DateField(auto_now_add=True, verbose_name="Fecha de creación")
    entrega_estimada = models.DateField(null=True, blank=True, verbose_name="Fecha estimada de entrega")
    mecanico = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
    verbose_name="Mecánico asignado")
    diagnostico = models.TextField(verbose_name="Diagnóstico inicial")
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='P', verbose_name="Estado de la orden")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Total")

    class Meta:
        db_table = 'ordenes_trabajo'
        verbose_name = "Orden"
        verbose_name_plural = "Órdenes de trabajo"
        constraints = [
            models.UniqueConstraint(
                fields=['id_vehiculo'],
                condition=models.Q(estado__in=['P', 'E']),
                name='unique_orden_activa_vehiculo'
            )
        ]
        permissions = [
            ("iniciar_orden", "Puede iniciar orden")
        ]

    def __str__(self):
        return f"Orden #{self.id_orden} - {self.id_vehiculo}"

    def clean(self):
        if self.estado in ['P', 'E'] and m_orden_trabajo.objects.filter(
            id_vehiculo=self.id_vehiculo,
            estado__in=['P', 'E']
        ).exclude(pk=self.pk).exists():
            orden_existente = m_orden_trabajo.objects.get(
                id_vehiculo=self.id_vehiculo,
                estado__in=['P', 'E']
            )
            raise ValidationError(
                f'¡Este vehículo ya tiene una orden activa (#{orden_existente.id_orden})!'
            )

    def calcular_total(self):
        """Calcula el total sin requerir que la orden esté guardada."""
        total_servicios = 0
        total_refacciones = 0
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
        if hasattr(self, '_refacciones_temporales'):
            total_refacciones += sum(
                detalle.subtotal()
                for detalle in self._refacciones_temporales
            )
        return total_servicios + total_refacciones

    def save(self, *args, **kwargs):
        self.full_clean()
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

    def clean(self):
        if not self.producto:
            return  # Seguridad

        # Cantidad actual registrada en la base de datos
        cantidad_actual = 0
        if self.pk:
            try:
                cantidad_actual = m_refaccion.objects.get(pk=self.pk).cantidad
            except m_refaccion.DoesNotExist:
                cantidad_actual = 0

        # Calcula el cambio neto de stock
        diferencia = self.cantidad - cantidad_actual

        if diferencia > 0:  # Solo validamos si se va a usar más
            if self.producto.stock == 0:
                raise ValidationError(
                    f'Stock insuficiente. No hay unidades de {self.producto.nombre_p}'
                )
            if self.producto.stock < diferencia:
                raise ValidationError(
                    f'Stock insuficiente. Solo hay {self.producto.stock} unidades de {self.producto.nombre_p}'
                )
            
    def save(self, *args, **kwargs):
        self.full_clean()
        is_new = not self.pk
        if is_new:
            if self.orden.pk:
                self.producto.stock -= self.cantidad
                self.producto.save()
                MovimientoInventario.objects.create(
                producto=self.producto,
                tipo='salida',
                cantidad=self.cantidad,
                fecha=timezone.now())
            else:
                if not hasattr(self.orden, '_refacciones_temporales'):
                    self.orden._refacciones_temporales = []
                self.orden._refacciones_temporales.append(self)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
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
    orden = models.ForeignKey(m_orden_trabajo, on_delete=models.CASCADE, related_name='servicios_asociados')
    servicio = models.ForeignKey(m_servicio, on_delete=models.PROTECT)

    class Meta:
        db_table = 'detalle_servicio'
        verbose_name = "Detalle de Servicio"
        verbose_name_plural = "Detalles de los servicios"

    def save(self, *args, **kwargs):
        is_new = not self.pk
        if is_new:
            if self.orden.pk:
                super().save(*args, **kwargs)
            else:
                if not hasattr(self.orden, '_servicios_temporales'):
                    self.orden._servicios_temporales = []
                self.orden._servicios_temporales.append(self)
        else:
            super().save(*args, **kwargs)

    def costo(self):
        return self.servicio.costo

    def __str__(self):
        return f"{self.servicio} (Orden #{self.orden.id_orden})"
