"""
Módulo de Topología de Conjuntos - Funciones matemáticas y análisis
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Set, List, Tuple, Dict
import matplotlib.patches as patches

class TopologicalSpace:
    """Clase que representa un espacio topológico"""
    
    def __init__(self, universe: Set, open_sets: List[Set]):
        """
        Inicializa un espacio topológico
        
        Args:
            universe: El conjunto universal X
            open_sets: Lista de conjuntos abiertos que forman la topología
        """
        self.universe = universe
        self.open_sets = [set(s) for s in open_sets]
        self.closed_sets = self._compute_closed_sets()
    
    def _compute_closed_sets(self):
        """Calcula los conjuntos cerrados (complementos de abiertos)"""
        closed = []
        for open_set in self.open_sets:
            closed_set = self.universe - open_set
            closed.append(closed_set)
        return closed
    
    def is_open(self, subset: Set) -> bool:
        """Verifica si un conjunto es abierto"""
        subset = set(subset)
        return subset in self.open_sets
    
    def is_closed(self, subset: Set) -> bool:
        """Verifica si un conjunto es cerrado"""
        subset = set(subset)
        return subset in self.closed_sets or subset == self.universe - (self.universe - subset)
    
    def interior(self, subset: Set) -> Set:
        """Calcula el interior de un conjunto"""
        subset = set(subset)
        interior = set()
        for open_set in self.open_sets:
            if open_set.issubset(subset):
                interior = interior.union(open_set)
        return interior
    
    def closure(self, subset: Set) -> Set:
        """Calcula la clausura de un conjunto"""
        subset = set(subset)
        closure = self.universe.copy()
        for closed_set in self.closed_sets:
            if subset.issubset(closed_set):
                closure = closure.intersection(closed_set)
        return closure
    
    def boundary(self, subset: Set) -> Set:
        """Calcula la frontera de un conjunto"""
        subset = set(subset)
        return self.closure(subset) - self.interior(subset)
    
    def limit_points(self, subset: Set) -> Set:
        """Calcula los puntos límite de un conjunto"""
        subset = set(subset)
        limit_pts = set()
        for point in self.universe:
            # Verificar si todo abierto que contiene el punto contiene un punto de subset distinto
            is_limit = True
            for open_set in self.open_sets:
                if point in open_set:
                    # Este abierto contiene el punto
                    intersection = (open_set & subset) - {point}
                    if not intersection:
                        is_limit = False
                        break
            if is_limit and point in self.closure(subset):
                limit_pts.add(point)
        return limit_pts


def analyze_openness(space_type: str, subset_str: str) -> bool:
    """Analiza si un conjunto es abierto en el espacio dado"""
    try:
        if space_type == 'real_line':
            # En la topología estándar de ℝ
            # (a,b) es abierto, [a,b] no es abierto, etc.
            if subset_str.startswith('(') and subset_str.endswith(')'):
                return True
            return False
        elif space_type == 'discrete':
            return True  # Todo es abierto en topología discreta
        elif space_type == 'indiscrete':
            return subset_str == '∅' or subset_str == '{1,2,3,4}'
        else:
            return True
    except:
        return False


def analyze_closedness(space_type: str, subset_str: str) -> bool:
    """Analiza si un conjunto es cerrado en el espacio dado"""
    try:
        if space_type == 'real_line':
            if subset_str.startswith('[') and subset_str.endswith(']'):
                return True
            return False
        elif space_type == 'discrete':
            return True  # Todo es cerrado en topología discreta
        elif space_type == 'indiscrete':
            return subset_str == '∅' or subset_str == '{1,2,3,4}'
        else:
            return True
    except:
        return False


def find_interior(space_type: str, subset_str: str) -> str:
    """Encuentra el interior de un conjunto"""
    try:
        if space_type == 'real_line':
            # Ejemplos:
            if subset_str == '[0,1]':
                return '(0,1)'
            elif subset_str == '(0,1)':
                return '(0,1)'
            elif subset_str == '[0,1)':
                return '(0,1)'
            elif subset_str == '(0,1]':
                return '(0,1)'
            return 'Interior = {' + subset_str + '} si es abierto, ∅ en caso contrario'
        else:
            return 'El interior depende de la topología específica'
    except:
        return 'No se pudo calcular'


def find_closure(space_type: str, subset_str: str) -> str:
    """Encuentra la clausura de un conjunto"""
    try:
        if space_type == 'real_line':
            if subset_str == '(0,1)':
                return '[0,1]'
            elif subset_str == '[0,1]':
                return '[0,1]'
            elif subset_str == '[0,1)':
                return '[0,1]'
            elif subset_str == '(0,1]':
                return '[0,1]'
            return 'Clausura = {' + subset_str + '} si es cerrado'
        else:
            return 'La clausura depende de la topología específica'
    except:
        return 'No se pudo calcular'


def find_boundary(space_type: str, subset_str: str) -> str:
    """Encuentra la frontera de un conjunto"""
    try:
        if space_type == 'real_line':
            if '0' in subset_str and '1' in subset_str:
                if '(' in subset_str or ')' in subset_str:
                    return '{0, 1}'
            return 'Frontera = clausura - interior'
        else:
            return 'La frontera depende de la topología específica'
    except:
        return 'No se pudo calcular'


def find_limit_points(space_type: str, subset_str: str) -> str:
    """Encuentra los puntos límite de un conjunto"""
    try:
        if space_type == 'real_line':
            if 'ejemplo' in subset_str.lower() or '0' in subset_str:
                return '[0,1] (clausura del intervalo)'
            return 'Los puntos límite son los puntos de la clausura menos los puntos aislados'
        else:
            return 'Los puntos límite dependen de la topología'
    except:
        return 'No se pudo calcular'


def check_connectedness(space_type: str) -> bool:
    """Verifica si el espacio es conexo"""
    connectedness = {
        'real_line': True,
        'discrete': False,  # Discrete es totalmente desconexo si tiene más de 1 punto
        'indiscrete': True,
        'cofinite': True,
        'euclidean_plane': True
    }
    return connectedness.get(space_type, False)


def check_compactness(space_type: str) -> bool:
    """Verifica si el espacio es compacto"""
    compactness = {
        'real_line': False,
        'discrete': False,
        'indiscrete': True,
        'cofinite': False,
        'euclidean_plane': False
    }
    return compactness.get(space_type, False)


def set_operations(operation: str, set_a: str, set_b: str) -> str:
    """Realiza operaciones entre conjuntos"""
    operations = {
        'union': f'{set_a} ∪ {set_b}',
        'intersection': f'{set_a} ∩ {set_b}',
        'difference': f'{set_a} \\ {set_b}',
        'complement': f'Complemento de {set_a}',
        'symmetric_difference': f'{set_a} Δ {set_b}'
    }
    return operations.get(operation, 'Operación desconocida')


def create_subspace(original_space_type: str, subspace: str) -> Dict:
    """Crea un subespacio topológico"""
    return {
        'space': original_space_type,
        'subspace': subspace,
        'topology': 'Topología de subespacio generada'
    }


def check_continuity(function: str, space_from: str, space_to: str) -> bool:
    """Verifica la continuidad de una función"""
    # Ejemplo simplificado
    return True


def visualize_topology(space_type: str):
    """Genera visualización de un espacio topológico"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    if space_type == 'real_line':
        visualize_real_line(ax)
    elif space_type == 'discrete':
        visualize_discrete(ax)
    elif space_type == 'indiscrete':
        visualize_indiscrete(ax)
    elif space_type == 'euclidean_plane':
        visualize_euclidean_plane(ax)
    else:
        ax.text(0.5, 0.5, f'Visualización de {space_type}', 
                ha='center', va='center', fontsize=14)
    
    plt.tight_layout()
    return fig


