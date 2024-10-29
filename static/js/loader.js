function showLoader() {
    const loader = document.getElementById('loader');
    loader.classList.remove('hidden');
    loader.classList.add('flex');
}

function hideLoader() {
    const loader = document.getElementById('loader');
    loader.classList.add('hidden');
    loader.classList.remove('flex');
}

// Interceptar todas las solicitudes de GET en enlaces y formularios
document.addEventListener('DOMContentLoaded', function() {
    // Interceptar los enlaces
    document.querySelectorAll('.route').forEach(function(link) {
        link.addEventListener('click', function(event) {
            // Si el enlace tiene un href, mostrar el loader
            if (link.getAttribute('href')) {
                showLoader();

                // Esperar un momento antes de redirigir
                setTimeout(() => {
                    window.location.href = link.getAttribute('href');
                }, 100); // Esto da tiempo para mostrar el loader antes del cambio de página
                event.preventDefault();
            }
        });
    });

    // Interceptar los formularios que usan GET
    document.querySelectorAll('form').forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (form.getAttribute('method').toLowerCase() === 'get') {
                showLoader();
            }
        });
    });

    // Ocultar el loader cuando se carga la página
    window.addEventListener('load', function() {
        hideLoader();
    });
});

// Mostrar el loader al cambiar de página
window.addEventListener('beforeunload', function () {
    showLoader();
});
