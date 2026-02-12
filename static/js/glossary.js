/* ==============================================
   glossary.js - Glosario interactivo de topología
============================================== */

let allTerms = {};

// Cargar términos al iniciar
document.addEventListener('DOMContentLoaded', () => {
    loadGlossaryTerms();
});

// Cargar términos desde la API
function loadGlossaryTerms() {
    fetch('/api/glossary-terms')
        .then(response => response.json())
        .then(data => {
            allTerms = data;
            renderTerms(data);
        })
        .catch(error => {
            console.error('Error al cargar glosario:', error);
            const container = document.getElementById('glossary-content');
            if (container) {
                container.innerHTML = '<p>Error al cargar los términos del glosario.</p>';
            }
        });
}

// Renderizar las tarjetas de términos
function renderTerms(terms) {
    const container = document.getElementById('glossary-content');
    if (!container) return;

    container.innerHTML = '';

    const keys = Object.keys(terms);

    if (keys.length === 0) {
        container.innerHTML = '<p>No se encontraron términos.</p>';
        return;
    }

    keys.forEach(key => {
        const term = terms[key];
        const card = document.createElement('div');
        card.className = 'glossary-term';
        card.dataset.term = term.term.toLowerCase();
        card.innerHTML = `
            <dl>
                <dt>${term.term}</dt>
                <dd><strong>Definición:</strong> ${term.definition}</dd>
                <dd><strong>Ejemplo:</strong> ${term.example}</dd>
            </dl>
        `;
        container.appendChild(card);
    });
}

// Filtrar por texto de búsqueda
function filterTerms() {
    const query = document.getElementById('search-input').value.toLowerCase().trim();

    if (!query) {
        renderTerms(allTerms);
        return;
    }

    const filtered = {};
    Object.keys(allTerms).forEach(key => {
        const term = allTerms[key];
        if (
            term.term.toLowerCase().includes(query) ||
            term.definition.toLowerCase().includes(query) ||
            term.example.toLowerCase().includes(query)
        ) {
            filtered[key] = term;
        }
    });

    renderTerms(filtered);
}

// Filtrar por letra inicial
function filterByLetter(letter) {
    if (!letter) {
        renderTerms(allTerms);
        return;
    }

    const filtered = {};
    Object.keys(allTerms).forEach(key => {
        const term = allTerms[key];
        if (term.term.toUpperCase().startsWith(letter.toUpperCase())) {
            filtered[key] = term;
        }
    });

    renderTerms(filtered);

    // Resaltar letra activa
    document.querySelectorAll('.alphabet-index a').forEach(a => {
        a.classList.remove('active');
        if (a.textContent.trim() === letter) {
            a.classList.add('active');
        }
    });
}
