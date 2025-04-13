#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para generar un ejecutable de la aplicación usando PyInstaller
"""

import os
import sys
import subprocess
import shutil
import platform

def main():
    """
    Función principal para crear el ejecutable
    """
    print("Generando ejecutable para la Herramienta de Evaluación de Deducciones Fiscales I+D+i...")
    
    # Determinar el sistema operativo
    system = platform.system()
    
    # Nombre del ejecutable
    exe_name = "DeduccionesIDI"
    if system == "Windows":
        exe_name += ".exe"
    
    # Directorio actual
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Asegurarse de que existen las carpetas necesarias
    for dir_name in ['dist', 'build']:
        dir_path = os.path.join(current_dir, dir_name)
        if os.path.exists(dir_path):
            print(f"Limpiando directorio {dir_name}...")
            shutil.rmtree(dir_path)
    
    # Comando de PyInstaller
    pyinstaller_cmd = [
        "pyinstaller",
        "--onefile",  # Generar un único archivo ejecutable
        "--windowed",  # No mostrar consola en Windows
        "--name", exe_name,
        "--add-data", f"templates{os.pathsep}templates",
        "--add-data", f"static{os.pathsep}static",
        "--add-data", f"config{os.pathsep}config",
        "--add-data", f"version.txt{os.pathsep}.",
        # Icono para Windows (si existe)
        "run.py"  # Script principal
    ]
    
    # Agregar icono si existe
    if os.path.exists(os.path.join("static", "images", "favicon.ico")):
        pyinstaller_cmd.extend(["--icon", os.path.join("static", "images", "favicon.ico")])
    
    # Eliminar None del comando
    pyinstaller_cmd = [cmd for cmd in pyinstaller_cmd if cmd is not None]
    
    try:
        # Ejecutar PyInstaller
        subprocess.run(pyinstaller_cmd, check=True)
        
        print("\n¡Ejecutable generado con éxito!")
        print(f"El ejecutable se encuentra en: {os.path.join(current_dir, 'dist', exe_name)}")
        
        # Copiar README o generar instrucciones
        dist_dir = os.path.join(current_dir, 'dist')
        
        # Crear archivo de instrucciones
        with open(os.path.join(dist_dir, 'LEEME.txt'), 'w', encoding='utf-8') as f:
            f.write("HERRAMIENTA DE EVALUACIÓN DE DEDUCCIONES FISCALES I+D+i\n")
            f.write("=======================================================\n\n")
            f.write("Desarrollado para la Red Empresarial de Innovación de FADE\n\n")
            f.write("INSTRUCCIONES DE USO:\n\n")
            f.write("1. Haga doble clic en el archivo ejecutable 'DeduccionesIDI' para iniciar la aplicación.\n")
            f.write("2. Se abrirá automáticamente su navegador web predeterminado con la aplicación.\n")
            f.write("3. Si el navegador no se abre automáticamente, acceda a http://localhost:XXXX\n")
            f.write("   (El número de puerto se mostrará en la ventana de la aplicación).\n\n")
            f.write("AVISO IMPORTANTE:\n\n")
            f.write("Esta herramienta proporciona una orientación preliminar y no vinculante. ")
            f.write("No constituye asesoramiento fiscal profesional.\n")
            f.write("Los resultados obtenidos deben ser contrastados con un experto en deducciones fiscales por I+D+i.\n\n")
            f.write("Para cerrar la aplicación, cierre la ventana del ejecutable o presione Ctrl+C en ella.\n")
        
        print(f"Se ha creado un archivo de instrucciones en: {os.path.join(dist_dir, 'LEEME.txt')}")
        
    except subprocess.CalledProcessError as e:
        print(f"\nError al generar el ejecutable: {e}")
        print("\nAsegúrese de tener instalado PyInstaller:")
        print("pip install pyinstaller")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