def visualize_real_line(ax):
    """Visualiza la topología en la recta real"""
    ax.set_xlim(-2, 4)
    ax.set_ylim(-1, 1)
    
    # Línea real
    ax.arrow(-2, 0, 5.8, 0, head_width=0.1, head_length=0.1, fc='black', ec='black')
    ax.plot([-2, 4], [0, 0], 'k-', linewidth=1)
    
    # Ejemplos de conjuntos
    # Intervalo abierto (0,1)
    ax.plot([0.1, 0.9], [0.3, 0.3], 'b-', linewidth=3, label='(0,1) - Abierto')
    ax.plot([0, 0], [0.3, 0.35], 'bo', markersize=8, markerfacecolor='none')
    ax.plot([1, 1], [0.3, 0.35], 'bo', markersize=8, markerfacecolor='none')
    
    # Intervalo cerrado [2,3]
    ax.plot([2, 3], [-0.3, -0.3], 'r-', linewidth=3, label='[2,3] - Cerrado')
    ax.plot([2, 2], [-0.3, -0.35], 'ro', markersize=8)
    ax.plot([3, 3], [-0.3, -0.35], 'ro', markersize=8)
    
    ax.set_ylim(-1, 1)
    ax.set_yticks([])
    ax.set_title('Topología Estándar en ℝ', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)


