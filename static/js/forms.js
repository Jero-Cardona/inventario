// Configuración del toast de SweetAlert2
const Toast = Swal.mixin({
    toast: true,
    position: "top",
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
        toast.onmouseenter = Swal.stopTimer;
        toast.onmouseleave = Swal.resumeTimer;
    }
});

// Función para formatear el campo de entrada con separadores de miles
function formatInput() {
    const inputs = document.querySelectorAll('input[id="costo_inicial"]');
    
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            let value = input.value.replace(/,/g, '');  // Eliminar comas previas
            if (value) {
                value = parseInt(value, 10).toLocaleString('en-US');  // Formatear con separadores
                input.value = value;
            }
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    formatInput(); // Llamar la función para formatear al escribir

    const forms = document.querySelectorAll('.form');

    forms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();

            // Eliminar separadores de miles antes de enviar el formulario
            const input = form.querySelector('input[id="costo_inicial"]');
            if (input) {
                input.value = input.value.replace(/,/g, '');  // Eliminar comas antes de enviar
            }

            const formData = new FormData(form);
            const action = form.getAttribute('action');
            const method = form.getAttribute('method') || 'POST';

            try {
                const response = await fetch(action, {
                    method: method.toUpperCase(),
                    body: formData,
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                    }
                });

                if (!response.ok) {
                    const errorData = await response.json();

                    if (response.status === 422) {
                        Toast.fire({
                            icon: 'error',
                            title: 'Hubo un problema con la solicitud, intenta de nuevo'
                        });
                    } else if (response.status === 403) {
                        Toast.fire({
                            icon: 'error',
                            title: '¡Sesion expirada! Iniciar sesión nuevamente.'
                        });
                    } else {
                        Toast.fire({
                            icon: 'error',
                            title: errorData.detail || 'Hubo un problema al enviar los datos.'
                        });
                    }
                } else {
                    Swal.fire({
                        title: 'Éxito',
                        text: 'Datos enviados correctamente',
                        icon: 'success',
                        confirmButtonText: 'Entendido',
                        confirmButtonColor: '#13A438',
                    }).then(() => {
                        window.location.reload();
                    });
                }
            } catch (error) {
                console.error('Error en el envío del formulario:', error);
                Toast.fire({
                    icon: 'error',
                    title: 'Hubo un problema al procesar la solicitud.'
                });
            }
        });
    });
});
