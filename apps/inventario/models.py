from django.db import models
from django.utils import timezone

# Create your models here.
class m_inventario(models.Model):
    id_producto = models.AutoField(primary_key = True, db_column='id_producto')

    #Campos
    nombre_p = models.CharField(max_length=250, null=True, unique=True, verbose_name="Producto")
    descripcion = models.CharField(max_length=250, null=True, verbose_name="Descripción")
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True, verbose_name="Categoría")
    stock = models.IntegerField(null=True, verbose_name="Stock")
    precio = models.DecimalField(max_digits=10,  decimal_places=2,  default=0.00, verbose_name="Precio")
    class Meta:
    #Tabla en postgrest
        db_table = 'inventario'
        verbose_name = "Producto"
        verbose_name_plural = "Productos"


    #Como se muestra en el admin
    def __str__(self):
        return self.nombre_p


class Categoria(models.Model):
    id_categoria = models.AutoField(primary_key = True, db_column='id_categoria')

    categoria = models.CharField(max_length=250, unique=True, verbose_name="Categoría",)

    class Meta:
        db_table = 'categorias'
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
    
    def __str__(self):
        return self.categoria

#Registro de Inventarios
class MovimientoInventario(models.Model):
    TIPO_MOVIMIENTO = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
    ]

    producto = models.ForeignKey('m_inventario', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_MOVIMIENTO)
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.tipo} - {self.producto.nombre} ({self.cantidad})'
