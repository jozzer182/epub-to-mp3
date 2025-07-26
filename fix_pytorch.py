#!/usr/bin/env python3
"""
Script para configurar PyTorch y solucionar problemas de compatibilidad con XTTS v2
Ejecuta este script antes de usar main.py si tienes problemas con PyTorch 2.6+
"""

import torch
import os
import sys
import warnings

def configure_pytorch_for_xtts():
    """
    Configura PyTorch para ser compatible con el modelo XTTS v2
    """
    print("🔧 Configurando PyTorch para compatibilidad con XTTS...")
    
    # Verificar versión de PyTorch
    torch_version = torch.__version__
    print(f"📦 PyTorch versión: {torch_version}")
    
    # Suprimir warnings
    warnings.filterwarnings("ignore", message="`gpu` will be deprecated")
    
    # Configurar torch.load para usar weights_only=False por defecto
    original_torch_load = torch.load
    
    def patched_torch_load(*args, **kwargs):
        if 'weights_only' not in kwargs:
            kwargs['weights_only'] = False
        return original_torch_load(*args, **kwargs)
    
    torch.load = patched_torch_load
    print("✅ torch.load configurado para weights_only=False")
    
    # Verificar disponibilidad de CUDA
    if torch.cuda.is_available():
        print(f"🚀 CUDA disponible: {torch.cuda.get_device_name(0)}")
    else:
        print("⚠️  CUDA no disponible, usando CPU")
    
    print("✅ Configuración completada")

if __name__ == "__main__":
    configure_pytorch_for_xtts()
    
    # Probar importar TTS
    try:
        from TTS.api import TTS
        print("✅ TTS importado exitosamente")
        
        # Probar cargar el modelo
        print("🔄 Probando cargar modelo XTTS...")
        tts = TTS(
            model_name="tts_models/multilingual/multi-dataset/xtts_v2",
            progress_bar=False,
            gpu=torch.cuda.is_available()
        )
        print("✅ Modelo XTTS cargado exitosamente")
        
    except Exception as e:
        print(f"❌ Error al probar TTS: {e}")
        sys.exit(1)
