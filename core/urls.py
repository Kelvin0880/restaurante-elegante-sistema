from django.urls import path
from . import views

urlpatterns = [
    # Páginas principales
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('noticias/', views.noticias, name='noticias'),
    path('noticias/<int:pk>/', views.noticia_detalle, name='noticia_detalle'),
    path('contacto/', views.contacto, name='contacto'),
    path('privacidad/', views.privacidad, name='privacidad'),
    
    # Autenticación
    path('registro/', views.registro, name='registro'),
    path('logout/', views.custom_logout, name='custom_logout'),
    
    # Carrito y pedidos
    path('carrito/', views.carrito, name='carrito'),
    path('agregar-carrito/<int:plato_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('actualizar-carrito/<int:item_id>/', views.actualizar_carrito, name='actualizar_carrito'),
    path('eliminar-carrito/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('realizar-pedido/', views.realizar_pedido, name='realizar_pedido'),
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    
    # Panel administrativo
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-pedidos/', views.admin_pedidos, name='admin_pedidos'),
    path('actualizar-pedido/<int:pedido_id>/', views.actualizar_estado_pedido, name='actualizar_estado_pedido'),
    path('admin/pedido/<int:pedido_id>/detalles/', views.pedido_detalles, name='pedido_detalles'),
]
