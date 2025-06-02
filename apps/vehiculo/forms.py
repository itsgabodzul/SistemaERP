from django import forms
import re
from datetime import date, timedelta, datetime
from .models import m_vehiculo
from dal import autocomplete


class VehiculoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['cliente'].empty_label = "Selecciona un cliente"

    class Meta:
        model = m_vehiculo
        fields = [
            'marca', 'modelo', 'anio', 'color', 'kilometraje', 'transmision',
            'numero_serie', 'placas', 'observaciones', 'cliente'
        ]
        widgets = {
            'marca': forms.Select(attrs={'id': 'id_marca', 'class': 'form-control casilla'}),
            'modelo': forms.Select(attrs={'id': 'id_modelo', 'class': 'form-control casilla'}),
            'anio': forms.NumberInput(attrs={'class': 'form-control casilla'}),
            'color': forms.TextInput(attrs={'class': 'form-control casilla'}),
            'kilometraje': forms.NumberInput(attrs={'class': 'form-control casilla'}),
            'transmision': forms.Select(attrs={'class': 'form-control casilla'}),
            'numero_serie': forms.TextInput(attrs={'class': 'form-control casilla'}),
            'placas': forms.TextInput(attrs={'class': 'form-control casilla'}),
            'observaciones': forms.TextInput(attrs={'class': 'form-control casilla'}),
            # 'cliente': forms.Select(attrs={'class': 'form-select casilla'}),
            'cliente': autocomplete.ModelSelect2(url='cliente-autocomplete', attrs={'class': 'form-select casilla select2-autocomplete prueba'}),
        }

    # Validaciones personalizadas
    def clean_marca(self):
        marca = self.cleaned_data.get('marca', '').strip()
        if not marca:
            raise forms.ValidationError('Este campo es obligatorio.')
        return marca

    def clean_modelo(self):
        modelo = self.cleaned_data.get('modelo', '').strip()
        if not modelo:
            raise forms.ValidationError('Este campo es obligatorio.')
        return modelo

    def clean_color(self):
        color = self.cleaned_data.get('color', '').strip()
        if not color:
            raise forms.ValidationError('Este campo es obligatorio.')
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$', color):
            raise forms.ValidationError('No use números o símbolos (@, #, etc.).')
        return color

    def clean_anio(self):
        anio = self.cleaned_data.get('anio')
        año_actual = datetime.now().year
        año_minimo = 1900

        if anio is None:
            raise forms.ValidationError('Este campo es obligatorio.')
        if anio < año_minimo:
            raise forms.ValidationError(f'El año no puede ser menor a {año_minimo}')
        if anio> (año_actual + 1):
            raise forms.ValidationError(f'El año no puede ser mayor a {año_actual + 1}')
        return anio

    def clean_numero_serie(self):
        numero_serie = self.cleaned_data.get('numero_serie', '').strip()
        if not numero_serie:
            raise forms.ValidationError('Este campo es obligatorio.')
        return numero_serie

    def clean_placas(self):
        placas = self.cleaned_data.get('placas', '').strip()
        if not placas:
            raise forms.ValidationError('Este campo es obligatorio.')
        return placas

    def clean_cliente(self):
        cliente = self.cleaned_data.get('cliente')
        if not cliente:
            raise forms.ValidationError('Este campo es obligatorio.')
        return cliente
