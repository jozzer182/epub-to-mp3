import time
import re
from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup
import os
import subprocess
import torch

# === Configurar PyTorch para compatibilidad con XTTS ===
# Método alternativo: configurar torch.load para usar weights_only=False por defecto
import warnings

# Suprimir el warning sobre weights_only
warnings.filterwarnings("ignore", message="`gpu` will be deprecated")

# Parchear torch.load temporalmente
original_torch_load = torch.load

def patched_torch_load(*args, **kwargs):
    if 'weights_only' not in kwargs:
        kwargs['weights_only'] = False
    return original_torch_load(*args, **kwargs)

torch.load = patched_torch_load

from TTS.api import TTS

# === Iniciar temporizador ===
inicio = time.time()

# === Inicializar modelo XTTS con voz personalizada ===
try:
    tts = TTS(
        model_name="tts_models/multilingual/multi-dataset/xtts_v2",
        progress_bar=False,
        gpu=True
    )
    print("✅ Modelo cargado exitosamente (GPU)")
except Exception as e:
    print(f"❌ Error al cargar el modelo TTS: {e}")
    print("💡 Intentando cargar sin GPU...")
    try:
        tts = TTS(
            model_name="tts_models/multilingual/multi-dataset/xtts_v2",
            progress_bar=False,
            gpu=False
        )
        print("✅ Modelo cargado exitosamente (CPU)")
    except Exception as e2:
        print(f"❌ Error crítico al cargar TTS: {e2}")
        exit(1)

# === Configurar voz de referencia y lenguaje ===
voz_referencia = "vlc.wav"  # Cambia esto por tu archivo si usas otro
idioma = "es"

# === Buscar el primer archivo EPUB en la carpeta input ===
input_folder = "input"
epub_files = [f for f in os.listdir(input_folder) if f.endswith('.epub')]

if not epub_files:
    print("❌ No se encontraron archivos .epub en la carpeta 'input'")
    exit(1)

epub_path = os.path.join(input_folder, epub_files[0])
print(f"📖 Procesando archivo: {epub_path}")

# === Cargar el libro EPUB ===
libro = epub.read_epub(epub_path)

# === Crear carpeta de salida ===
os.makedirs('output', exist_ok=True)

def dividir_texto_en_fragmentos(texto, max_chars=400):
    """
    Divide un texto largo en fragmentos más pequeños respetando oraciones
    Incluye estrategia para dividir oraciones muy largas
    """
    if len(texto) <= max_chars:
        return [texto]
    
    # Dividir por oraciones
    oraciones = texto.split('. ')
    fragmentos = []
    fragmento_actual = ""
    
    for oracion in oraciones:
        oracion_completa = oracion + '. '
        
        # Si la oración es muy larga (más de max_chars), dividirla inteligentemente
        if len(oracion_completa) > max_chars:
            print(f"      📏 Oración muy larga detectada ({len(oracion_completa)} chars), dividiéndola...")
            
            # Guardar fragmento actual si existe
            if fragmento_actual:
                fragmentos.append(fragmento_actual.strip())
                fragmento_actual = ""
            
            # Dividir la oración larga por diferentes separadores
            sub_fragmentos = dividir_oracion_larga(oracion, max_chars)
            fragmentos.extend(sub_fragmentos)
            
        # Si agregar esta oración no excede el límite
        elif len(fragmento_actual + oracion_completa) <= max_chars:
            fragmento_actual += oracion_completa
        else:
            # Guardar el fragmento actual y empezar uno nuevo
            if fragmento_actual:
                fragmentos.append(fragmento_actual.strip())
            fragmento_actual = oracion_completa
    
    # Agregar el último fragmento
    if fragmento_actual:
        fragmentos.append(fragmento_actual.strip())
    
    return fragmentos

