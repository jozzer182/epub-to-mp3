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

- Python 3.9 o superior
- NVIDIA GPU (recomendado)
- [ffmpeg](https://ffmpeg.org/) instalado y accesible desde terminal
- Archivo de voz de referencia (`vlc.wav`) ubicado en la raíz del proyecto

---

## 📦 Instalación

```bash
# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Clonar el repositorio
git clone https://github.com/tuusuario/epub-to-mp3.git
cd epub-to-mp3

# Instalar dependencias
pip install -r requirements.txt
```

---

## 📁 Estructura esperada

```
epub-to-mp3/
├── main.py
├── requirements.txt
├── vlc.wav              ← voz de referencia
├── input/               ← coloca aquí tu archivo .epub
│   └── mi_libro.epub
└── output/              ← aquí se generarán los archivos .mp3
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

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Offline-TTS](https://img.shields.io/badge/TTS-Offline%20xtts_v2-critical?logo=soundcloud)
![Status](https://img.shields.io/badge/Estado-Activo-brightgreen)

---

## 📜 Licencia

Este proyecto se publica bajo la licencia MIT. Eres libre de usarlo, modificarlo y compartirlo.

---

## 💡 Créditos

Desarrollado por [@tuusuario](https://github.com/tuusuario) como primer repositorio público. Utiliza tecnologías de:

- [Coqui TTS](https://github.com/coqui-ai/TTS)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [EbookLib](https://github.com/aerkalov/ebooklib)

---

## 🌱 Siguiente paso

Puedes ampliar este proyecto para:
- Soportar múltiples archivos EPUB
- Agregar un lector de PDF o TXT
- Cambiar entre distintos modelos TTS