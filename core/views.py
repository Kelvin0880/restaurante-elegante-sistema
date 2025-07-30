from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from .models import Plato, Noticia, Carrito, ItemCarrito, Pedido, ItemPedido, Contacto, Categoria
from .forms import ContactoForm, RegistroForm
import json


def home(request):
    """Vista principal del restaurante"""
    platos_destacados = Plato.objects.filter(disponible=True)[:6]
    noticias_recientes = Noticia.objects.filter(activa=True)[:3]
    categorias = Categoria.objects.all()
    
    context = {
        'platos_destacados': platos_destacados,
        'noticias_recientes': noticias_recientes,
        'categorias': categorias,
    }
    return render(request, 'core/home.html', context)


def menu(request):
    """Vista del menú completo"""
    categoria_id = request.GET.get('categoria')
    buscar = request.GET.get('q')
    
    platos = Plato.objects.filter(disponible=True)
    
    if categoria_id:
        platos = platos.filter(categoria_id=categoria_id)
    
    if buscar:
        platos = platos.filter(
            Q(nombre__icontains=buscar) | 
            Q(descripcion__icontains=buscar)
        )
    
    categorias = Categoria.objects.all()
    
    context = {
        'platos': platos,
        'categorias': categorias,
        'categoria_seleccionada': categoria_id,
        'busqueda': buscar,
    }
    return render(request, 'core/menu.html', context)


def noticias(request):
    """Vista de todas las noticias"""
    noticias_list = Noticia.objects.filter(activa=True)
    context = {'noticias': noticias_list}
    return render(request, 'core/noticias.html', context)


def noticia_detalle(request, pk):
    """Vista de detalle de una noticia"""
    noticia = get_object_or_404(Noticia, pk=pk, activa=True)
    context = {'noticia': noticia}
    return render(request, 'core/noticia_detalle.html', context)


def contacto(request):
    """Vista del formulario de contacto"""
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Mensaje enviado correctamente! Te contactaremos pronto.')
            return redirect('contacto')
    else:
        form = ContactoForm()
    
    context = {'form': form}
    return render(request, 'core/contacto.html', context)


def privacidad(request):
    """Vista de política de privacidad"""
    return render(request, 'core/privacidad.html')


def custom_logout(request):
    """Vista personalizada para logout"""
    logout(request)
    messages.success(request, '¡Has cerrado sesión exitosamente!')
    return redirect('home')


def registro(request):
    """Vista de registro de usuarios"""
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Cuenta creada exitosamente!')
            return redirect('home')
    else:
        form = RegistroForm()
    
    context = {'form': form}
    return render(request, 'registration/registro.html', context)


@login_required
def carrito(request):
    """Vista del carrito de compras"""
    carrito_obj, created = Carrito.objects.get_or_create(
        usuario=request.user, 
        activo=True
    )
    
    context = {'carrito': carrito_obj}
    return render(request, 'core/carrito.html', context)


@login_required
def agregar_al_carrito(request, plato_id):
    """Agregar plato al carrito via AJAX"""
    if request.method == 'POST':
        plato = get_object_or_404(Plato, id=plato_id, disponible=True)
        carrito_obj, created = Carrito.objects.get_or_create(
            usuario=request.user, 
            activo=True
        )
        
        item, created = ItemCarrito.objects.get_or_create(
            carrito=carrito_obj,
            plato=plato,
            defaults={'cantidad': 1}
        )
        
        if not created:
            item.cantidad += 1
            item.save()
        
        return JsonResponse({
            'success': True,
            'message': f'{plato.nombre} agregado al carrito',
            'total_items': carrito_obj.items.count()
        })
    
    return JsonResponse({'success': False})


@login_required
def actualizar_carrito(request, item_id):
    """Actualizar cantidad de item en carrito"""
    if request.method == 'POST':
        item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
        data = json.loads(request.body)
        nueva_cantidad = data.get('cantidad', 1)
        
        if nueva_cantidad > 0:
            item.cantidad = nueva_cantidad
            item.save()
        else:
            item.delete()
        
        return JsonResponse({
            'success': True,
            'subtotal': float(item.get_subtotal()) if nueva_cantidad > 0 else 0,
            'total': float(item.carrito.get_total())
        })
    
    return JsonResponse({'success': False})


@login_required
def eliminar_del_carrito(request, item_id):
    """Eliminar item del carrito"""
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    item.delete()
    messages.success(request, 'Producto eliminado del carrito.')
    return redirect('carrito')


@login_required
def realizar_pedido(request):
    """Crear pedido desde el carrito"""
    carrito_obj = get_object_or_404(Carrito, usuario=request.user, activo=True)
    
    if not carrito_obj.items.exists():
        messages.error(request, 'Tu carrito está vacío.')
        return redirect('carrito')
    
    # Crear pedido
    pedido = Pedido.objects.create(
        usuario=request.user,
        total=carrito_obj.get_total(),
        notas=request.POST.get('notas', '')
    )
    
    # Crear items del pedido
    for item in carrito_obj.items.all():
        ItemPedido.objects.create(
            pedido=pedido,
            plato=item.plato,
            cantidad=item.cantidad,
            precio=item.plato.precio
        )
    
    # Limpiar carrito
    carrito_obj.activo = False
    carrito_obj.save()
    
    messages.success(request, f'¡Pedido #{pedido.id} realizado exitosamente!')
    return redirect('mis_pedidos')


