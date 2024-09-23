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

document.getElementById('searchForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const productCode = document.getElementById('search-historial').value;

    fetch(`/producto/${productCode}/historial-mantenimiento`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Producto no encontrado o sin historial de mantenimiento');
            }
            return response.json(); 
        })
        .then(data => {
            showHistorialModal(data);
        })
        .catch(error => {
            console.error('Error:', error);

            // Mostrar un toast de error con SweetAlert2
            Toast.fire({
                icon: "error",
                title: error.message
            });
        });
});

// Función para mostrar la modal con los datos del historial
function showHistorialModal(data) {
    const modal = document.getElementById('historialModal');
    const historialContent = document.getElementById('historialContent');

    // Limpiar el contenido anterior
    historialContent.innerHTML = '';

    // Crear los detalles del producto con las clases de Tailwind
    const productoDetalles = `
        <h3 class="text-xl font-bold text-gray-800 mb-4">Detalles del Producto</h3>
        <div class="p-4 bg-gray-100 rounded-lg shadow-md">
            <p class="mb-2"><strong class="font-semibold">Código:</strong> ${data.producto.codigo}</p>
            <p class="mb-2"><strong class="font-semibold">Estado:</strong> ${data.producto.estado}</p>
            <p class="mb-2"><strong class="font-semibold">Responsable:</strong> ${data.producto.responsable}</p>
            <p class="mb-2"><strong class="font-semibold">Sede:</strong> ${data.producto.sede}</p>
            <p class="mb-2"><strong class="font-semibold">Proveedor:</strong> ${data.producto.proveedor}</p>
        </div>
    `;

    let historialMantenimiento = `
        <h3 class="text-xl font-bold text-gray-800 mt-6 mb-2">Historial de Mantenimiento</h3>
    `;

    data.historial_mantenimiento.forEach(mantenimiento => {
        historialMantenimiento += `
            <div class="border-t bg-gray-50 rounded-md shadow-md px-2 border-gray-300 py-4 mt-4">
                <p class="mb-2"><strong class="font-semibold">Fecha:</strong> ${mantenimiento.fecha_mantenimiento}</p>
                <p class="mb-2"><strong class="font-semibold">Observación:</strong> ${mantenimiento.observacion}</p>
                <p class="mb-2"><strong class="font-semibold">Responsable:</strong> ${mantenimiento.usuario_responsable}</p>
                <p class="mb-2"><strong class="font-semibold">Proveedor:</strong> ${mantenimiento.proveedor_mantenimiento}</p>
                <p class="mb-2"><strong class="font-semibold">Contacto Proveedor:</strong> ${mantenimiento.contacto_proveedor}</p>
            </div>
        `;
    });

    // Insertar todo el contenido en la modal
    historialContent.innerHTML = productoDetalles + historialMantenimiento;

    // Mostrar la modal con transiciones
    modal.classList.remove('opacity-0', 'pointer-events-none');
    modal.classList.add('opacity-100', 'pointer-events-auto');
}

// Asegurarse de que el DOM esté cargado antes de asignar los event listeners
document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('historialModal');
    const closeModalButton = document.getElementById('closeModal');

    // Verificar si el botón de cerrar existe
    if (closeModalButton) {
        closeModalButton.addEventListener('click', function () {
            if (modal) {
                // Ocultar la modal con transiciones
                modal.classList.remove('opacity-100', 'pointer-events-auto');
                modal.classList.add('opacity-0', 'pointer-events-none');
            }
        });
    }
});