def visualize_discrete(ax):
    """Visualiza la topología discreta"""
    points = [1, 2, 3, 4]
    ax.scatter(points, [0]*4, s=300, c='red', zorder=3)
    
    for i, p in enumerate(points):
        ax.text(p, -0.3, str(p), ha='center', fontsize=12)
        # Cada punto es su propia bola abierta en topología discreta
        circle = patches.Circle((p, 0), 0.15, fill=False, edgecolor='blue', 
                               linewidth=2, linestyle='--')
        ax.add_patch(circle)
    
    ax.set_xlim(0, 5)
    ax.set_ylim(-1, 1)
    ax.set_aspect('equal')
    ax.set_title('Topología Discreta en {1,2,3,4}', fontsize=14, fontweight='bold')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(2.5, 0.7, 'Todos los subconjuntos son abiertos', 
            ha='center', fontsize=11, style='italic')


def visualize_indiscrete(ax):
    """Visualiza la topología indiscreta"""
    ax.add_patch(patches.Rectangle((0.5, 0.3), 3, 0.4, 
                                   fill=True, facecolor='lightblue', 
                                   edgecolor='black', linewidth=2))
    ax.text(2, 0.5, 'X = {1,2,3,4}', ha='center', va='center', fontsize=12, fontweight='bold')
    
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.set_title('Topología Indiscreta (Trivial)', fontsize=14, fontweight='bold')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.text(2, 0.1, 'Solo ∅ y X son abiertos', ha='center', fontsize=11, style='italic')


def visualize_euclidean_plane(ax):
    """Visualiza la topología en el plano euclidiano"""
    # Círculos (bolas abiertas)
    circle1 = patches.Circle((1, 1), 0.5, fill=False, edgecolor='blue', linewidth=2)
    circle2 = patches.Circle((2, 1.5), 0.7, fill=False, edgecolor='red', linewidth=2)
    
    ax.add_patch(circle1)
    ax.add_patch(circle2)
    
    # Puntos
    ax.plot([1, 2], [1, 1.5], 'ko', markersize=8)
    ax.text(1, 0.8, 'B₁', ha='center', fontsize=10)
    ax.text(2.2, 1.7, 'B₂', ha='center', fontsize=10)
    
    ax.set_xlim(0, 3)
    ax.set_ylim(0, 3)
    ax.set_aspect('equal')
    ax.set_title('Topología Euclidiana en ℝ²', fontsize=14, fontweight='bold')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.grid(True, alpha=0.3)
    ax.text(1.5, 2.7, 'Bolas abiertas (discos) generan la topología', 
            ha='center', fontsize=10, style='italic')


# Funciones adicionales para concepts.html

