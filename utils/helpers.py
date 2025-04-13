"""
Funciones de utilidad para la herramienta de deducciones fiscales
"""

import os
import json
import locale
import platform
from datetime import datetime

def get_app_dir():
    """
    Obtiene el directorio de la aplicación
    
    Returns:
        str: Ruta al directorio de la aplicación
    """
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_user_data_dir():
    """
    Obtiene el directorio de datos del usuario
    
    Returns:
        str: Ruta al directorio de datos del usuario
    """
    # Determinar el directorio de datos según el sistema operativo
    if platform.system() == 'Windows':
        base_dir = os.path.join(os.environ['APPDATA'], 'DeduccionesFiscalesFADE')
    elif platform.system() == 'Darwin':  # macOS
        base_dir = os.path.expanduser('~/Library/Application Support/DeduccionesFiscalesFADE')
    else:  # Linux y otros
        base_dir = os.path.expanduser('~/.deduccionesfiscalesfade')
    
    # Crear el directorio si no existe
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    return base_dir

def get_saved_assessments_dir():
    """
    Obtiene el directorio para guardar las evaluaciones
    
    Returns:
        str: Ruta al directorio de evaluaciones guardadas
    """
    assessments_dir = os.path.join(get_user_data_dir(), 'assessments')
    
    # Crear el directorio si no existe
    if not os.path.exists(assessments_dir):
        os.makedirs(assessments_dir)
    
    return assessments_dir

def format_currency(value):
    """
    Formatea un valor como moneda
    
    Args:
        value (float): Valor a formatear
    
    Returns:
        str: Valor formateado como moneda
    """
    try:
        # Intentar configurar la localización para español
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
    except locale.Error:
        try:
            # Alternativa para Windows
            locale.setlocale(locale.LC_ALL, 'Spanish_Spain.1252')
        except locale.Error:
            # Si no funciona, usar formato general
            return f"{value:,.2f} €"
    
    return locale.currency(value, grouping=True, symbol=True)

def get_version():
    """
    Obtiene la versión de la aplicación
    
    Returns:
        str: Versión de la aplicación
    """
    version_file = os.path.join(get_app_dir(), 'version.txt')
    
    if os.path.exists(version_file):
        with open(version_file, 'r') as f:
            return f.read().strip()
    
    return "1.0.0"  # Versión por defecto

def generate_filename(company_name=None):
    """
    Genera un nombre de archivo para guardar una evaluación
    
    Args:
        company_name (str, optional): Nombre de la empresa
    
    Returns:
        str: Nombre de archivo
    """
    date_str = datetime.now().strftime('%Y%m%d-%H%M%S')
    
    if company_name:
        # Limpiar el nombre de la empresa para usarlo como nombre de archivo
        clean_name = ''.join(c for c in company_name if c.isalnum() or c in ' _-').strip()
        clean_name = clean_name.replace(' ', '_')
        
        if clean_name:
            return f"evaluacion_{clean_name}_{date_str}.json"
    
    return f"evaluacion_{date_str}.json"

def load_section_title(section_id):
    """
    Obtiene el título de una sección
    
    Args:
        section_id (str): ID de la sección
    
    Returns:
        str: Título de la sección
    """
    section_titles = {
        'basic_info': 'Información Básica',
        'project_identification': 'Identificación del Proyecto',
        'qualification': 'Calificación del Proyecto',
        'expenses': 'Gastos Elegibles'
    }
    
    return section_titles.get(section_id, section_id.capitalize())

def load_qualification_label(qualification):
    """
    Obtiene la etiqueta para una calificación
    
    Args:
        qualification (str): Código de calificación
    
    Returns:
        tuple: (Etiqueta, Clase CSS)
    """
    labels = {
        'ID': ('Investigación y Desarrollo (I+D)', 'success'),
        'IT': ('Innovación Tecnológica (IT)', 'primary'),
        'MIXED': ('Proyecto Mixto (I+D + IT)', 'info'),
        'POTENTIAL': ('Potencial I+D/IT', 'warning'),
        'NOT_QUALIFIED': ('No Califica', 'danger')
    }
    
    return labels.get(qualification, ('No determinado', 'secondary'))
