document.addEventListener('DOMContentLoaded', function() {
    const inputsBuscador = document.querySelectorAll('.searchInput'); // Seleccionar múltiples inputs de búsqueda
    let currentPage = 1; // Mantener la página actual
    let rowsPerPage = 5; // Número de filas por página

    // Función que muestra la página actual respetando la paginación
    function showPage(page, tableBody) {
        const rows = Array.from(tableBody.querySelectorAll('tr'));
        const start = (page - 1) * rowsPerPage;
        const end = start + rowsPerPage;

        rows.forEach((row, index) => {
            row.style.display = (index >= start && index < end) ? '' : 'none';
        });
    }

    // Función que ejecuta el filtrado
    function filtrarRegistros(inputBuscador, tableBody, cardContainer) {
        const texto = inputBuscador.value.toLowerCase(); 
        const filasTabla = tableBody.querySelectorAll('tr');
        const tarjetas = cardContainer ? cardContainer.querySelectorAll('.bg-white') : [];

        if (texto.trim() === "") {
            // Si el input está vacío, aplicar la paginación normal
            showPage(currentPage, tableBody);
        } else {
            // Filtrar filas de la tabla
            filasTabla.forEach(fila => {
                const contenidoFila = fila.textContent.toLowerCase();
                fila.style.display = contenidoFila.includes(texto) ? '' : 'none';
            });

            // Filtrar tarjetas (si las hay)
            tarjetas.forEach(tarjeta => {
                const contenidoTarjeta = tarjeta.textContent.toLowerCase();
                tarjeta.style.display = contenidoTarjeta.includes(texto) ? '' : 'none';
            });
        }
    }

    // Asignar el evento 'input' a cada buscador y su tabla correspondiente
    inputsBuscador.forEach((inputBuscador, index) => {
        const tableBody = document.querySelectorAll('tbody.tables-body')[index]; // Obtener la tabla correspondiente
        const cardContainer = document.querySelectorAll('.cards-responsive')[index]; // Obtener el contenedor de tarjetas correspondiente

        inputBuscador.addEventListener('input', function() {
            filtrarRegistros(inputBuscador, tableBody, cardContainer);
        });

        // Iniciar mostrando la primera página de la tabla correspondiente
        showPage(currentPage, tableBody);
    });
});
