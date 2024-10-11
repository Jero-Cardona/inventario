document.addEventListener('DOMContentLoaded', () => {

    // Escucha el evento de submit del formulario
    document.getElementById('config-form').addEventListener('submit', async function(event) {
        event.preventDefault(); // Evitar que el formulario se envíe de forma predeterminada

        // Obtener los datos del formulario
        const formData = new FormData(event.target);
        const selectedRoutes = formData.getAll('routes'); // Obtiene todas las rutas seleccionadas

        try {
            // Hacer la solicitud POST al servidor
            const response = await fetch('/configurar-rutas', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json', // Asegurarse de que el contenido sea JSON
                },
                body: JSON.stringify({ routes: selectedRoutes }), // Enviar las rutas seleccionadas
            });

            // Verificar si la respuesta es exitosa
            if (!response.ok) {
                throw new Error(`Error al actualizar las rutas: ${response.statusText}`);
            }

            const result = await response.json();
            // Mostrar un mensaje de éxito (puedes usar SweetAlert o cualquier otra librería)
            Swal.fire({
                title: 'Éxito',
                text: 'Las rutas fueron actualizadas correctamente.',
                icon: 'success',
                confirmButtonText: 'Aceptar'
            });
            
        } catch (error) {
            // Manejar los errores de la solicitud
            const errorData = await response.json();
            console.error('Error al guardar las rutas:', error);

            // Mostrar un mensaje de error al usuario
            Swal.fire({
                title: 'Error',
                text: errorData.detail || 'Problema al procesar la solcitud',
                icon: 'error',
                confirmButtonText: 'Aceptar'
            });
        }
    });

});
