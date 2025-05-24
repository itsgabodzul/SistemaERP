from django.shortcuts import render, redirect
from .models import m_refaccion
from .forms import OrdenTrabajoForm, RefaccionFormSet

# Create your views here.
def p_orden(request):
    return render(request, 'ordenes/ordenes.html')

def crear_orden_trabajo(request):
    if request.method == 'POST':
        form = OrdenTrabajoForm(request.POST)
        formset = RefaccionFormSet(request.POST, queryset=m_refaccion.objects.none())

        if form.is_valid() and formset.is_valid():
            orden = form.save()
            orden.estado = 'Pendiente'
            refacciones = formset.save(commit=False)
            for refaccion in refacciones:
                refaccion.orden = orden
                refaccion.save()
            return redirect('orden')  # o donde necesites
    else:
        form = OrdenTrabajoForm()
        formset = RefaccionFormSet(queryset=m_refaccion.objects.none())

    return render(request, 'ordenes/nueva_orden.html', {
        'form': form,
        'formset': formset,
    })
