from django.db import models

# Create your models here.
class m_cliente(models.Model):
    id_cliente = models.AutoField(primary_key = True, db_column='id_cliente')

    nombre = models.CharField(max_length=250, null=True, verbose_name="Nombre(s)")
    ap_01 = models.CharField(max_length=250, null=True, verbose_name="Apellidos")
    SEXO_CHOICES = [('', 'Selecciona'),('M', 'Masculino'),('F', 'Femenino'),]
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    email = models.CharField(max_length=250, null=True, verbose_name="Email")
    telefono = models.CharField(max_length=10, null=True, verbose_name="Telefono")
    direccion = models.CharField(max_length=250, null=True, verbose_name="Dirección")
    date_created = models.DateTimeField(auto_now=True, null=True, verbose_name="Creacion")

    class Meta:
        db_table = 'cliente'
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return '%s %s' % (self.nombre, self.ap_01)

