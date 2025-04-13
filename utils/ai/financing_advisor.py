"""
Módulo de asesoramiento en financiación mediante IA generativa
"""
import os
import json
import requests
from datetime import datetime
import re

class FinancingAdvisor:
    """Clase para gestionar el asesoramiento en financiación mediante IA"""
    
    def __init__(self, api_key=None):
        # Preferimos usar variable de entorno para seguridad, pero aceptamos clave directa para pruebas
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY", "AIzaSyCLEE2lzOAxDV3KQVOXhFDNA1GeolBDZDo")
        if not self.api_key:
            raise ValueError("Se requiere una API key de Gemini para usar el asistente de financiación")
        
        self.model = "gemini-1.5-flash"
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        
    def get_financing_advice(self, company_info, project_info):
        """
        Obtiene recomendaciones de financiación basadas en la información proporcionada
        
        Args:
            company_info (dict): Información de la empresa
            project_info (dict): Información del proyecto
            
        Returns:
            dict: Respuesta estructurada con recomendaciones
        """
        try:
            # Crear el prompt con instrucciones específicas
            prompt = self._build_prompt(company_info, project_info)
            
            # Llamar a la API de Gemini
            headers = {
                "Content-Type": "application/json",
                "x-goog-api-key": self.api_key
            }
            
            data = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {
                    "temperature": 0.2,
                    "topK": 40,
                    "topP": 0.95,
                    "maxOutputTokens": 8192,
                }
            }
            
            response = requests.post(self.api_url, headers=headers, json=data)
            response.raise_for_status()  # Lanzar excepción si hay error HTTP
            
            # Procesar la respuesta
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                text_result = result['candidates'][0]['content']['parts'][0]['text']
                
                # Limpiar la respuesta (eliminar etiquetas <br> literales)
                text_result = text_result.replace('<br>', '\n')
                
                # Procesar JSON estructurado si existe
                structured_data = None
                try:
                    # Buscar si hay JSON en la respuesta usando regex más preciso
                    json_pattern = r'```json\s*([\s\S]*?)\s*```'
                    json_match = re.search(json_pattern, text_result)
                    
                    if json_match:
                        json_text = json_match.group(1).strip()
                        # Limpiar espacios y caracteres especiales que podrían causar problemas
                        json_text = re.sub(r'\s+', ' ', json_text)
                        json_text = json_text.replace('\t', '').replace('\r', '')
                        
                        # Intentar parsear el JSON
                        structured_data = json.loads(json_text)
                        print("JSON extraído correctamente")
                    else:
                        # Si no se encuentra el patrón de JSON, crear una estructura simplificada
                        print("No se encontró JSON en la respuesta")
                        structured_data = None
                        
                except Exception as e:
                    print(f"Error al procesar JSON: {str(e)}")
                    structured_data = None
                
                # Agregar recordatorio de asesoramiento personalizado
                reminder = """

### Recordatorio importante

Este es un asesoramiento preliminar generado automáticamente basado en la información proporcionada. Para un análisis más detallado y personalizado de sus opciones de financiación, póngase en contacto con Alejandro Cuesta, Consultor Senior de la REI.

Email: acuesta@fade.es
Teléfono: 680 82 91 80

La Red Empresarial de Innovación (REI) de FADE ofrece servicios de asesoramiento especializado en financiación de la I+D+i y le ayudará a encontrar las mejores opciones para su proyecto específico.
                """
                
                # Reemplazar cualquier bloque JSON por nuestro recordatorio
                text_result = re.sub(r'```json\s*[\s\S]*?\s*```', reminder, text_result)
                
                # Eliminar texto "Resumen en JSON"
                text_result = re.sub(r'Resumen en JSON.*?Recordatorio importante', '### Recordatorio importante', text_result, flags=re.DOTALL)
                
                # Eliminar cualquier despedida final
                text_result = re.sub(r'Espero que esta información.*?proyecto!.*?$', '', text_result, flags=re.DOTALL)
                
                # Devolver tanto la respuesta estructurada como el texto completo
                return {
                    "status": "success",
                    "structured_data": structured_data,
                    "full_response": text_result
                }
            else:
                return {
                    "status": "error",
                    "message": "No se recibió una respuesta válida del modelo",
                    "full_response": "Lo sentimos, no pudimos procesar su solicitud. Por favor, inténtelo de nuevo."
                }
                
        except Exception as e:
            print(f"Error general en el asesor de financiación: {str(e)}")
            return {
                "status": "error",
                "message": f"Error al obtener recomendaciones: {str(e)}",
                "full_response": f"Lo sentimos, ocurrió un error: {str(e)}"
            }
    
    def _build_prompt(self, company_info, project_info):
        """
        Construye el prompt para el modelo de IA
        """
        current_date = datetime.now().strftime("%d/%m/%Y")
        
        # Información de financiaciones desde un CSV o base de datos
        financing_info = """
## Base de datos de financiación disponible

1. **CDTI - Proyectos de I+D**
   - Organismo: Centro para el Desarrollo Tecnológico Industrial
   - Tipo: Préstamo parcialmente reembolsable
   - Intensidad: Hasta 85% del presupuesto con tramo no reembolsable del 33%
   - Convocatoria: Abierta todo el año
   - Requisitos: Proyectos empresariales de I+D, TRL 4-7
   - Presupuesto mínimo: 175.000€

2. **CDTI - Línea Directa de Innovación**
   - Organismo: Centro para el Desarrollo Tecnológico Industrial
   - Tipo: Préstamo parcialmente reembolsable
   - Intensidad: 75% del presupuesto con tramo no reembolsable del 2-5%
   - Convocatoria: Abierta todo el año
   - Requisitos: Proyectos de innovación tecnológica, TRL 7-9
   - Presupuesto mínimo: 175.000€

3. **Misiones Ciencia e Innovación**
   - Organismo: CDTI
   - Tipo: Subvención
   - Intensidad: Hasta 65% para pequeñas empresas
   - Convocatoria: Junio-Julio 2025 (estimado)
   - Requisitos: Proyectos colaborativos alineados con misiones estratégicas
   - Presupuesto mínimo: 1.500.000€ (proyectos en cooperación)

4. **Kit Digital**
   - Organismo: Red.es
   - Tipo: Bono digital/Subvención directa
   - Intensidad: Hasta 12.000€ para empresas de 10-49 empleados
   - Convocatoria: Abierta hasta agotar fondos
   - Requisitos: Digitalización de pymes y autónomos
   - Segmentos: Por tamaño de empresa

5. **Proyectos de Innovación IDEPA**
   - Organismo: IDEPA (Asturias)
   - Tipo: Subvención
   - Intensidad: Hasta 55% (pequeñas empresas), 45% (medianas), 35% (grandes)
   - Convocatoria: Marzo-Abril 2025 (estimado)
   - Requisitos: Empresas con establecimiento en Asturias
   - Presupuesto mínimo: 10.000€

6. **Cheques de Innovación**
   - Organismo: IDEPA (Asturias)
   - Tipo: Subvención
   - Intensidad: Hasta 75% con un máximo de 15.000€
   - Convocatoria: Mayo-Junio 2025 (estimado)
   - Requisitos: Pequeñas y medianas empresas asturianas
   - Modalidades: Asesoramiento tecnológico, consultoría I+D+i

7. **Proyectos de I+D en Cooperación Internacional**
   - Organismo: CDTI
   - Tipo: Ayuda Parcialmente Reembolsable
   - Intensidad: 33% de subvención y 42% de préstamo (PYMEs)
   - Convocatoria: Varias a lo largo del año (Eureka, Iberoeka, etc.)
   - Requisitos: Consorcio internacional (mínimo dos países)
   - Presupuesto: Variable según programa

8. **Ayudas Industria 4.0**
   - Organismo: Ministerio de Industria, Comercio y Turismo
   - Tipo: Préstamo reembolsable (o mix préstamo-subvención)
   - Intensidad: Hasta 80% del presupuesto
   - Convocatoria: Marzo-Mayo 2025 (estimado)
   - Requisitos: Proyectos de implementación de tecnologías 4.0
   - Presupuesto mínimo: 50.000€

9. **Ayudas a la Investigación Industrial (IDI) FICYT**
   - Organismo: FICYT (Asturias)
   - Tipo: Subvención
   - Intensidad: Hasta 80% (según tamaño empresa)
   - Convocatoria: 1º trimestre 2025 (estimado)
   - Requisitos: Proyectos de I+D en empresas asturianas
   - Duración: 1-3 años

10. **NEOTEC**
   - Organismo: CDTI
   - Tipo: Subvención
   - Intensidad: Hasta 250.000€ (70% del presupuesto)
   - Convocatoria: Abril-Mayo 2025 (estimado)
   - Requisitos: Empresas innovadoras con menos de 3 años
   - Presupuesto mínimo: 175.000€

11. **INNOVA - Transformación Digital**
   - Organismo: IDEPA (Asturias)
   - Tipo: Subvención
   - Intensidad: Hasta 50% para PYMEs
   - Convocatoria: Junio-Julio 2025 (estimado)
   - Requisitos: Digitalización de procesos productivos
   - Presupuesto mínimo: 15.000€

12. **Programa Promoción Internacional**
   - Organismo: ICEX / ASTUREX
   - Tipo: Subvención
   - Intensidad: Hasta 80% de los costes elegibles (máx. 30.000€)
   - Convocatoria: Marzo-Abril y Septiembre-Octubre 2025
   - Requisitos: Empresas con plan de internacionalización
   - Acciones: Ferias, misiones comerciales, marketing digital
"""
        
        # Crear JSON seguro para el prompt
        company_json = json.dumps(company_info, ensure_ascii=False, indent=2)
        project_json = json.dumps(project_info, ensure_ascii=False, indent=2)
        
        # Construir el prompt
        prompt = f"""
# Instrucciones para el asesor de financiación

Eres un asesor especializado en financiación para proyectos de innovación, I+D y desarrollo empresarial. 
Tu tarea es analizar la información proporcionada sobre una empresa y su proyecto, y recomendar las mejores opciones de financiación disponibles en Asturias y España.

Fecha actual: {current_date}

## Información de la empresa
```json
{company_json}
```

## Información del proyecto
```json
{project_json}
```

{financing_info}

## Tu tarea

1. Analiza la información proporcionada sobre la empresa y el proyecto.

2. Identifica las 3-5 opciones de financiación más adecuadas según:
   - Tamaño de empresa
   - Sector de actividad
   - Tipo de proyecto
   - Nivel tecnológico
   - Presupuesto aproximado
   - Plazos de ejecución

3. Para cada opción de financiación recomendada, proporciona:
   - Nombre del programa
   - Organismo que lo gestiona
   - Tipo de ayuda (subvención, préstamo, mixta)
   - Porcentaje o intensidad de la ayuda
   - Fechas aproximadas de convocatoria
   - Requisitos principales
   - Nivel de adecuación para este caso concreto (alto, medio, bajo)
   - Una breve justificación

4. Incluye también 3-5 consejos específicos para aumentar las probabilidades de éxito en los programas recomendados.

5. Tu respuesta debe ser en texto conversacional y también debe incluir un resumen estructurado en formato JSON.

6. IMPORTANTE: El JSON debe usar este formato exacto sin ninguna modificación:

```json
{{
  "empresa": {{
    "tamaño": "pequeña", 
    "sector": "tecnología"
  }},
  "proyecto": {{
    "tipo": "innovación",
    "presupuesto_estimado": "100000 euros",
    "duración_estimada": "12 meses"
  }},
  "recomendaciones": [
    {{
      "programa": "Kit Digital",
      "organismo": "Red.es",
      "tipo_ayuda": "subvención",
      "intensidad": "50%",
      "convocatoria": "Marzo 2025",
      "adecuación": "alta",
      "justificación": "Breve justificación"
    }}
  ],
  "consejos_generales": [
    "Consejo uno",
    "Consejo dos"
  ]
}}
```

Mantén un tono profesional pero cercano. Sé específico y proporciona información práctica y accionable. No inventes programas que no estén en la base de datos proporcionada.
"""
        
        return prompt