def dividir_oracion_larga(oracion, max_chars):
    """
    Divide una oración muy larga usando múltiples estrategias
    """
    # Lista de separadores en orden de preferencia
    separadores = [
        ' Capítulo ',  # Separar por capítulos
        ' Regla ',     # Separar por reglas
        ' Conclusión ', # Separar por conclusiones
        ', ',          # Separar por comas
        ' y ',         # Separar por conjunciones
        ' de ',        # Separar por preposiciones
        ' ',           # Último recurso: separar por espacios
    ]
    
    fragmentos = []
    texto_restante = oracion
    
    while len(texto_restante) > max_chars:
        mejor_corte = -1
        mejor_separador = None
        
        # Buscar el mejor punto de corte
        for separador in separadores:
            # Buscar el último separador que permita un fragmento <= max_chars
            pos = 0
            while True:
                siguiente_pos = texto_restante.find(separador, pos)
                if siguiente_pos == -1:  # No se encontró más este separador
                    break
                
                fragmento_candidato = texto_restante[:siguiente_pos + len(separador)]
                if len(fragmento_candidato) <= max_chars:
                    mejor_corte = siguiente_pos + len(separador)
                    mejor_separador = separador
                    pos = siguiente_pos + 1
                else:
                    break  # Ya es demasiado largo
        
        # Si encontramos un buen punto de corte
        if mejor_corte > 0:
            fragmento = texto_restante[:mejor_corte].strip()
            if fragmento:
                fragmentos.append(fragmento + '.')
            texto_restante = texto_restante[mejor_corte:].strip()
        else:
            # Último recurso: cortar a max_chars
            fragmento = texto_restante[:max_chars].strip()
            if fragmento:
                fragmentos.append(fragmento + '...')
            texto_restante = texto_restante[max_chars:].strip()
    
    # Agregar lo que queda
    if texto_restante:
        fragmentos.append(texto_restante.strip() + '.')
    
    return fragmentos

# === Función para limpiar nombres de archivo ===
def limpiar_nombre(texto):
    texto = texto.strip().replace('\n', ' ')
    texto = re.sub(r'[\\/*?:"<>|]', '', texto)
    texto = re.sub(r'\s+', ' ', texto)
    return texto[:60]

