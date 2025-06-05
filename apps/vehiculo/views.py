from django.shortcuts import render, redirect, get_object_or_404
from .forms import VehiculoForm
from django.http import JsonResponse
from django.db.models import Q
import requests
from django.contrib import messages
from apps.vehiculo.models import m_vehiculo
from apps.cliente.models import m_cliente
from dal import autocomplete
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# Create your views here.
class ClienteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Todos los clientes al inicio
        qs = m_cliente.objects.all()

        # Si el usuario está buscando algo (self.q = término de búsqueda)
        if self.q:
            qs = qs.filter(nombre__icontains=self.q)  # Busca coincidencias en el nombre

        return qs

@login_required
def p_vehiculo(request):
    query = request.GET.get('busca_vehiculo')  # Captura lo que escribió el usuario
    vehiculos = m_vehiculo.objects.all().order_by('-date_created')
    clientes = m_cliente.objects.all()

    if query:
        vehiculos = vehiculos.filter(
            Q(placas__icontains=query) |
            Q(cliente__nombre__icontains=query) |
            Q(cliente__ap_01__icontains=query)
        )
        # clientes = clientes.filter(
        #     Q(nombre__icontains=query) |
        #     Q(ap_01__icontains=query)
        # )

    context = {
        'vehiculos': vehiculos,
        # 'clientes': clientes,
        'query': query,  # Para mostrar el valor buscado en el input
    }
    return render(request, 'vehiculos/vehiculos.html', context)

@login_required
def agregar_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST) #Para guardar un formulario
        if form.is_valid():
            form.save()
            messages.success(request, 'vehiculo|agregado|Vehiculo agregado correctamente')
            return redirect('vehiculos') #Redireccionamiento
    else:
        form = VehiculoForm()

    return render(request, 'vehiculos/agregar.html',  {'form': form})

@login_required
def ver_vehiculo(request, id_vehiculo):
    vehiculo = get_object_or_404(m_vehiculo, pk=id_vehiculo) #Para pasar la id
    return render(request, 'vehiculos/ver_vehiculo.html', {'vehiculo': vehiculo})

@login_required
def editar_vehiculo(request, id_vehiculo):
    vehiculo = get_object_or_404(m_vehiculo, pk=id_vehiculo)
    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculo)
        form.fields['numero_serie'].disabled = True
        if form.is_valid():
            form.save()
            messages.success(request, 'vehiculo|actualizado|Vehiculo actualizado correctamente')
            return redirect('vehiculos')
    else:
        form = VehiculoForm(instance=vehiculo)
        form.fields['numero_serie'].disabled = True,
    return render(request, 'vehiculos/editar_vehiculo.html', {'form': form, 'vehiculo': vehiculo})

@require_POST
def eliminar_vehiculo(request):
    id_vehiculo = request.POST.get('id_vehiculo')
    producto = get_object_or_404(m_vehiculo, pk=id_vehiculo)
    producto.delete()
    messages.success(request, 'vehiculo|eliminado|Vehiculo eliminado correctamente')
    return redirect('vehiculos')


def obtener_marcas(request):
    url = "https://vpic.nhtsa.dot.gov/api/vehicles/GetAllMakes?format=json"
    response = requests.get(url)
    data = response.json()
    marca = sorted(set([item["Make_Name"] for item in data["Results"]]))
    return JsonResponse({"marca": marca})

def obtener_modelos(request, marca):
    url = f"https://vpic.nhtsa.dot.gov/api/vehicles/GetModelsForMake/{marca}?format=json"
    response = requests.get(url)
    data = response.json()
    modelo = [item["Model_Name"] for item in data["Results"]]
    return JsonResponse({"modelo": modelo})