@login_required
def mis_pedidos(request):
    """Vista de pedidos del usuario"""
    pedidos = Pedido.objects.filter(usuario=request.user)
    context = {'pedidos': pedidos}
    return render(request, 'core/mis_pedidos.html', context)


def is_admin(user):
    """Verificar si el usuario es administrador"""
    return user.is_staff or user.is_superuser


@user_passes_test(is_admin)
def admin_dashboard(request):
    """Dashboard administrativo"""
    total_pedidos = Pedido.objects.count()
    pedidos_pendientes = Pedido.objects.filter(estado='pendiente').count()
    total_platos = Plato.objects.count()
    contactos_no_leidos = Contacto.objects.filter(leido=False).count()
    
    pedidos_recientes = Pedido.objects.all()[:10]
    contactos_recientes = Contacto.objects.filter(leido=False)[:5]
    
    context = {
        'total_pedidos': total_pedidos,
        'pedidos_pendientes': pedidos_pendientes,
        'total_platos': total_platos,
        'contactos_no_leidos': contactos_no_leidos,
        'pedidos_recientes': pedidos_recientes,
        'contactos_recientes': contactos_recientes,
    }
    return render(request, 'core/admin_dashboard.html', context)


@user_passes_test(is_admin)
def admin_pedidos(request):
    """Gestión de pedidos para administradores"""
    estado_filtro = request.GET.get('estado', '')
    pedidos = Pedido.objects.all()
    
    if estado_filtro:
        pedidos = pedidos.filter(estado=estado_filtro)
    
    context = {
        'pedidos': pedidos,
        'estado_filtro': estado_filtro,
        'estados': Pedido.ESTADOS,
    }
    return render(request, 'core/admin_pedidos.html', context)


@user_passes_test(is_admin)
def actualizar_estado_pedido(request, pedido_id):
    """Actualizar estado de un pedido"""
    if request.method == 'POST':
        pedido = get_object_or_404(Pedido, id=pedido_id)
        nuevo_estado = request.POST.get('estado')
        
        if nuevo_estado in dict(Pedido.ESTADOS):
            pedido.estado = nuevo_estado
            pedido.save()
            messages.success(request, f'Estado del pedido #{pedido.id} actualizado.')
        
        return redirect('admin_pedidos')
    
    return redirect('admin_pedidos')


@user_passes_test(is_admin)
def pedido_detalles(request, pedido_id):
    """Obtener detalles de un pedido para modal (AJAX)"""
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    html_content = f"""
    <div class="pedido-detalles">
        <h5>Pedido #{pedido.id}</h5>
        <div class="row">
            <div class="col-md-6">
                <h6>Información del Cliente:</h6>
                <p><strong>Nombre:</strong> {pedido.usuario.get_full_name() or pedido.usuario.username}</p>
                <p><strong>Email:</strong> {pedido.usuario.email}</p>
                <p><strong>Fecha:</strong> {pedido.fecha_pedido.strftime('%d/%m/%Y %H:%M')}</p>
                <p><strong>Estado:</strong> <span class="estado estado-{pedido.estado}">{pedido.get_estado_display()}</span></p>
            </div>
            <div class="col-md-6">
                <h6>Resumen del Pedido:</h6>
                <p><strong>Total:</strong> €{pedido.total:.2f}</p>
                {'<p><strong>Notas:</strong> ' + pedido.notas + '</p>' if pedido.notas else ''}
            </div>
        </div>
        
        <h6>Productos:</h6>
        <div class="productos-pedido">
    """
    
    for item in pedido.items.all():
        html_content += f"""
            <div class="producto-item">
                <div class="producto-info">
                    <strong>{item.plato.nombre}</strong>
                    <span class="cantidad">x{item.cantidad}</span>
                </div>
                <div class="producto-precio">
                    €{item.precio:.2f} c/u - Total: €{(item.precio * item.cantidad):.2f}
                </div>
            </div>
        """
    
    html_content += """
        </div>
    </div>
    <style>
        .pedido-detalles h5 { color: var(--color-primario); margin-bottom: 1rem; }
        .pedido-detalles h6 { color: #333; margin-top: 1rem; margin-bottom: 0.5rem; }
        .productos-pedido { border-top: 1px solid #eee; padding-top: 1rem; }
        .producto-item { 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            padding: 0.5rem 0; 
            border-bottom: 1px solid #f8f9fa; 
        }
        .producto-info { display: flex; align-items: center; gap: 1rem; }
        .cantidad { 
            background: var(--color-primario); 
            color: white; 
            padding: 0.25rem 0.5rem; 
            border-radius: 4px; 
            font-size: 0.875rem; 
        }
        .producto-precio { font-weight: bold; color: var(--color-primario); }
    </style>
    """
    
    return JsonResponse({'html': html_content})
