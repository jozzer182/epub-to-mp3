# 📚 epub-to-mp3

Convierte automáticamente el **primer archivo EPUB** encontrado en la carpeta `input/` a una serie de **audiocapítulos en MP3**, utilizando el modelo TTS **xtts_v2** de [Coqui.ai](https://github.com/coqui-ai/TTS). Todo el proceso se realiza **completamente offline** y con soporte para **voz personalizada y multilingüe**.

---

## 🚀 Características

- 🎙️ Conversión de texto a voz con calidad natural (modelo `xtts_v2`)
- 🧠 Compatible con español, inglés y otros idiomas
- 🧾 Extrae y limpia el texto desde capítulos EPUB
- ✂️ División automática de textos largos en fragmentos manejables
- � Concatenación automática de fragmentos en un MP3 único por capítulo
- �🗂️ Genera archivos MP3 con nombres amigables
- ⚡ Totalmente offline (requiere GPU para mejor rendimiento)
- 🔧 Manejo robusto de errores con diagnóstico detallado
- 🧹 Limpieza automática de archivos temporales

---

## 🛠️ Requisitos

- Python **3.10** (específicamente requerido para compatibilidad con el modelo xtts_v2)
- NVIDIA GPU (recomendado)
- [ffmpeg](https://ffmpeg.org/) instalado y accesible desde terminal
- Archivo de voz de referencia (`vlc.wav`) ubicado en la raíz del proyecto

---

## 📦 Instalación

En tu terminal ejecuta lo siguiente para configurar el entorno correctamente:

```bash
:: Crear entorno virtual (opcional pero recomendado)
py -3.10 -m venv venv-epub2mp3
venv-epub2mp3\Scripts\activate

# En Linux/MacOS usa:
# source venv-epub2mp3/bin/activate

# Clonar el repositorio
git clone https://github.com/jozzer182/epub-to-mp3.git
cd epub-to-mp3

# Instalar dependencias
pip install -r requirements.txt
```

---

### 💻 Si trabajas con Visual Studio Code

1. Abre VS Code.
2. Ve al menú `Archivo` → `Abrir carpeta...` y selecciona la carpeta `epub-to-mp3`.
3. Abre la paleta de comandos con `Ctrl+Shift+P` (o `F1`).
4. Escribe y selecciona: `Python: Select Interpreter`.
5. Elige el entorno `venv-epub2mp3` (debería aparecer con la ruta `./venv-epub2mp3/Scripts/python.exe` o similar).
6. Abre el archivo `main.py` y presiona `F5` o haz clic en el botón ▶️ para ejecutar.

> Esto asegura que estás usando el entorno virtual correcto dentro de VS Code.

---

### 🧪 ¿Tienes problemas para ejecutar el modelo?

**Para PyTorch 2.6+ (Error de weights_only):**
Si ves un error sobre `weights_only` o `WeightsUnpickler`, ejecuta primero el script de configuración:

```bash
python fix_pytorch.py
```

Este script configura PyTorch para ser compatible con XTTS v2. Una vez ejecutado exitosamente, puedes usar `python main.py` normalmente.

**Para PyTorch 2.9+ (Versiones más recientes):**
Si ya tienes una versión más nueva de PyTorch (como 2.9.0) y **no quieres cambiarla**, simplemente:

1. Instala las dependencias básicas sin tocar PyTorch:
   ```bash
   pip install beautifulsoup4 ebooklib transformers==4.36.2
   pip install git+https://github.com/coqui-ai/TTS.git --no-deps
   ```

2. Ejecuta el script de configuración:
   ```bash
   python fix_pytorch.py
   ```

3. Ejecuta el programa normalmente:
   ```bash
   python main.py
   ```

> ✅ **Comprobado exitosamente con PyTorch 2.9.0.dev20250716+cu129 en GPU RTX 5060**

**Para GPU GTX 1060:**
Si estás usando una tarjeta gráfica **GTX 1060** y los pasos de instalación generales no funcionan, puedes intentar con esta secuencia que ha sido comprobada exitosamente:

```bash
py -3.10 -m venv venv-epub2mp3
venv-epub2mp3\Scripts\activate
python -m pip install --upgrade pip
pip install git+https://github.com/coqui-ai/TTS.git
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 
pip install transformers==4.36.2 --force-reinstall
pip install numpy==1.22.0 --force-reinstall
pip install beautifulsoup4 ebooklib
pip install -r requirements.txt
```

> Estos pasos fueron validados con una GPU NVIDIA GTX 1060. Si estás usando una tarjeta diferente (por ejemplo, RTX 4060 o 5060), es posible que las versiones de PyTorch y `torchaudio` deban ajustarse.  
> Si ves errores, consulta con ChatGPT copiando el mensaje de error para recibir ayuda personalizada según tu sistema.

---

## 📁 Estructura esperada

```
epub-to-mp3/
├── main.py
├── requirements.txt
├── vlc.wav              ← ⚠️ IMPORTANTE: archivo de voz de referencia (debes crearlo)
├── input/               ← coloca aquí tu archivo .epub
└── output/              ← carpeta vacía, donde se generarán los archivos .mp3
```

### 🎤 Sobre el archivo de voz de referencia (`vlc.wav`)

El archivo `vlc.wav` es **tu voz de referencia** que el modelo XTTS utilizará para clonar tu voz. 

**Características requeridas:**
- **Formato**: WAV (no MP3)
- **Duración**: 6-10 segundos mínimo (ideal: 10-30 segundos)
- **Calidad**: Audio claro, sin ruido de fondo
- **Contenido**: Lee una frase en el idioma que desees usar (español recomendado)

**Ejemplo de texto para grabar:**
> "Hola, mi nombre es [tu nombre] y esta es mi voz de referencia para el sistema de texto a voz. Hablo con claridad y naturalidad."

**Cómo crear el archivo:**
1. Usa cualquier grabadora (Windows Voice Recorder, Audacity, etc.)
2. Graba el audio en un lugar silencioso
3. Guarda como WAV con el nombre exacto `vlc.wav`
4. Colócalo en la raíz del proyecto (misma carpeta que `main.py`)

---

## ▶️ Uso

```bash
python main.py
```

### 🔄 Proceso de conversión

El programa sigue estos pasos para cada capítulo:

1. **📖 Extracción**: Lee el contenido del archivo EPUB
2. **✂️ División**: Si el texto es muy largo (>800 caracteres), lo divide en fragmentos manejables
3. **🎤 Síntesis**: Genera audio para cada fragmento usando tu voz de referencia
4. **🔗 Concatenación**: Si hay múltiples fragmentos, los une en un solo archivo MP3
5. **🧹 Limpieza**: Elimina archivos temporales automáticamente

**Resultado final**: Un archivo MP3 completo por cada capítulo del libro.

### ⚠️ Manejo de errores comunes

**Fragmentos demasiado largos:**
Si ves mensajes como `XTTS can only generate text with a maximum of 400 tokens`, el programa automáticamente:
- Omite el fragmento problemático
- Continúa con los fragmentos restantes
- Concatena solo los fragmentos exitosos
- Reporta cuántos fragmentos se procesaron vs. el total

**Capítulos que fallan completamente:**
- El programa continúa con el siguiente capítulo
- Se registra un mensaje `❌ [nombre] falló completamente`
- No se genera MP3 para ese capítulo específico
- El proceso global continúa normalmente

> 💡 **Tip**: Si un capítulo específico falla constantemente, puede contener mucho texto técnico o caracteres especiales. Estos casos son raros y no afectan el procesamiento del resto del libro.

---

## 📌 Badges

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Offline-TTS](https://img.shields.io/badge/TTS-Offline%20xtts_v2-critical?logo=soundcloud)
![Status](https://img.shields.io/badge/Estado-Activo-brightgreen)

---

## 📜 Licencia

Este proyecto se publica bajo la licencia MIT. Eres libre de usarlo, modificarlo y compartirlo.

---

## 💡 Créditos

Desarrollado por [@jozzer182](https://github.com/jozzer182) como primer repositorio público. Utiliza tecnologías de:

- [Coqui TTS](https://github.com/coqui-ai/TTS)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [EbookLib](https://github.com/aerkalov/ebooklib)

---

## 🌱 Siguiente paso

Puedes ampliar este proyecto para:
- Soportar múltiples archivos EPUB
- Agregar un lector de PDF o TXT
- Cambiar entre distintos modelos TTS