# 📚 epub-to-mp3

Convierte automáticamente el **primer archivo EPUB** encontrado en la carpeta `input/` a una serie de **audiocapítulos en MP3**, utilizando el modelo TTS **xtts_v2** de [Coqui.ai](https://github.com/coqui-ai/TTS). Todo el proceso se realiza **completamente offline** y con soporte para **voz personalizada y multilingüe**.

---

## 🚀 Características

- 🎙️ Conversión de texto a voz con calidad natural (modelo `xtts_v2`)
- 🧠 Compatible con español, inglés y otros idiomas
- 🧾 Extrae y limpia el texto desde capítulos EPUB
- 🗂️ Genera archivos MP3 con nombres amigables
- ⚡ Totalmente offline (requiere GPU para mejor rendimiento)

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
# En Linux/MacOS usa:
# source venv-epub2mp3/bin/activate

# Clonar el repositorio
git clone https://github.com/jozzer182/epub-to-mp3.git
cd epub-to-mp3

# 🛠️ PASO FINAL: Modificar el archivo `io.py` de Coqui TTS

Después de instalar las dependencias, debes editar manualmente un archivo del paquete `TTS` para que el modelo `xtts_v2` funcione correctamente.

Ubica este archivo dentro del entorno virtual (ajusta la ruta según tu usuario y nombre del entorno):

```
C:\Users\<TU_USUARIO>\venv-epub2mp3\Lib\site-packages\TTS\utils\io.py
```

Y **reemplaza las siguientes dos líneas**:

```python
return torch.load(f, map_location=map_location, **kwargs)
```

por esta versión:

```python
return torch.load(f, map_location=map_location, weights_only=False, **kwargs)
```

Este cambio debe hacerse en ambas apariciones de esa línea dentro del archivo.

> ⚠️ Este paso es necesario para evitar errores de carga del modelo XTTS.

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

## 📁 Estructura esperada

```
epub-to-mp3/
├── main.py
├── requirements.txt
├── vlc.wav              ← voz de referencia
├── input/               ← coloca aquí tu archivo .epub
└── output/              ← carpeta vacía, donde se generarán los archivos .mp3
```

---

## ▶️ Uso

```bash
python main.py
```

El script:
1. Busca el primer archivo `.epub` dentro de la carpeta `input/`.
2. Extrae y limpia el contenido de los capítulos.
3. Convierte cada capítulo en un archivo `.mp3` con una voz natural personalizada.
4. Guarda los audios en la carpeta `output/`.

---

## 🧠 Personalización

- Puedes cambiar el idioma modificando esta línea en `main.py`:

```python
idioma = "es"  # Cambia por "en", "fr", etc.
```

- También puedes reemplazar el archivo `vlc.wav` por cualquier muestra de voz compatible (misma persona, mismo idioma).

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