document.addEventListener("DOMContentLoaded", function() { 
    let rowsPerPage = 5;  // Número de filas por página inicial
    let currentPage = 1;
    const maxVisiblePages = 5;  // Número máximo de botones visibles
    const tableBodies = document.querySelectorAll(".tables-body"); // Cambiado a clase
    const paginationContainers = document.querySelectorAll(".pagination"); // Cambiado a clase
    const rows = Array.from(tableBodies[0].querySelectorAll("tr")); // Selecciona filas del primer tbody

    // Obtener tarjetas de producto
    const cardContainers = document.querySelectorAll(".cards-responsive"); // Cambiado a clase
    const allCards = Array.from(cardContainers[0].children); // Selecciona tarjetas del primer contenedor

    function showPage(page, isCardView = false) {
        const start = (page - 1) * rowsPerPage;
        const end = start + rowsPerPage;

        if (isCardView) {
            // Ocultar todas las tarjetas en todos los contenedores
            cardContainers.forEach(container => {
                const cards = Array.from(container.children);
                cards.forEach((card, index) => {
                    card.style.display = (index >= start && index < end) ? "" : "none";
                });
            });
        } else {
            // Ocultar todas las filas en todos los tbody
            tableBodies.forEach(tableBody => {
                const rows = Array.from(tableBody.querySelectorAll("tr"));
                rows.forEach((row, index) => {
                    row.style.display = (index >= start && index < end) ? "" : "none";
                });
            });
        }
    }

    function createPagination() {
        paginationContainers.forEach(paginationContainer => {
            paginationContainer.innerHTML = ""; 
            const totalRows = Array.from(tableBodies[0].querySelectorAll("tr")).length; 
            const totalPages = Math.ceil(totalRows / rowsPerPage);

            // Botón "Primero"
            const firstButton = document.createElement("button");
            firstButton.textContent = "Primero";
            firstButton.classList.add("px-4", "py-2", "border", "border-gray-400", "bg-gray-50", "hover:bg-green-200", "rounded-md", "max-sm:text-sm", "max-sm:px-2");
            firstButton.addEventListener("click", () => {
                currentPage = 1;
                showPage(currentPage);
                showPage(currentPage, true);
                createPagination();
            });
            paginationContainer.appendChild(firstButton);

            // Botón "Anterior"
            const prevButton = document.createElement("button");
            prevButton.textContent = "Anterior";
            prevButton.classList.add("px-4", "py-2", "border", "border-gray-400", "bg-gray-50", "hover:bg-green-200", "rounded-md", "max-sm:text-sm", "max-sm:px-2");
            prevButton.disabled = currentPage === 1;
            prevButton.addEventListener("click", () => {
                if (currentPage > 1) {
                    currentPage--;
                    showPage(currentPage);
                    showPage(currentPage, true);
                    createPagination();
                }
            });
            paginationContainer.appendChild(prevButton);

            // Cálculo del rango de botones visibles
            let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
            let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);

            if (endPage - startPage < maxVisiblePages - 1) {
                startPage = Math.max(1, endPage - maxVisiblePages + 1);
            }

            // Crear botones de página visibles
            for (let i = startPage; i <= endPage; i++) {
                const button = document.createElement("button");
                button.textContent = i;
                button.classList.add("px-4", "py-2", "border", "border-gray-400", "bg-gray-50", "hover:bg-green-200", "rounded-md", "max-sm:text-sm", "max-sm:px-2", "hidden", "md:block");
                if (i === currentPage) {
                    button.classList.remove("bg-gray-50", "hover:bg-green-200");
                    button.classList.add("bg-[#13A438]", "text-white", "hover:bg-green-600");
                }
                button.addEventListener("click", () => {
                    currentPage = i;
                    showPage(currentPage);
                    showPage(currentPage, true); // Mostrar la página correspondiente en tarjetas
                    createPagination();
                });
                paginationContainer.appendChild(button);
            }
            // Botón "Siguiente"
            const nextButton = document.createElement("button");
            nextButton.textContent = "Siguiente";
            nextButton.classList.add("px-4", "py-2", "border", "border-gray-400", "bg-gray-50", "hover:bg-green-200", "rounded-md", "max-sm:text-sm", "max-sm:px-2");
            nextButton.disabled = currentPage === totalPages;
            nextButton.addEventListener("click", () => {
                if (currentPage < totalPages) {
                    currentPage++;
                    showPage(currentPage);
                    showPage(currentPage, true);
                    createPagination();
                }
            });
            paginationContainer.appendChild(nextButton);

            // Botón "Último"
            const lastButton = document.createElement("button");
            lastButton.textContent = "Último";
            lastButton.classList.add("px-4", "py-2", "border", "border-gray-400", "bg-gray-50", "hover:bg-green-200", "rounded-md", "max-sm:text-sm", "max-sm:px-2");
            lastButton.addEventListener("click", () => {
                currentPage = totalPages;
                showPage(currentPage);
                showPage(currentPage, true); // Mostrar la última página en tarjetas
                createPagination();
            });
            paginationContainer.appendChild(lastButton);
        });
    }

    // Inicializar con la primera página
    showPage(currentPage);
    showPage(currentPage, true); 
    createPagination();

    document.querySelectorAll(".rowsPerPage").forEach(selectElement => {
        selectElement.addEventListener("change", function() {
            rowsPerPage = parseInt(this.value);
            currentPage = 1; 
            createPagination();
            showPage(currentPage); 
            showPage(currentPage, true); 
        });
    });
});
