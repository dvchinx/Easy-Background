# Makefile para Easy Background

.PHONY: install test clean lint format examples help

# Variables
PYTHON = python
VENV = .venv
VENV_PYTHON = $(VENV)/Scripts/python.exe
PIP = $(VENV_PYTHON) -m pip

# Comandos principales
help: ## Mostrar esta ayuda
	@echo "Easy Background - Comandos disponibles:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-15s %s\n", $$1, $$2}'

install: ## Instalar dependencias y configurar entorno
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install -e .
	@echo "✅ Instalación completada"

test: ## Ejecutar todos los tests
	$(VENV_PYTHON) -m pytest tests/ -v
	@echo "✅ Tests completados"

examples: ## Crear imágenes de ejemplo
	$(VENV_PYTHON) tests/test_white_bg_generator.py --create-examples
	@echo "✅ Ejemplos creados en examples/"

demo: examples ## Ejecutar demo con imágenes de ejemplo
	$(VENV_PYTHON) main.py examples/simple_circle.jpg -o examples/output_simple.jpg -v
	$(VENV_PYTHON) main.py examples/multiple_objects.jpg -o examples/output_multiple.jpg -v
	$(VENV_PYTHON) main.py examples/gradient_background.jpg -o examples/output_gradient.jpg -v
	@echo "✅ Demo completado - revisa examples/"

lint: ## Verificar código con flake8
	$(VENV_PYTHON) -m flake8 src/ tests/ main.py --max-line-length=88 --ignore=E203,W503

format: ## Formatear código con black
	$(VENV_PYTHON) -m black src/ tests/ main.py

models: ## Listar modelos disponibles
	$(VENV_PYTHON) main.py models

test-basic: ## Probar funcionalidad básica
	$(VENV_PYTHON) main.py test

clean: ## Limpiar archivos temporales y cache
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/
	@echo "✅ Limpieza completada"

dist: ## Crear distribución
	$(VENV_PYTHON) setup.py sdist bdist_wheel

upload: dist ## Subir a PyPI (requiere configuración)
	$(VENV_PYTHON) -m twine upload dist/*

dev-install: ## Instalación para desarrollo
	$(PIP) install -e ".[dev]"

benchmark: ## Ejecutar benchmark básico
	@echo "Ejecutando benchmark..."
	$(VENV_PYTHON) -c "import time; from src.background_remover import BackgroundRemover; from PIL import Image; img = Image.new('RGB', (1024, 1024), 'red'); gen = BackgroundRemover(); start = time.time(); gen.process_image(img); print(f'Tiempo: {time.time()-start:.2f}s')"

# Comandos de desarrollo
dev: install examples test-basic ## Configuración completa para desarrollo
	@echo "🎉 Entorno de desarrollo listo!"
	@echo "Ejecuta: $(VENV_PYTHON) main.py --help"