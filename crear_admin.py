#!/usr/bin/env python
import os
import sys
import django

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurante_elegante.settings')
django.setup()

from django.contrib.auth.models import User

def crear_admin():
    """Crear usuario administrador"""
    try:
        # Verificar si ya existe el admin
        if User.objects.filter(username='admin').exists():
            print("El usuario admin ya existe.")
            admin_user = User.objects.get(username='admin')
            admin_user.set_password('admin123')
            admin_user.save()
            print("Contraseña del admin actualizada a: admin123")
        else:
            # Crear nuevo usuario admin
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@restauranteelegante.com',
                password='admin123',
                first_name='Administrador',
                last_name='Restaurante'
            )
            print("Usuario admin creado exitosamente!")
            print("Username: admin")
            print("Password: admin123")
            
        return True
    except Exception as e:
        print(f"Error al crear admin: {e}")
        return False

if __name__ == "__main__":
    crear_admin()
