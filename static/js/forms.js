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

document.addEventListener('DOMContentLoaded', () => {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault(); 

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
                    // Mostrar un toast de error con SweetAlert2
                    Toast.fire({
                        icon: 'error',
                        title: errorData.detail || 'Hubo un problema al enviar los datos.'
                    });
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