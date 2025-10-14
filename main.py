"""
White Background Generator - CLI
Interfaz de línea de comandos para cambiar fondos de imágenes a blanco
"""

import os
import sys
import glob
import time
from pathlib import Path
from typing import List, Optional

import click
from PIL import Image

# Agregar el directorio src al path para importar módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.white_bg_generator import WhiteBGGenerator
    from src.utils import validate_image_path, get_file_list, format_file_size
except ImportError as e:
    print(f"Error importando módulos: {e}")
    print("Asegúrate de estar en el directorio raíz del proyecto")
    sys.exit(1)


@click.command()
@click.argument('input_path', type=click.Path(exists=True))
@click.option('-o', '--output', type=click.Path(), 
              help='Ruta de salida (archivo o directorio)')
@click.option('-m', '--model', default='u2net',
              type=click.Choice(['u2net', 'u2netp', 'u2net_human_seg', 'silueta', 'isnet-general-use']),
              help='Modelo de segmentación a usar')
@click.option('--resize', type=int, metavar='SIZE',
              help='Redimensionar imagen a tamaño máximo (mantiene proporción)')
@click.option('--prefix', default='white_bg_',
              help='Prefijo para archivos de salida en procesamiento por lotes')
@click.option('--recursive', '-r', is_flag=True,
              help='Buscar imágenes recursivamente en subdirectorios')
@click.option('--quality', default=95, type=click.IntRange(1, 100),
              help='Calidad de compresión JPEG (1-100)')
@click.option('--verbose', '-v', is_flag=True,
              help='Mostrar información detallada')
@click.option('--gpu/--no-gpu', default=True,
              help='Usar GPU para acelerar procesamiento')
@click.option('--output-format', default='white-bg',
              type=click.Choice(['white-bg', 'transparent-png']),
              help='Formato de salida: fondo blanco o PNG transparente')
