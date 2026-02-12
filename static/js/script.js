/* ================================================
   script.js - Funciones generales de la aplicación
================================================ */

// Smooth scroll para enlaces internos
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// Resaltar enlace activo en navegación
function updateActiveNav() {
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

// Inicializar al cargar la página
document.addEventListener('DOMContentLoaded', updateActiveNav);

// Función para mostrar notificaciones
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#6366f1'};
        color: white;
        border-radius: 0.5rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        z-index: 9999;
        animation: slideIn 0.3s ease;
    `;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, duration);
}

// Estilos de animación
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Función para hacer scroll a un elemento
function scrollToElement(selector) {
    const element = document.querySelector(selector);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Función para copiar al portapapeles
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('¡Copiado al portapapeles!', 'success', 2000);
    }).catch(() => {
        showNotification('Error al copiar', 'error');
    });
}

// Almacenamiento local para progreso del usuario
const UserProgress = {
    save: function(key, value) {
        localStorage.setItem(`topology_${key}`, JSON.stringify(value));
    },
    
    load: function(key) {
        const data = localStorage.getItem(`topology_${key}`);
        return data ? JSON.parse(data) : null;
    },
    
    remove: function(key) {
        localStorage.removeItem(`topology_${key}`);
    },
    
    clear: function() {
        const keys = Object.keys(localStorage);
        keys.forEach(key => {
            if (key.startsWith('topology_')) {
                localStorage.removeItem(key);
            }
        });
    }
};

// Registro de acciones para analytics
const Analytics = {
    track: function(action, data = {}) {
        console.log(`[Analytics] ${action}:`, data);
        const event = {
            action,
            timestamp: new Date().toISOString(),
            ...data
        };
        
        let events = UserProgress.load('analytics_events') || [];
        events.push(event);
        // Mantener solo los últimos 100 eventos
        if (events.length > 100) {
            events = events.slice(-100);
        }
        UserProgress.save('analytics_events', events);
    },
    
    trackPageView: function() {
        this.track('page_view', {
            page: window.location.pathname,
            title: document.title
        });
    },
    
    trackConceptViewed: function(conceptName) {
        this.track('concept_viewed', { concept: conceptName });
    },
    
    trackQuizCompleted: function(score, total) {
        this.track('quiz_completed', { score, total, percentage: (score/total)*100 });
    }
};

// Inicializar analytics al cargar
document.addEventListener('DOMContentLoaded', () => {
    Analytics.trackPageView();
});

// Tema claro/oscuro (opcional)
const ThemeToggle = {
    init: function() {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const savedTheme = UserProgress.load('theme') || (prefersDark ? 'dark' : 'light');
        this.setTheme(savedTheme);
    },
    
    setTheme: function(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        UserProgress.save('theme', theme);
    },
    
    toggle: function() {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        this.setTheme(newTheme);
    }
};

// Utilidades matemáticas
const MathUtils = {
    // Verificar si un intervalo es abierto
    isOpenInterval: function(interval) {
        return interval.startsWith('(') && interval.endsWith(')');
    },
    
    // Verificar si un intervalo es cerrado
    isClosedInterval: function(interval) {
        return interval.startsWith('[') && interval.endsWith(']');
    },
    
    // Extraer límites de un intervalo
    getIntervalBounds: function(interval) {
        const match = interval.match(/[\[\(](.*?)[,](.*?)[\)\]]/);
        if (match) {
            return {
                lower: parseFloat(match[1]) || match[1],
                upper: parseFloat(match[2]) || match[2],
                lowerInclusive: interval.startsWith('['),
                upperInclusive: interval.endsWith(']')
            };
        }
        return null;
    }
};

// Sistema de ayuda emergente
const HelpSystem = {
    tips: {
        'open_set': 'Un conjunto es abierto si puedes encontrar una pequeña bola alrededor de cada punto contenida en el conjunto.',
        'closed_set': 'Un conjunto es cerrado si su complemento es abierto. Alternativamente, si contiene todos sus puntos límite.',
        'interior': 'El interior es el mayor conjunto abierto contenido en tu conjunto. Los puntos "definitivamente dentro".',
        'closure': 'La clausura es el menor conjunto cerrado que contiene tu conjunto. Los puntos límite incluidos.',
        'boundary': 'La frontera está formada por los puntos en la orilla. Parte del interior ni del interior del complemento.',
    },
    
    showTip: function(topic) {
        if (this.tips[topic]) {
            showNotification(this.tips[topic], 'info', 5000);
        }
    }
};

// Función para exportar datos
function exportData(data, filename = 'datos.json') {
    const jsonString = JSON.stringify(data, null, 2);
    const blob = new Blob([jsonString], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
}

// Función para importar datos
function importData(callback) {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.onchange = (e) => {
        const file = e.target.files[0];
        const reader = new FileReader();
        reader.onload = (event) => {
            try {
                const data = JSON.parse(event.target.result);
                callback(data);
                showNotification('Datos importados correctamente', 'success');
            } catch (error) {
                showNotification('Error al importar datos', 'error');
            }
        };
        reader.readAsText(file);
    };
    input.click();
}
