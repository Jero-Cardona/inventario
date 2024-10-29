document.addEventListener('DOMContentLoaded', () => {
    let isNavigating = false; // Variable para prevenir solicitudes duplicadas

    async function fetchData(url) {
        try {
            const response = await fetch(url);

            if (response.status === 401) {
                const data = await response.json();
                Swal.fire({
                    toast: true,
                    position: 'top',
                    icon: 'info',
                    title: '¡No permitido!, tienes bloqueado el acceso a esta ruta',
                    showConfirmButton: false,
                    timer: 3000,
                    timerProgressBar: true,
                });
            } else if (response.ok) {
                window.location.href = url; // Realiza la navegación normalmente
            } else {
                const data = await response.text();
                let errorMessage = 'Ocurrió un error inesperado.';

                if (data.includes('<!DOCTYPE html>')) {
                    errorMessage = 'El servidor devolvió una página de error.';
                } else {
                    try {
                        const json = JSON.parse(data);
                        errorMessage = json.detail || 'Error desconocido.';
                    } catch (e) {
                        errorMessage = 'Error al analizar la respuesta.';
                    }
                }

                Swal.fire({
                    toast: true,
                    position: 'top',
                    icon: 'error',
                    title: errorMessage,
                    showConfirmButton: false,
                    timer: 3000,
                    timerProgressBar: true,
                });
            }
        } catch (error) {
            console.error('Error:', error);
            Swal.fire({
                toast: true,
                position: 'top',
                icon: 'error',
                title: 'Error de conexión. Servidor caído',
                showConfirmButton: false,
                timer: 3000,
                timerProgressBar: true,
            });
        } finally {
            isNavigating = false; // Resetear la variable para permitir más navegaciones
        }
    }

    // Añadir listener a los enlaces con clase 'route'
    document.querySelectorAll('.route').forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();

            if (!isNavigating) {  // Verifica si no hay una navegación en proceso
                isNavigating = true;
                const url = this.href;
                fetchData(url); // Llama a fetchData y navega a la nueva URL
            }
        });
    });

    // Manejar la navegación en el historial del navegador
    window.addEventListener('popstate', (event) => {
        if (!isNavigating) {  // Asegúrate de que no haya navegación en proceso
            isNavigating = true;
            fetchData(window.location.href); // Navega a la nueva URL
        }
    });
});
