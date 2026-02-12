/* ==============================================
   quiz.js - Motor del cuestionario de topología
============================================== */

let questions = [];
let currentQuestion = 0;
let score = 0;
let selectedOption = null;
let answered = false;
let userAnswers = [];

// Cargar preguntas al iniciar
document.addEventListener('DOMContentLoaded', () => {
    loadStats();
});

// Iniciar cuestionario
function startQuiz() {
    fetch('/api/quiz-questions')
        .then(response => response.json())
        .then(data => {
            questions = data;
            currentQuestion = 0;
            score = 0;
            selectedOption = null;
            answered = false;
            userAnswers = [];

            document.getElementById('quiz-intro').style.display = 'none';
            document.getElementById('quiz-content').style.display = 'block';
            document.getElementById('quiz-results').style.display = 'none';

            showQuestion();

            if (typeof Analytics !== 'undefined') {
                Analytics.track('quiz_started', { totalQuestions: questions.length });
            }
        })
        .catch(error => {
            console.error('Error al cargar preguntas:', error);
            if (typeof showNotification !== 'undefined') {
                showNotification('Error al cargar las preguntas', 'error');
            }
        });
}

// Mostrar pregunta actual
function showQuestion() {
    if (currentQuestion >= questions.length) {
        showResults();
        return;
    }

    const q = questions[currentQuestion];
    selectedOption = null;
    answered = false;

    // Actualizar barra de progreso
    const progress = ((currentQuestion) / questions.length) * 100;
    document.getElementById('progress-fill').style.width = progress + '%';
    document.getElementById('question-counter').textContent =
        `Pregunta ${currentQuestion + 1} de ${questions.length}`;

    // Mostrar texto de la pregunta
    document.getElementById('question-text').textContent = q.question;

    // Generar opciones
    const container = document.getElementById('options-container');
    container.innerHTML = '';

    q.options.forEach((option, index) => {
        const optionEl = document.createElement('label');
        optionEl.className = 'option';
        optionEl.innerHTML = `
            <input type="radio" name="answer" value="${index}"
                   onchange="selectOption(${index})">
            ${option}
        `;
        container.appendChild(optionEl);
    });

    // Ocultar explicación y resetear botones
    document.getElementById('explanation').style.display = 'none';
    document.getElementById('submit-btn').style.display = 'inline-flex';
    document.getElementById('submit-btn').disabled = true;
    document.getElementById('next-btn').style.display = 'none';
}

// Seleccionar una opción
function selectOption(index) {
    if (answered) return;

    selectedOption = index;
    document.getElementById('submit-btn').disabled = false;

    // Resaltar la opción seleccionada
    document.querySelectorAll('.option').forEach((opt, i) => {
        opt.classList.remove('selected');
        if (i === index) {
            opt.classList.add('selected');
        }
    });
}

// Enviar respuesta
function submitAnswer() {
    if (selectedOption === null || answered) return;

    answered = true;
    const q = questions[currentQuestion];
    const isCorrect = selectedOption === q.correct;

    if (isCorrect) {
        score++;
    }

    userAnswers.push({
        question: q.question,
        selected: selectedOption,
        correct: q.correct,
        isCorrect: isCorrect
    });

    // Resaltar opciones correctas/incorrectas
    document.querySelectorAll('.option').forEach((opt, i) => {
        opt.classList.remove('selected');
        const radio = opt.querySelector('input');
        radio.disabled = true;

        if (i === q.correct) {
            opt.classList.add('correct');
        } else if (i === selectedOption && !isCorrect) {
            opt.classList.add('incorrect');
        }
    });

    // Mostrar explicación
    document.getElementById('explanation-text').textContent = q.explanation;
    document.getElementById('explanation').style.display = 'block';

    // Cambiar botones
    document.getElementById('submit-btn').style.display = 'none';

    if (currentQuestion < questions.length - 1) {
        document.getElementById('next-btn').textContent = 'Siguiente';
    } else {
        document.getElementById('next-btn').textContent = 'Ver Resultados';
    }
    document.getElementById('next-btn').style.display = 'inline-flex';
}

