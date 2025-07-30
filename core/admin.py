from django.contrib import admin
from .models import Categoria, Plato, Noticia, Carrito, ItemCarrito, Pedido, ItemPedido, Contacto, PerfilUsuario


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ['precio']


@admin.register(Plato)
class PlatoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'disponible', 'fecha_creacion']
    list_filter = ['categoria', 'disponible', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'disponible']


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'fecha_publicacion', 'activa']
    list_filter = ['fecha_publicacion', 'activa', 'autor']
    search_fields = ['titulo', 'contenido']
    list_editable = ['activa']
    readonly_fields = ['fecha_publicacion']


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'fecha_pedido', 'estado', 'total']
    list_filter = ['estado', 'fecha_pedido']
    search_fields = ['usuario__username', 'usuario__email']
    list_editable = ['estado']
    inlines = [ItemPedidoInline]
    readonly_fields = ['fecha_pedido', 'total']


@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'asunto', 'fecha_envio', 'leido']
    list_filter = ['fecha_envio', 'leido']
    search_fields = ['nombre', 'email', 'asunto']
    list_editable = ['leido']
    readonly_fields = ['fecha_envio']


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'telefono', 'fecha_nacimiento']
    search_fields = ['usuario__username', 'usuario__email', 'telefono']


# No registramos Carrito e ItemCarrito en admin ya que se manejan por código
