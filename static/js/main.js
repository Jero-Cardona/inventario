document.addEventListener('DOMContentLoaded', function () {
    const swaledits = document.querySelectorAll('.editar');
    const swaldelete = document.querySelectorAll('.delete');
    const swalldownloand = document.querySelectorAll('.descargar');

    // Asigna un evento de clic a cada botón con la clase 'delete'
    swaldelete.forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault(); // Evita el comportamiento predeterminado del enlace

            const url = this.getAttribute('href'); // Obtiene la URL del atributo 'data-href'

            // Muestra un SweetAlert2 de confirmación
            Swal.fire({
                title: '¿Estás seguro?',
                text: 'Eliminarias este registro en el aplicativo web',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Sí',
                cancelButtonText: 'Cancelar',
                confirmButtonColor:  '#13A438',
                cancelButtonColor: '#084F21',
            }).then((result) => {
                // Si se hace clic en el botón 'Sí, eliminarlo', redirige a la URL
                if (result.isConfirmed) {
                    Swal.fire({
                        title: "Listo!",
                        text: "Tu registro ha cambiado de estado",
                        icon: "success",
                        confirmButtonText: 'Listo',
                        confirmButtonColor: '#13A438',
                        timer: 5000,
                        timerProgressBar: true,
                    });
                    window.location.href = url;
                }
            });
        });
    });

    // Asigna un evento de clic a cada botón con la clase 'editar'
    swaledits.forEach(button => {
        button.addEventListener('click', function(e){
            e.preventDefault();

            const url = this.getAttribute('data-href');

            Swal.fire({
                title: '¿Editar Registro?',
                text: 'Ir al formulario de actualizar',
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'Editar',
                cancelButtonText: 'Cancelar',
                confirmButtonColor: '#13A438',
                cancelButtonColor: '#084F21',
            }).then((result) => {
                // Si se hace clic en 'Editar'
                if (result.isConfirmed) {
                    window.location.href = url;
                }
            });
        });
    });
    
    // Asigna un evento de clic a cada botón con la clase 'editar'
    swalldownloand.forEach(button => {
        button.addEventListener('click', function(e){
            e.preventDefault();
            const url = this.getAttribute('href');
            Swal.fire({
                title: 'Descargar csv',
                text: 'Al aceptar descargaras todos los registros de esta tabla',
                icon: 'Info',
                showCancelButton: true,
                confirmButtonText: 'Descargar',
                cancelButtonText: 'Cancelar',
                confirmButtonColor: '#13A438',
                cancelButtonColor: '#084F21',
            }).then((result) => {
                // Si se hace clic en 'Editar'
                if (result.isConfirmed) {
                    window.location.href = url;
                }
            });
        });
    });

    // funciones de modales
    const openModal = document.querySelector('.open_modal');
    const modal = document.querySelector('.modal');
    const closeModal = document.querySelector('.modal__close');
    
    // Modales
    openModal.addEventListener('click', (e) => {
        e.preventDefault();
        modal.style.opacity = '1';
        modal.style.pointerEvents = 'unset';
        modal.style.transition = 'opacity .2s .4s';
    });
    
    function closeForm() {
        modal.style.opacity = '0';
        modal.style.pointerEvents = 'none';
    }
    
    closeModal.addEventListener('click', (e) => {
        e.preventDefault();
        closeForm();
    });
    
    // Mostrar más columnas de una tabla
    document.getElementById('toggleButton').addEventListener('click', function () {
        // Obtener todas las columnas del grupo 1 y grupo 2
        var group1Columns = document.querySelectorAll('.group1');
        var group2Columns = document.querySelectorAll('.group2');
    
        // Alternar la visibilidad de cada columna del grupo 1
        group1Columns.forEach(function (column) {
            column.classList.toggle('hidden');
        });
    
        // Alternar la visibilidad de cada columna del grupo 2
        group2Columns.forEach(function (column) {
            column.classList.toggle('hidden');
        });
    
        // Cambiar el texto del botón
        if (this.textContent === 'Mostrar más columnas') {
            this.textContent = 'Mostrar menos columnas';
        } else {
            this.textContent = 'Mostrar más columnas';
        }
    });
    
    // función de mostrar opciones usuario
    document.getElementById('toggle-sidebar').addEventListener('click', function () {
        const sidebar = document.getElementById('logo-sidebar');
        sidebar.classList.toggle('-translate-x-full');
    });

    // funcion para ver mas sobre la observcion
    var descripciones = document.querySelectorAll('.descripcion');
    descripciones.forEach(function(descripcion) {
        var contenido = descripcion.textContent;
        var limiteCaracteres = 50; // Cambia este valor al límite de caracteres deseado
    
        if (contenido.length > limiteCaracteres) {
            var textoCorto = contenido.substring(0, limiteCaracteres) + '...';
            var textoCompleto = contenido;
            descripcion.innerHTML = textoCorto + ' <a href="#" class="ver-mas ">Ver más</a>';
    
            var verMas = descripcion.querySelector('.ver-mas');
            verMas.addEventListener('click', function(event) {
                event.preventDefault();
                if (descripcion.innerHTML === textoCorto + ' <a href="#" class="ver-mas ">Ver más</a>') {
                    descripcion.innerHTML = textoCompleto + ' <a href="#" class="ver-menos ">Ver menos</a>';
                } else {
                    descripcion.innerHTML = textoCorto + ' <a href="#" class="ver-mas ">Ver más</a>';
                }
            });
        }
    });
    
    // Agregamos el evento click para "Ver menos"
    document.addEventListener("click", function(event) {
        if (event.target.classList.contains("ver-menos")) {
            event.preventDefault();
            var descripcion = event.target.parentNode;
            var contenido = descripcion.textContent.replace('Ver menos', '').trim();
            var limiteCaracteres = 50; // Asegúrate de que este valor coincida con el de arriba
            var textoCorto = contenido.substring(0, limiteCaracteres) + '...';
            descripcion.innerHTML = textoCorto + ' <a href="#" class="ver-mas ">Ver más</a>';
        }
    });

    
    // cierre del DOM
});

