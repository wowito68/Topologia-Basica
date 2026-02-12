/* ==============================================
   interactive.js - Funciones del laboratorio interactivo
============================================== */

let currentSpace = null;

// Obtener URL parameters
function getUrlParameter(name) {
    const params = new URLSearchParams(window.location.search);
    return params.get(name);
}

// Cargar espacio al iniciar
document.addEventListener('DOMContentLoaded', () => {
    const spaceParam = getUrlParameter('space');
    if (spaceParam) {
        document.getElementById('space-select').value = spaceParam;
        loadSpace();
    }
    
    populateExamples();
});

// Cargar espacio seleccionado
function loadSpace() {
    const select = document.getElementById('space-select');
    currentSpace = select.value;
    
    if (!currentSpace) {
        document.getElementById('analysis-section').style.display = 'none';
        document.getElementById('operations-section').style.display = 'none';
        document.getElementById('properties-section').style.display = 'none';
        document.getElementById('visualization-section').style.display = 'none';
        return;
    }
    
    // Obtener información del espacio
    fetch(`/api/space-info/${currentSpace}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('space-title').textContent = data.name;
            document.getElementById('space-description').textContent = data.description;
            document.getElementById('space-info').style.display = 'block';
            
            // Mostrar secciones
            document.getElementById('analysis-section').style.display = 'block';
            document.getElementById('operations-section').style.display = 'block';
            document.getElementById('properties-section').style.display = 'block';
            document.getElementById('visualization-section').style.display = 'block';
            
            // Actualizar ejemplos
            populateExamples();
            
            Analytics.track('space_loaded', { space: currentSpace });
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error al cargar el espacio', 'error');
        });
}

// Llenar lista de ejemplos
function populateExamples() {
    const examplesList = document.getElementById('examples-list');
    if (!examplesList) return;
    
    let examples = [];
    
    if (currentSpace === 'real_line') {
        examples = ['(0,1)', '[0,1]', '(0,1]', '[0,1)', '(0,∞)', '(-∞,0)'];
    } else if (currentSpace === 'discrete') {
        examples = ['{1}', '{2}', '{1,2}', '{1,2,3}', '{1,2,3,4}'];
    } else if (currentSpace === 'indiscrete') {
        examples = ['∅', '{1,2,3,4}', '{1}', '{1,2}'];
    } else if (currentSpace === 'cofinite') {
        examples = ['∅', 'ℕ', 'ℕ\\{1}', 'ℕ\\{1,2,3}'];
    }
    
    examplesList.innerHTML = examples.map(ex => 
        `<button class="example-btn" onclick="document.getElementById('subset-input').value='${ex}'">${ex}</button>`
    ).join('');
    
    // Agregar estilos
    const style = document.createElement('style');
    style.textContent = `
        .example-btn {
            padding: 0.5rem 0.75rem;
            background: white;
            border: 1px solid var(--border-color);
            border-radius: 0.25rem;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.9rem;
        }
        .example-btn:hover {
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
        }
    `;
    if (!document.getElementById('example-btn-style')) {
        style.id = 'example-btn-style';
        document.head.appendChild(style);
    }
}

// Analizar subconjunto
function analyzeSubset() {
    const subset = document.getElementById('subset-input').value.trim();
    
    if (!subset) {
        showNotification('Por favor ingresa un conjunto', 'warning');
        return;
    }
    
    if (!currentSpace) {
        showNotification('Por favor selecciona un espacio primero', 'warning');
        return;
    }
    
    fetch('/api/analyze-subset', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            space_type: currentSpace,
            subset: subset
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('result-open').textContent = 
            data.is_open ? '✓ Sí' : '✗ No';
        document.getElementById('result-closed').textContent = 
            data.is_closed ? '✓ Sí' : '✗ No';
        document.getElementById('result-interior').textContent = data.interior;
        document.getElementById('result-closure').textContent = data.closure;
        document.getElementById('result-boundary').textContent = data.boundary;
        document.getElementById('result-limit-points').textContent = data.limit_points;
        
        document.getElementById('analysis-results').style.display = 'block';
        
        Analytics.track('subset_analyzed', { space: currentSpace, subset: subset });
        showNotification('Análisis completado', 'success');
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error al analizar el subconjunto', 'error');
    });
}

// Realizar operación entre conjuntos
function performOperation() {
    const setA = document.getElementById('set-a').value.trim();
    const setB = document.getElementById('set-b').value.trim();
    const operation = document.getElementById('operation-select').value;
    
    if (!setA || !setB) {
        showNotification('Por favor completa ambos conjuntos', 'warning');
        return;
    }
    
    fetch('/api/set-operation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            operation: operation,
            set_a: setA,
            set_b: setB
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('operation-result').textContent = 
            `${data.set_a} ${getOperationSymbol(data.operation)} ${data.set_b} = ${data.result}`;
        document.getElementById('operation-results').style.display = 'block';
        
        Analytics.track('operation_performed', { 
            space: currentSpace,
            operation: operation,
            set_a: setA,
            set_b: setB
        });
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error al realizar la operación', 'error');
    });
}

// Obtener símbolo de operación
function getOperationSymbol(operation) {
    const symbols = {
        'union': '∪',
        'intersection': '∩',
        'difference': '\\',
        'complement': 'ᶜ',
        'symmetric_difference': 'Δ'
    };
    return symbols[operation] || operation;
}

// Analizar propiedades del espacio
function analyzeSpaceProperties() {
    if (!currentSpace) {
        showNotification('Por favor selecciona un espacio', 'warning');
        return;
    }
    
    fetch('/api/space-properties', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            space_type: currentSpace
        })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('prop-connected').textContent = 
            data.is_connected ? '✓ Sí' : '✗ No';
        document.getElementById('prop-compact').textContent = 
            data.is_compact ? '✓ Sí' : '✗ No';
        document.getElementById('prop-separable').textContent = 
            data.is_separable ? '✓ Sí' : '✗ No';
        document.getElementById('prop-hausdorff').textContent = 
            data.is_hausdorff ? '✓ Sí' : '✗ No';
        
        document.getElementById('properties-results').style.display = 'block';
        
        Analytics.track('space_properties_analyzed', { space: currentSpace });
        showNotification('Análisis de propiedades completado', 'success');
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error al analizar propiedades', 'error');
    });
}

// Generar visualización
function generateVisualization() {
    if (!currentSpace) {
        showNotification('Por favor selecciona un espacio', 'warning');
        return;
    }
    
    fetch('/api/generate-visualization', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            space_type: currentSpace
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification(data.message, 'success');
            Analytics.track('visualization_generated', { space: currentSpace });
        } else {
            showNotification('Error al generar la visualización', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error en la visualización', 'error');
    });
}

// Cargar ejercicio propuesto
function loadExercise(exerciseNum) {
    const exercises = {
        1: {
            space: 'real_line',
            sets: ['(0,1)', '[0,1]', '(0,1]', '[0,1)'],
            instruction: 'Analiza cada intervalo y determina cuál es abierto y cuál es cerrado'
        },
        2: {
            space: 'discrete',
            sets: ['{1}', '{1,2}', '{1,2,3,4}'],
            instruction: 'En topología discreta, todos los subconjuntos son abiertos'
        },
        3: {
            space: 'indiscrete',
            sets: ['∅', '{1}', '{1,2,3,4}'],
            instruction: 'En topología indiscreta, solo ∅ y el conjunto completo son abiertos'
        },
        4: {
            space: 'real_line',
            sets: ['(0,1) ∪ [1,2)', '(0,2) ∩ [1,3)'],
            instruction: 'Realiza las operaciones y determina si son abiertas o cerradas'
        }
    };
    
    const exercise = exercises[exerciseNum];
    if (exercise) {
        document.getElementById('space-select').value = exercise.space;
        loadSpace();
        
        setTimeout(() => {
            showNotification(exercise.instruction, 'info', 5000);
        }, 500);
        
        Analytics.track('exercise_loaded', { exercise: exerciseNum });
    }
}

// Teclado de acceso rápido
document.addEventListener('keydown', (e) => {
    // Shift + A: Analizar
    if (e.shiftKey && e.key === 'A') {
        analyzeSubset();
    }
    // Shift + O: Operación
    if (e.shiftKey && e.key === 'O') {
        performOperation();
    }
    // Shift + P: Propiedades
    if (e.shiftKey && e.key === 'P') {
        analyzeSpaceProperties();
    }
});

// Función para exportar resultados
function exportResults() {
    const results = {
        space: currentSpace,
        timestamp: new Date().toISOString(),
        analysis: {
            subset: document.getElementById('subset-input').value,
            isOpen: document.getElementById('result-open').textContent,
            isClosed: document.getElementById('result-closed').textContent,
            interior: document.getElementById('result-interior').textContent,
            closure: document.getElementById('result-closure').textContent,
            boundary: document.getElementById('result-boundary').textContent,
            limitPoints: document.getElementById('result-limit-points').textContent
        }
    };
    
    exportData(results, `topology_analysis_${Date.now()}.json`);
    showNotification('Resultados exportados', 'success');
}
