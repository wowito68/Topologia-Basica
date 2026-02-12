# Topologia de Conjuntos - Portal Educativo Interactivo

Plataforma web educativa desarrollada con Flask para la ensenanza interactiva de Topologia de Conjuntos. El proyecto ofrece explicaciones teoricas, un laboratorio interactivo para analizar espacios topologicos, un cuestionario de evaluacion y un glosario de terminos matematicos.

---

## Tabla de Contenidos

1. [Descripcion General](#descripcion-general)
2. [Caracteristicas](#caracteristicas)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Requisitos Previos](#requisitos-previos)
5. [Instalacion](#instalacion)
6. [Ejecucion](#ejecucion)
7. [Uso de la Aplicacion](#uso-de-la-aplicacion)
8. [API REST](#api-rest)
9. [Espacios Topologicos Disponibles](#espacios-topologicos-disponibles)
10. [Tecnologias Utilizadas](#tecnologias-utilizadas)

---

## Descripcion General

Este proyecto es una aplicacion web que sirve como herramienta pedagogica para el estudio de la topologia de conjuntos, una rama fundamental de las matematicas. La plataforma permite a los estudiantes:

- Estudiar los conceptos teoricos de topologia a traves de articulos detallados.
- Experimentar en un laboratorio interactivo con diferentes espacios topologicos.
- Analizar propiedades de conjuntos como apertura, clausura, interior, frontera y puntos limite.
- Evaluar sus conocimientos a traves de un cuestionario con retroalimentacion inmediata.
- Consultar un glosario completo de terminos y definiciones.

---

## Caracteristicas

### Modulo de Conceptos Teoricos
Articulos detallados sobre los fundamentos de la topologia, incluyendo:
- Axiomas de una topologia.
- Conjuntos abiertos y cerrados.
- Interior, clausura y frontera de un conjunto.
- Puntos limite y puntos de acumulacion.
- Continuidad de funciones entre espacios topologicos.
- Compacidad y conexidad.

### Laboratorio Interactivo
Herramienta para explorar y analizar espacios topologicos en tiempo real:
- Selector de espacio topologico (Linea Real, Discreta, Indiscreta, Cofinita, Plano Euclidiano).
- Analisis de subconjuntos: determinar si son abiertos, cerrados, calcular interior, clausura, frontera y puntos limite.
- Operaciones entre conjuntos: union, interseccion, diferencia, complemento y diferencia simetrica.
- Verificacion de propiedades del espacio: conexidad, compacidad, separabilidad y condicion de Hausdorff.
- Generacion de visualizaciones graficas mediante Matplotlib.

### Cuestionario de Evaluacion
Cuestionario de opcion multiple con cinco preguntas sobre conceptos fundamentales de topologia. Incluye retroalimentacion y explicacion detallada para cada respuesta.

### Glosario
Diccionario de terminos topologicos con definiciones formales y ejemplos. Incluye: topologia, conjunto abierto, conjunto cerrado, interior, clausura, frontera, punto limite, funcion continua, espacio compacto y espacio conexo.

---

## Estructura del Proyecto

```
Virtualizacion/
|-- app.py                  # Aplicacion principal Flask (rutas y API)
|-- topology.py             # Motor matematico de topologia
|-- requirements.txt        # Dependencias del proyecto
|-- .env                    # Variables de entorno (no versionado)
|-- .gitignore              # Archivos excluidos de Git
|
|-- templates/
|   |-- index.html          # Pagina principal
|   |-- concepts.html       # Pagina de conceptos teoricos
|   |-- interactive.html    # Laboratorio interactivo
|   |-- quiz.html           # Cuestionario de evaluacion
|   |-- glossary.html       # Glosario de terminos
|   |-- 404.html            # Pagina de error 404
|   |-- 500.html            # Pagina de error 500
|
|-- static/
|   |-- css/
|   |   |-- style.css       # Hoja de estilos principal
|   |
|   |-- js/
|       |-- script.js       # Logica general del sitio
|       |-- interactive.js  # Logica del laboratorio interactivo
|       |-- quiz.js         # Logica del cuestionario
|       |-- glossary.js     # Logica del glosario
|
|-- venv/                   # Entorno virtual de Python (no versionado)
```

---

## Requisitos Previos

- Python 3.8 o superior.
- pip (gestor de paquetes de Python).
- Acceso a un terminal o linea de comandos.

---

## Instalacion

### 1. Clonar el repositorio

```bash
git clone <https://github.com/wowito68/Topologia-Basica.git>
cd Virtualizacion
```

### 2. Crear un entorno virtual

```bash
python3 -m venv venv
```

### 3. Activar el entorno virtual

En Linux o macOS:

```bash
source venv/bin/activate
```

En Windows:

```bash
venv\Scripts\activate
```

### 4. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar las variables de entorno

Crear un archivo `.env` en la raiz del proyecto con el siguiente contenido:

```
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1
SECRET_KEY=tu-clave-secreta-aqui
```

---

## Ejecucion

### Iniciar el servidor de desarrollo

```bash
source venv/bin/activate
python app.py
```

La aplicacion se ejecutara en `http://127.0.0.1:5000` por defecto.

### Notas sobre la ejecucion

- El servidor se ejecuta en modo debug por defecto (configurable a traves de `FLASK_DEBUG` en `.env`).
- Si el puerto 5000 esta ocupado por otro proceso, se debe detener dicho proceso o modificar el puerto en `app.py` (linea 309).
- Para detener el servidor, presionar `Ctrl+C` en la terminal.

---

## Uso de la Aplicacion

### Pagina Principal (/)
Pagina de bienvenida con una vista general del contenido disponible, tarjetas informativas sobre las secciones, listado de espacios topologicos disponibles y una ruta de aprendizaje recomendada de cuatro pasos.

### Conceptos (/concepts)
Seccion de lectura con articulos sobre cada concepto topologico. Incluye una barra lateral de navegacion con enlaces internos a cada tema. Los articulos contienen definiciones formales, propiedades, ejemplos y formulas en notacion matematica.

### Laboratorio Interactivo (/interactive)
Panel de control con dos areas principales:
- **Panel izquierdo**: Selector de espacio topologico, campo de entrada para subconjuntos y botones para analizar propiedades, realizar operaciones y generar visualizaciones.
- **Panel derecho**: Seccion de ayuda con ejemplos de conjuntos, consejos de uso y un mini-glosario de terminos clave.

### Cuestionario (/quiz)
Evaluacion de cinco preguntas de opcion multiple. Al seleccionar una respuesta, se muestra inmediatamente si es correcta o incorrecta junto con una explicacion. Al finalizar, se muestra la puntuacion total.

### Glosario (/glossary)
Listado alfabetico de terminos topologicos. Cada entrada incluye el termino, su definicion formal y un ejemplo concreto.

---

## API REST

La aplicacion expone los siguientes endpoints:

| Metodo | Ruta                          | Descripcion                                       |
|--------|-------------------------------|---------------------------------------------------|
| GET    | `/api/space-info/<tipo>`      | Informacion de un espacio topologico               |
| POST   | `/api/analyze-subset`         | Analisis completo de un subconjunto               |
| POST   | `/api/set-operation`          | Operacion entre dos conjuntos                     |
| POST   | `/api/space-properties`       | Propiedades del espacio (conexidad, compacidad)   |
| POST   | `/api/generate-visualization` | Generar visualizacion grafica de la topologia     |
| GET    | `/api/quiz-questions`         | Obtener las preguntas del cuestionario             |
| GET    | `/api/glossary-terms`         | Obtener todos los terminos del glosario            |

### Ejemplo de uso del API

Analizar un subconjunto:

```bash
curl -X POST http://127.0.0.1:5000/api/analyze-subset \
  -H "Content-Type: application/json" \
  -d '{"space_type": "real_line", "subset": "(0,1)"}'
```

Respuesta:

```json
{
  "is_open": true,
  "is_closed": false,
  "interior": "(0,1)",
  "closure": "[0,1]",
  "boundary": "{0, 1}",
  "limit_points": "[0,1] (clausura del intervalo)",
  "description": "Analisis del conjunto (0,1) en Linea Real"
}
```

---

## Espacios Topologicos Disponibles

| Espacio              | Conjunto Universal | Descripcion                                        |
|----------------------|--------------------|----------------------------------------------------|
| Linea Real           | R                  | Topologia estandar de numeros reales               |
| Topologia Discreta   | {1, 2, 3, 4}      | Todos los subconjuntos son abiertos                |
| Topologia Indiscreta | {1, 2, 3, 4}      | Solo el vacio y X son abiertos                     |
| Topologia Cofinita   | N                  | Abiertos: vacio y complementos de conjuntos finitos|
| Plano Euclidiano     | R x R              | Topologia estandar del plano                       |

---

## Tecnologias Utilizadas

### Backend
- **Python 3** - Lenguaje de programacion principal.
- **Flask 3.0.0** - Framework web para servir la aplicacion y el API REST.
- **Werkzeug 3.0.1** - Biblioteca WSGI utilizada internamente por Flask.
- **Jinja2 3.1.2** - Motor de plantillas para renderizar las vistas HTML.
- **python-dotenv 1.0.0** - Carga de variables de entorno desde el archivo `.env`.

### Motor Matematico
- **NumPy 1.26.2** - Biblioteca para calculo numerico.
- **Matplotlib 3.8.2** - Generacion de visualizaciones y graficas de espacios topologicos.

### Frontend
- **HTML5** - Estructura de las paginas.
- **CSS3** - Estilos personalizados con tema oscuro, tipografia Inter y JetBrains Mono, y diseno responsive.
- **JavaScript (ES6)** - Logica del lado del cliente para interactividad, cuestionarios y comunicacion con el API.

---

## Licencia

Proyecto academico con fines educativos.
