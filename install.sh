#!/bin/bash

# Script de instalación y configuración para White Background Generator
# Autor: Tu Nombre
# Fecha: $(date)

echo "🎨 Configurando White Background Generator..."

# Verificar Python
if ! command -v python &> /dev/null; then
    echo "❌ Error: Python no está instalado"
    exit 1
fi

# Verificar versión de Python
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo "🐍 Python detectado: $PYTHON_VERSION"

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python -m venv venv
fi

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo "⬆️  Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

# Instalar en modo desarrollo
echo "🔧 Instalando en modo desarrollo..."
pip install -e .

# Ejecutar tests
echo "🧪 Ejecutando tests..."
python -m pytest tests/ -v

# Crear imágenes de ejemplo
echo "🖼️  Creando imágenes de ejemplo..."
python tests/test_white_bg_generator.py --create-examples

# Probar instalación
echo "✅ Probando instalación..."
python main.py test

echo ""
echo "🎉 ¡Instalación completada!"
echo ""
echo "📋 Comandos útiles:"
echo "  • Activar entorno: source venv/bin/activate"
echo "  • Procesar imagen: python main.py imagen.jpg -o resultado.jpg"
echo "  • Ver ayuda: python main.py --help"
echo "  • Listar modelos: python main.py models"
echo "  • Ejecutar tests: python -m pytest tests/"
echo ""