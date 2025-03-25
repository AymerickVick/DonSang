// Background Particles
function createParticles() {
    const particlesContainer = document.getElementById('particles');
    if (!particlesContainer) return;

    const numParticles = 100;
    const colors = [
        'rgba(52, 152, 219, 0.1)',   // Blue
        'rgba(231, 76, 60, 0.1)',    // Red
        'rgba(46, 204, 113, 0.1)',   // Green
        'rgba(241, 196, 15, 0.1)'    // Yellow
    ];

    for (let i = 0; i < numParticles; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');

        particle.style.width = `${Math.random() * 15 + 2}px`;
        particle.style.height = particle.style.width;
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `${Math.random() * 100}%`;
        particle.style.animationDuration = `${Math.random() * 30 + 15}s`;
        particle.style.animationDelay = `${Math.random() * 10}s`;
        particle.style.opacity = Math.random() * 0.5;
        particle.style.background = colors[Math.floor(Math.random() * colors.length)];

        particlesContainer.appendChild(particle);
    }
}

// Medical Silhouettes
function createMedicalSilhouettes() {
    const silhouettesContainer = document.getElementById('medicalSilhouettes');
    if (!silhouettesContainer) return;

    const numSilhouettes = 15;
    for (let i = 0; i < numSilhouettes; i++) {
        const silhouette = document.createElement('div');
        silhouette.classList.add('medical-silhouette');

        silhouette.style.left = `${Math.random() * 100}%`;
        silhouette.style.top = `${Math.random() * 100}%`;
        silhouette.style.transform = `
            rotate(${Math.random() * 360}deg) 
            translateZ(${Math.random() * 100 - 50}px) 
            scale(${Math.random() * 0.5 + 0.5})
        `;
        silhouette.style.opacity = Math.random() * 0.3;

        silhouettesContainer.appendChild(silhouette);
    }
}

// Dynamic Form Validation
function setupFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            let isValid = true;
            const requiredFields = form.querySelectorAll('[required]');

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('invalid');
                    const errorSpan = document.createElement('span');
                    errorSpan.classList.add('validation-error');
                    errorSpan.textContent = 'Ce champ est obligatoire';
                    field.parentNode.appendChild(errorSpan);
                }
            });

            if (!isValid) {
                event.preventDefault();
            }
        });

        form.addEventListener('input', function(event) {
            if (event.target.classList.contains('invalid')) {
                event.target.classList.remove('invalid');
                const errorSpan = event.target.parentNode.querySelector('.validation-error');
                if (errorSpan) {
                    errorSpan.remove();
                }
            }
        });
    });
}

// Typewriter Title Effect
function typewriterEffect() {
    const h1 = document.querySelector('.typed-title');
    if (h1) {
        const text = h1.innerText;
        h1.innerText = '';
        let i = 0;

        function typeWriter() {
            if (i < text.length) {
                h1.innerText += text.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            }
        }

        typeWriter();
    }
}

// Interactive Form Hints
function setupFormHints() {
    const inputs = document.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.classList.add('focused');
        });

        input.addEventListener('blur', function() {
            this.classList.remove('focused');
        });
    });
}

// Initialize Everything
document.addEventListener('DOMContentLoaded', () => {
    createParticles();
    createMedicalSilhouettes();
    setupFormValidation();
    typewriterEffect();
    setupFormHints();
});