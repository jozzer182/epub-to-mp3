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
├── vlc.wav              ← voz de referencia
├── input/               ← coloca aquí tu archivo .epub
└── output/              ← carpeta vacía, donde se generarán los archivos .mp3
```

---

## ▶️ Uso

```bash
python main.py
```

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