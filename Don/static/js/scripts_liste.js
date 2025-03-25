document.addEventListener('DOMContentLoaded', () => {
    // Fonction pour limiter les appels répétés (debounce)
    function debounce(func, wait) {
        let timeout;
        return function (...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }

    // Background Particles
    function createParticles() {
        const particlesContainer = document.getElementById('particles');
        if (!particlesContainer) return;

        const isMobile = window.innerWidth <= 768;
        const numParticles = isMobile ? 50 : 150; // Réduire le nombre de particules sur mobile
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
            particle.style.background = colors[Math.floor(Math.random() * colors.length)];

            particlesContainer.appendChild(particle);
        }
    }

    // Medical Silhouettes with Animation
    function createMedicalSilhouettes() {
        const silhouettesContainer = document.getElementById('medicalSilhouettes');
        if (!silhouettesContainer) return;

        const isMobile = window.innerWidth <= 768;
        const numSilhouettes = isMobile ? 5 : 15; // Réduire le nombre de silhouettes sur mobile
        for (let i = 0; i < numSilhouettes; i++) {
            const silhouette = document.createElement('div');
            silhouette.classList.add('medical-silhouette');

            silhouette.style.left = `${Math.random() * 100}%`;
            silhouette.style.top = `${Math.random() * 100}%`;
            silhouette.style.animationDelay = `${Math.random() * 5}s`;
            silhouette.style.opacity = Math.random() * 0.3;

            silhouettesContainer.appendChild(silhouette);
        }
    }

    // Enhanced Table Row Hover Effects
    function setupTableHoverEffects() {
        const table = document.querySelector('.donneur-table');
        if (!table) return;

        table.addEventListener('mouseover', (e) => {
            const row = e.target.closest('tr');
            if (row && row.parentElement.tagName === 'TBODY') {
                row.style.transition = 'all 0.3s ease';
                row.style.transform = 'scale(1.02) translateX(10px)';
                row.style.zIndex = '10';
                row.style.boxShadow = '0 10px 20px rgba(0,0,0,0.1)';
            }
        });

        table.addEventListener('mouseout', (e) => {
            const row = e.target.closest('tr');
            if (row && row.parentElement.tagName === 'TBODY') {
                row.style.transform = 'scale(1) translateX(0)';
                row.style.zIndex = '1';
                row.style.boxShadow = 'none';
            }
        });
    }

    // Enhanced Typewriter Effect for Title with Cursor
    function typewriterEffect() {
        const h1 = document.querySelector('h1');
        if (!h1) return;

        const text = h1.innerText;
        h1.innerHTML = '<span class="cursor"></span>';
        const cursor = h1.querySelector('.cursor');
        let i = 0;

        function typeWriter() {
            if (i < text.length) {
                h1.insertBefore(document.createTextNode(text.charAt(i)), cursor);
                i++;
                requestAnimationFrame(typeWriter); // Utilisation de requestAnimationFrame pour une animation fluide
            } else {
                cursor.style.animation = 'blink 0.7s infinite';
            }
        }

        typeWriter();
    }

    // Table Search Functionality with Animation
    function setupTableSearch() {
        const tableHeader = document.createElement('div');
        tableHeader.classList.add('table-header');

        const searchContainer = document.createElement('div');
        searchContainer.classList.add('search-container');
        searchContainer.innerHTML = `
            <input type="text" id="donor-search" placeholder="Rechercher un donneur..." aria-label="Rechercher un donneur">
        `;

        const container = document.querySelector('.container');
        const table = container.querySelector('.donneur-table');
        if (!table) return;

        const btnGroup = container.querySelector('.btn-group');
        tableHeader.appendChild(btnGroup);
        tableHeader.appendChild(searchContainer);
        container.insertBefore(tableHeader, table);

        const searchInput = document.getElementById('donor-search');
        const tableRows = document.querySelectorAll('.donneur-table tbody tr');

        const searchHandler = debounce(() => {
            const searchTerm = searchInput.value.toLowerCase();

            tableRows.forEach(row => {
                const rowText = row.textContent.toLowerCase();
                if (rowText.includes(searchTerm)) {
                    row.style.display = '';
                    row.style.animation = 'fadeInRow 0.5s ease';
                } else {
                    row.style.display = 'none';
                }
            });
        }, 300);

        searchInput.addEventListener('input', searchHandler);

        // Accessibilité : Permettre la recherche avec la touche "Enter"
        searchInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter') {
                searchHandler();
            }
        });
    }

    // Gestion du popup de suppression
    function setupDeleteModal() {
        const deleteButtons = document.querySelectorAll('.btn-delete');
        const modal = document.getElementById('deleteModal');
        const closeModal = document.querySelector('.modal-close');
        const cancelButton = document.getElementById('cancelDelete');
        const confirmButton = document.getElementById('confirmDelete');

        if (!modal || !closeModal || !cancelButton || !confirmButton) return;

        function openModal() {
            modal.classList.add('show');
            confirmButton.focus(); // Accessibilité : Focus sur le bouton de confirmation
        }

        function closeModalFunc() {
            modal.classList.remove('show');
        }

        deleteButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                const donneurId = button.getAttribute('data-id');
                confirmButton.setAttribute('href', `/supprimer-donneur/${donneurId}/`);
                openModal();
            });
        });

        closeModal.addEventListener('click', closeModalFunc);
        cancelButton.addEventListener('click', closeModalFunc);

        window.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModalFunc();
            }
        });

        // Accessibilité : Fermer le modal avec la touche "Échap"
        window.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && modal.classList.contains('show')) {
                closeModalFunc();
            }
        });
    }

    const style = document.createElement('style');
    style.innerHTML = `
        .cursor {
            display: inline-block;
            width: 2px;
            height: 2.5rem;
            background: var(--secondary-color);
            vertical-align: middle;
        }
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0; }
        }
        @keyframes fadeInRow {
            0% { opacity: 0; transform: translateY(10px); }
            100% { opacity: 1; transform: translateY(0); }
        }
    `;
    document.head.appendChild(style);

    createParticles();
    createMedicalSilhouettes();
    setupTableHoverEffects();
    typewriterEffect();
    setupTableSearch();
    setupDeleteModal();
});