from django import forms
from .models import m_vehiculo
from dal import autocomplete


class VehiculoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['cliente'].empty_label = "Selecciona un cliente"

        # Hacer todos los campos obligatorios y agregar atributos
        for field in self.fields:
            self.fields[field].required = True
            self.fields[field].widget.attrs['required'] = 'required'

    class Meta:
        model = m_vehiculo
        fields = [
            'marca', 'modelo', 'anio', 'color',
            'numero_serie', 'placas', 'cliente'
        ]
        widgets = {
            'marca': forms.TextInput(attrs={'class': 'form-control casilla'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control casilla'}),
            'anio': forms.NumberInput(attrs={
                'class': 'form-control casilla',
                'min': '1900',
                'max': '2030',
            }),
            'color': forms.TextInput(attrs={'class': 'form-control casilla'}),
            'numero_serie': forms.TextInput(attrs={'class': 'form-control casilla'}),
            'placas': forms.TextInput(attrs={'class': 'form-control casilla'}),
            # 'cliente': ClienteWidget(attrs={'class': 'form-select casilla'}),
            'cliente': forms.Select(attrs={'class': 'form-select casilla'}),
            'cliente': autocomplete.ModelSelect2(url='cliente-autocomplete', attrs={'class': 'form-select casilla select2-autocomplete'}),
        }

    # Validaciones personalizadas
    def clean_marca(self):
        marca = self.cleaned_data.get('marca', '').strip()
        if not marca:
            raise forms.ValidationError('La marca no puede estar vacía.')
        return marca

    def clean_modelo(self):
        modelo = self.cleaned_data.get('modelo', '').strip()
        if not modelo:
            raise forms.ValidationError('El modelo no puede estar vacío.')
        return modelo

    def clean_color(self):
        color = self.cleaned_data.get('color', '').strip()
        if not color:
            raise forms.ValidationError('El color no puede estar vacío.')
        return color

    def clean_anio(self):
        anio = self.cleaned_data.get('anio')
        if anio is None:
            raise forms.ValidationError('El año es obligatorio.')
        if anio < 1900 or anio > 2030:
            raise forms.ValidationError('El año debe estar entre 1900 y 2030.')
        return anio

    def clean_numero_serie(self):
        numero_serie = self.cleaned_data.get('numero_serie', '').strip()
        if not numero_serie:
            raise forms.ValidationError('El número de serie no puede estar vacío.')
        return numero_serie

    def clean_placas(self):
        placas = self.cleaned_data.get('placas', '').strip()
        if not placas:
            raise forms.ValidationError('Las placas no pueden estar vacías.')
        return placas

    def clean_cliente(self):
        cliente = self.cleaned_data.get('cliente')
        if not cliente:
            raise forms.ValidationError('Debes seleccionar un cliente.')
        return cliente
