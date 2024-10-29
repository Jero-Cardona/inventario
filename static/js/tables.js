document.addEventListener("DOMContentLoaded", function() {
    const maxVisiblePages = 5;  // Número máximo de botones visibles
    const tableBodies = document.querySelectorAll(".tables-body"); // Seleccionar todos los tbody
    const paginationContainers = document.querySelectorAll(".pagination"); // Seleccionar todos los contenedores de paginación
    const rowsPerPageSelects = document.querySelectorAll(".rowsPerPage"); // Seleccionar todos los selects de "filas por página"
    const cardContainers = document.querySelectorAll(".cards-responsive"); // Seleccionar todos los contenedores de tarjetas

    tableBodies.forEach((tableBody, index) => {
        let currentPage = 1;  // Página actual para cada tabla
        let rowsPerPage = parseInt(rowsPerPageSelects[index].value); // Número de filas por página inicial por tabla
        const rows = Array.from(tableBody.querySelectorAll("tr")); // Selecciona filas del tbody actual
        const cards = Array.from(cardContainers[index]?.children || []); // Selecciona tarjetas del contenedor actual, si existe

        // Función para mostrar la página actual, ya sea en la tabla o en las tarjetas
        function showPage(page) {
            const start = (page - 1) * rowsPerPage;
            const end = start + rowsPerPage;

            // Ocultar o mostrar filas de la tabla
            rows.forEach((row, rowIndex) => {
                row.style.display = (rowIndex >= start && rowIndex < end) ? "" : "none";
            });

            // Ocultar o mostrar tarjetas si hay un contenedor de tarjetas asociado
            if (cards.length > 0) {
                cards.forEach((card, cardIndex) => {
                    card.style.display = (cardIndex >= start && cardIndex < end) ? "" : "none";
                });
            }
        }

        // Función para crear la paginación
        function createPagination() {
            const paginationContainer = paginationContainers[index]; // Contenedor de paginación correspondiente
            paginationContainer.innerHTML = "";
            const totalRows = rows.length; // Total de filas en la tabla
            const totalPages = Math.ceil(totalRows / rowsPerPage);

            // Botón "Primero"
            const firstButton = document.createElement("button");
            firstButton.textContent = "Primero";
            firstButton.classList.add("px-4", "py-2", "border", "border-gray-400", "bg-gray-50", "hover:bg-green-200", "rounded-md", "max-sm:text-sm", "max-sm:px-2");
            firstButton.addEventListener("click", () => {
                currentPage = 1;
                showPage(currentPage);
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
                    createPagination();
                }
            });
            paginationContainer.appendChild(prevButton);

            // Rango de botones visibles
            let startPage = Math.max(1, currentPage - Math.floor(maxVisiblePages / 2));
            let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);

            if (endPage - startPage < maxVisiblePages - 1) {
                startPage = Math.max(1, endPage - maxVisiblePages + 1);
            }

            // Crear botones de paginación
            for (let i = startPage; i <= endPage; i++) {
                const button = document.createElement("button");
                button.textContent = i;
                button.classList.add("px-4", "py-2", "border", "border-gray-400", "bg-gray-50", "hover:bg-green-200", "rounded-md", "max-sm:text-sm", "max-sm:px-2", "hidden", "md:block");
                if (i === currentPage) {
                    button.classList.remove("bg-gray-50", "hover:bg-green-200");
                    button.classList.add("bg-Andes", "text-white", "hover:bg-green-600");
                }
                button.addEventListener("click", () => {
                    currentPage = i;
                    showPage(currentPage);
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
                createPagination();
            });
            paginationContainer.appendChild(lastButton);
        }

        // Inicializar la primera página para esta tabla y sus tarjetas
        showPage(currentPage);
        createPagination();

        // Cambiar el número de filas por página cuando se cambie el valor del select
        rowsPerPageSelects[index].addEventListener("change", function() {
            rowsPerPage = parseInt(this.value);
            currentPage = 1;  // Reiniciar a la primera página
            showPage(currentPage);
            createPagination();
        });
    });
});
