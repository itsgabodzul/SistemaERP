from django import forms
from .models import m_cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = m_cliente
        fields = ['nombre', 'ap_01', 'sexo', 'email', 'telefono', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control casilla'}),
            'ap_01': forms.TextInput(attrs={'class': 'form-control casilla'}),
            'sexo': forms.Select(attrs={'class': 'form-select casilla'}),
            'email': forms.EmailInput(attrs={'class': 'form-control casilla'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control casilla'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control casilla'}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre', '').strip()
        if not nombre:
            raise forms.ValidationError('Este campo no puede estar vacío ni contener solo espacios.')
        return nombre

    def clean_ap_01(self):
        ap_01 = self.cleaned_data.get('ap_01', '').strip()
        if not ap_01:
            raise forms.ValidationError('Este campo no puede estar vacío ni contener solo espacios.')
        return ap_01

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion', '').strip()
        if not direccion:
            raise forms.ValidationError('Este campo no puede estar vacío ni contener solo espacios.')
        return direccion

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '').strip()
        if not telefono.isdigit():
            raise forms.ValidationError('El teléfono solo debe contener números.')
        if len(telefono) != 10:
            raise forms.ValidationError('El teléfono debe contener exactamente 10 dígitos.')
        return telefono

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if not email:
            raise forms.ValidationError('El campo de correo electrónico es obligatorio.')
        if '@' not in email:
            raise forms.ValidationError('Debe ingresar un correo electrónico válido con @.')
        return email
