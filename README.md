# White Background Generator

Un proyecto de Python que permite cambiar el fondo de cualquier imagen a blanco RGB(255,255,255), manteniendo automáticamente el objeto principal mediante técnicas de segmentación por IA.

## Características

- 🎯 **Detección automática de objetos**: Usa modelos preentrenados para identificar el objeto principal
- 🎨 **Fondo blanco perfecto**: Convierte cualquier fondo a blanco puro RGB(255,255,255)
- 🚀 **Fácil de usar**: Interfaz de línea de comandos simple
- 📁 **Procesamiento por lotes**: Procesa múltiples imágenes a la vez
- 🔧 **Personalizable**: Ajusta parámetros de segmentación según tus necesidades

## Ejemplos

### Resultados de Antes y Después

#### Ejemplo 1: Personaje
| Antes | Después |
|-------|---------|
| ![Imagen Original](examples/character.png) | ![Fondo Blanco](examples/character_new.jpg) |
| *Imagen original con fondo colorido* | *Mismo personaje con fondo blanco puro* |

#### Ejemplo 2: Fotografía
| Antes | Después |
|-------|---------|
| ![Imagen Original](examples/foto.png) | ![Fondo Blanco](examples/foto_new.jpg) |
| *Fotografía con fondo complejo* | *Objeto principal preservado, fondo blanco* |

### Comando utilizado:
```bash
# Procesar las imágenes de ejemplo
python main.py examples/character.png -o examples/character_new.jpg
python main.py examples/foto.png -o examples/foto_new.jpg
```

💡 **Nota**: Todas las imágenes de salida mantienen el objeto principal intacto mientras el fondo se convierte a blanco puro RGB(255,255,255).

## Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/dvchinx/White-BG-Gen.git
cd White-BG-Gen
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

### Usar desde línea de comandos

```bash
# Procesar una sola imagen
python main.py input.jpg -o output.jpg

# Procesar múltiples imágenes
python main.py *.jpg -o output_folder/

# Usar modelo específico de segmentación
python main.py input.jpg -o output.jpg --model rembg-u2net
```

### Usar como módulo de Python

```python
from src.white_bg_generator import WhiteBGGenerator

# Crear el generador
generator = WhiteBGGenerator()

# Procesar una imagen
result = generator.process_image("input.jpg")
result.save("output.jpg")

# Procesar desde array numpy
import cv2
image = cv2.imread("input.jpg")
result = generator.process_array(image)
```

## Modelos disponibles

- `rembg-u2net`: Modelo general, bueno para la mayoría de objetos
- `rembg-u2netp`: Versión ligera y rápida
- `rembg-silueta`: Optimizado para personas
- `rembg-isnet`: Modelo de alta calidad para objetos complejos

## Estructura del proyecto

```
White-BG-Gen/
├── src/
│   ├── __init__.py
│   ├── white_bg_generator.py    # Módulo principal
│   └── utils.py                 # Utilidades
├── examples/                    # Imágenes de ejemplo
├── tests/                       # Tests unitarios
├── main.py                      # Script CLI
├── requirements.txt             # Dependencias
└── README.md                    # Este archivo
```

## Dependencias principales

- **rembg**: Para segmentación automática de fondo
- **Pillow**: Manipulación de imágenes
- **OpenCV**: Procesamiento de imágenes
- **NumPy**: Operaciones matriciales

## Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Créditos

- Utiliza la librería [rembg](https://github.com/danielgatis/rembg) para la segmentación de fondo
- Modelos de IA entrenados por la comunidad