def main(input_path: str, output: Optional[str], model: str, resize: Optional[int],
         prefix: str, recursive: bool, quality: int, verbose: bool, gpu: bool, output_format: str):
    """
    Procesa imágenes para cambiar el fondo a blanco o crear PNG transparente.
    
    INPUT_PATH puede ser un archivo de imagen o un directorio con imágenes.
    
    Ejemplos:
    
    \b
        # Procesar una imagen con fondo blanco
        python main.py imagen.jpg -o resultado.jpg
        
        # Crear PNG transparente
        python main.py imagen.jpg -o resultado.png --output-format transparent-png
        
        # Procesar todas las imágenes de un directorio
        python main.py fotos/ -o resultados/
        
        # Usar modelo específico y redimensionar
        python main.py imagen.jpg -o resultado.jpg -m u2netp --resize 1024
        
        # Procesar recursivamente con PNG transparente
        python main.py fotos/ -o resultados/ -r --output-format transparent-png
    """
    
    # Configurar logging si es verbose
    if verbose:
        import logging
        logging.basicConfig(level=logging.INFO, 
                          format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Mostrar información inicial
    click.echo(click.style("🎨 White Background Generator", fg='blue', bold=True))
    click.echo(f"Modelo: {model}")
    click.echo(f"Formato de salida: {'PNG transparente' if output_format == 'transparent-png' else 'Fondo blanco'}")
    
    try:
        # Inicializar generador
        click.echo("Inicializando generador...")
        generator = WhiteBGGenerator(model_name=model, enable_gpu=gpu)
        
        # Mostrar información del modelo
        if verbose:
            model_info = generator.get_model_info()
            click.echo(f"Información del modelo: {model_info}")
        
        # Obtener lista de archivos
        if os.path.isfile(input_path):
            if not validate_image_path(input_path):
                click.echo(click.style(f"❌ Error: {input_path} no es una imagen válida", fg='red'))
                return
            
            image_files = [input_path]
            click.echo(f"📁 Procesando archivo: {os.path.basename(input_path)}")
            
        elif os.path.isdir(input_path):
            image_files = get_file_list(input_path, recursive=recursive)
            if not image_files:
                click.echo(click.style(f"❌ No se encontraron imágenes en {input_path}", fg='red'))
                return
            
            click.echo(f"📁 Encontradas {len(image_files)} imágenes en {input_path}")
            
        else:
            click.echo(click.style(f"❌ Error: {input_path} no existe", fg='red'))
            return
        
        # Determinar rutas de salida
        if not output:
            # Generar nombre de salida automático
            if len(image_files) == 1:
                input_file = image_files[0]
                name, ext = os.path.splitext(input_file)
                if output_format == 'transparent-png':
                    output = f"{name}_transparent.png"
                else:
                    output = f"{name}_white_bg{ext}"
            else:
                output = "output/"
        
        # Procesar archivos
        start_time = time.time()
        
        if len(image_files) == 1:
            # Procesar archivo único
            input_file = image_files[0]
            click.echo(f"🔄 Procesando: {os.path.basename(input_file)}")
            
            # Ajustar extensión según formato de salida
            if output_format == 'transparent-png' and output and not output.lower().endswith('.png'):
                name, _ = os.path.splitext(output)
                output = f"{name}.png"
            
            with click.progressbar(length=100, label='Procesando') as bar:
                if output_format == 'transparent-png':
                    # Solo remover fondo, mantener transparencia
                    result = generator.remove_background(input_file)
                    if resize:
                        from src.utils import resize_image
                        result = resize_image(result, resize)
                    if output:
                        from src.utils import ensure_output_directory
                        ensure_output_directory(output)
                        result.save(output, "PNG")
                else:
                    # Procesamiento normal con fondo blanco
                    result = generator.process_image(
                        input_file, 
                        output_path=output,
                        resize_max=resize
                    )
                bar.update(100)
            
            # Mostrar información del resultado
            if os.path.exists(output):
                file_size = format_file_size(os.path.getsize(output))
                click.echo(click.style(f"✅ Completado: {output} ({file_size})", fg='green'))
            
        else:
            # Procesamiento por lotes
            if not os.path.isdir(output):
                os.makedirs(output, exist_ok=True)
            
            click.echo(f"🔄 Procesando {len(image_files)} imágenes...")
            
            success_count = 0
            with click.progressbar(image_files, label='Procesando imágenes') as bar:
                for input_file in bar:
                    try:
                        # Generar nombre de salida
                        filename = os.path.basename(input_file)
                        name, ext = os.path.splitext(filename)
                        
                        # Ajustar extensión según formato de salida
                        if output_format == 'transparent-png':
                            output_file = os.path.join(output, f"{prefix}{name}.png")
                        else:
                            output_file = os.path.join(output, f"{prefix}{name}{ext}")
                        
                        # Procesar imagen según formato
                        if output_format == 'transparent-png':
                            # Solo remover fondo, mantener transparencia
                            result = generator.remove_background(input_file)
                            if resize:
                                from src.utils import resize_image
                                result = resize_image(result, resize)
                            result.save(output_file, "PNG")
                        else:
                            # Procesamiento normal con fondo blanco
                            generator.process_image(
                                input_file,
                                output_path=output_file,
                                resize_max=resize
                            )
                        success_count += 1
                        
                    except Exception as e:
                        if verbose:
                            click.echo(f"\n❌ Error procesando {filename}: {e}")
                        continue
            
            click.echo(click.style(f"✅ Completado: {success_count}/{len(image_files)} imágenes procesadas", fg='green'))
        
        # Mostrar tiempo total
        elapsed_time = time.time() - start_time
        click.echo(f"⏱️  Tiempo total: {elapsed_time:.2f} segundos")
        
    except KeyboardInterrupt:
        click.echo(click.style("\n⏹️  Procesamiento cancelado por el usuario", fg='yellow'))
        
    except Exception as e:
        click.echo(click.style(f"❌ Error: {e}", fg='red'))
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


@click.group()
def cli():
    """White Background Generator - Herramientas para cambiar fondos a blanco"""
    pass


@cli.command()
def models():
    """Lista los modelos de segmentación disponibles"""
    click.echo(click.style("🤖 Modelos disponibles:", fg='blue', bold=True))
    
    models_info = {
        'u2net': 'Modelo general, bueno para la mayoría de objetos',
        'u2netp': 'Versión ligera y rápida de U2Net',
        'u2net_human_seg': 'Optimizado para personas y figuras humanas',
        'silueta': 'Especializado en siluetas y contornos',
        'isnet-general-use': 'Modelo de alta calidad para objetos complejos'
    }
    
    for model, description in models_info.items():
        click.echo(f"  • {click.style(model, fg='green', bold=True)}: {description}")


@cli.command()
@click.option('--model', default='u2net', help='Modelo a probar')
def test(model: str):
    """Prueba si el generador funciona correctamente"""
    click.echo(click.style("🧪 Probando White Background Generator...", fg='blue', bold=True))
    
    try:
        # Crear imagen de prueba
        from PIL import Image, ImageDraw
        
        test_image = Image.new('RGB', (300, 300), color='red')
        draw = ImageDraw.Draw(test_image)
        draw.ellipse([50, 50, 250, 250], fill='blue')
        
        # Inicializar generador
        generator = WhiteBGGenerator(model_name=model)
        
        # Mostrar información
        model_info = generator.get_model_info()
        click.echo(f"Modelo: {model_info['model_name']}")
        click.echo(f"REMBG disponible: {model_info['rembg_available']}")
        click.echo(f"Sesión cargada: {model_info['session_loaded']}")
        
        # Procesar imagen de prueba
        result = generator.process_image(test_image)
        
        click.echo(click.style("✅ Prueba exitosa - El generador funciona correctamente", fg='green'))
        
    except Exception as e:
        click.echo(click.style(f"❌ Error en la prueba: {e}", fg='red'))


if __name__ == '__main__':
    # Si se ejecuta directamente, usar el comando principal
    if len(sys.argv) == 1:
        cli(['--help'])
    else:
        # Detectar si es comando del grupo o comando principal
        if sys.argv[1] in ['models', 'test']:
            cli()
        else:
            main()