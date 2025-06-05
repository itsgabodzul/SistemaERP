from django import forms
from .models import m_orden_trabajo, m_refaccion, DetalleServicio
from dal import autocomplete
from django.forms import modelformset_factory


class OrdenTrabajoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Etiqueta vacía para selects
        self.fields['id_vehiculo'].empty_label = "Selecciona un vehículo"
        self.fields['mecanico'].empty_label = "Selecciona un mecánico (opcional)"

        for field in self.fields:
            if field != 'entrega_estimada':  # Permitir nulo en entrega_estimada
                self.fields[field].required = True
                self.fields[field].widget.attrs['required'] = 'required'

    class Meta:
        model = m_orden_trabajo
        fields = [
            'id_vehiculo', 'entrega_estimada',
            'mecanico', 'diagnostico'
        ]
        widgets = {
            'id_vehiculo': autocomplete.ModelSelect2(url='vehiculo-autocomplete', attrs={'class': 'form-select casilla select2-autocomplete-placas'}),
            'entrega_estimada': forms.DateInput(attrs={'type': 'date', 'class': 'form-control casilla'}),
            'mecanico': forms.Select(attrs={'class': 'form-select casilla'}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control casilla', 'rows': 3}),
        }

    def clean_diagnostico(self):
        diagnostico = self.cleaned_data.get('diagnostico', '').strip()
        if not diagnostico:
            raise forms.ValidationError("El diagnóstico no puede estar vacío.")
        return diagnostico

class RefaccionForm(forms.ModelForm):
    class Meta:
        model = m_refaccion
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-select casilla'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control casilla', 'min': 1}),
        }

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad < 1:
            raise forms.ValidationError("La cantidad debe ser mayor a cero.")
        return cantidad

class ServicioForm(forms.ModelForm):
    class Meta:
        model = DetalleServicio
        fields = ['servicio']
        widgets = {
            'servicio': forms.Select(attrs={'class': 'form-select casilla'})
        }


from django.forms import modelformset_factory

RefaccionFormSet = modelformset_factory(
    m_refaccion,
    form=RefaccionForm,
    extra=1,  # Una fila por defecto
    can_delete=True  # Permitir eliminar
)

ServicioFormSet = modelformset_factory(
    DetalleServicio,
    form=ServicioForm,
    extra=1,  # Una fila por defecto
    can_delete=True  # Permitir eliminar
)
