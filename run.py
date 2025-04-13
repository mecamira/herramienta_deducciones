#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para ejecutar la herramienta de evaluación de deducciones fiscales I+D+i
"""

import os
import sys
import webbrowser
import threading
import socket
import platform
from app import app

def check_windows_compatibility():
    """
    Verifica si el sistema operativo Windows es compatible con la aplicación.
    Devuelve True si es compatible, False si no lo es.
    """
    if platform.system() != 'Windows':
        return True  # No estamos en Windows, se asume compatibilidad
    
    # Obtenemos la versión de Windows
    win_ver = platform.win32_ver()[0]
    
    # Diccionario de versiones de Windows
    win_versions = {
        '5.1': 'Windows XP',
        '5.2': 'Windows XP 64-bit/Server 2003',
        '6.0': 'Windows Vista/Server 2008',
        '6.1': 'Windows 7/Server 2008 R2',
        '6.2': 'Windows 8/Server 2012',
        '6.3': 'Windows 8.1/Server 2012 R2',
        '10.0': 'Windows 10/11/Server 2016+'
    }
    
    # Advertir sobre Windows XP o Vista
    if win_ver.startswith('5.') or win_ver.startswith('6.0'):
        print("\n" + "="*80)
        print(f"ADVERTENCIA: Está ejecutando esta aplicación en {win_versions.get(win_ver, f'Windows {win_ver}')}.")
        print("Esta versión tiene soporte limitado. Se recomienda Windows 7 o superior.")
        print("La aplicación intentará ejecutarse, pero podría experimentar problemas.")
        print("="*80 + "\n")
        
        # En Windows, intentar mostrar un MessageBox si es posible
        try:
            import ctypes
            MessageBox = ctypes.windll.user32.MessageBoxW
            MB_ICONWARNING = 0x30
            MessageBox(None, 
                      f"Advertencia: Está ejecutando esta aplicación en {win_versions.get(win_ver, f'Windows {win_ver}')}\n\n" +
                      "Esta versión tiene soporte limitado. Se recomienda Windows 7 o superior.\n\n" +
                      "La aplicación intentará ejecutarse, pero podría experimentar problemas.", 
                      "Verificación de Compatibilidad", 
                      MB_ICONWARNING)
        except:
            pass  # Si falla mostrar el MessageBox, continuamos con la advertencia en consola
            
        return True  # Continuamos con la ejecución con advertencia
    
    return True  # Compatible por defecto

def find_free_port():
    """
    Encuentra un puerto libre para ejecutar la aplicación
    
    Returns:
        int: Número de puerto disponible
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 0))
    port = sock.getsockname()[1]
    sock.close()
    return port

def open_browser(port):
    """
    Abre el navegador con la aplicación
    
    Args:
        port (int): Número de puerto
    """
    # Esperar un momento para asegurar que Flask esté en marcha
    threading.Timer(1.5, lambda: webbrowser.open(f'http://localhost:{port}')).start()

def main():
    """
    Función principal para ejecutar la aplicación
    """
    # Verificar compatibilidad con el sistema operativo
    check_windows_compatibility()
    
    # Determinar si se está ejecutando desde PyInstaller
    if getattr(sys, 'frozen', False):
        # Ejecutable de PyInstaller
        application_path = os.path.dirname(sys.executable)
    else:
        # Script Python normal
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    # Cambiar al directorio de la aplicación
    os.chdir(application_path)
    
    # Verificar si existe un directorio de datos específico (para portable)
    if os.environ.get('DEDUCCIONESIDI_DATA_DIR'):
        data_dir = os.environ.get('DEDUCCIONESIDI_DATA_DIR')
        print(f"Usando directorio de datos externo: {data_dir}")
    
    # Encontrar puerto libre
    port = find_free_port()
    
    # Imprimir mensaje informativo
    print(f"\nIniciando Herramienta de Evaluación de Deducciones Fiscales I+D+i...")
    print(f"Acceda a la aplicación en: http://localhost:{port}")
    print(f"Utilice Ctrl+C para detener la aplicación\n")
    
    # Abrir navegador
    open_browser(port)
    
    # Iniciar Flask
    app.run(host='localhost', port=port, debug=False)

if __name__ == "__main__":
    main()
