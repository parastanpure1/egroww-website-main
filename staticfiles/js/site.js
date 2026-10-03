document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.querySelector("[data-product-search]");
    const productGrid = document.querySelector("[data-product-grid]");

    if (!searchInput || !productGrid) {
        return;
    }

    const cards = Array.from(productGrid.querySelectorAll("[data-product-card]"));
    const emptyState = productGrid.querySelector("[data-search-empty-state]");

    const filterCards = () => {
        const query = searchInput.value.trim().toLowerCase();
        let visibleCount = 0;

        cards.forEach((card) => {
            const name = card.dataset.productName || "";
            const matches = !query || name.includes(query);
            card.classList.toggle("is-hidden", !matches);
            if (matches) {
                visibleCount += 1;
            }
        });

        if (emptyState) {
            emptyState.classList.toggle("is-hidden", visibleCount > 0);
        }
    };

    searchInput.addEventListener("input", filterCards);
    filterCards();
});
