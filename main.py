import time
import re
from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup
from TTS.api import TTS
import os
import subprocess

# === Iniciar temporizador ===
inicio = time.time()

# === Inicializar modelo XTTS con voz personalizada ===
tts = TTS(
    model_name="tts_models/multilingual/multi-dataset/xtts_v2",
    progress_bar=False,
    gpu=True
)

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

        wav_path = f"output/{nombre_base}.wav"
        mp3_path = f"output/{nombre_base}.mp3"

        print(f"🎧 Procesando: {nombre_base}...")

        # Generar audio con XTTS
        try:
            tts.tts_to_file(
                text=texto,
                speaker_wav=voz_referencia,
                language=idioma,
                file_path=wav_path
            )

            # Convertir a MP3
            subprocess.run(["ffmpeg", "-y", "-i", wav_path, mp3_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            os.remove(wav_path)

        except Exception as e:
            print(f"⚠️ Error al procesar {nombre_base}: {e}")

        capitulo += 1

# === Mostrar tiempo total ===
fin = time.time()
print("✅ Conversión completada.")
print(f"⏱️ Tiempo total: {fin - inicio:.2f} segundos")
