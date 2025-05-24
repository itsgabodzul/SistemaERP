from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.
class m_rol(models.Model):
    id_rol = models.AutoField(primary_key=True, db_column='id_rol')
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Rol")

    class Meta:
        db_table = 'rol'
        verbose_name = "Rol"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.nombre


class m_empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True, db_column='id_empleado')

    nombre = models.CharField(max_length=250, null=True, verbose_name="Nombre(s)")
    apellidos = models.CharField(max_length=250, null=True, verbose_name="Apellidos")
    SEXO_CHOICES = [('', 'Selecciona'), ('M', 'Masculino'), ('F', 'Femenino')]
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    correo = models.EmailField(max_length=250, null=True, verbose_name="Correo Electrónico")
    contrasenia = models.CharField(max_length=128, verbose_name="Contraseña")
    rol = models.ForeignKey(m_rol, on_delete=models.SET_NULL, null=True, verbose_name="Rol")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    date_created = models.DateTimeField(auto_now=True, null=True, verbose_name="Fecha de creación")

    class Meta:
        db_table = 'empleado'
        verbose_name = "Empleado"
        verbose_name_plural = "Empleados"

    def __str__(self):
        return f'{self.nombre} {self.apellidos}'

    def set_password(self, raw_password):
        self.contrasenia = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.contrasenia)