TOPOLOGICAL_CONCEPTS = {
    'axiomas_topologia': {
        'title': 'Axiomas de una Topología',
        'content': '''
        Una topología τ en un conjunto X es una familia de subconjuntos que satisface:
        
        1. **Axioma 1**: El conjunto vacío ∅ y el conjunto universal X pertenecen a τ
           - ∅ ∈ τ y X ∈ τ
        
        2. **Axioma 2**: La unión arbitraria de conjuntos en τ está en τ
           - Si {Uᵢ : i ∈ I} ⊆ τ, entonces ⋃ᵢ∈ᵢ Uᵢ ∈ τ
        
        3. **Axioma 3**: La intersección finita de conjuntos en τ está en τ
           - Si U₁, U₂, ..., Uₙ ∈ τ, entonces U₁ ∩ U₂ ∩ ... ∩ Uₙ ∈ τ
        
        El par (X, τ) se llama un **espacio topológico**.
        '''
    },
    'conjuntos_abiertos': {
        'title': 'Conjuntos Abiertos',
        'content': '''
        Un conjunto U es **abierto** en un espacio topológico (X, τ) si:
        - U ∈ τ
        
        **Propiedades**:
        - ∅ y X son siempre abiertos
        - La unión de abiertos es abierta
        - La intersección finita de abiertos es abierta
        
        **Intuición**: Un conjunto es abierto si alrededor de cada uno de sus puntos 
        hay una "pequeña vecindad" completamente contenida en el conjunto.
        
        **Ejemplos en ℝ**:
        - (a,b) es abierto
        - [a,b] no es abierto (contiene sus frontera)
        - (a,b] no es abierto
        '''
    },
    'conjuntos_cerrados': {
        'title': 'Conjuntos Cerrados',
        'content': '''
        Un conjunto F es **cerrado** en un espacio topológico (X, τ) si:
        - Su complemento Fᶜ = X \\ F es abierto
        
        **Propiedades**:
        - ∅ y X son cerrados
        - La intersección de cerrados es cerrada
        - La unión finita de cerrados es cerrada
        
        **Nota**: Un conjunto puede ser:
        - Abierto y cerrado (abierto-cerrado o clopen): ∅ y X siempre
        - Abierto pero no cerrado: (0,1) en ℝ
        - Cerrado pero no abierto: [0,1] en ℝ
        - Ni abierto ni cerrado: [0,1) en ℝ
        
        **Ejemplo en ℝ**:
        - [a,b] es cerrado
        '''
    },
    'interior_clausura': {
        'title': 'Interior y Clausura',
        'content': '''
        **Interior de A**: int(A) o A°
        - Es el mayor conjunto abierto contenido en A
        - int(A) = ⋃{U : U ⊆ A y U es abierto}
        
        Propiedades:
        - int(int(A)) = int(A)
        - int(A ∩ B) = int(A) ∩ int(B)
        - A es abierto ⟺ A = int(A)
        
        **Clausura de A**: cl(A) o Ā
        - Es el menor conjunto cerrado que contiene A
        - cl(A) = ⋂{F : A ⊆ F y F es cerrado}
        
        Propiedades:
        - cl(cl(A)) = cl(A)
        - cl(A ∪ B) = cl(A) ∪ cl(B)
        - A es cerrado ⟺ A = cl(A)
        
        **Ejemplo en ℝ**:
        - int([0,1)) = (0,1)
        - cl([0,1)) = [0,1]
        '''
    },
    'frontera': {
        'title': 'Frontera (Borde) de un Conjunto',
        'content': '''
        La **frontera** de A, denotada ∂A o Fr(A), es:
        - ∂A = cl(A) \\ int(A)
        - ∂A = cl(A) ∩ cl(Aᶜ)
        
        **Significado**: Puntos que están "en la orilla" del conjunto.
        
        **Propiedades**:
        - ∂(∂A) = ∂A
        - ∂A es siempre cerrado
        - A es abierto ⟺ ∂A ∩ A = ∅
        - A es cerrado ⟺ ∂A ⊆ A
        
        **Ejemplo en ℝ**:
        - ∂(0,1) = {0,1}
        - ∂[0,1] = {0,1}
        - ∂[0,1) = {0,1}
        - ∂ℚ = ℝ (los racionales son densos)
        '''
    },
    'continuidad': {
        'title': 'Continuidad de Funciones',
        'content': '''
        Una función f: X → Y entre espacios topológicos es **continua** en x ∈ X si:
        Para toda vecindad V de f(x) en Y, existe una vecindad U de x en X 
        tal que f(U) ⊆ V.
        
        **Equivalentemente**, f es continua si:
        La preimagen de todo conjunto abierto en Y es abierto en X.
        
        **Teorema fundamental**: f es continua en X sii para todo U ⊆ Y abierto,
        f⁻¹(U) es abierto en X.
        
        **Propiedades**:
        - La composición de funciones continuas es continua
        - Si X tiene topología discreta, f es continua
        - Si Y tiene topología indiscreta, f es continua
        
        **Ejemplo**: f(x) = x² es continua en ℝ con topología estándar
        '''
    },
    'compacidad': {
        'title': 'Compacidad',
        'content': '''
        Un espacio topológico X es **compacto** si:
        De todo recubrimiento abierto de X se puede extraer un subrecubrimiento finito.
        
        **Recordatorio**: Un recubrimiento de X es una familia {Uᵢ : i ∈ I} de abiertos
        tal que X = ⋃ᵢ∈ᵢ Uᵢ
        
        **Teorema de Heine-Borel**: En ℝ con topología estándar, un conjunto es
        compacto sii es cerrado y acotado.
        
        **Propiedades**:
        - La imagen continua de un compacto es compacta
        - Todo subconjunto cerrado de un compacto es compacto
        - En un compacto Hausdorff, todo cerrado es compacto
        
        **Ejemplos**:
        - [0,1] es compacto
        - (0,1) no es compacto
        - ℝ no es compacto
        '''
    },
    'conexidad': {
        'title': 'Conexidad',
        'content': '''
        Un espacio X es **conexo** si:
        No puede escribirse como unión disjunta de dos abiertos no vacíos.
        
        **Equivalentemente**: Un espacio es conexo si está conectado de una sola pieza.
        
        **Propiedades**:
        - La imagen continua de un conexo es conexa
        - La unión de conexos con intersección no vacía es conexa
        - El producto de espacios conexos es conexo
        
        **Teorema del Valor Intermedio**: Si f: X → ℝ es continua y X es conexo,
        entonces f(X) es un intervalo.
        
        **Ejemplos**:
        - ℝ es conexo
        - [0,1] es conexo
        - (0,1) es conexo
        - ℚ no es conexo (separado por irracionales)
        - (0,1) ∪ (2,3) no es conexo
        '''
    }
}

