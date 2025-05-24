from django.contrib import admin

# Register your models here.
from .models import m_empleado, m_rol

admin.site.register(m_empleado)
admin.site.register(m_rol)