"""
Módulo para la estructuración de proyectos de I+D+i.
Contiene modelos y funciones relacionados con la guía de estructura de proyectos.
"""

import json
import os

class ProjectStructureGuide:
    """
    Clase que proporciona guías y recomendaciones para estructurar proyectos de I+D+i.
    """
    
    def __init__(self):
        """Inicializa la guía de estructura de proyectos."""
        self.sections = self._load_sections()
        self.methodologies = self._load_methodologies()
        self.writing_tips = self._load_writing_tips()
        self.budget_categories = self._load_budget_categories()
        self.checklist = self._load_checklist()
        
    def _load_sections(self):
        """Carga la información de las secciones de un proyecto."""
        try:
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                      'config', 
                                      'project_sections.json')
            
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            else:
                # Si el archivo no existe, devolver estructura por defecto
                return self._default_sections()
        except Exception as e:
            print(f"Error al cargar secciones: {e}")
            return self._default_sections()
    
    def _load_methodologies(self):
        """Carga la información de metodologías de I+D+i."""
        try:
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                      'config', 
                                      'project_methodologies.json')
            
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            else:
                # Si el archivo no existe, devolver metodologías por defecto
                return self._default_methodologies()
        except Exception as e:
            print(f"Error al cargar metodologías: {e}")
            return self._default_methodologies()
    
    def _load_writing_tips(self):
        """Carga consejos de redacción para proyectos de I+D+i."""
        try:
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                      'config', 
                                      'project_writing_tips.json')
            
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            else:
                # Si el archivo no existe, devolver consejos por defecto
                return self._default_writing_tips()
        except Exception as e:
            print(f"Error al cargar consejos de redacción: {e}")
            return self._default_writing_tips()
            
    def _load_budget_categories(self):
        """Carga categorías del presupuesto y consejos de planificación."""
        try:
            config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                      'config', 
                                      'project_budget.json')
            
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as file:
                    return json.load(file)
            else:
                # Si el archivo no existe, devolver categorías por defecto
                return self._default_budget_categories()
        except Exception as e:
            print(f"Error al cargar categorías de presupuesto: {e}")
            return self._default_budget_categories()
            
    def _load_checklist(self):
        """Carga la lista de verificación para proyectos."""
        try:
            # Obtener la ruta absoluta del directorio actual y construir la ruta al archivo JSON
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            config_path = os.path.join(parent_dir, 'config', 'project_checklist.json')
            
            if not os.path.exists(config_path):
                print("Usando lista de verificación por defecto (archivo no existe)")
                return self._default_checklist()
            
            # Intentar abrir y cargar el archivo JSON
            try:
                with open(config_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    
                    # Intentar parsear el JSON
                    try:
                        data = json.loads(content)
                        print("JSON parseado correctamente")
                        if isinstance(data, dict) and 'sections' in data:
                            # Verificar estructura básica
                            sections = data['sections']
                            print(f"Número de secciones encontradas: {len(sections)}")
                            
                            # Verificar secciones rápidamente
                            for i, section in enumerate(sections):
                                section_id = section.get('id', f'section_{i}')
                                items = section.get('checklist_items', [])
                                print(f"  Sección '{section_id}': {len(items)} elementos")
                                
                            # Devolver los datos cargados
                            return data
                        else:
                            print("La estructura del JSON no es válida, usando lista por defecto")
                            return self._default_checklist()
                        
                    except json.JSONDecodeError as json_error:
                        print(f"ERROR: El archivo no es un JSON válido: {json_error}")
                        return self._default_checklist()
                        
            except Exception as file_error:
                print(f"ERROR: No se pudo leer el archivo: {file_error}")
                return self._default_checklist()
                
        except Exception as e:
            print(f"ERROR GENERAL al cargar checklist: {e}")
            return self._default_checklist()
            
    def _default_sections(self):
        """Proporciona una estructura de secciones predeterminada."""
        return {
            "sections": [
                {
                    "id": "resumen",
                    "title": "Resumen ejecutivo",
                    "description": "Síntesis clara y concisa del proyecto, enfocada a destacar su innovación y valor.",
                    "content": "El resumen ejecutivo debe presentar de forma sintética pero completa los aspectos clave del proyecto. No debe exceder de 1-2 páginas y debe ser comprensible para personas con perfil técnico pero no especializadas en el campo específico.",
                    "key_elements": [
                        "Descripción breve del objetivo y novedad del proyecto",
                        "Problema que resuelve o necesidad que satisface",
                        "Aspectos innovadores y ventajas respecto al estado del arte",
                        "Impacto esperado (económico, social, medioambiental)",
                        "Resumen de recursos necesarios y plazos"
                    ],
                    "recommendations": [
                        "Redactar al final, cuando ya se tenga clara toda la propuesta",
                        "Debe poder leerse de forma independiente y transmitir la esencia del proyecto",
                        "Utilizar lenguaje claro y preciso, evitando jerga excesivamente técnica",
                        "Destacar claramente los elementos innovadores y de I+D+i"
                    ]
                },
                {
                    "id": "antecedentes",
                    "title": "Antecedentes y estado del arte",
                    "description": "Análisis del contexto científico-técnico actual y los avances previos en el campo.",
                    "content": "Esta sección debe establecer el marco de conocimiento sobre el que se construye el proyecto, demostrando un conocimiento profundo del estado actual de la tecnología o conocimiento en el ámbito del proyecto.",
                    "key_elements": [
                        "Revisión de la literatura científica y técnica relevante",
                        "Análisis de soluciones existentes y sus limitaciones",
                        "Productos o servicios competidores",
                        "Patentes o propiedad intelectual relacionada",
                        "Trabajos previos del equipo en este campo"
                    ],
                    "recommendations": [
                        "Ser exhaustivo pero relevante, centrado en lo directamente relacionado con el proyecto",
                        "Citar fuentes académicas y técnicas actualizadas y de prestigio",
                        "Identificar claramente las carencias o limitaciones actuales que justifican el proyecto",
                        "Establecer el punto de partida tecnológico del proyecto"
                    ]
                },
                {
                    "id": "objetivos",
                    "title": "Objetivos y resultados esperados",
                    "description": "Definición clara de los fines del proyecto y de los productos o conocimientos a obtener.",
                    "content": "Los objetivos deben describir de forma clara y medible qué se pretende lograr con el proyecto. Deben ser específicos, medibles, alcanzables, relevantes y acotados en el tiempo (SMART).",
                    "key_elements": [
                        "Objetivo general del proyecto",
                        "Objetivos específicos (técnicos, científicos, de innovación)",
                        "Resultados esperados y entregables concretos",
                        "Indicadores de éxito y forma de medirlos",
                        "Impacto previsto en la competitividad de la empresa"
                    ],
                    "recommendations": [
                        "Formular objetivos SMART (Específicos, Medibles, Alcanzables, Relevantes y Temporales)",
                        "Diferenciar entre objetivos científico-técnicos y objetivos empresariales",
                        "Establecer indicadores claros para cada objetivo",
                        "Los objetivos deben justificar claramente el carácter de I+D+i"
                    ]
                },
                {
                    "id": "innovacion",
                    "title": "Elementos de innovación y avance",
                    "description": "Aspectos novedosos y diferenciales del proyecto respecto al estado actual de la técnica.",
                    "content": "Esta sección debe destacar con claridad qué aspectos del proyecto constituyen una novedad objetiva o subjetiva, y qué avances técnicos o científicos se espera conseguir.",
                    "key_elements": [
                        "Novedad objetiva (mundial) o subjetiva (para la empresa) del proyecto",
                        "Elementos innovadores específicos",
                        "Riesgo técnico o incertidumbre científica",
                        "Comparativa con soluciones existentes",
                        "Potencial de protección de resultados (patentes, modelos de utilidad)"
                    ],
                    "recommendations": [
                        "Ser específico sobre la innovación, evitando generalidades",
                        "Cuantificar siempre que sea posible las mejoras respecto a soluciones existentes",
                        "Describir detalladamente los obstáculos técnicos a superar",
                        "Resaltar elementos que evidencien I+D (incertidumbre científica, metodología) o IT (novedad tecnológica)"
                    ]
                },
                {
                    "id": "metodologia",
                    "title": "Metodología y plan de trabajo",
                    "description": "Enfoque técnico, actividades a realizar y organización temporal.",
                    "content": "La metodología debe detallar el enfoque técnico y científico que se seguirá para alcanzar los objetivos, así como la organización del trabajo en actividades, tareas y paquetes de trabajo.",
                    "key_elements": [
                        "Enfoque metodológico (científico o de desarrollo)",
                        "Actividades y tareas a desarrollar",
                        "Cronograma o planificación temporal",
                        "Hitos y puntos de control",
                        "Asignación de recursos a cada actividad",
                        "Gestión de riesgos y plan de contingencia"
                    ],
                    "recommendations": [
                        "Demostrar un enfoque sistemático y riguroso",
                        "Para proyectos de I+D, seguir una metodología científica clara",
                        "Para IT, detallar el proceso de desarrollo tecnológico",
                        "Incluir diagramas de Gantt o similares para la planificación",
                        "Identificar riesgos y plantear medidas para mitigarlos"
                    ]
                },
                {
                    "id": "equipo",
                    "title": "Equipo y recursos",
                    "description": "Descripción del personal y medios materiales destinados al proyecto.",
                    "content": "Esta sección debe detallar los recursos humanos y materiales que se dedicarán al proyecto, demostrando la capacidad técnica para llevarlo a cabo.",
                    "key_elements": [
                        "Composición del equipo y perfiles profesionales",
                        "Capacitación y experiencia previa relevante",
                        "Colaboraciones externas (universidades, centros tecnológicos)",
                        "Infraestructuras y equipamientos a utilizar",
                        "Otros recursos necesarios"
                    ],
                    "recommendations": [
                        "Destacar la cualificación específica del personal para las tareas de I+D+i",
                        "Explicar el valor añadido de las colaboraciones externas",
                        "Demostrar que se dispone de los medios adecuados o cómo se obtendrán",
                        "Para personal exclusivo de I+D, detallar su dedicación y titulación"
                    ]
                },
                {
                    "id": "presupuesto",
                    "title": "Presupuesto detallado",
                    "description": "Costes del proyecto desglosados por partidas y actividades.",
                    "content": "El presupuesto debe reflejar los recursos económicos necesarios para el desarrollo del proyecto, con un desglose detallado que permita valorar su adecuación.",
                    "key_elements": [
                        "Costes de personal (interno)",
                        "Colaboraciones externas",
                        "Materiales y consumibles",
                        "Amortización de activos",
                        "Otros gastos directos",
                        "Gastos generales indirectos"
                    ],
                    "recommendations": [
                        "Desglosar los costes por actividades o paquetes de trabajo",
                        "Justificar adecuadamente cada partida",
                        "Diferenciar claramente los gastos elegibles para deducciones fiscales",
                        "Prever posibles desviaciones y contingencias",
                        "Ser realista y preciso en las estimaciones"
                    ]
                },
                {
                    "id": "impacto",
                    "title": "Impacto y explotación de resultados",
                    "description": "Beneficios esperados y estrategia de aprovechamiento de los resultados.",
                    "content": "Esta sección debe abordar el impacto previsto del proyecto y cómo se aprovecharán los resultados obtenidos, tanto a nivel técnico como comercial o empresarial.",
                    "key_elements": [
                        "Impacto técnico o científico esperado",
                        "Impacto económico para la empresa",
                        "Estrategia de protección de resultados (propiedad intelectual)",
                        "Plan de explotación comercial",
                        "Impacto social o medioambiental, si procede",
                        "Estrategia de difusión (si no compromete aspectos confidenciales)"
                    ],
                    "recommendations": [
                        "Cuantificar en lo posible el retorno de inversión previsto",
                        "Detallar las ventajas competitivas que generará el proyecto",
                        "Considerar varios escenarios de explotación",
                        "Valorar la posibilidad de transferencia tecnológica",
                        "Incluir estrategia para gestionar la propiedad industrial/intelectual"
                    ]
                }
            ]
        }
    
    def _default_methodologies(self):
        """Proporciona una estructura de metodologías predeterminada."""
        return {
            "methodologies": [
                {
                    "id": "cientifica",
                    "title": "Método científico (para I+D)",
                    "description": "Metodología sistemática basada en evidencias para generar nuevo conocimiento.",
                    "appropriate_for": "Proyectos de Investigación y Desarrollo con alto componente científico o con incertidumbre técnica sustancial.",
                    "key_phases": [
                        {
                            "name": "Observación y formulación del problema",
                            "description": "Identificación del problema o fenómeno a investigar y planteamiento de preguntas precisas."
                        },
                        {
                            "name": "Documentación e investigación previa",
                            "description": "Revisión exhaustiva de la literatura científica y el estado del arte actual."
                        },
                        {
                            "name": "Formulación de hipótesis",
                            "description": "Planteamiento de posibles explicaciones o soluciones que puedan ser contrastadas empíricamente."
                        },
                        {
                            "name": "Diseño experimental",
                            "description": "Planificación de experimentos o pruebas que permitan validar o refutar las hipótesis."
                        },
                        {
                            "name": "Experimentación",
                            "description": "Ejecución de los experimentos diseñados en condiciones controladas."
                        },
                        {
                            "name": "Análisis de resultados",
                            "description": "Procesamiento y evaluación de los datos obtenidos para extraer conclusiones."
                        },
                        {
                            "name": "Conclusiones",
                            "description": "Interpretación de los resultados y validación o refinamiento de las hipótesis iniciales."
                        },
                        {
                            "name": "Comunicación y documentación",
                            "description": "Registro riguroso de todo el proceso y resultados para su validación y reproducibilidad."
                        }
                    ],
                    "recommendations": [
                        "Documentar rigurosamente todo el proceso, incluyendo experimentos fallidos",
                        "Incluir análisis estadístico o cuantificable de los resultados",
                        "Garantizar la reproducibilidad de los experimentos",
                        "Contrastar los resultados con el conocimiento previo",
                        "Identificar claramente las nuevas aportaciones al conocimiento"
                    ],
                    "documentation_focus": [
                        "Formulación detallada de las hipótesis",
                        "Protocolos experimentales completos y precisos",
                        "Datos crudos y procesados de los experimentos",
                        "Análisis estadístico o métodos de validación",
                        "Referencias bibliográficas exhaustivas"
                    ]
                },
                {
                    "id": "agile",
                    "title": "Metodologías ágiles (para IT)",
                    "description": "Enfoque iterativo e incremental para el desarrollo de productos o procesos tecnológicos.",
                    "appropriate_for": "Proyectos de Innovación Tecnológica centrados en desarrollo de software, nuevos procesos o mejoras tecnológicas incrementales.",
                    "key_phases": [
                        {
                            "name": "Conceptualización inicial",
                            "description": "Definición del problema, objetivos y visión general del producto o proceso a desarrollar."
                        },
                        {
                            "name": "Planificación de sprints/iteraciones",
                            "description": "Organización del trabajo en ciclos cortos (1-4 semanas) con entregables definidos."
                        },
                        {
                            "name": "Desarrollo iterativo",
                            "description": "Implementación del producto o proceso en ciclos sucesivos, cada uno añadiendo funcionalidad."
                        },
                        {
                            "name": "Pruebas continuas",
                            "description": "Verificación constante durante el proceso para detectar y corregir problemas tempranamente."
                        },
                        {
                            "name": "Revisión y adaptación",
                            "description": "Evaluación regular de los avances y ajustes en la planificación según resultados."
                        },
                        {
                            "name": "Integración y validación",
                            "description": "Combinación de los componentes desarrollados y comprobación del funcionamiento conjunto."
                        },
                        {
                            "name": "Demostración y feedback",
                            "description": "Presentación de resultados a stakeholders y recogida de opiniones para mejora."
                        },
                        {
                            "name": "Documentación y cierre",
                            "description": "Registro de los desarrollos, decisiones técnicas y conocimiento generado."
                        }
                    ],
                    "recommendations": [
                        "Mantener reuniones breves y frecuentes del equipo de desarrollo",
                        "Priorizar las funcionalidades según su valor e impacto",
                        "Monitorizar el progreso con herramientas visuales (tableros Kanban, burndown charts)",
                        "Incorporar mecanismos de feedback continuo",
                        "Documentar las decisiones técnicas y los problemas resueltos, no solo el resultado final"
                    ],
                    "documentation_focus": [
                        "Historias de usuario o requisitos funcionales",
                        "Documentación técnica de arquitectura y componentes",
                        "Registros de pruebas y validaciones",
                        "Documentación del código o proceso desarrollado",
                        "Lecciones aprendidas y problemas resueltos"
                    ]
                },
                {
                    "id": "design_thinking",
                    "title": "Design Thinking",
                    "description": "Enfoque centrado en el usuario para resolver problemas complejos mediante soluciones innovadoras.",
                    "appropriate_for": "Proyectos de innovación centrados en el usuario, desarrollo de nuevos productos o servicios con alto componente de experiencia de usuario.",
                    "key_phases": [
                        {
                            "name": "Empatizar",
                            "description": "Comprender profundamente las necesidades de los usuarios finales mediante investigación cualitativa."
                        },
                        {
                            "name": "Definir",
                            "description": "Establecer con precisión el problema a resolver desde la perspectiva del usuario."
                        },
                        {
                            "name": "Idear",
                            "description": "Generar múltiples soluciones potenciales mediante técnicas de creatividad y pensamiento divergente."
                        },
                        {
                            "name": "Prototipar",
                            "description": "Materializar las ideas más prometedoras en prototipos rápidos y de bajo coste."
                        },
                        {
                            "name": "Evaluar",
                            "description": "Probar los prototipos con usuarios reales para obtener feedback y refinar la solución."
                        },
                        {
                            "name": "Implementar",
                            "description": "Desarrollar la solución final en base a los aprendizajes obtenidos durante el proceso."
                        }
                    ],
                    "recommendations": [
                        "Involucrar a usuarios reales en todo el proceso",
                        "Favorecer la generación de múltiples ideas antes de seleccionar soluciones",
                        "Utilizar prototipado rápido para validar conceptos",
                        "Iterar basándose en feedback real, no en suposiciones",
                        "Documentar los insights de usuario y cómo influyeron en las decisiones"
                    ],
                    "documentation_focus": [
                        "Investigación de usuarios (entrevistas, observaciones, journey maps)",
                        "Definición del problema (punto de vista, insights)",
                        "Ideación (sesiones de brainstorming, selección de ideas)",
                        "Prototipos y sus evoluciones",
                        "Resultados de las evaluaciones con usuarios"
                    ]
                },
                {
                    "id": "trl",
                    "title": "Desarrollo por niveles de madurez tecnológica (TRL)",
                    "description": "Enfoque sistemático para el desarrollo tecnológico basado en la progresión a través de niveles de madurez.",
                    "appropriate_for": "Proyectos de desarrollo tecnológico complejos, especialmente útil para innovaciones que requieren investigación fundamental y un largo recorrido hasta el mercado.",
                    "key_phases": [
                        {
                            "name": "TRL 1: Investigación básica",
                            "description": "Observación de principios básicos, investigación científica inicial."
                        },
                        {
                            "name": "TRL 2: Formulación tecnológica",
                            "description": "Definición de aplicaciones prácticas potenciales, conceptos tecnológicos."
                        },
                        {
                            "name": "TRL 3: Prueba de concepto",
                            "description": "Validación analítica o experimental de los conceptos clave."
                        },
                        {
                            "name": "TRL 4: Validación en laboratorio",
                            "description": "Pruebas de componentes o procesos básicos en entorno controlado."
                        },
                        {
                            "name": "TRL 5: Validación en entorno relevante",
                            "description": "Integración de componentes y pruebas en condiciones similares a las reales."
                        },
                        {
                            "name": "TRL 6: Demostración en entorno relevante",
                            "description": "Prototipo completo funcionando en condiciones próximas a las operativas."
                        },
                        {
                            "name": "TRL 7: Demostración en entorno operativo",
                            "description": "Prototipo cerca del sistema final funcionando en condiciones reales."
                        },
                        {
                            "name": "TRL 8: Sistema completo validado",
                            "description": "Tecnología probada y calificada a través de pruebas y demostraciones."
                        },
                        {
                            "name": "TRL 9: Sistema real operativo",
                            "description": "Tecnología en su forma final y probada en entorno operativo real."
                        }
                    ],
                    "recommendations": [
                        "Definir claramente el TRL inicial y objetivo del proyecto",
                        "Establecer criterios objetivos de evaluación para pasar de un TRL a otro",
                        "Incluir hitos de validación para cada nivel TRL",
                        "Documentar rigurosamente las evidencias de cada nivel alcanzado",
                        "Considerar aspectos no solo técnicos sino también de industrialización y mercado en los TRL altos"
                    ],
                    "documentation_focus": [
                        "Evidencias científicas y técnicas para cada TRL",
                        "Protocolos de prueba específicos para cada nivel",
                        "Resultados de validaciones y demostraciones",
                        "Análisis de brechas tecnológicas entre niveles",
                        "Planes para la transición entre TRLs"
                    ]
                }
            ]
        }
    
    def _default_writing_tips(self):
        """Proporciona consejos de redacción predeterminados."""
        return {
            "general_tips": [
                {
                    "title": "Claridad y precisión",
                    "content": "Utilice un lenguaje claro, preciso y específico. Evite ambigüedades, generalidades vagas o jerga innecesaria. Cada afirmación debe ser respaldada por datos, ejemplos concretos o referencias."
                },
                {
                    "title": "Estructura lógica",
                    "content": "Organice el contenido siguiendo una estructura coherente. Cada sección debe fluir lógicamente a la siguiente, y debe quedar clara la relación entre las diferentes partes del documento."
                },
                {
                    "title": "Objetividad",
                    "content": "Mantenga un tono objetivo y respalde las afirmaciones con evidencias. Evite exageraciones o declaraciones sin fundamento sobre la innovación o impacto del proyecto."
                },
                {
                    "title": "Audiencia adaptada",
                    "content": "Considere quién evaluará el proyecto. Para evaluaciones técnicas, incluya detalles metodológicos; para evaluaciones económicas o de gestión, enfatice impacto, viabilidad y planificación."
                },
                {
                    "title": "Elementos visuales",
                    "content": "Complemente el texto con diagramas, gráficos, tablas o esquemas que faciliten la comprensión. Estos elementos son especialmente útiles para presentar metodologías, cronogramas, flujos de trabajo o comparativas técnicas."
                },
                {
                    "title": "Consistencia terminológica",
                    "content": "Mantenga la coherencia en los términos técnicos y conceptos clave a lo largo de todo el documento. Defina claramente cualquier término especializado en su primera aparición."
                },
                {
                    "title": "Enfoque en la innovación",
                    "content": "Destaque explícitamente los elementos innovadores y diferenciales del proyecto. Sea específico al explicar qué aspectos constituyen novedad respecto al estado del arte o la técnica actual."
                },
                {
                    "title": "Honestidad técnica",
                    "content": "Reconozca abiertamente las limitaciones, riesgos o incertidumbres del proyecto. Esto refuerza la credibilidad y demuestra un enfoque riguroso. Incluya siempre medidas para mitigar estos aspectos."
                }
            ],
            "technical_content_tips": [
                {
                    "title": "Estado del arte bien fundamentado",
                    "content": "Demuestre conocimiento profundo del estado actual de la tecnología o conocimiento en el ámbito del proyecto. Cite fuentes actualizadas y relevantes (artículos científicos, patentes, informes técnicos)."
                },
                {
                    "title": "Nivel de detalle técnico",
                    "content": "Proporcione suficiente detalle técnico para demostrar la viabilidad y novedad, pero sin perderse en minucias que dificulten la comprensión general. Los detalles muy específicos pueden incluirse en anexos."
                },
                {
                    "title": "Cuantificación",
                    "content": "Cuantifique siempre que sea posible los objetivos, mejoras esperadas o indicadores de éxito. Expresiones como \"mejorar sustancialmente\" o \"aumentar la eficiencia\" son demasiado vagas sin métricas concretas."
                },
                {
                    "title": "Metodología explícita",
                    "content": "Detalle explícitamente la metodología científica o técnica a emplear. Para I+D, describa el proceso experimental; para IT, el enfoque tecnológico. Esto es clave para justificar la calificación del proyecto."
                },
                {
                    "title": "Problemas y soluciones",
                    "content": "Articule claramente los problemas técnicos a resolver y las aproximaciones para abordarlos. Destaque la complejidad o incertidumbre que justifica un enfoque de I+D+i."
                }
            ],
            "fiscal_qualification_tips": [
                {
                    "title": "Vocabulario estratégico",
                    "content": "Utilice terminología alineada con los criterios fiscales de I+D+i. Para I+D, enfatice términos como \"incertidumbre científica\", \"novedad objetiva\", \"metodología experimental\"; para IT, \"aplicación práctica\", \"mejora tecnológica\", \"novedad subjetiva\"."
                },
                {
                    "title": "Evidencia de actividad sistemática",
                    "content": "Demuestre que el trabajo sigue un proceso sistemático y documentado, no actividades rutinarias. Describa protocolos, controles, registro de resultados o metodologías formales."
                },
                {
                    "title": "Disociación de componentes",
                    "content": "Diferencie claramente los componentes de I+D de aquellos de IT en proyectos mixtos. Esto facilita la aplicación correcta de deducciones fiscales según la naturaleza de cada actividad."
                },
                {
                    "title": "Trazabilidad de gastos",
                    "content": "Establezca una clara correlación entre actividades de I+D+i y los recursos asignados. Esto facilita identificar los gastos elegibles para deducciones fiscales y justificarlos en caso de inspección."
                },
                {
                    "title": "Personal cualificado",
                    "content": "Resalte la cualificación técnica del personal, especialmente para aquellos exclusivamente dedicados a I+D (cuya deducción es mayor). Especifique titulaciones, experiencia y dedicación."
                }
            ],
            "common_mistakes": [
                {
                    "title": "Generalidad excesiva",
                    "description": "Presentar ideas, objetivos o innovaciones de forma vaga, sin detalles concretos o cuantificables.",
                    "example": "\"El proyecto mejorará significativamente la eficiencia del proceso\"",
                    "correction": "\"El proyecto buscará reducir el tiempo de procesamiento en un 30% mediante la optimización algorítmica de la fase de segmentación de datos\""
                },
                {
                    "title": "Falta de diferenciación",
                    "description": "No distinguir claramente qué aspectos constituyen novedad frente al estado del arte o las soluciones existentes.",
                    "example": "\"Nuestro sistema implementará tecnología de inteligencia artificial avanzada\"",
                    "correction": "\"A diferencia de los sistemas actuales que utilizan reglas predefinidas, nuestra solución implementará un modelo de aprendizaje profundo basado en la arquitectura X, capaz de adaptarse a variaciones en los datos de entrada sin reprogramación\""
                },
                {
                    "title": "Confusión conceptual I+D/IT",
                    "description": "No diferenciar adecuadamente entre actividades de Investigación, Desarrollo o Innovación Tecnológica.",
                    "example": "\"Este proyecto de innovación investigará nuevos algoritmos...\"",
                    "correction": "\"Este proyecto de Investigación y Desarrollo (I+D) abordará la incertidumbre científica existente mediante la formulación y validación experimental de nuevos algoritmos...\""
                },
                {
                    "title": "Ausencia de riesgo técnico",
                    "description": "No mencionar o subestimar la incertidumbre, dificultades o riesgos técnicos, que son esenciales para justificar actividades de I+D.",
                    "example": "\"La implementación de la solución seguirá procedimientos estándar de desarrollo\"",
                    "correction": "\"La implementación presenta retos técnicos significativos, ya que se desconoce si el nuevo enfoque X podrá superar las limitaciones actuales en condiciones Y. Se requerirá diseñar múltiples aproximaciones y someterlas a pruebas rigurosas\""
                },
                {
                    "title": "Metodología imprecisa",
                    "description": "Describir vagamente el enfoque metodológico, sin detallar el proceso científico o técnico a seguir.",
                    "example": "\"Se analizarán diferentes opciones y se seleccionará la más adecuada\"",
                    "correction": "\"Se seguirá una metodología experimental estructurada en tres fases: 1) Formulación de hipótesis sobre los mecanismos causales; 2) Diseño de experimentos controlados con variables específicas; 3) Análisis estadístico de resultados mediante técnicas X e Y\""
                }
            ]
        }
    
    def _default_budget_categories(self):
        """Proporciona categorías de presupuesto predeterminadas."""
        return {
            "categories": [
                {
                    "id": "personal",
                    "name": "Gastos de personal",
                    "description": "Costes salariales del personal interno dedicado al proyecto, incluyendo seguridad social a cargo de la empresa.",
                    "eligible_fiscal": True,
                    "key_considerations": [
                        "Solo el tiempo efectivamente dedicado al proyecto es elegible",
                        "Debe documentarse mediante partes de trabajo o similar",
                        "Para personal exclusivo de I+D, se aplica una deducción adicional del 17%",
                        "El personal debe tener titulación adecuada para las tareas asignadas"
                    ],
                    "documentation_needed": [
                        "Contratos laborales",
                        "Titulaciones académicas",
                        "Registros de dedicación horaria",
                        "Nóminas y TC2 de la seguridad social",
                        "Descripción de tareas realizadas"
                    ],
                    "calculation_method": "Coste empresa/hora × Horas dedicadas",
                    "common_mistakes": [
                        "Incluir horas no dedicadas directamente al proyecto",
                        "Falta de registro detallado de dedicación por actividades",
                        "No distinguir entre personal de I+D y otro personal"
                    ]
                },
                {
                    "id": "colaboraciones",
                    "name": "Colaboraciones externas",
                    "description": "Contratación de servicios a universidades, centros tecnológicos u otras entidades especializadas para actividades específicas del proyecto.",
                    "eligible_fiscal": True,
                    "key_considerations": [
                        "Deben estar directamente relacionadas con el proyecto",
                        "Se recomienda contratación a entidades reconocidas por el MINECO",
                        "Debe existir un contrato o acuerdo formal de colaboración",
                        "Los resultados deben ser propiedad de la empresa contratante"
                    ],
                    "documentation_needed": [
                        "Contrato o convenio de colaboración",
                        "Facturas detalladas de los servicios",
                        "Informes técnicos de los trabajos realizados",
                        "Evidencias de los resultados obtenidos"
                    ],
                    "calculation_method": "Según presupuesto/facturación de la entidad colaboradora",
                    "common_mistakes": [
                        "Contratos genéricos sin vinculación clara al proyecto",
                        "Ausencia de informes técnicos detallados",
                        "Colaboraciones que no aportan valor técnico sustancial"
                    ]
                },
                {
                    "id": "materiales",
                    "name": "Materiales y suministros",
                    "description": "Materiales fungibles consumidos directamente en el proyecto, como materias primas, componentes, reactivos o similar.",
                    "eligible_fiscal": True,
                    "key_considerations": [
                        "Solo materiales consumidos específicamente en el proyecto",
                        "No son elegibles materiales de producción normal",
                        "Debe existir trazabilidad del uso en actividades de I+D+i"
                    ],
                    "documentation_needed": [
                        "Facturas de compra",
                        "Registros de uso/consumo en el proyecto",
                        "Albaranes o documentos de entrada en almacén",
                        "Justificación técnica de la necesidad"
                    ],
                    "calculation_method": "Coste de adquisición × Unidades consumidas",
                    "common_mistakes": [
                        "Incluir materiales de uso general no específicos del proyecto",
                        "Falta de registro del consumo real en el proyecto",
                        "No distinguir entre materiales de I+D+i y producción normal"
                    ]
                },
                {
                    "id": "amortizaciones",
                    "name": "Amortización de activos",
                    "description": "Depreciación de equipos, instrumentos y software utilizados en el proyecto durante su vida útil.",
                    "eligible_fiscal": True,
                    "key_considerations": [
                        "Solo la parte proporcional al uso en el proyecto y período de ejecución",
                        "No elegible para activos adquiridos mediante subvenciones",
                        "Debe seguir las normas contables de amortización",
                        "Solo para equipos específicos de I+D+i o con uso demostrable en estas actividades"
                    ],
                    "documentation_needed": [
                        "Facturas de adquisición",
                        "Registros de uso en el proyecto",
                        "Cálculo detallado de la amortización",
                        "Contabilidad de los activos"
                    ],
                    "calculation_method": "(Coste adquisición / Años vida útil) × (Meses uso en proyecto / 12) × (% dedicación al proyecto)",
                    "common_mistakes": [
                        "Incluir el coste total del activo en lugar de la amortización",
                        "No documentar adecuadamente el % de uso en el proyecto",
                        "Aplicar períodos de amortización incorrectos"
                    ]
                },
                {
                    "id": "patentes",
                    "name": "Patentes y propiedad industrial",
                    "description": "Costes de registro y mantenimiento de patentes generadas por el proyecto, o licencias necesarias para la investigación.",
                    "eligible_fiscal": True,
                    "key_considerations": [
                        "Elegibles los costes de solicitud y mantenimiento de patentes propias",
                        "Para licencias externas, solo si son imprescindibles para el proyecto",
                        "Debe existir vinculación directa con los resultados del proyecto"
                    ],
                    "documentation_needed": [
                        "Solicitudes de patentes o registros",
                        "Contratos de licencia",
                        "Facturas de gestorías o agentes de patentes",
                        "Tasas oficiales pagadas"
                    ],
                    "calculation_method": "Costes directos de tramitación, tasas y mantenimiento",
                    "common_mistakes": [
                        "Incluir patentes no relacionadas con el proyecto",
                        "Falta de vinculación entre la patente y la actividad de I+D+i",
                        "No distinguir entre costes elegibles y no elegibles"
                    ]
                },
                {
                    "id": "otros_gastos",
                    "name": "Otros gastos directos",
                    "description": "Otros costes directamente vinculados al proyecto, como viajes técnicos, servicios específicos o costes de certificación.",
                    "eligible_fiscal": True,
                    "key_considerations": [
                        "Debe existir relación directa y exclusiva con el proyecto",
                        "Gastos de viaje solo para actividades técnicas, no comerciales",
                        "Servicios directamente necesarios para las actividades de I+D+i"
                    ],
                    "documentation_needed": [
                        "Facturas detalladas",
                        "Justificación de la necesidad para el proyecto",
                        "Informes de viaje o actividad",
                        "Evidencias de los resultados obtenidos"
                    ],
                    "calculation_method": "Costes reales incurridos y justificados",
                    "common_mistakes": [
                        "Incluir gastos generales no específicos del proyecto",
                        "Falta de justificación técnica de la necesidad",
                        "Mezclar gastos comerciales con los técnicos"
                    ]
                },
                {
                    "id": "indirectos",
                    "name": "Gastos indirectos/generales",
                    "description": "Costes indirectos como electricidad, alquiler, comunicaciones, etc., que no pueden imputarse directamente pero son necesarios para el proyecto.",
                    "eligible_fiscal": True,
                    "key_considerations": [
                        "Solo la parte proporcional atribuible al proyecto",
                        "Se debe aplicar un método de cálculo razonable y consistente",
                        "La Administración suele aceptar hasta un 15-20% de los costes directos",
                        "Debe poder justificarse el criterio de imputación"
                    ],
                    "documentation_needed": [
                        "Método de cálculo documentado",
                        "Facturas de los gastos generales",
                        "Contabilidad analítica (si existe)",
                        "Justificación del % imputado"
                    ],
                    "calculation_method": "% aplicado sobre costes directos o fórmula justificada de reparto",
                    "common_mistakes": [
                        "Aplicar porcentajes arbitrarios sin justificación",
                        "Porcentajes excesivamente altos difíciles de defender",
                        "Falta de consistencia en el método de cálculo"
                    ]
                }
            ],
            "budget_tips": [
                {
                    "title": "Coherencia con el plan técnico",
                    "content": "El presupuesto debe reflejar fielmente las actividades descritas en el plan técnico. Cada partida debe corresponder a necesidades específicas del proyecto."
                },
                {
                    "title": "Desglose detallado",
                    "content": "Presente un presupuesto con suficiente nivel de detalle, preferiblemente desglosado por actividades o paquetes de trabajo, además de por categorías de gasto."
                },
                {
                    "title": "Justificación de importes",
                    "content": "Incluya notas explicativas que justifiquen los importes más significativos, especialmente para equipamiento costoso, personal especializado o colaboraciones externas."
                },
                {
                    "title": "Realismo en las estimaciones",
                    "content": "Evite tanto la infraestimación (que puede comprometer la viabilidad) como la sobreestimación (que reduce la credibilidad). Base las estimaciones en costes reales y experiencia previa."
                },
                {
                    "title": "Previsión de contingencias",
                    "content": "Incorpore un margen razonable para imprevistos, especialmente en proyectos con alto grado de incertidumbre técnica. Un 5-10% suele ser aceptable."
                },
                {
                    "title": "Distribución temporal",
                    "content": "Presente la distribución del presupuesto a lo largo del tiempo (anualidades o fases), coherente con el cronograma de actividades técnicas."
                }
            ]
        }
    
    def _default_checklist(self):
        """Proporciona una lista de verificación predeterminada para proyectos."""
        return {
            "sections": [
                {
                    "id": "general",
                    "title": "Aspectos generales",
                    "checklist_items": [
                        {
                            "id": "g1",
                            "text": "¿El título del proyecto refleja claramente su contenido y carácter innovador?",
                            "recommendation": "Un buen título debe ser específico, conciso y reflejar la naturaleza innovadora del proyecto. Evite títulos genéricos o puramente comerciales."
                        },
                        {
                            "id": "g2",
                            "text": "¿El resumen ejecutivo sintetiza adecuadamente los aspectos clave del proyecto?",
                            "recommendation": "El resumen debe incluir: objetivo principal, problema/necesidad, aproximación innovadora, resultados esperados e impacto previsto."
                        },
                        {
                            "id": "g3",
                            "text": "¿La estructura del documento es coherente y sigue un orden lógico?",
                            "recommendation": "Verifique que existe una progresión lógica entre secciones y que no hay información importante que falte o que esté duplicada innecesariamente."
                        },
                        {
                            "id": "g4",
                            "text": "¿El lenguaje utilizado es claro, preciso y adecuado para la audiencia objetivo?",
                            "recommendation": "Equilibre el rigor técnico con la claridad. Defina términos especializados y mantenga un tono profesional pero accesible."
                        },
                        {
                            "id": "g5",
                            "text": "¿Incluye elementos visuales (diagramas, tablas, gráficos) que faciliten la comprensión?",
                            "recommendation": "Los elementos visuales deben complementar el texto, no simplemente decorarlo, y estar correctamente referenciados y explicados."
                        }
                    ]
                },
                {
                    "id": "innovacion",
                    "title": "Elementos de innovación",
                    "checklist_items": [
                        {
                            "id": "i1",
                            "text": "¿Se identifica claramente el estado del arte o la técnica actual?",
                            "recommendation": "Debe demostrarse conocimiento actualizado de soluciones existentes, sus limitaciones y el punto de partida del proyecto."
                        },
                        {
                            "id": "i2",
                            "text": "¿Se explica con precisión qué aspectos del proyecto son novedosos o innovadores?",
                            "recommendation": "Especifique si la innovación es de producto, proceso, metodológica o tecnológica, y qué la diferencia de soluciones existentes."
                        },
                        {
                            "id": "i3",
                            "text": "¿Se distingue si la novedad es objetiva (mundial) o subjetiva (para la empresa)?",
                            "recommendation": "Para I+D se requiere principalmente novedad objetiva; para IT puede ser suficiente la novedad subjetiva correctamente justificada."
                        },
                        {
                            "id": "i4",
                            "text": "¿Se identifican los retos técnicos o la incertidumbre científica a superar?",
                            "recommendation": "Describa explícitamente los obstáculos técnicos, problemas no resueltos o aspectos donde existe incertidumbre sobre la solución."
                        },
                        {
                            "id": "i5",
                            "text": "¿Se cuantifican las mejoras esperadas respecto a soluciones existentes?",
                            "recommendation": "Siempre que sea posible, cuantifique las mejoras (ej. 30% más eficiente, reducción del 50% en tiempo de proceso, etc.)."
                        }
                    ]
                },
                {
                    "id": "metodologia",
                    "title": "Metodología y planificación",
                    "checklist_items": [
                        {
                            "id": "m1",
                            "text": "¿Se describe claramente la metodología científica o técnica a emplear?",
                            "recommendation": "Especifique el enfoque metodológico, justificando su idoneidad para abordar los retos identificados."
                        },
                        {
                            "id": "m2",
                            "text": "¿El plan de trabajo está estructurado en actividades y tareas con un cronograma detallado?",
                            "recommendation": "Incluya un desglose de actividades, dependencias entre ellas, duraciones estimadas y un diagrama temporal (Gantt o similar)."
                        },
                        {
                            "id": "m3",
                            "text": "¿Se han definido hitos y entregables específicos para cada fase del proyecto?",
                            "recommendation": "Cada fase debería tener resultados concretos y verificables que permitan evaluar el progreso."
                        },
                        {
                            "id": "m4",
                            "text": "¿Se han identificado los principales riesgos técnicos y se incluyen planes de contingencia?",
                            "recommendation": "Analice los riesgos, valore su probabilidad e impacto, y proponga medidas preventivas y correctivas."
                        },
                        {
                            "id": "m5",
                            "text": "¿Se especifican los medios materiales y técnicos necesarios para cada actividad?",
                            "recommendation": "Detalle qué equipamiento, software, instrumentación o infraestructuras serán necesarios para cada fase."
                        }
                    ]
                },
                {
                    "id": "equipo",
                    "title": "Equipo y recursos humanos",
                    "checklist_items": [
                        {
                            "id": "e1",
                            "text": "¿Se describe la composición del equipo, con perfiles y responsabilidades definidas?",
                            "recommendation": "Especifique los perfiles profesionales, titulaciones, experiencia relevante y rol en el proyecto de cada miembro del equipo."
                        },
                        {
                            "id": "e2",
                            "text": "¿Se justifica la capacitación técnica del equipo para abordar los retos del proyecto?",
                            "recommendation": "Demuestre que el personal cuenta con conocimientos y experiencia adecuados para las tareas asignadas."
                        },
                        {
                            "id": "e3",
                            "text": "¿Se identifican claramente los investigadores o técnicos exclusivos de I+D+i?",
                            "recommendation": "Para obtener mayor deducción fiscal, identifique explícitamente el personal con dedicación exclusiva a I+D y su titulación."
                        },
                        {
                            "id": "e4",
                            "text": "¿Se detallan las colaboraciones externas y su aportación concreta al proyecto?",
                            "recommendation": "Justifique la necesidad de cada colaboración externa, describiendo su contribución específica y valor añadido."
                        },
                        {
                            "id": "e5",
                            "text": "¿Se especifica la dedicación temporal de cada perfil a las diferentes actividades?",
                            "recommendation": "Incluya una matriz de asignación de recursos que muestre la dedicación de cada perfil a cada actividad o paquete de trabajo."
                        }
                    ]
                },
                {
                    "id": "presupuesto",
                    "title": "Presupuesto y aspectos económicos",
                    "checklist_items": [
                        {
                            "id": "p1",
                            "text": "¿El presupuesto está detallado por categorías de gasto y actividades o fases?",
                            "recommendation": "Presente el presupuesto con suficiente desglose, mostrando tanto el reparto por partidas como por actividades o periodos."
                        },
                        {
                            "id": "p2",
                            "text": "¿Existe coherencia entre el presupuesto y las actividades técnicas descritas?",
                            "recommendation": "Cada partida presupuestaria debe estar justificada por las necesidades técnicas del proyecto descritas anteriormente."
                        },
                        {
                            "id": "p3",
                            "text": "¿Se han diferenciado claramente los gastos elegibles para deducciones fiscales?",
                            "recommendation": "Identifique qué gastos podrían ser elegibles para I+D y cuáles para IT, facilitando la posterior justificación fiscal."
                        },
                        {
                            "id": "p4",
                            "text": "¿Se justifican adecuadamente los importes más significativos del presupuesto?",
                            "recommendation": "Incluya notas explicativas para partidas importantes (ej. colaboraciones externas costosas, equipamiento específico)."
                        },
                        {
                            "id": "p5",
                            "text": "¿Existe un plan de financiación que asegure la viabilidad económica del proyecto?",
                            "recommendation": "Especifique las fuentes de financiación previstas (recursos propios, financiación externa, subvenciones, etc.)."
                        }
                    ]
                },
                {
                    "id": "resultados",
                    "title": "Resultados e impacto",
                    "checklist_items": [
                        {
                            "id": "r1",
                            "text": "¿Se describen concretamente los resultados esperados del proyecto?",
                            "recommendation": "Especifique los productos, procesos, servicios, conocimientos o tecnologías que se obtendrán como resultado."
                        },
                        {
                            "id": "r2",
                            "text": "¿Se han definido indicadores objetivos para medir el éxito del proyecto?",
                            "recommendation": "Establezca métricas específicas que permitirán evaluar si se han alcanzado los objetivos propuestos."
                        },
                        {
                            "id": "r3",
                            "text": "¿Se detalla el impacto económico esperado para la empresa?",
                            "recommendation": "Cuantifique cuando sea posible el retorno de inversión, mejora de productividad, reducción de costes o incremento de ventas previsto."
                        },
                        {
                            "id": "r4",
                            "text": "¿Existe un plan para la protección y explotación de los resultados?",
                            "recommendation": "Describa la estrategia de protección (patentes, secreto industrial, etc.) y el plan para llevar los resultados al mercado."
                        },
                        {
                            "id": "r5",
                            "text": "¿Se contempla el impacto más allá de la empresa (sector, sociedad, medio ambiente)?",
                            "recommendation": "Considere y describa efectos positivos más amplios como creación de empleo, sostenibilidad, mejora social, etc."
                        }
                    ]
                },
                {
                    "id": "documentacion",
                    "title": "Documentación y justificación",
                    "checklist_items": [
                        {
                            "id": "d1",
                            "text": "¿Se ha previsto un sistema para documentar adecuadamente las actividades de I+D+i?",
                            "recommendation": "Planifique cómo se registrarán los avances, experimentos, prototipos y resultados para facilitar la justificación posterior."
                        },
                        {
                            "id": "d2",
                            "text": "¿Se describen los mecanismos para el seguimiento y control técnico del proyecto?",
                            "recommendation": "Defina cómo se supervisará el avance, quién lo hará y qué medidas se tomarán ante desviaciones."
                        },
                        {
                            "id": "d3",
                            "text": "¿Se han planificado reuniones o informes periódicos de seguimiento?",
                            "recommendation": "Establezca una periodicidad para informes técnicos y reuniones de evaluación del avance del proyecto."
                        },
                        {
                            "id": "d4",
                            "text": "¿Se ha considerado la posibilidad de solicitar un Informe Motivado Vinculante?",
                            "recommendation": "Para mayor seguridad jurídica en la aplicación de deducciones fiscales, considere la solicitud de un IMV al MINECO."
                        },
                        {
                            "id": "d5",
                            "text": "¿Existe un procedimiento para conservar evidencias de gastos e inversiones?",
                            "recommendation": "Defina cómo se conservarán y organizarán las facturas, nóminas, contratos y otros documentos justificativos de gastos, especialmente para una eventual inspección."
                        }
                    ]
                }
            ]
        }
    
    def get_project_section(self, section_id):
        """Obtiene información sobre una sección específica de un proyecto."""
        for section in self.sections.get('sections', []):
            if section.get('id') == section_id:
                return section
        return None
    
    def get_methodology(self, methodology_id):
        """Obtiene información sobre una metodología específica."""
        for methodology in self.methodologies.get('methodologies', []):
            if methodology.get('id') == methodology_id:
                return methodology
        return None
    
    def get_budget_category(self, category_id):
        """Obtiene información sobre una categoría de presupuesto específica."""
        for category in self.budget_categories.get('categories', []):
            if category.get('id') == category_id:
                return category
        return None
        
    def get_checklist_section(self, section_id):
        """Obtiene una sección específica de la lista de verificación."""
        for section in self.checklist.get('sections', []):
            if section.get('id') == section_id:
                return section
        return None
        
    def generate_project_structure_template(self, project_type='general'):
        """
        Genera una plantilla de estructura de proyecto basada en el tipo especificado.
        
        Args:
            project_type (str): Tipo de proyecto ('general', 'software', 'industrial', etc.)
            
        Returns:
            dict: Estructura de proyecto recomendada
        """
        # Por ahora utilizamos la estructura general para todos los tipos
        # En el futuro se puede personalizar según el tipo de proyecto
        return {
            'sections': self.sections.get('sections', []),
            'methodologies': self._recommend_methodologies(project_type),
            'writing_tips': self.writing_tips
        }
    
    def _recommend_methodologies(self, project_type):
        """Recomienda metodologías basadas en el tipo de proyecto."""
        # Implementación simplificada, en el futuro se podría hacer más sofisticada
        if project_type.lower() == 'software':
            return [m for m in self.methodologies.get('methodologies', []) 
                   if m.get('id') in ['agile', 'design_thinking']]
        elif project_type.lower() == 'industrial':
            return [m for m in self.methodologies.get('methodologies', []) 
                   if m.get('id') in ['trl']]
        elif project_type.lower() == 'investigacion':
            return [m for m in self.methodologies.get('methodologies', []) 
                   if m.get('id') in ['cientifica', 'trl']]
        else:
            # Para 'general' u otros tipos no específicos, devolver todas
            return self.methodologies.get('methodologies', [])