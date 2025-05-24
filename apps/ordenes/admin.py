from django.contrib import admin

# Register your models here.
from .models import m_orden_trabajo, m_servicio, m_refaccion

admin.site.register(m_servicio)
admin.site.register(m_orden_trabajo)
admin.site.register(m_refaccion)