// Siguiente pregunta
function nextQuestion() {
    currentQuestion++;
    showQuestion();
}

// Mostrar resultados
function showResults() {
    document.getElementById('quiz-content').style.display = 'none';
    document.getElementById('quiz-results').style.display = 'block';

    // Actualizar puntuación
    document.getElementById('final-score').textContent = score;

    // Mensaje según puntaje
    const percentage = (score / questions.length) * 100;
    let message = '';
    if (percentage === 100) {
        message = '¡Excelente! ¡Dominas la topología de conjuntos! 🏆';
    } else if (percentage >= 80) {
        message = '¡Muy bien! Tienes un gran conocimiento de topología. 🌟';
    } else if (percentage >= 60) {
        message = '¡Bien! Pero aún puedes mejorar. Revisa los conceptos. 📚';
    } else if (percentage >= 40) {
        message = 'Necesitas repasar algunos conceptos fundamentales. 📖';
    } else {
        message = 'Te recomendamos estudiar los conceptos antes de reintentar. 💪';
    }
    document.getElementById('score-message').textContent = message;

    // Generar detalle de respuestas
    const resultsList = document.getElementById('results-list');
    resultsList.innerHTML = '';

    userAnswers.forEach((ans, i) => {
        const item = document.createElement('div');
        item.className = `result-item ${ans.isCorrect ? 'correct' : 'incorrect'}`;
        item.innerHTML = `
            <span class="result-status">${ans.isCorrect ? '✓' : '✗'}</span>
            <strong>P${i + 1}:</strong> ${ans.question}
        `;
        resultsList.appendChild(item);
    });

    // Retroalimentación
    const feedback = document.getElementById('feedback-text');
    if (percentage >= 80) {
        feedback.textContent = 'Excelente dominio de los conceptos fundamentales de topología. Estás listo para temas avanzados como espacios de Hilbert y variedades topológicas.';
    } else if (percentage >= 60) {
        feedback.textContent = 'Buen manejo de los conceptos básicos. Te recomendamos profundizar en interior, clausura y frontera antes de avanzar.';
    } else {
        feedback.textContent = 'Recomendamos repasar los conceptos fundamentales: axiomas de topología, conjuntos abiertos y cerrados, y las operaciones topológicas básicas.';
    }

    // Guardar estadísticas
    saveStats(score, questions.length);

    if (typeof Analytics !== 'undefined') {
        Analytics.trackQuizCompleted(score, questions.length);
    }
}

// Reiniciar
function restartQuiz() {
    document.getElementById('quiz-results').style.display = 'none';
    document.getElementById('quiz-intro').style.display = 'block';
}

// --- Estadísticas con localStorage ---

function saveStats(score, total) {
    let stats = JSON.parse(localStorage.getItem('topology_quiz_stats') || '{"scores":[],"attempts":0}');
    stats.scores.push({ score, total, date: new Date().toISOString() });
    stats.attempts++;
    localStorage.setItem('topology_quiz_stats', JSON.stringify(stats));
    loadStats();
}

function loadStats() {
    const stats = JSON.parse(localStorage.getItem('topology_quiz_stats') || '{"scores":[],"attempts":0}');

    const bestEl = document.getElementById('best-score');
    const avgEl = document.getElementById('avg-score');
    const attemptsEl = document.getElementById('attempts');
    const topicEl = document.getElementById('strongest-topic');

    if (!bestEl) return; // no estamos en la página de quiz

    attemptsEl.textContent = stats.attempts;

    if (stats.scores.length > 0) {
        const scores = stats.scores.map(s => s.score);
        const best = Math.max(...scores);
        const avg = (scores.reduce((a, b) => a + b, 0) / scores.length).toFixed(1);

        bestEl.textContent = `${best}/5`;
        avgEl.textContent = `${avg}/5`;
        topicEl.textContent = best >= 4 ? 'Conjuntos Abiertos' : 'En progreso';
    } else {
        bestEl.textContent = '-';
        avgEl.textContent = '-';
        topicEl.textContent = '-';
    }
}
