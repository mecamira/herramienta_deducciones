"""
Módulo que contiene el modelo de datos para la evaluación de deducciones fiscales
"""

import uuid
from datetime import datetime
import json

class Assessment:
    """
    Clase que representa una evaluación de deducción fiscal
    """
    
    def __init__(self, company_name=None):
        """
        Inicializa una nueva evaluación
        
        Args:
            company_name (str, optional): Nombre de la empresa
        """
        self.id = str(uuid.uuid4())
        self.timestamp = datetime.now().isoformat()
        self.company_name = company_name
        self.responses = {
            'basic_info': {},
            'project_identification': {},
            'qualification': {},
            'expenses': {}
        }
        self.results = {
            'qualification': None,
            'deduction': None,
            'recommendations': []
        }
    
    def update_responses(self, section, responses):
        """
        Actualiza las respuestas de una sección
        
        Args:
            section (str): Nombre de la sección
            responses (dict): Respuestas a actualizar
        """
        if section in self.responses:
            self.responses[section].update(responses)
    
    def set_results(self, qualification, deduction, recommendations):
        """
        Establece los resultados de la evaluación
        
        Args:
            qualification (str): Calificación del proyecto
            deduction (dict): Deducción calculada
            recommendations (list): Recomendaciones
        """
        self.results['qualification'] = qualification
        self.results['deduction'] = deduction
        self.results['recommendations'] = recommendations
    
    def to_dict(self):
        """
        Convierte la evaluación a un diccionario
        
        Returns:
            dict: Diccionario con los datos de la evaluación
        """
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'company_name': self.company_name,
            'responses': self.responses,
            'results': self.results
        }
    
    def to_json(self):
        """
        Convierte la evaluación a una cadena JSON
        
        Returns:
            str: Cadena JSON con los datos de la evaluación
        """
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data):
        """
        Crea una evaluación a partir de un diccionario
        
        Args:
            data (dict): Diccionario con los datos de la evaluación
        
        Returns:
            Assessment: Instancia de Assessment
        """
        assessment = cls()
        assessment.id = data.get('id', assessment.id)
        assessment.timestamp = data.get('timestamp', assessment.timestamp)
        assessment.company_name = data.get('company_name')
        assessment.responses = data.get('responses', assessment.responses)
        assessment.results = data.get('results', assessment.results)
        return assessment
    
    @classmethod
    def from_json(cls, json_str):
        """
        Crea una evaluación a partir de una cadena JSON
        
        Args:
            json_str (str): Cadena JSON con los datos de la evaluación
        
        Returns:
            Assessment: Instancia de Assessment
        """
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def save(self, filepath):
        """
        Guarda la evaluación en un archivo JSON
        
        Args:
            filepath (str): Ruta del archivo
        
        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(self.to_json())
            return True
        except Exception:
            return False
    
    @classmethod
    def load(cls, filepath):
        """
        Carga una evaluación desde un archivo JSON
        
        Args:
            filepath (str): Ruta del archivo
        
        Returns:
            Assessment: Instancia de Assessment
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return cls.from_json(f.read())
        except Exception:
            return None
