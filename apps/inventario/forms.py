from django import forms
from django.core.validators import MinValueValidator
from .models import m_inventario

class ExcelUploadForm(forms.Form):
    archivo = forms.FileField(label='Selecciona un archivo Excel (.xlsx)')

class InventarioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].empty_label = "Selecciona una categoria"

        # Hacer todos los campos obligatorios
        for field in self.fields:
            self.fields[field].required = True
            self.fields[field].widget.attrs['required'] = 'required'

    class Meta:
        model = m_inventario
        fields = ['nombre_p', 'descripcion', 'categoria', 'stock', 'precio']
        widgets = {
            'nombre_p': forms.TextInput(attrs={'class': 'form-control casilla'}),
            'descripcion': forms.TextInput(attrs={'class': 'form-control casilla'}),
            'categoria': forms.Select(attrs={'class': 'form-select casilla'}),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control casilla',
                'min': '0'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control casilla',
                'min': '0.00',
                'step': '1.00'
            }),
        }

    # Validaciones
    def clean_nombre_p(self):
        nombre_p = self.cleaned_data.get('nombre_p', '').strip()
        if not nombre_p:
            raise forms.ValidationError('Este campo es obligatorio.')
        return nombre_p

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion', '').strip()
        if not descripcion:
            raise forms.ValidationError('Este campo es obligatorio.')
        return descripcion

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is None:
            raise forms.ValidationError('Este campo es obligatorio.')
        if stock < 0:
            raise forms.ValidationError('El stock no puede ser negativo.')
        return stock

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is None:
            raise forms.ValidationError('Este campo es obligatorio.')
        if precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor que cero.')
        return precio

    def clean_categoria(self):
        categoria = self.cleaned_data.get('categoria')
        if not categoria:
            raise forms.ValidationError('Este campo es obligatorio.')
        return categoria