"""
Utilidades para el White Background Generator
"""

import os
from pathlib import Path
from typing import List, Union, Tuple
import numpy as np
from PIL import Image


def validate_image_path(image_path: str) -> bool:
    """
    Valida si la ruta de imagen existe y es un archivo de imagen válido.
    
    Args:
        image_path (str): Ruta al archivo de imagen
        
    Returns:
        bool: True si es válida, False en caso contrario
    """
    if not os.path.exists(image_path):
        return False
    
    valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp', '.gif'}
    return Path(image_path).suffix.lower() in valid_extensions


def get_supported_formats() -> List[str]:
    """
    Retorna la lista de formatos de imagen soportados.
    
    Returns:
        List[str]: Lista de extensiones soportadas
    """
    return ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp', '.gif']


def ensure_output_directory(output_path: str) -> str:
    """
    Asegura que el directorio de salida existe.
    
    Args:
        output_path (str): Ruta de salida
        
    Returns:
        str: Ruta de salida normalizada
    """
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    return output_path


def pil_to_numpy(image: Image.Image) -> np.ndarray:
    """
    Convierte una imagen PIL a array numpy.
    
    Args:
        image (PIL.Image): Imagen PIL
        
    Returns:
        np.ndarray: Array numpy de la imagen
    """
    return np.array(image)


def numpy_to_pil(array: np.ndarray) -> Image.Image:
    """
    Convierte un array numpy a imagen PIL.
    
    Args:
        array (np.ndarray): Array numpy de la imagen
        
    Returns:
        PIL.Image: Imagen PIL
    """
    # Asegurar que el array esté en el rango correcto
    if array.dtype == np.float64 or array.dtype == np.float32:
        array = (array * 255).astype(np.uint8)
    
    return Image.fromarray(array)


def create_white_background(size: Tuple[int, int], mode: str = 'RGB') -> Image.Image:
    """
    Crea una imagen con fondo blanco del tamaño especificado.
    
    Args:
        size (Tuple[int, int]): Tamaño (ancho, alto) de la imagen
        mode (str): Modo de color ('RGB', 'RGBA')
        
    Returns:
        PIL.Image: Imagen con fondo blanco
    """
    if mode == 'RGBA':
        return Image.new('RGBA', size, (255, 255, 255, 255))
    else:
        return Image.new('RGB', size, (255, 255, 255))


def resize_image(image: Image.Image, max_size: int = 1024) -> Image.Image:
    """
    Redimensiona una imagen manteniendo la proporción si excede el tamaño máximo.
    
    Args:
        image (PIL.Image): Imagen a redimensionar
        max_size (int): Tamaño máximo para el lado más largo
        
    Returns:
        PIL.Image: Imagen redimensionada
    """
    width, height = image.size
    
    if max(width, height) <= max_size:
        return image
    
    if width > height:
        new_width = max_size
        new_height = int((height * max_size) / width)
    else:
        new_height = max_size
        new_width = int((width * max_size) / height)
    
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)


def blend_images(foreground: Image.Image, background: Image.Image, 
                 mask: Image.Image) -> Image.Image:
    """
    Combina una imagen de primer plano con un fondo usando una máscara.
    
    Args:
        foreground (PIL.Image): Imagen de primer plano
        background (PIL.Image): Imagen de fondo
        mask (PIL.Image): Máscara de transparencia
        
    Returns:
        PIL.Image: Imagen combinada
    """
    # Convertir todas las imágenes al mismo modo
    if foreground.mode != 'RGBA':
        foreground = foreground.convert('RGBA')
    if background.mode != 'RGBA':
        background = background.convert('RGBA')
    if mask.mode != 'L':
        mask = mask.convert('L')
    
    # Redimensionar fondo si es necesario
    if background.size != foreground.size:
        background = background.resize(foreground.size, Image.Resampling.LANCZOS)
    
    # Usar la máscara para combinar las imágenes
    result = Image.composite(foreground, background, mask)
    
    return result


def get_file_list(input_path: str, recursive: bool = False) -> List[str]:
    """
    Obtiene una lista de archivos de imagen desde una ruta.
    
    Args:
        input_path (str): Ruta de entrada (archivo o directorio)
        recursive (bool): Si buscar recursivamente en subdirectorios
        
    Returns:
        List[str]: Lista de rutas de archivos de imagen
    """
    files = []
    
    if os.path.isfile(input_path):
        if validate_image_path(input_path):
            files.append(input_path)
    elif os.path.isdir(input_path):
        pattern = "**/*" if recursive else "*"
        path_obj = Path(input_path)
        
        for ext in get_supported_formats():
            files.extend(str(p) for p in path_obj.glob(f"{pattern}{ext}"))
            files.extend(str(p) for p in path_obj.glob(f"{pattern}{ext.upper()}"))
    
    return sorted(files)


def format_file_size(size_bytes: int) -> str:
    """
    Formatea el tamaño de archivo en una cadena legible.
    
    Args:
        size_bytes (int): Tamaño en bytes
        
    Returns:
        str: Tamaño formateado (ej: "1.5 MB")
    """
    if size_bytes == 0:
        return "0 B"
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.1f} TB"