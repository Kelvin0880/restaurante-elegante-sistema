#!/usr/bin/env python
"""
Script para poblar la base de datos con datos de prueba
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurante_elegante.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Categoria, Plato, Noticia, PerfilUsuario
from decimal import Decimal

# Crear categorías
categorias_data = [
    {'nombre': 'Entrantes', 'descripcion': 'Deliciosos aperitivos para comenzar'},
    {'nombre': 'Platos Principales', 'descripcion': 'Nuestras especialidades de la casa'},
    {'nombre': 'Postres', 'descripcion': 'Dulces finales perfectos'},
    {'nombre': 'Bebidas', 'descripcion': 'Selección de vinos y cócteles'},
    {'nombre': 'Especiales del Chef', 'descripcion': 'Creaciones únicas de nuestro chef'},
]

for cat_data in categorias_data:
    categoria, created = Categoria.objects.get_or_create(
        nombre=cat_data['nombre'],
        defaults={'descripcion': cat_data['descripcion']}
    )
    if created:
        print(f"Categoría creada: {categoria.nombre}")

# Crear platos con imágenes específicas
platos_data = [
    {
        'nombre': 'Carpaccio de Ternera',
        'descripcion': 'Finas láminas de ternera con rúcula, parmesano y vinagreta de limón',
        'precio': Decimal('18.50'),
        'categoria': 'Entrantes',
        'imagen': 'images/Carpaccio de Ternera.jpg'
    },
    {
        'nombre': 'Pulpo a la Gallega',
        'descripcion': 'Pulpo tierno con patatas, pimentón dulce y aceite de oliva virgen',
        'precio': Decimal('19.50'),
        'categoria': 'Entrantes',
        'imagen': 'images/Pulpo a la Gallega.jpg'
    },
    {
        'nombre': 'Salmón a la Plancha',
        'descripcion': 'Salmón fresco con puré de batata y verduras al vapor',
        'precio': Decimal('24.90'),
        'categoria': 'Platos Principales',
        'imagen': 'images/Salmn a la Plancha.jpg'
    },
    {
        'nombre': 'Risotto de Setas',
        'descripcion': 'Cremoso risotto con setas variadas y trufa negra',
        'precio': Decimal('22.00'),
        'categoria': 'Platos Principales',
        'imagen': 'images/Risotto de Setas.jpg'
    },
    {
        'nombre': 'Paella Valenciana',
        'descripcion': 'Tradicional paella con pollo, conejo, garrofón y judía verde',
        'precio': Decimal('26.00'),
        'categoria': 'Especiales del Chef',
        'imagen': 'images/Paella Valenciana.jpg'
    },
    {
        'nombre': 'Tiramisu de la Casa',
        'descripcion': 'Clásico postre italiano con nuestra receta secreta',
        'precio': Decimal('8.50'),
        'categoria': 'Postres',
        'imagen': 'images/Tiramisú de la Casa.jpg'
    },
    {
        'nombre': 'Tarta de Chocolate',
        'descripcion': 'Intensa tarta de chocolate belga con helado de vainilla',
        'precio': Decimal('9.00'),
        'categoria': 'Postres',
        'imagen': 'images/Tarta de Chocolate.jpg'
    },
    {
        'nombre': 'Vino Tinto Reserva',
        'descripcion': 'Selección de vinos tintos de nuestras mejores bodegas',
        'precio': Decimal('32.00'),
        'categoria': 'Bebidas',
        'imagen': 'images/Vino Tinto Reserva.jpg'
    },
]

for plato_data in platos_data:
    categoria = Categoria.objects.get(nombre=plato_data['categoria'])
    plato, created = Plato.objects.get_or_create(
        nombre=plato_data['nombre'],
        defaults={
            'descripcion': plato_data['descripcion'],
            'precio': plato_data['precio'],
            'categoria': categoria,
            'disponible': True,
            'imagen': plato_data.get('imagen', '')
        }
    )
    if created:
        print(f"Plato creado: {plato.nombre}")
    else:
        # Actualizar imagen si ya existe
        if 'imagen' in plato_data:
            plato.imagen = plato_data['imagen']
            plato.save()
            print(f"Plato actualizado: {plato.nombre}")

# Crear usuario de prueba si no existe
usuario_test, created = User.objects.get_or_create(
    username='cliente_test',
    defaults={
        'email': 'cliente@test.com',
        'first_name': 'Cliente',
        'last_name': 'Prueba',
        'is_active': True
    }
)
if created:
    usuario_test.set_password('test1234')
    usuario_test.save()
    # Crear perfil
    PerfilUsuario.objects.create(
        usuario=usuario_test,
        telefono='+34 123 456 789',
        direccion='Calle Test 123, Madrid'
    )
    print(f"Usuario de prueba creado: {usuario_test.username}")

# Crear noticias
admin_user = User.objects.filter(is_superuser=True).first()
if admin_user:
    noticias_data = [
        {
            'titulo': 'Nuevo Menú de Primavera',
            'contenido': '''Estamos emocionados de presentar nuestro nuevo menú de primavera, que incluye ingredientes frescos y de temporada.

Nuestro chef ha creado platos únicos que capturan la esencia de la primavera, con sabores vibrantes y presentaciones espectaculares.

Destacamos nuestro nuevo plato estrella: Lubina con espárragos trigueros y salsa de limón, que promete convertirse en el favorito de nuestros comensales.

¡Te invitamos a visitarnos y descubrir estos nuevos sabores!''',
            'imagen': 'images/Nuevo Menú de Primavera.jpg'
        },
        {
            'titulo': 'Renovación del Comedor Principal',
            'contenido': '''Nos complace anunciar que hemos completado la renovación de nuestro comedor principal.

Los cambios incluyen:
- Nueva decoración con un estilo más moderno y elegante
- Iluminación LED regulable para crear el ambiente perfecto
- Muebles ergonómicos para mayor comodidad
- Sistema de sonido mejorado

El objetivo es ofrecer una experiencia gastronómica aún más placentera y memorable para nuestros queridos clientes.

¡Esperamos verte pronto para que disfrutes de nuestro renovado espacio!''',
            'imagen': 'images/Renovación del Comedor Principal.jpg'
        }
    ]
    
    for noticia_data in noticias_data:
        noticia, created = Noticia.objects.get_or_create(
            titulo=noticia_data['titulo'],
            defaults={
                'contenido': noticia_data['contenido'],
                'autor': admin_user,
                'activa': True,
                'imagen': noticia_data.get('imagen', '')
            }
        )
        if created:
            print(f"Noticia creada: {noticia.titulo}")
        else:
            # Actualizar imagen si ya existe
            if 'imagen' in noticia_data:
                noticia.imagen = noticia_data['imagen']
                noticia.save()
                print(f"Noticia actualizada: {noticia.titulo}")

print("\n¡Datos de prueba creados exitosamente!")
print("\nCuentas disponibles:")
print("- Administrador: admin / admin123")
print("- Cliente prueba: cliente_test / test1234")
print("\nYa puedes explorar el sitio web con datos reales.")
