from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.models import User, Group
from apps.cliente.models import m_cliente
from apps.inventario.models import Categoria
from apps.ordenes.models import m_servicio
from apps.inventario.models import m_inventario
from apps.vehiculo.models import m_vehiculo
from apps.ordenes.models import m_orden_trabajo
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import update_session_auth_hash


#Paginas privadas
def v_inicio(request):
    return render(request, 'inicio.html', {})

#Paginas publicas
def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        password = request.POST.get('password')

        try:
            usuario = User.objects.get(email=correo)
            user = authenticate(request, username=usuario.username, password=password)
            if user is not None:
                login(request, user)

                if user.is_superuser:
                    return redirect('admin:index')  # Panel de admin
                else:
                    return redirect('inicio')  # Ruta genérica

            else:
                messages.error(request, 'Contraseña incorrecta.')
        except User.DoesNotExist:
            messages.error(request, 'Correo no registrado.')

    return render(request, 'public/login.html')

def logout_view(request):
    logout(request)
    return redirect('u_home')

@login_required
def p_inicio(request):
    total_clientes = m_cliente.objects.count()
    total_vehiculos = m_vehiculo.objects.count()
    ordenes_en_proceso = m_orden_trabajo.objects.filter(estado='E').count()
    productos = m_inventario.objects.all()
    stock_minimo = 5

    productos = productos.filter(stock__lte=stock_minimo)
    total_minimos = productos.filter(stock__lte=stock_minimo).count()

    context ={
        'total_clientes': total_clientes ,
        'total_vehiculos': total_vehiculos ,
        'total_minimos': total_minimos,
        'ordenes_en_proceso': ordenes_en_proceso,
    }
    return render(request, 'public/inicio.html', context)

@login_required
def p_perfil(request):
    user = request.user

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        apellidos = request.POST.get('apellidos', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password')
        repetir_password = request.POST.get('repetir_password')

        # Validar contraseñas
        if password and password != repetir_password:
            messages.warning(request, 'prodcuto|error|Las contraseñas no coinciden')
            return render(request, 'public/perfil.html', {'user': user})

        # Actualizar campos
        user.first_name = nombre
        user.last_name = apellidos
        user.email = email

        if password:
            user.set_password(password)
            update_session_auth_hash(request, user)  # Mantener sesión iniciada

        user.save()
        messages.success(request, 'prodcuto|actualizado|Datos actualizados correctamente')
        return redirect('perfil')

    return render(request, 'public/perfil.html', {'user': user})

@login_required
def p_config(request):
    grupos = Group.objects.all()

    if request.method == 'POST':
        if 'form_categoria' in request.POST:
            categoria = request.POST.get('categoria', '').strip()
            if categoria:
                Categoria.objects.create(categoria=categoria)
                messages.success(request, 'empleado|agregado|Agregado correctamente')
            else:
                messages.error(request, 'empleado|error|Campo categoría requerido.')

        elif 'form_servicio' in request.POST:
            servicio = request.POST.get('servicio', '')
            descripcion = request.POST.get('descripcion', '')
            costo = request.POST.get('costo', '')
            if servicio and descripcion and costo:
                m_servicio.objects.create(servicio=servicio, descripcion=descripcion, costo=costo)
                messages.success(request, 'empleado|agregado|Agregado correctamente')
            else:
                messages.error(request,'empleado|error|Todos los campos del servicio son obligatorios.')

        elif 'form_empleado' in request.POST:
            username = request.POST.get('username')
            first = request.POST.get('first_name')
            last = request.POST.get('last_name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            rol_id = request.POST.get('rol')

            if User.objects.filter(username=username).exists():
                messages.error(request, 'empleado|error|El usuario ya existe.')
            else:
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=first,
                    last_name=last
                )
                if rol_id:
                    grupo = Group.objects.get(id=rol_id)
                    user.groups.add(grupo)
                messages.success(request, 'empleado|agregado|Agregado correctamente')

    categorias = Categoria.objects.all()
    servicios = m_servicio.objects.all()
    empleados = User.objects.filter(is_superuser=False)

    context = {
        'grupos': grupos,
        'categorias': categorias,
        'servicios': servicios,
        'empleados': empleados,
    }
    return render(request, 'public/configuracion.html', context)


@require_POST
def eliminar_categoria(request):
    id = request.POST.get('id_categoria')
    categoria = get_object_or_404(Categoria, pk=id)
    categoria.delete()
    messages.success(request, 'prodcuto|actualizado|Eliminado correctamente')
    return redirect('config')


@require_POST
def eliminar_servicio(request):
    id = request.POST.get('id_servicio')
    servicio = get_object_or_404(m_servicio, pk=id)
    servicio.delete()
    messages.success(request, 'prodcuto|actualizado|Eliminado correctamente')
    return redirect('config')


@require_POST
def eliminar_empleado(request):
    id = request.POST.get('id')
    empleado = get_object_or_404(User, pk=id)
    if not empleado.is_superuser:
        empleado.delete()
        messages.success(request, 'prodcuto|actualizado|Eliminado correctamente')
    else:
        messages.error(request, 'No se puede eliminar un superusuario.')
    return redirect('config')

@require_POST
def editar_servicio(request):
    try:
        servicio = m_servicio.objects.get(id_servicio=request.POST.get('id_servicio'))
        servicio.servicio = request.POST.get('servicio')
        servicio.descripcion = request.POST.get('descripcion')
        servicio.costo = request.POST.get('costo')
        servicio.save()
        messages.success(request, 'prodcuto|actualizado|Actualizado correctamente')
    except m_servicio.DoesNotExist:
        messages.error(request, 'empleado|error|Servicio no encontrado.')
    return redirect('config')

@require_POST
def editar_empleado(request):
    try:
        empleado = User.objects.get(id=request.POST.get('id'))
        empleado.username = request.POST.get('username')
        empleado.first_name = request.POST.get('first_name')
        empleado.last_name = request.POST.get('last_name')
        empleado.email = request.POST.get('email')
        empleado.save()

        # Actualizar grupo
        rol_id = request.POST.get('rol')
        if rol_id:
            grupo = Group.objects.get(id=rol_id)
            empleado.groups.clear()
            empleado.groups.add(grupo)

        messages.success(request, 'prodcuto|actualizado|Actualizado correctamente')
    except User.DoesNotExist:
        messages.error(request, 'empleado|error|Empleado no encontrado.')
    return redirect('config')
