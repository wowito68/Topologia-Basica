"""
Aplicación Flask para enseñanza interactiva de Topología de Conjuntos
Autor: Sistema Educativo
"""

import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import json

load_dotenv()
from topology import (
    TopologicalSpace, 
    set_operations,
    visualize_topology,
    analyze_openness,
    analyze_closedness,
    find_interior,
    find_closure,
    find_boundary,
    find_limit_points,
    check_connectedness,
    check_compactness,
    create_subspace,
    check_continuity
)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Espacios topológicos predefinidos
predefined_spaces = {
    'real_line': {
        'name': 'Línea Real (ℝ)',
        'description': 'Topología estándar de números reales',
        'X': 'ℝ',
        'sets': ['(0,1)', '[0,1]', '(0,1]', '[0,1)', 'single_points', 'intervals']
    },
    'discrete': {
        'name': 'Topología Discreta',
        'description': 'Todos los subconjuntos son abiertos',
        'X': '{1, 2, 3, 4}',
        'sets': ['{1}', '{2}', '{1,2}', '{1,2,3}', '{1,2,3,4}']
    },
    'indiscrete': {
        'name': 'Topología Indiscreta (Trivial)',
        'description': 'Solo ∅ y X son abiertos',
        'X': '{1, 2, 3, 4}',
        'sets': ['∅', '{1,2,3,4}', '{1}', '{1,2}']
    },
    'cofinite': {
        'name': 'Topología Cofinita',
        'description': 'Abiertos: ∅ y complementos de conjuntos finitos',
        'X': 'ℕ',
        'sets': ['∅', 'ℕ', 'ℕ\\{1}', 'ℕ\\{1,2,3}']
    },
    'euclidean_plane': {
        'name': 'Plano Euclidiano (ℝ²)',
        'description': 'Topología estándar del plano',
        'X': 'ℝ²',
        'sets': ['Bola abierta', 'Disco cerrado', 'Rectángulo abierto', 'Cuadrante']
    }
}

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html', spaces=predefined_spaces)

@app.route('/concepts')
def concepts():
    """Página de conceptos teóricos"""
    return render_template('concepts.html')

@app.route('/interactive')
def interactive():
    """Página de actividades interactivas"""
    return render_template('interactive.html', spaces=predefined_spaces)

@app.route('/api/space-info/<space_type>')
def get_space_info(space_type):
    """API: Obtener información de un espacio topológico"""
    if space_type not in predefined_spaces:
        return jsonify({'error': 'Espacio no encontrado'}), 404
    
    return jsonify(predefined_spaces[space_type])

