@echo off
REM Script de instalación para Windows - Easy Background
REM Autor: Jesús Flórez

echo 🎨 Configurando Easy Background...

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python no está instalado
    pause
    exit /b 1
)

REM Mostrar versión de Python
echo 🐍 Python detectado:
python --version

REM Crear entorno virtual si no existe
if not exist "venv" (
    echo 📦 Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno virtual
echo 🔄 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Actualizar pip
echo ⬆️  Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo 📥 Instalando dependencias...
pip install -r requirements.txt

REM Instalar en modo desarrollo
echo 🔧 Instalando en modo desarrollo...
pip install -e .

REM Ejecutar tests
echo 🧪 Ejecutando tests...
python -m pytest tests/ -v

REM Crear imágenes de ejemplo
echo 🖼️  Creando imágenes de ejemplo...
python tests/test_white_bg_generator.py --create-examples

REM Probar instalación
echo ✅ Probando instalación...
python main.py test

echo.
echo 🎉 ¡Instalación completada!
echo.
echo 📋 Comandos útiles:
echo   • Activar entorno: venv\Scripts\activate.bat
echo   • Procesar imagen: python main.py imagen.jpg -o resultado.jpg
echo   • Ver ayuda: python main.py --help
echo   • Listar modelos: python main.py models
echo   • Ejecutar tests: python -m pytest tests/
echo.

pause
