from django import forms
import re
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from django.core.validators import validate_email
from .models import m_cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = m_cliente
        fields = ['nombre', 'ap_01', 'fecha_nacimiento', 'sexo', 'email', 'telefono', 'direccion'] #Datos del moedlo
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control casilla'}),
            'ap_01': forms.TextInput(attrs={'class': 'form-control casilla '}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date','class': 'form-control casilla'}),
            'sexo': forms.Select(attrs={'class': 'form-select casilla'}),
            'email': forms.EmailInput(attrs={'class': 'form-control casilla'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control casilla'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control casilla'}),
        } #Inputs del formulario


#Validaciones del formulario
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not nombre:
            raise forms.ValidationError('Este campo es obligatorio.')
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$', nombre):
            raise forms.ValidationError('No use números o símbolos (@, #, etc.).')
        return nombre

    def clean_ap_01(self):
        ap_01 = self.cleaned_data.get('ap_01', '').strip()
        if not ap_01:
            raise forms.ValidationError('Este campo es obligatorio.')
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$', ap_01):
            raise forms.ValidationError('No use números o símbolos (@, #, etc.).')
        return ap_01

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento', '')
        hoy = date.today()
        edad = relativedelta(hoy, fecha_nacimiento).years
        limite_antiguedad = hoy - timedelta(days=90*365)
        if fecha_nacimiento > hoy:
            raise forms.ValidationError('La fecha es incorrecta.')
        if edad < 18:
            raise forms.ValidationError('Debes tener al menos 18 años.')
        if fecha_nacimiento < limite_antiguedad:
            raise forms.ValidationError('Verifique el año ingresado.')
        return fecha_nacimiento

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion', '').strip()
        if not direccion:
            raise forms.ValidationError('Este campo es obligatorio.')
        return direccion

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '').strip()
        if not telefono.isdigit():
            raise forms.ValidationError('El teléfono debe contener solo números.')
        if len(telefono) != 10:
            raise forms.ValidationError('El teléfono debe contener exactamente 10 dígitos.')
        return telefono

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if not email:
            raise forms.ValidationError('El correo electrónico es obligatorio.')
        try:
            validate_email(email)
        except forms.ValidationError:
            raise forms.ValidationError('Ingresa un correo válido.')
        return email