# === Procesar cada capítulo ===
capitulo = 1
for item in libro.get_items():
    if item.get_type() == ITEM_DOCUMENT:
        soup = BeautifulSoup(item.get_content(), 'html.parser')
        texto = soup.get_text(separator=' ', strip=True)

        if len(texto.strip()) < 200:
            continue

        titulo = soup.find(['h1', 'h2', 'h3'])
        if titulo:
            nombre_base = f"{capitulo:02d}. {limpiar_nombre(titulo.get_text())}"
        else:
            nombre_base = f"{capitulo:02d}. capitulo_{capitulo:02d}"

        print(f"🎧 Procesando: {nombre_base}...")
        print(f"   📝 Longitud del texto: {len(texto)} caracteres")

        # Dividir texto en fragmentos si es muy largo
        fragmentos = dividir_texto_en_fragmentos(texto)
        print(f"   🔄 Dividido en {len(fragmentos)} fragmento(s)")

        # Procesar cada fragmento
        audios_fragmentos = []
        temp_folder = f"output/temp_{capitulo:02d}"
        
        # Crear carpeta temporal para fragmentos si hay más de uno
        if len(fragmentos) > 1:
            os.makedirs(temp_folder, exist_ok=True)
        
        for i, fragmento in enumerate(fragmentos):
            if len(fragmentos) > 1:
                # Usar carpeta temporal para fragmentos
                fragmento_nombre = f"fragmento_{i+1:02d}"
                wav_path = f"{temp_folder}/{fragmento_nombre}.wav"
                mp3_path = f"{temp_folder}/{fragmento_nombre}.mp3"
            else:
                # Si solo hay un fragmento, usar directamente el nombre final
                wav_path = f"output/{nombre_base}.wav"
                mp3_path = f"output/{nombre_base}.mp3"
            
            # Generar audio con XTTS
            try:
                # Verificar que el archivo de voz existe antes de intentar usarlo
                if not os.path.exists(voz_referencia):
                    print(f"❌ Error: No se encuentra el archivo de voz '{voz_referencia}'")
                    continue
                    
                print(f"      🎤 Generando fragmento {i+1}/{len(fragmentos)} ({len(fragmento)} chars)...")
                
                tts.tts_to_file(
                    text=fragmento,
                    speaker_wav=voz_referencia,
                    language=idioma,
                    file_path=wav_path
                )

                # Convertir a MP3
                subprocess.run(["ffmpeg", "-y", "-i", wav_path, mp3_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                # Eliminar archivo WAV temporal solo si la conversión fue exitosa
                if os.path.exists(mp3_path):
                    os.remove(wav_path)
                    audios_fragmentos.append(mp3_path)
                    print(f"      ✅ Fragmento {i+1} completado")
                else:
                    print(f"      ⚠️ Error en conversión a MP3 para fragmento {i+1}")

            except Exception as e:
                print(f"      ⚠️ Error al procesar fragmento {i+1}: {e}")
                # Mostrar información adicional para debug
                print(f"         - Archivo de voz: {voz_referencia} (existe: {os.path.exists(voz_referencia)})")
                print(f"         - Tamaño del fragmento: {len(fragmento)} caracteres")
                if "400 tokens" in str(e):
                    print("         💡 Sugerencia: El fragmento sigue siendo demasiado largo, reduciendo tamaño...")
                continue

        # Concatenar fragmentos si hay más de uno
        if len(audios_fragmentos) > 1:
            print(f"   🔗 Concatenando {len(audios_fragmentos)} fragmentos en un solo archivo...")
            
            # Crear archivo final
            archivo_final = f"output/{nombre_base}.mp3"
            
            # Verificar que todos los archivos de fragmentos existen
            fragmentos_validos = []
            for archivo in audios_fragmentos:
                if os.path.exists(archivo):
                    fragmentos_validos.append(archivo)
                else:
                    print(f"      ⚠️ Fragmento no encontrado: {archivo}")
            
            if len(fragmentos_validos) == 0:
                print(f"   ❌ No hay fragmentos válidos para concatenar en {nombre_base}")
                capitulo += 1
                continue
            
            # Crear lista de archivos para ffmpeg
            lista_archivos = f"{temp_folder}/lista_archivos.txt"
            try:
                with open(lista_archivos, 'w', encoding='utf-8') as f:
                    for archivo in fragmentos_validos:
                        # Usar rutas absolutas para evitar problemas
                        archivo_absoluto = os.path.abspath(archivo)
                        f.write(f"file '{archivo_absoluto}'\n")
                
                print(f"      📝 Lista de archivos creada con {len(fragmentos_validos)} fragmentos")
                
                # Concatenar con ffmpeg
                concat_cmd = [
                    "ffmpeg", "-y", "-f", "concat", "-safe", "0", 
                    "-i", lista_archivos, "-c", "copy", archivo_final
                ]
                
                print(f"      🔧 Ejecutando concatenación...")
                result = subprocess.run(concat_cmd, capture_output=True, text=True)
                
                if result.returncode == 0 and os.path.exists(archivo_final):
                    print(f"   ✅ Concatenación exitosa: {nombre_base}.mp3")
                    
                    # Limpiar archivos temporales
                    import shutil
                    shutil.rmtree(temp_folder)
                    print(f"   🧹 Archivos temporales eliminados")
                    
                else:
                    print(f"   ⚠️ Error en la concatenación de {nombre_base}")
                    print(f"      📋 Código de error: {result.returncode}")
                    if result.stderr:
                        print(f"      📋 Error detallado: {result.stderr[:200]}...")
                    
                    # Intentar usar el primer fragmento como respaldo
                    if fragmentos_validos:
                        print(f"      🔄 Usando primer fragmento como respaldo...")
                        import shutil
                        shutil.copy2(fragmentos_validos[0], archivo_final)
                        if os.path.exists(archivo_final):
                            print(f"   ✅ Archivo de respaldo creado: {nombre_base}.mp3")
                        
                        # Limpiar archivos temporales
                        shutil.rmtree(temp_folder)
                        print(f"   🧹 Archivos temporales eliminados")
                        
            except Exception as e:
                print(f"   ⚠️ Error al concatenar fragmentos: {e}")
                print(f"      📋 Detalles: {str(e)[:200]}...")
                
                # Intentar usar el primer fragmento como respaldo
                if fragmentos_validos:
                    print(f"      🔄 Usando primer fragmento como respaldo...")
                    try:
                        import shutil
                        archivo_final = f"output/{nombre_base}.mp3"
                        shutil.copy2(fragmentos_validos[0], archivo_final)
                        if os.path.exists(archivo_final):
                            print(f"   ✅ Archivo de respaldo creado: {nombre_base}.mp3")
                        
                        # Limpiar archivos temporales
                        if os.path.exists(temp_folder):
                            shutil.rmtree(temp_folder)
                            print(f"   🧹 Archivos temporales eliminados")
                    except Exception as e2:
                        print(f"      ❌ Error también en respaldo: {e2}")
        
        elif len(audios_fragmentos) == 1:
            # Solo un fragmento, ya está en la ubicación correcta
            print(f"   ✅ Fragmento único procesado directamente")
        
        # Mostrar resumen del capítulo
        archivo_final_path = f"output/{nombre_base}.mp3"
        if os.path.exists(archivo_final_path):
            print(f"✅ {nombre_base} completado (archivo único generado)")
        else:
            print(f"❌ {nombre_base} falló completamente")

        capitulo += 1

# === Mostrar tiempo total ===
fin = time.time()
print("✅ Conversión completada.")
print(f"⏱️ Tiempo total: {fin - inicio:.2f} segundos")
