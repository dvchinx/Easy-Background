# White Background Generator

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![AI](https://img.shields.io/badge/AI-Computer%20Vision-orange.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

[![GitHub stars](https://img.shields.io/github/stars/dvchinx/White-Background?style=social)](https://github.com/dvchinx/Easy-Background/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/dvchinx/White-Background?style=social)](https://github.com/dvchinx/Easy-Background/network/members)
[![GitHub issues](https://img.shields.io/github/issues/dvchinx/White-Background)](https://github.com/dvchinx/Easy-Background/issues)

</div>

<div align="center">
  <h3>🎨 Transformación Inteligente de Fondos con IA</h3>
  <p>
    <strong>Convierte cualquier imagen a fondo blanco o PNG transparente</strong><br>
    Usando técnicas avanzadas de segmentación por Inteligencia Artificial
  </p>
</div>

---

## 🚀 Características Principales

<div align="center">

| 🎯 **IA Avanzada** | 🎨 **Fondo Perfecto** | 🔍 **PNG Transparente** | ⚡ **Procesamiento Rápido** |
|:---:|:---:|:---:|:---:|
| Detección automática de objetos con modelos preentrenados | Fondo blanco puro RGB(255,255,255) | Imágenes PNG con transparencia total | Soporte GPU y procesamiento por lotes |

</div>

Proyecto Open Source de Python que permite cambiar el fondo de cualquier imagen a blanco RGB(255,255,255) o crear imágenes PNG con fondo transparente, manteniendo automáticamente el objeto principal mediante técnicas de segmentación por IA.

## ✨ Características

- 🎯 **Detección automática de objetos**: Usa modelos preentrenados para identificar el objeto principal
- 🎨 **Fondo blanco perfecto**: Convierte cualquier fondo a blanco puro RGB(255,255,255)
- 🔍 **PNG transparente**: Opción para crear imágenes PNG sin fondo (transparente)
- 🚀 **Fácil de usar**: Interfaz de línea de comandos simple
- 📁 **Procesamiento por lotes**: Procesa múltiples imágenes a la vez
- 🔧 **Personalizable**: Ajusta parámetros de segmentación según tus necesidades

## Ejemplos

### Resultados de Antes y Después

#### Ejemplo 1: Personaje
| Antes | Después (Fondo Blanco) | Después (Transparente) |
|-------|---------|---------|
| ![Imagen Original](examples/character.png) | ![Fondo Blanco](examples/character_new.jpg) | ![PNG Transparente](examples/character_transparent.png)
|*Imagen original con fondo colorido* | *Mismo personaje con fondo blanco puro* | *Solo el objeto, fondo transparente* |

### Comando utilizado:
```bash
# Crear JPG con Fondo Blanco
python main.py examples/character.png -o examples/character_new.jpg

# Crear PNG transparente
python main.py examples/character.png -o examples/character_transparent.png --output-format transparent-png
```

💡 **Nota**: 
- **Fondo blanco**: Todas las imágenes de salida mantienen el objeto principal intacto mientras el fondo se convierte a blanco puro RGB(255,255,255).
  
- **PNG transparente**: El fondo se remueve completamente, creando un PNG con canal alfa para transparencia perfecta.

## 📦 Instalación

<div align="center">

![Requirements](https://img.shields.io/badge/Requirements-Python%203.8+-blue.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)
![Dependencies](https://img.shields.io/badge/Dependencies-PyTorch%20%7C%20OpenCV%20%7C%20Pillow-orange.svg)

</div>

### 🔧 Instalación Automática

```bash
# 1. Clonar el repositorio
git clone https://github.com/dvchinx/Easy-Background.git
cd Easy-Background

# 2. Ejecutar instalador automático
# Windows
install.bat

# Linux/macOS
chmod +x install.sh && ./install.sh
```

### ⚙️ Instalación Manual

```bash
# 1. Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# o
venv\Scripts\activate     # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Instalar en modo desarrollo
pip install -e .
```

<div align="center">

**✅ ¡Listo para usar!** | **🧪 Ejecutar tests:** `pytest tests/` | **📖 Ver ejemplos:** `python main.py models`

</div>

## 🎮 Uso

<div align="center">

![CLI](https://img.shields.io/badge/Interface-Command%20Line-blue.svg)
![API](https://img.shields.io/badge/API-Python%20Module-green.svg)
![Batch](https://img.shields.io/badge/Processing-Single%20%7C%20Batch-orange.svg)

</div>

### 💻 Línea de Comandos

<div align="center">

| 🎨 **Fondo Blanco** | 🔍 **PNG Transparente** | 📁 **Procesamiento por Lotes** |
|:---:|:---:|:---:|
| `--output-format white-bg` | `--output-format transparent-png` | Procesa carpetas completas |

</div>

```bash
# 🎨 Procesar imagen con fondo blanco
python main.py input.jpg -o output.jpg

# 🔍 Crear PNG transparente (sin fondo)
python main.py input.jpg -o output.png --output-format transparent-png

# 📁 Procesar múltiples imágenes
python main.py *.jpg -o output_folder/

# ⚡ Usar modelo rápido con redimensionado
python main.py input.jpg -o output.jpg --model u2netp --resize 1024

# 🔄 Procesamiento en lote con PNGs transparentes
python main.py fotos/ -o resultados/ --output-format transparent-png
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

## 🤖 Modelos de IA Disponibles

<div align="center">

![Models](https://img.shields.io/badge/Models-5%20Available-blue.svg)
![Performance](https://img.shields.io/badge/Performance-GPU%20Optimized-green.svg)
![Accuracy](https://img.shields.io/badge/Accuracy-High%20Quality-orange.svg)

</div>

<div align="center">

| Modelo | Velocidad | Calidad | Uso Recomendado | Comando |
|:------:|:---------:|:-------:|:---------------:|:-------:|
| 🚀 **u2netp** | ⚡⚡⚡ | ⭐⭐⭐ | Procesamiento rápido | `--model u2netp` |
| 🎯 **u2net** | ⚡⚡ | ⭐⭐⭐⭐ | Uso general | `--model u2net` |
| 👤 **u2net_human_seg** | ⚡⚡ | ⭐⭐⭐⭐ | Personas y retratos | `--model u2net_human_seg` |
| 🎨 **silueta** | ⚡⚡ | ⭐⭐⭐ | Siluetas y contornos | `--model silueta` |
| 💎 **isnet-general-use** | ⚡ | ⭐⭐⭐⭐⭐ | Máxima calidad | `--model isnet-general-use` |

</div>

```bash
# Ver todos los modelos disponibles
python main.py models
```

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

## 📊 Dependencias Principales

<div align="center">

![rembg](https://img.shields.io/badge/rembg-2.0.57-blue.svg)
![Pillow](https://img.shields.io/badge/Pillow-10.0+-green.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.8+-red.svg)
![NumPy](https://img.shields.io/badge/NumPy-1.24+-yellow.svg)

</div>

- 🧠 **rembg**: Segmentación automática de fondo con IA
- 🖼️ **Pillow**: Manipulación y procesamiento de imágenes
- 📷 **OpenCV**: Procesamiento avanzado de computer vision
- 🔢 **NumPy**: Operaciones matriciales de alto rendimiento

## 🤝 Contribuir

<div align="center">

![Contributors](https://img.shields.io/badge/Contributors-Welcome-brightgreen.svg)
![PRs](https://img.shields.io/badge/PRs-Welcome-blue.svg)
![Issues](https://img.shields.io/badge/Issues-Open-orange.svg)

</div>

¡Las contribuciones son bienvenidas! Por favor:

1. 🍴 **Fork** el proyecto
2. 🌿 **Crea** una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. 💾 **Commit** tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. 📤 **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. 📋 **Abre** un Pull Request

## 📜 Licencia

<div align="center">

![License](https://img.shields.io/badge/License-MIT-green.svg)

Este proyecto está bajo la **Licencia MIT**. Ver el archivo [`LICENSE`](LICENSE) para más detalles.

</div>

## 🙏 Créditos y Agradecimientos

<div align="center">

![rembg](https://img.shields.io/badge/Powered%20by-rembg-blue.svg)
![AI](https://img.shields.io/badge/AI%20Models-Community%20Trained-orange.svg)

</div>

- 🚀 Utiliza la librería [**rembg**](https://github.com/danielgatis/rembg) para la segmentación de fondo
- 🧠 Modelos de IA entrenados por la comunidad open source
- 💡 Inspirado en la necesidad de herramientas de edición de imágenes accesibles

---

<div align="center">

**⭐ Si este proyecto te fue útil, ¡dale una estrella!** 

[![GitHub stars](https://img.shields.io/github/stars/dvchinx/White-Background?style=social)](https://github.com/dvchinx/Easy-Background/stargazers)

**🔗 Comparte con la comunidad**

</div>
