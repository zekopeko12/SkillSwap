console.log("SkillSwap static assets loaded.");



function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerText = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}

document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('skill-search');
    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            const cards = document.querySelectorAll('.listing-card');
            const noResults = document.getElementById('no-results');
            let foundAny = false;

            cards.forEach(card => {
                const text = card.innerText.toLowerCase();
                const isMatch = text.includes(term);
                card.style.display = isMatch ? 'block' : 'none';
                if (isMatch) foundAny = true;
            });

            if (noResults) noResults.style.display = foundAny ? 'none' : 'block';
        });
    }
    
    // Use Event Delegation to handle all form submissions reliably
    document.addEventListener('submit', (event) => {
        const form = event.target;

        // Handle Cancellation Confirmation
        const statusInput = form.querySelector('input[name="status"]');

        if (statusInput && statusInput.value === 'cancelled') {
            const confirmed = confirm(
                "Are you sure you want to cancel this booking? This action cannot be undone."
            );

            if (!confirmed) {
                event.preventDefault();
                return;
            }
        }

        // Handle Deletion Confirmation
        const actionInput = form.querySelector('input[name="action"]');

        if (actionInput && actionInput.value === 'delete') {
            const confirmed = confirm(
                "Are you sure you want to delete this listing? This action cannot be undone."
            );

            if (!confirmed) {
                event.preventDefault();
            }
        }
    });

    const toggle = document.getElementById('dark-toggle');
    
    if (toggle) {
        toggle.addEventListener('click', () => {
            const isDark = document.documentElement.classList.toggle('dark-mode');
            
            showToast(isDark ? "Dark Mode Enabled" : "Light Mode Enabled");

            localStorage.setItem(
                'darkMode',
                document.documentElement.classList.contains('dark-mode')
            );
        });
    }

    // 3. Generic Sorting Function
    function sortElements(containerId, cardClass, sortBy) {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        const cards = Array.from(container.querySelectorAll(cardClass));
        cards.sort((a, b) => {
            if (sortBy.startsWith('date')) {
                const dateA = new Date(a.dataset.date);
                const dateB = new Date(b.dataset.date);
                return sortBy === 'date-asc' ? dateA - dateB : dateB - dateA;
            } else if (sortBy.startsWith('price')) {
                const priceA = parseFloat(a.dataset.price);
                const priceB = parseFloat(b.dataset.price);
                return sortBy === 'price-asc' ? priceA - priceB : priceB - priceA;
            }
            return 0;
        });

        cards.forEach(card => container.appendChild(card));
    }

    const sortSelect = document.getElementById('sort-select');
    if (sortSelect) {
        sortSelect.addEventListener('change', (e) => {
            const sortBy = e.target.value;
            sortElements('student-bookings', '.booking-card', sortBy);
            sortElements('teacher-bookings', '.booking-card', sortBy);
        });
    }

    const listingSortSelect = document.getElementById('listing-sort-select');
    if (listingSortSelect) {
        listingSortSelect.addEventListener('change', (e) => {
            const sortBy = e.target.value;
            sortElements('listings-container', '.listing-card', sortBy);
        });
    }
});