#!/usr/bin/env python3
"""
Script para crear un favicon personalizado para Restaurante Elegante
Crea un favicon con icono de utensilio en fondo marrón elegante
"""

from PIL import Image, ImageDraw, ImageFont
import os

def crear_favicon():
    """Crea un favicon personalizado para el restaurante"""
    
    # Configuración
    size = 32  # Tamaño del favicon
    bg_color = '#2F4F4F'  # Verde oscuro elegante
    icon_color = '#FFD700'  # Dorado brillante para el icono
    border_color = '#8B4513'  # Marrón para el borde
    
    # Crear imagen
    img = Image.new('RGBA', (size, size), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Dibujar un plato circular
    plate_margin = 4
    plate_size = size - (plate_margin * 2)
    draw.ellipse([plate_margin, plate_margin, 
                 plate_margin + plate_size, plate_margin + plate_size], 
                 fill=icon_color, outline=border_color, width=2)
    
    # Dibujar el icono de utensilio en el centro
    center_x = size // 2
    center_y = size // 2
    
    # Tenedor (lado izquierdo del plato)
    fork_x = center_x - 6
    fork_y = center_y
    
    # Mango del tenedor
    draw.line([fork_x, fork_y - 4, fork_x, fork_y + 6], fill=bg_color, width=2)
    
    # Dientes del tenedor
    for i in range(3):
        x = fork_x - 2 + i * 2
        draw.line([x, fork_y - 6, x, fork_y - 2], fill=bg_color, width=1)
    
    # Cuchillo (lado derecho del plato)
    knife_x = center_x + 6
    knife_y = center_y
    
    # Mango del cuchillo
    draw.line([knife_x, knife_y - 4, knife_x, knife_y + 6], fill=bg_color, width=2)
    
    # Hoja del cuchillo
    draw.polygon([(knife_x - 1, knife_y - 6), 
                  (knife_x + 1, knife_y - 6), 
                  (knife_x + 1, knife_y - 2),
                  (knife_x - 1, knife_y - 2)], fill=bg_color)
    
    # Añadir puntos decorativos
    for i in range(4):
        angle = i * 90
        x = center_x + int(8 * (1 if angle == 0 else -1 if angle == 180 else 0))
        y = center_y + int(8 * (1 if angle == 90 else -1 if angle == 270 else 0))
        if x != center_x or y != center_y:
            draw.ellipse([x-1, y-1, x+1, y+1], fill=border_color)
    
    # Guardar como ICO
    favicon_path = os.path.join('static', 'images', 'favicon.ico')
    
    # Crear múltiples tamaños para el ICO
    sizes = [16, 32, 48]
    favicon_images = []
    
    for ico_size in sizes:
        if ico_size != size:
            resized_img = img.resize((ico_size, ico_size), Image.Resampling.LANCZOS)
        else:
            resized_img = img
        favicon_images.append(resized_img)
    
    # Guardar el favicon
    favicon_images[0].save(
        favicon_path,
        format='ICO',
        sizes=[(img.width, img.height) for img in favicon_images],
        append_images=favicon_images[1:]
    )
    
    print(f"✅ Favicon creado exitosamente en: {favicon_path}")
    
    # También crear una versión PNG para apple-touch-icon
    apple_icon_path = os.path.join('static', 'images', 'apple-touch-icon.png')
    apple_img = img.resize((180, 180), Image.Resampling.LANCZOS)
    apple_img.save(apple_icon_path, format='PNG')
    
    print(f"✅ Apple touch icon creado en: {apple_icon_path}")
    
    return True

if __name__ == "__main__":
    try:
        crear_favicon()
        print("\n🍽️ ¡Favicon personalizado para Restaurante Elegante creado con éxito!")
        print("El nuevo favicon aparecerá en la pestaña del navegador cuando recargues la página.")
    except Exception as e:
        print(f"❌ Error al crear favicon: {e}")
        print("Asegúrate de tener PIL (Pillow) instalado: pip install Pillow")
