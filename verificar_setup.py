#!/usr/bin/env python3
"""
Script de verificación de archivos necesarios para epub-to-mp3
Ejecuta este script antes de usar main.py para asegurar que todo esté configurado correctamente
"""

import os
import sys
from pathlib import Path

def verificar_estructura():
    """
    Verifica que todos los archivos y carpetas necesarios estén presentes
    """
    print("🔍 Verificando estructura del proyecto...")
    
    # Lista de archivos/carpetas requeridos
    requeridos = {
        'main.py': 'archivo',
        'requirements.txt': 'archivo', 
        'vlc.wav': 'archivo',
        'input/': 'carpeta',
        'output/': 'carpeta'
    }
    
    errores = []
    advertencias = []
    
    # Verificar cada elemento
    for item, tipo in requeridos.items():
        ruta = Path(item)
        
        if tipo == 'archivo':
            if not ruta.exists():
                errores.append(f"❌ Falta el archivo: {item}")
            elif ruta.stat().st_size == 0:
                advertencias.append(f"⚠️  El archivo {item} está vacío")
            else:
                print(f"✅ {item} - OK")
        
        elif tipo == 'carpeta':
            if not ruta.exists():
                errores.append(f"❌ Falta la carpeta: {item}")
            else:
                print(f"✅ {item} - OK")
    
    # Verificación especial para input/
    input_dir = Path('input')
    if input_dir.exists():
        epub_files = list(input_dir.glob('*.epub'))
        if not epub_files:
            advertencias.append("⚠️  No hay archivos .epub en la carpeta 'input/'")
        else:
            print(f"📚 Encontrado(s) {len(epub_files)} archivo(s) .epub en input/")
    
    # Verificación especial para vlc.wav
    vlc_path = Path('vlc.wav')
    if vlc_path.exists():
        size = vlc_path.stat().st_size
        if size < 100000:  # Menos de ~100KB probablemente es muy corto
            advertencias.append("⚠️  El archivo vlc.wav parece muy pequeño (¿menos de 6 segundos?)")
        else:
            print(f"🎤 vlc.wav - {size//1000}KB (tamaño adecuado)")
    
    # Mostrar resultados
    print("\n" + "="*50)
    
    if errores:
        print("🚨 ERRORES ENCONTRADOS:")
        for error in errores:
            print(f"   {error}")
        print("\n💡 Para solucionar:")
        if "vlc.wav" in str(errores):
            print("   • Graba tu voz en formato WAV (6-30 segundos)")
            print("   • Nómbralo exactamente 'vlc.wav'")
            print("   • Colócalo en la raíz del proyecto")
        if "input/" in str(errores):
            print("   • Crea la carpeta 'input/'")
        if "output/" in str(errores):
            print("   • Crea la carpeta 'output/'")
    
    if advertencias:
        print("\n⚠️  ADVERTENCIAS:")
        for advertencia in advertencias:
            print(f"   {advertencia}")
    
    if not errores and not advertencias:
        print("🎉 ¡Todo está configurado correctamente!")
        print("   Puedes ejecutar: python main.py")
    elif not errores:
        print("✅ Configuración básica completa")
        print("   Puedes continuar, pero revisa las advertencias")
    else:
        print("❌ Corrige los errores antes de continuar")
        return False
    
    print("="*50)
    return len(errores) == 0

def verificar_dependencias():
    """
    Verifica que las dependencias necesarias estén instaladas
    """
    print("\n🔍 Verificando dependencias de Python...")
    
    dependencias = [
        ('TTS', 'TTS'),
        ('torch', 'torch'), 
        ('ebooklib', 'ebooklib'),
        ('beautifulsoup4', 'bs4')
    ]
    
    faltantes = []
    
    for nombre_paquete, modulo_import in dependencias:
        try:
            __import__(modulo_import)
            print(f"✅ {nombre_paquete} - Instalado")
        except ImportError:
            faltantes.append(nombre_paquete)
            print(f"❌ {nombre_paquete} - No encontrado")
    
    if faltantes:
        print(f"\n💡 Para instalar las dependencias faltantes:")
        print(f"   pip install {' '.join(faltantes)}")
        return False
    
    print("✅ Todas las dependencias están instaladas")
    return True

def main():
    print("🔧 epub-to-mp3 - Verificador de configuración")
    print("="*50)
    
    estructura_ok = verificar_estructura()
    dependencias_ok = verificar_dependencias()
    
    print("\n" + "="*50)
    if estructura_ok and dependencias_ok:
        print("🎉 ¡Configuración completa! Ejecuta: python main.py")
    else:
        print("⚠️  Corrige los problemas encontrados antes de continuar")
        sys.exit(1)

if __name__ == "__main__":
    main()