@app.route('/api/analyze-subset', methods=['POST'])
def analyze_subset():
    """API: Analizar un subconjunto"""
    data = request.json
    space_type = data.get('space_type')
    subset = data.get('subset')
    
    try:
        # Análisis del subconjunto
        results = {
            'is_open': analyze_openness(space_type, subset),
            'is_closed': analyze_closedness(space_type, subset),
            'interior': find_interior(space_type, subset),
            'closure': find_closure(space_type, subset),
            'boundary': find_boundary(space_type, subset),
            'limit_points': find_limit_points(space_type, subset),
            'description': f"Análisis del conjunto {subset} en {predefined_spaces[space_type]['name']}"
        }
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/set-operation', methods=['POST'])
def perform_set_operation():
    """API: Realizar operación entre conjuntos"""
    data = request.json
    operation = data.get('operation')
    set_a = data.get('set_a')
    set_b = data.get('set_b')
    
    try:
        result = set_operations(operation, set_a, set_b)
        return jsonify({
            'operation': operation,
            'set_a': set_a,
            'set_b': set_b,
            'result': result
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/space-properties', methods=['POST'])
def get_space_properties():
    """API: Obtener propiedades del espacio"""
    data = request.json
    space_type = data.get('space_type')
    
    try:
        properties = {
            'is_connected': check_connectedness(space_type),
            'is_compact': check_compactness(space_type),
            'is_separable': space_type in ('real_line', 'discrete', 'cofinite', 'euclidean_plane'),
            'is_hausdorff': space_type not in ('indiscrete', 'cofinite'),
            'description': f"Propiedades de {predefined_spaces[space_type]['name']}"
        }
        return jsonify(properties)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/generate-visualization', methods=['POST'])
def generate_visualization():
    """API: Generar visualización de topología"""
    data = request.json
    space_type = data.get('space_type')
    
    try:
        fig = visualize_topology(space_type)
        return jsonify({
            'success': True,
            'message': f'Visualización de {predefined_spaces[space_type]["name"]} generada'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/quiz')
def quiz():
    """Página de cuestionario"""
    return render_template('quiz.html')

@app.route('/api/quiz-questions')
def get_quiz_questions():
    """API: Obtener preguntas del cuestionario"""
    questions = [
        {
            'id': 1,
            'question': '¿Cuál es la característica principal de un conjunto abierto?',
            'options': [
                'Contiene todos sus puntos límite',
                'No contiene ninguno de sus puntos límite',
                'Para cada punto, existe una bola abierta contenida en el conjunto',
                'Es el complemento de un conjunto cerrado'
            ],
            'correct': 2,
            'explanation': 'Un conjunto U en un espacio topológico es abierto si para cada punto x en U, existe una bola abierta B(x) completamente contenida en U.'
        },
        {
            'id': 2,
            'question': '¿En la topología discreta, qué conjuntos son abiertos?',
            'options': [
                'Solo ∅ y X',
                'Todos los subconjuntos',
                'Solo los singletons',
                'Solo conjuntos finitos'
            ],
            'correct': 1,
            'explanation': 'En la topología discreta, TODOS los subconjuntos son abiertos, lo que la hace la topología más fina.'
        },
        {
            'id': 3,
            'question': '¿Cuál es la relación entre conjuntos abiertos y cerrados?',
            'options': [
                'Un conjunto no puede ser ni abierto ni cerrado',
                'La clausura de un conjunto cerrado es el conjunto mismo',
                'Todo abierto es cerrado',
                'En espacios finitos, abierto implica cerrado'
            ],
            'correct': 1,
            'explanation': 'La clausura de un conjunto cerrado A es el mismo conjunto: cl(A) = A. El complemento de un conjunto abierto es cerrado.'
        },
        {
            'id': 4,
            'question': '¿Qué es el interior de un conjunto?',
            'options': [
                'El mayor subconjunto abierto contenido en él',
                'El complemento del conjunto',
                'La intersección de todos los cerrados que lo contienen',
                'El conjunto de puntos límite'
            ],
            'correct': 0,
            'explanation': 'El interior int(A) es el mayor subconjunto abierto contenido en A, o equivalentemente, la unión de todos los abiertos contenidos en A.'
        },
        {
            'id': 5,
            'question': '¿Cuál es la clausura de un conjunto?',
            'options': [
                'El menor conjunto cerrado que contiene el conjunto original',
                'El conjunto vacío',
                'El interior del conjunto',
                'El complemento del conjunto'
            ],
            'correct': 0,
            'explanation': 'La clausura cl(A) es el menor conjunto cerrado que contiene al conjunto A. Equivalentemente, es la intersección de todos los cerrados que contienen A.'
        }
    ]
    return jsonify(questions)

@app.route('/glossary')
def glossary():
    """Página de glosario"""
    return render_template('glossary.html')

@app.route('/api/glossary-terms')
def get_glossary_terms():
    """API: Obtener términos del glosario"""
    terms = {
        'topologia': {
            'term': 'Topología',
            'definition': 'Una familia τ de subconjuntos de X que satisface: (1) ∅ y X están en τ, (2) la unión arbitraria de conjuntos en τ está en τ, (3) la intersección finita de conjuntos en τ está en τ.',
            'example': 'La topología estándar en ℝ está formada por uniones de intervalos abiertos'
        },
        'conjunto_abierto': {
            'term': 'Conjunto Abierto',
            'definition': 'Un subconjunto U de un espacio topológico (X, τ) si U ∈ τ. Intuitivamente, para cada punto x ∈ U existe una bola abierta alrededor de x contenida en U.',
            'example': 'El intervalo (0,1) es abierto en ℝ con la topología estándar'
        },
        'conjunto_cerrado': {
            'term': 'Conjunto Cerrado',
            'definition': 'Un subconjunto F de un espacio topológico es cerrado si su complemento es abierto.',
            'example': 'El intervalo [0,1] es cerrado en ℝ porque su complemento (-∞,0) ∪ (1,∞) es abierto'
        },
        'interior': {
            'term': 'Interior',
            'definition': 'El interior de A, denotado int(A), es el mayor conjunto abierto contenido en A. int(A) = ∪{U ⊆ A : U es abierto}',
            'example': 'int([0,1]) = (0,1) en la topología estándar de ℝ'
        },
        'clausura': {
            'term': 'Clausura',
            'definition': 'La clausura de A, denotada cl(A) o Ā, es el menor conjunto cerrado que contiene a A. cl(A) = ∩{F ⊇ A : F es cerrado}',
            'example': 'cl((0,1)) = [0,1] en la topología estándar de ℝ'
        },
        'frontera': {
            'term': 'Frontera (Borde)',
            'definition': 'La frontera de A, denotada ∂A, es el conjunto de puntos donde todo abierto contiene tanto puntos de A como su complemento. ∂A = cl(A) - int(A)',
            'example': '∂(0,1) = {0,1} en la topología estándar de ℝ'
        },
        'punto_limite': {
            'term': 'Punto Límite',
            'definition': 'Un punto x es punto límite de A si todo abierto que contiene x también contiene un punto de A distinto de x.',
            'example': '1 es punto límite de (0,1) en ℝ'
        },
        'continua': {
            'term': 'Función Continua',
            'definition': 'Una función f: X → Y es continua si la preimagen de todo conjunto abierto en Y es abierto en X.',
            'example': 'La función f(x) = x² es continua en ℝ con la topología estándar'
        },
        'compacto': {
            'term': 'Espacio Compacto',
            'definition': 'Un espacio topológico es compacto si de todo recubrimiento abierto se puede extraer un subrecubrimiento finito.',
            'example': '[0,1] con la topología estándar es compacto; (0,1) no lo es'
        },
        'conectado': {
            'term': 'Espacio Conexo',
            'definition': 'Un espacio X es conexo si no puede escribirse como unión disjunta de dos abiertos no vacíos.',
            'example': 'ℝ con la topología estándar es conexo; ℚ no es conexo'
        }
    }
    return jsonify(terms)

@app.errorhandler(404)
def not_found(error):
    """Manejo de páginas no encontradas"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    """Manejo de errores del servidor"""
    return render_template('500.html'), 500

if __name__ == '__main__':
    debug = os.getenv('FLASK_DEBUG', '1') == '1'
    app.run(debug=debug, host='127.0.0.1', port=5000)
