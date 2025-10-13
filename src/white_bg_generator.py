"""
White Background Generator
Módulo principal para cambiar fondos de imágenes a blanco RGB(255,255,255)
"""

import os
import logging
from typing import Optional, Union, List, Tuple
import numpy as np
from PIL import Image
import cv2

try:
    from rembg import remove, new_session
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False
    logging.warning("rembg no está disponible. Instala con: pip install rembg")

try:
    from .utils import (
        validate_image_path, ensure_output_directory, pil_to_numpy, 
        numpy_to_pil, create_white_background, resize_image, blend_images
    )
except ImportError:
    # Importación directa cuando se ejecuta como script
    from utils import (
        validate_image_path, ensure_output_directory, pil_to_numpy, 
        numpy_to_pil, create_white_background, resize_image, blend_images
    )


class WhiteBGGenerator:
    """
    Generador de fondos blancos para imágenes.
    
    Esta clase permite remover el fondo de una imagen y reemplazarlo
    con un fondo blanco RGB(255,255,255) usando diferentes métodos
    de segmentación.
    """
    
    AVAILABLE_MODELS = [
        'u2net',           # Modelo general
        'u2netp',          # Modelo ligero
        'u2net_human_seg', # Optimizado para personas
        'silueta',         # Siluetas
        'isnet-general-use', # Modelo de alta calidad
    ]
    
    def __init__(self, model_name: str = 'u2net', enable_gpu: bool = True):
        """
        Inicializa el generador de fondos blancos.
        
        Args:
            model_name (str): Nombre del modelo a usar para segmentación
            enable_gpu (bool): Si usar GPU para acelerar el procesamiento
        """
        self.model_name = model_name
        self.enable_gpu = enable_gpu
        self.session = None
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Inicializar sesión de rembg si está disponible
        if REMBG_AVAILABLE:
            try:
                self.session = new_session(model_name)
                self.logger.info(f"Modelo {model_name} cargado exitosamente")
            except Exception as e:
                self.logger.error(f"Error cargando modelo {model_name}: {e}")
                self.session = None
        else:
            self.logger.warning("rembg no disponible, usando método alternativo")
    
    def _remove_background_rembg(self, image: Image.Image) -> Image.Image:
        """
        Remueve el fondo usando rembg.
        
        Args:
            image (PIL.Image): Imagen de entrada
            
        Returns:
            PIL.Image: Imagen sin fondo (con canal alpha)
        """
        if not REMBG_AVAILABLE or self.session is None:
            raise RuntimeError("rembg no está disponible o no se pudo cargar el modelo")
        
        # Convertir a RGB si es necesario
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Remover fondo
        result = remove(image, session=self.session)
        
        return result
    
    def _remove_background_opencv(self, image: Image.Image) -> Image.Image:
        """
        Método alternativo usando OpenCV para remover fondo (básico).
        
        Args:
            image (PIL.Image): Imagen de entrada
            
        Returns:
            PIL.Image: Imagen sin fondo
        """
        # Convertir PIL a OpenCV
        cv_image = cv2.cvtColor(pil_to_numpy(image), cv2.COLOR_RGB2BGR)
        
        # Aplicar GrabCut (segmentación básica)
        mask = np.zeros(cv_image.shape[:2], np.uint8)
        bgd_model = np.zeros((1, 65), np.float64)
        fgd_model = np.zeros((1, 65), np.float64)
        
        # Definir rectángulo que probablemente contiene el objeto
        height, width = cv_image.shape[:2]
        rect = (int(width * 0.1), int(height * 0.1), 
                int(width * 0.8), int(height * 0.8))
        
        # Aplicar GrabCut
        cv2.grabCut(cv_image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
        
        # Crear máscara binaria
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        
        # Aplicar la máscara
        result = cv_image * mask2[:, :, np.newaxis]
        
        # Convertir de vuelta a PIL con canal alpha
        result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
        result_pil = numpy_to_pil(result_rgb)
        
        # Agregar canal alpha basado en la máscara
        result_rgba = result_pil.convert('RGBA')
        alpha = numpy_to_pil(mask2 * 255).convert('L')
        result_rgba.putalpha(alpha)
        
        return result_rgba
    
    def remove_background(self, image: Union[str, Image.Image, np.ndarray]) -> Image.Image:
        """
        Remueve el fondo de una imagen.
        
        Args:
            image: Imagen de entrada (ruta, PIL Image, o numpy array)
            
        Returns:
            PIL.Image: Imagen sin fondo con canal alpha
        """
        # Convertir entrada a PIL Image
        if isinstance(image, str):
            if not validate_image_path(image):
                raise ValueError(f"Ruta de imagen inválida: {image}")
            pil_image = Image.open(image)
        elif isinstance(image, np.ndarray):
            pil_image = numpy_to_pil(image)
        elif isinstance(image, Image.Image):
            pil_image = image.copy()
        else:
            raise TypeError("Tipo de imagen no soportado")
        
        # Intentar usar rembg primero
        try:
            if REMBG_AVAILABLE and self.session is not None:
                return self._remove_background_rembg(pil_image)
            else:
                self.logger.info("Usando método OpenCV alternativo")
                return self._remove_background_opencv(pil_image)
        except Exception as e:
            self.logger.error(f"Error removiendo fondo: {e}")
            # Fallback: retornar imagen original con alpha channel
            if pil_image.mode != 'RGBA':
                pil_image = pil_image.convert('RGBA')
            return pil_image
    
    def apply_white_background(self, image: Image.Image) -> Image.Image:
        """
        Aplica un fondo blanco a una imagen con canal alpha.
        
        Args:
            image (PIL.Image): Imagen con canal alpha
            
        Returns:
            PIL.Image: Imagen con fondo blanco RGB(255,255,255)
        """
        if image.mode != 'RGBA':
            # Si no tiene canal alpha, asumir que ya tiene fondo
            return image.convert('RGB')
        
        # Crear fondo blanco del mismo tamaño
        white_bg = create_white_background(image.size, 'RGBA')
        
        # Combinar la imagen con el fondo blanco
        result = Image.alpha_composite(white_bg, image)
        
        # Convertir a RGB para eliminar el canal alpha
        return result.convert('RGB')
    
    def process_image(self, image: Union[str, Image.Image, np.ndarray], 
                     output_path: Optional[str] = None,
                     resize_max: Optional[int] = None) -> Image.Image:
        """
        Procesa una imagen completa: remueve fondo y aplica fondo blanco.
        
        Args:
            image: Imagen de entrada
            output_path: Ruta para guardar el resultado (opcional)
            resize_max: Tamaño máximo para redimensionar (opcional)
            
        Returns:
            PIL.Image: Imagen procesada con fondo blanco
        """
        self.logger.info("Iniciando procesamiento de imagen...")
        
        # Cargar imagen
        if isinstance(image, str):
            original = Image.open(image)
            self.logger.info(f"Imagen cargada: {image}")
        else:
            original = image if isinstance(image, Image.Image) else numpy_to_pil(image)
        
        # Redimensionar si es necesario
        if resize_max:
            original = resize_image(original, resize_max)
            self.logger.info(f"Imagen redimensionada a máximo {resize_max}px")
        
        # Remover fondo
        self.logger.info("Removiendo fondo...")
        no_bg = self.remove_background(original)
        
        # Aplicar fondo blanco
        self.logger.info("Aplicando fondo blanco...")
        result = self.apply_white_background(no_bg)
        
        # Guardar si se especifica ruta de salida
        if output_path:
            ensure_output_directory(output_path)
            result.save(output_path, quality=95, optimize=True)
            self.logger.info(f"Imagen guardada: {output_path}")
        
        self.logger.info("Procesamiento completado")
        return result
    
    def process_batch(self, input_paths: List[str], output_dir: str,
                     resize_max: Optional[int] = None,
                     prefix: str = "white_bg_") -> List[str]:
        """
        Procesa múltiples imágenes en lote.
        
        Args:
            input_paths: Lista de rutas de imágenes de entrada
            output_dir: Directorio de salida
            resize_max: Tamaño máximo para redimensionar
            prefix: Prefijo para archivos de salida
            
        Returns:
            List[str]: Lista de rutas de archivos generados
        """
        os.makedirs(output_dir, exist_ok=True)
        output_paths = []
        
        for i, input_path in enumerate(input_paths):
            try:
                # Generar nombre de archivo de salida
                filename = os.path.basename(input_path)
                name, ext = os.path.splitext(filename)
                output_filename = f"{prefix}{name}{ext}"
                output_path = os.path.join(output_dir, output_filename)
                
                self.logger.info(f"Procesando {i+1}/{len(input_paths)}: {filename}")
                
                # Procesar imagen
                self.process_image(input_path, output_path, resize_max)
                output_paths.append(output_path)
                
            except Exception as e:
                self.logger.error(f"Error procesando {input_path}: {e}")
                continue
        
        self.logger.info(f"Procesamiento en lote completado: {len(output_paths)} imágenes")
        return output_paths
    
    def get_model_info(self) -> dict:
        """
        Obtiene información sobre el modelo actual.
        
        Returns:
            dict: Información del modelo
        """
        return {
            'model_name': self.model_name,
            'rembg_available': REMBG_AVAILABLE,
            'session_loaded': self.session is not None,
            'gpu_enabled': self.enable_gpu,
            'available_models': self.AVAILABLE_MODELS
        }
    
    @classmethod
    def get_available_models(cls) -> List[str]:
        """
        Retorna la lista de modelos disponibles.
        
        Returns:
            List[str]: Lista de nombres de modelos
        """
        return cls.AVAILABLE_MODELS.copy()