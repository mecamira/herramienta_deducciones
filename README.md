# Herramienta de Autoevaluación de Deducciones Fiscales I+D+i

Aplicación desarrollada para la Red Empresarial de Innovación de la Federación Asturiana de Empresarios (FADE).

## Descripción

Esta herramienta permite a las empresas realizar una autoevaluación preliminar de sus proyectos para determinar:

1. Si sus actividades podrían calificar como I+D (Investigación y Desarrollo) o IT (Innovación Tecnológica) según la normativa española.
2. Qué tipos de gastos podrían ser elegibles para deducciones fiscales.
3. Una estimación preliminar del potencial de deducción fiscal.
4. Recomendaciones sobre los siguientes pasos a seguir.

## Características

- Interfaz intuitiva para guiar al usuario a través del proceso de evaluación
- Cálculo automático de las deducciones fiscales basado en la calificación y los gastos
- Generación de informes en PDF con los resultados
- Procesamiento local de datos (no se envía información a servidores externos)
- Posibilidad de guardar y cargar evaluaciones

## Requisitos

- Python 3.7 o superior
- Flask
- Otras dependencias listadas en requirements.txt

## Instalación para desarrollo

```bash
# Clonar el repositorio o descargar los archivos
git clone <url-repositorio>

# Acceder al directorio
cd Herramienta_deducciones

# Crear un entorno virtual
python -m venv venv

# Activar el entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Ejecución

```bash
# Con el entorno virtual activado
python run.py
```

La aplicación se abrirá automáticamente en su navegador web predeterminado.

## Generación de ejecutable

Para crear un ejecutable standalone:

```bash
# Con el entorno virtual activado
pyinstaller --onefile --add-data "templates;templates" --add-data "static;static" --add-data "config;config" run.py --name DedFiscIDI
```

## Estructura del proyecto

```
Herramienta_deducciones/
├── app.py                    # Aplicación principal Flask
├── run.py                    # Script para ejecutar la aplicación
├── requirements.txt          # Dependencias
├── version.txt               # Versión de la aplicación
├── config/
│   ├── tax_rates.json        # Tasas fiscales configurables
│   └── questions.json        # Preguntas del cuestionario
├── models/
│   ├── assessment.py         # Modelo de datos para evaluaciones
│   └── calculator.py         # Lógica de cálculo de deducciones
├── static/
│   ├── css/
│   │   └── style.css         # Estilos CSS
│   ├── js/
│   │   └── main.js           # JavaScript principal
│   └── images/               # Imágenes y logos
├── templates/                # Plantillas HTML
│   ├── base.html             # Plantilla base
│   ├── welcome.html          # Página de bienvenida
│   ├── questionnaire.html    # Página de cuestionario
│   └── results.html          # Página de resultados
└── utils/
    ├── pdf_generator.py      # Generador de informes PDF
    └── helpers.py            # Funciones auxiliares
```

## Personalización

### Modificar tasas fiscales

Edite el archivo `config/tax_rates.json` para actualizar los porcentajes de deducción.

### Modificar preguntas

Edite el archivo `config/questions.json` para modificar, añadir o eliminar preguntas del cuestionario.

## Aviso legal

Esta herramienta proporciona una orientación preliminar y no vinculante. No constituye asesoramiento fiscal profesional. Los resultados obtenidos deben ser contrastados con un experto en deducciones fiscales por I+D+i.

## Licencia

Desarrollado para uso exclusivo de FADE y sus empresas asociadas.

## Contacto

Para más información o soporte, contacte con la Red Empresarial de Innovación de FADE.
