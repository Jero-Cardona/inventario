document.addEventListener('DOMContentLoaded', function() {
    const inputBuscador = document.getElementById('searchInput');

    // Función que ejecuta el filtrado
    function filtrarRegistros() {
        const texto = inputBuscador.value.toLowerCase(); 
        const filasTabla = document.querySelectorAll('tbody.tables-body tr');
        const tarjetas = document.querySelectorAll('.cards-responsive .bg-white'); 

        filasTabla.forEach(fila => {
            const contenidoFila = fila.textContent.toLowerCase();
            if (contenidoFila.includes(texto)) {
                fila.style.display = ''; // Mostrar la fila si coincide
            } else {
                fila.style.display = 'none'; // Ocultar la fila si no coincide
            }
        });

        // Filtrar tarjetas (divs)
        tarjetas.forEach(tarjeta => {
            const contenidoTarjeta = tarjeta.textContent.toLowerCase(); // Obtener el contenido de la tarjeta en minúsculas
            if (contenidoTarjeta.includes(texto)) {
                tarjeta.style.display = ''; // Mostrar la tarjeta si coincide
            } else {
                tarjeta.style.display = 'none'; // Ocultar la tarjeta si no coincide
            }
        });
    }

    // Escuchar el evento 'input' del buscador
    inputBuscador.addEventListener('input', filtrarRegistros);
});
