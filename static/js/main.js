function closeFormEdit() {
    const modal = document.querySelector('#form-container-editar');
    if (modal) {
        modal.style.opacity = '0'; 
        modal.style.pointerEvents = 'none'; 
        setTimeout(() => {
            modal.remove(); 
        }, 600); 
    }
}

document.addEventListener('DOMContentLoaded', function () {

    function closeForm() {
        if (modal) {
            modal.style.opacity = '0';
            modal.style.pointerEvents = 'none';
        }
    }
    const swaledits = document.querySelectorAll('.editar');
    const swalldownloand = document.querySelectorAll('.descargar');
    
    document.querySelectorAll('.delete').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
    
            const form = this.closest('form');
            const url = form.getAttribute('action');
    
            Swal.fire({
                title: '¿Estás seguro?',
                text: 'Eliminarias este registro en el aplicativo web',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Sí',
                cancelButtonText: 'Cancelar',
                confirmButtonColor: '#13A438',
                cancelButtonColor: '#084F21',
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(url, {
                        method: 'DELETE',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                    }).then(response => {
                        if (response.ok) {
                            Swal.fire({
                                title: "Listo!",
                                text: "Tu registro ha sido eliminado",
                                icon: "success",
                                confirmButtonText: 'Listo',
                                confirmButtonColor: '#13A438',
                                timer: 5000,
                                timerProgressBar: true,
                            }).then(() => {
                                window.location.reload(); 
                            });
                        } else {
                            Swal.fire({
                                title: "Error",
                                text: "No se logro eliminar el registro",
                                icon: "error",
                                confirmButtonText: 'Entendido',
                                confirmButtonColor: '#13A438',
                            });
                        }
                    });
                }
            });
        });
    });

    document.querySelectorAll('.estado').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
    
            const form = this.closest('form');
            const url = form.getAttribute('action');
    
            Swal.fire({
                title: '¿Estás seguro?',
                text: 'Cambiaras el estado de este registro en el aplicativo web',
                icon: 'info',
                showCancelButton: true,
                confirmButtonText: 'Sí',
                cancelButtonText: 'Cancelar',
                confirmButtonColor: '#13A438',
                cancelButtonColor: '#084F21',
            }).then((result) => {
                if (result.isConfirmed) {
                    fetch(url, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                    }).then(response => {
                        if (response.ok) {
                            Swal.fire({
                                title: "Listo!",
                                text: "Cambiaste el estado de usuario correctamente",
                                icon: "success",
                                confirmButtonText: 'Listo',
                                confirmButtonColor: '#13A438',
                                timer: 5000,
                                timerProgressBar: true,
                            }).then(() => {
                                window.location.reload(); 
                            });
                        } else {
                            Swal.fire({
                                title: "Error",
                                text: "No se logro activar el usuario, algo salio mal",
                                icon: "error",
                                confirmButtonText: 'Entendido',
                                confirmButtonColor: '#13A438',
                            });
                        }
                    });
                }
            });
        });
    });
    
    swaledits.forEach(button => {
        button.addEventListener('click', async function(e) {
            e.preventDefault();
    
            const id = this.getAttribute('data-id'); 
            const endpoint = this.getAttribute('data-endpoint');
    
            const endpointMap = {
                'responsable': `/responsable-obtener/${id}`,
                'usuario': `/usuario-obtener/${id}`,
                'producto': `/producto-obtener/${id}`,
                'proveedor': `/proveedor-obtener/${id}`,
                'sede': `/sede-obtener/${id}`,
                'categoria': `/categoria-obtener/${id}`,
                'mantenimiento': `/mantenimiento-obtener/${id}`,
                'rol': `/rol-obtener/${id}`,
            };
    
            const foreignKeyEndpoints = {
                'id_categoria': '/categorias-all/',
                'id_proveedor': '/proveedores-all/',
                'id_responsable': '/responsables-all/',
                'id_rol': '/roles-all/',
                'id_sede': '/sedes-all/',
                'id_producto': '/productos-all/',
                'id_usuarios': '/usuarios-all/',
            };
    
            const fetchUrl = endpointMap[endpoint];
            if (!fetchUrl) {
                console.error(`No se encontró un endpoint para el tipo: ${endpoint}`);
                return;
            }
            
            Swal.fire({
                title: '¿Editar Registro?',
                text: 'Ir al formulario de actualizar',
                icon: 'question',
                showCancelButton: true,
                confirmButtonText: 'Editar',
                cancelButtonText: 'Cancelar',
                confirmButtonColor: '#13A438',
                cancelButtonColor: '#084F21',
            }).then(async (result) => {
                if (result.isConfirmed) {
                    try {
                        const datosResponse = await fetch(fetchUrl);
                        if (!datosResponse.ok) throw new Error('Error al obtener los datos');
                        const datos = await datosResponse.json();
                        
                        let formInputs = '';
                        let hiddenInputs = '';

                        for (const key in datos) {
                            if (key === 'id' || typeof datos[key] === 'object') continue;
                            if (key === 'fecha_creacion' || key === 'fecha_ingreso') {
                                hiddenInputs += `<input type="hidden" name="${key}" value="${datos[key]}">`;
                                continue;
                            }
                            if (foreignKeyEndpoints.hasOwnProperty(key)) {
                                const optionsResponse = await fetch(foreignKeyEndpoints[key]);
                                if (!optionsResponse.ok) throw new Error(`Error al obtener los valores para ${key}`);
                                const optionsData = await optionsResponse.json();
                                console.log(optionsData)
                                // Define las clases dependiendo del endpoint
                                const selectClasses = endpoint === 'producto' && key === 'id_responsable' ? 
                                    'bg-gray-200 text-gray-800 border-0 rounded-md p-2 focus:bg-gray-200 focus:outline-none focus:ring-1 focus:ring-blue-500 transition ease-in-out duration-150 col-span-1 md:col-span-2' :
                                    (endpoint === 'producto'?  'bg-gray-200 text-gray-800 border-0 rounded-md p-2 focus:bg-gray-200 focus:outline-none focus:ring-1 focus:ring-blue-500 transition ease-in-out duration-150' :
                                        'bg-gray-100 text-gray-800 border-0 lg:w-96 rounded-md p-2 mb-4 focus:bg-gray-200 focus:outline-none focus:ring-1 focus:ring-blue-500 transition ease-in-out duration-150'
                                    );
                                    
                                formInputs += `
                                    <select 
                                        name="${key}" 
                                        required 
                                        class="${selectClasses}"
                                        ${key === 'id_categoria' ? 'id="categorias"' : ''}
                                    >
                                        <option value="" disabled selected class="bg-white">Escoge una Categoría</option>
                                `;
                                optionsData.forEach(option => {
                                    const selected = option.id === datos[key] ? 'selected' : '';
                                    const displayText = option.codigo ? option.codigo : option.nombre;
                                    formInputs += `<option value="${option.id}" ${selected}>${displayText}</option>`;
                                });
                                
                                formInputs += `</select>`;
                            } else if (key === 'observacion') {
                                const textareaClasses = endpoint === 'producto' ? 
                                    'bg-gray-200 text-gray-800 border-0 rounded-md p-2 focus:bg-gray-200 focus:outline-none focus:ring-1 focus:ring-blue-500 transition ease-in-out duration-150 col-span-1 md:col-span-2' :
                                    'bg-gray-100 text-gray-800 border-0 lg:w-96 rounded-md p-2 mb-4 focus:bg-gray-200 focus:outline-none focus:ring-1 focus:ring-blue-500 transition ease-in-out duration-150';
                                    
                                formInputs += `
                                    <textarea 
                                        name="${key}" 
                                        required 
                                        placeholder="${key}" 
                                        class="${textareaClasses}"
                                    >
                                        ${datos[key] || ''}
                                    </textarea>
                                `;
                            } else if (endpoint === 'usuario' && key === 'estado') {
                                formInputs += `
                                    <select 
                                        name="${key}" 
                                        required 
                                        class="bg-gray-100 text-gray-800 border-0 lg:w-96 rounded-md p-2 mb-4 focus:bg-gray-200 focus:outline-none focus:ring-1 focus:ring-blue-500 transition ease-in-out duration-150">
                                        <option value="" disabled>Selecciona una opción</option>
                                        <option value="activo" ${datos[key] === 'activo' ? 'selected' : ''}>Activo</option>
                                        <option value="inactivo" ${datos[key] === 'inactivo' ? 'selected' : ''}>Inactivo</option>
                                    </select>
                                `;
                            } else {
                                let inputValue = key === 'hashed_password' ? '' : datos[key] || '';
                                const inputType = key === 'fecha_mantenimiento' ? 'date' : 
                                                (key === 'correo' ? 'email' : 
                                                (key === 'telefono' ? 'number' : 
                                                (key === 'hashed_password' ? 'password' : 'text')));

                                if (endpoint !== 'producto') {
                                    formInputs += `
                                        <div class="relative">
                                            <input
                                                placeholder="${key === 'hashed_password' ? 'Nueva contraseña' : key}"
                                                name="${key}"
                                                value="${inputValue}"
                                                required
                                                class="bg-gray-100 text-gray-800 border-0 lg:w-96 rounded-md p-2 mb-4 focus:bg-gray-200 focus:outline-none focus:ring-1 focus:ring-blue-500 transition ease-in-out duration-150"
                                                type="${inputType}"
                                                id="${key === 'hashed_password' ? 'passwordInput' : ''}"
                                            />
                                            ${key === 'hashed_password' ? `
                                                <button type="button" id="togglePassword" class="absolute right-4 bottom-2 text-gray-600 hover:text-gray-800">
                                                    <i class="fas fa-eye" id="toggleIcon"></i>
                                                </button>
                                            ` : ''}
                                        </div>
                                    `;
                                } else {
                                    formInputs += `
                                        <input
                                            placeholder="${key === 'hashed_password' ? 'Nueva contraseña' : key}"
                                            name="${key}"
                                            value="${inputValue}"
                                            required
                                            class="bg-gray-200 text-gray-800 border-0 rounded-md p-2 focus:bg-gray-200 focus:outline-none focus:ring-1 focus:ring-blue-500 transition ease-in-out duration-150"
                                            type="${inputType}"
                                            id="${key === 'hashed_password' ? 'passwordInput' : ''}"
                                        />
                                        ${key === 'hashed_password' ? `
                                            <button type="button" id="togglePassword" class="absolute right-4 bottom-2 text-gray-600 hover:text-gray-800">
                                                <i class="fas fa-eye" id="toggleIcon"></i>
                                            </button>
                                        ` : ''}
                                    `;
                                }
                            }

                        }
                        let nuevoFormularioHtml = '';
                        if (endpoint === 'producto'){
                            nuevoFormularioHtml = `
                            <section id="form-container-editar" class="modal fixed inset-0 bg-[#111111bd] flex opacity-0 pointer-events-none">
                                <div class="modal__container m-auto w-9/10 max-w-[800px] max-h-[90%] bg-white rounded-[6px] p-[3em_2.5em] grid gap-[1em] place-items-center shadow-md relative">
                                    <button onclick="closeFormEdit()" class="modal__close absolute top-4 right-4 w-10 h-10 flex justify-center items-center cursor-pointer text-gray-600 hover:text-gray-900">✖</button>
                                    <h2 class="text-2xl font-bold text-gray-800 mb-1">Editar ${endpoint}</h2>
                                    <div id="form-datos-back-edit">
                                        <form id="form-edit" class="grid grid-cols-1 md:grid-cols-2 gap-2 w-full">
                                        ${formInputs}
                                        ${hiddenInputs}
                                            <button class="bg-gradient-to-r bg-Andes text-white font-bold py-2 px-4 rounded-md mt-4 hover:bg-green-700 transition ease-in-out duration-150 col-span-1 md:col-span-2" type="submit">
                                            Actualizar Datos
                                            </button>
                                        </form>
                                    </div>
                                </div>
                            </section>`;
                        }else{
                            nuevoFormularioHtml = `
                                <section id="form-container-editar" class="modal fixed inset-0 bg-[#111111bd] flex opacity-0 pointer-events-none">
                                    <div class="modal__container m-auto w-9/10 max-w-[800px] max-h-[90%] bg-white rounded-[6px] p-[3em_2.5em] grid gap-[1em] place-items-center shadow-md relative">
                                        <button onclick="closeFormEdit()" class="modal__close absolute top-4 right-4 w-10 h-10 flex justify-center items-center cursor-pointer text-gray-600 hover:text-gray-900">✖</button>
                                        <h2 class="text-2xl font-bold text-gray-800 mb-1">Editar ${endpoint}</h2>
                                        <div id="form-datos-back-edit">
                                            <form id="form-edit" class="flex flex-col">
                                            ${formInputs}
                                            ${hiddenInputs}
                                                <button class="bg-gradient-to-r m-auto w-full items-center flex bg-Andes text-white font-bold py-2 px-4 rounded-md mt-4 hover:bg-green-700 transition ease-in-out duration-150" type="submit">
                                                Actualizar Datos
                                                </button>
                                            </form>
                                        </div>
                                    </div>
                                </section>`;
                        }
                        
                        const formContainer = document.getElementById('form-container-edits');
                        if (!formContainer) throw new Error('Contenedor para el formulario no encontrado en el DOM');
                        formContainer.innerHTML = nuevoFormularioHtml;
    
                        const modal = document.querySelector('#form-container-editar');
                        modal.style.opacity = '1';
                        modal.style.pointerEvents = 'unset';
                        modal.style.transition = 'opacity .2s .4s';
                        
                        const closeModal = document.querySelector('.modal__close');
                        closeModal.addEventListener('click', closeFormEdit);
    
                        function closeFormEdit() {
                            const modal = document.querySelector('#form-container-editar');
                            if (modal) {
                                modal.style.opacity = '0'; 
                                modal.style.pointerEvents = 'none'; 
                                setTimeout(() => modal.remove(), 200);
                            }
                        }
    
                        const formEdit = document.getElementById('form-edit');
                        formEdit.addEventListener('submit', async (e) => {
                            e.preventDefault();
    
                            const formData = new FormData(formEdit);
                            const params = new URLSearchParams(formData).toString();
                            const url = `/${endpoint}-update/${id}?${params}`;
    
                            try {
                                const response = await fetch(url, { method: 'PUT' });
                                if (!response.ok) throw new Error(`Error al actualizar los datos: ${await response.text()}`);
    
                                const result = await response.json();
                                window.location.reload();
                                console.log('Datos actualizados:', result);
    
                                closeFormEdit(); 
                            } catch (error) {
                                console.error('Error en la actualización:', error);
                            }
                        });
    
                        const togglePassword = document.getElementById('togglePassword');
                        const passwordInput = document.getElementById('passwordInput');
                        const toggleIcon = document.getElementById('toggleIcon');
    
                        if (togglePassword && passwordInput && toggleIcon) {
                            togglePassword.addEventListener('click', () => {
                                const currentType = passwordInput.getAttribute('type');
    
                                if (currentType === 'password') {
                                    passwordInput.setAttribute('type', 'text');
                                    toggleIcon.classList.replace('fa-eye', 'fa-eye-slash');
                                } else {
                                    passwordInput.setAttribute('type', 'password');
                                    toggleIcon.classList.replace('fa-eye-slash', 'fa-eye');
                                }
                            });
                        }
                    } catch (error) {
                        console.error('Error al obtener los datos:', error);
                    }
                }
            });
        });
    });
    
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

    const openModal = document.querySelector('.open_modal');
    const modal = document.querySelector('.modal');
    const closeModal = document.querySelector('.modal__close');
    
    if (openModal && modal && closeModal) {
        openModal.addEventListener('click', (e) => {
            e.preventDefault();
            modal.style.opacity = '1';
            modal.style.pointerEvents = 'unset';
            modal.style.transition = 'opacity .2s .4s';
        });

        closeModal.addEventListener('click', (e) => {
            e.preventDefault();
            closeForm();
        });
    } else {
        console.error('Uno o más elementos no se encuentran en el DOM.');
    }

    var visualizarButton = document.getElementById('Visualizar');
    if (visualizarButton) {
        visualizarButton.addEventListener('click', function () {
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
    }

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

    if (document.getElementById("default-table") && typeof simpleDatatables.DataTable !== 'undefined') {
        const dataTable = new simpleDatatables.DataTable("#default-table", {
            searchable: false,
            perPageSelect: false
        });
    }

    // modal codigo qr
    const qrButtons = document.querySelectorAll('.codigoQR');
    const qrModal = document.getElementById('qrModal');
    const qrImage = document.getElementById('qrImage');
    const closeModalQR = document.getElementById('closeModalQR');

    // Función para mostrar la modal
    const showModal = () => {
            qrModal.classList.remove('opacity-0', 'pointer-events-none');
            qrModal.classList.add('opacity-100');
    };

    // Función para ocultar la modal
    const hideModal = () => {
            qrModal.classList.add('opacity-0', 'pointer-events-none');
            qrModal.classList.remove('opacity-100');
    };

    // Añadir eventos de clic a los botones de QR
    qrButtons.forEach(button => {
        button.addEventListener('click', async function () {
            const producto_id = this.getAttribute('data-id');

            try {
                // Hacer la petición para obtener el QR
                const response = await fetch(`/generar-codigoqr-producto/${producto_id}`);

                if (response.ok) {
                    // Actualizar la imagen del QR
                    const blob = await response.blob();
                    const imageUrl = URL.createObjectURL(blob);
                    qrImage.src = imageUrl;

                    // Mostrar la modal
                    showModal();
                } else {
                    console.error('Error al obtener el QR');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        });
    });

    closeModalQR.addEventListener('click', hideModal);
    function downloadQRImage() {
        const qrImage = document.getElementById('qrImage');
        const qrImageUrl = qrImage.src;  

        if (qrImageUrl) {
            const link = document.createElement('a');
            link.href = qrImageUrl;
            link.download = `productoQR.png`; 

            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        } else {
            console.error('URL de imagen no disponible');
        }
    }
    document.getElementById('downloadQrImage').addEventListener('click', downloadQRImage);



    // Seleccionar el input file
    const fileInput = document.getElementById('fileInput');

    // Escuchar cuando el archivo cambia (se selecciona un archivo)
    fileInput.addEventListener('change', async (event) => {
        const file = event.target.files[0];
        const modelName = fileInput.getAttribute('data-endpoint'); // Suponiendo que el input tiene este atributo
        console.log(modelName);

        if (file) {
            // Mostrar alerta de confirmación con SweetAlert
            Swal.fire({
                title: '¿Estás seguro?',
                text: "Estás a punto de cargar el archivo. Esta acción no puede deshacerse.",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: 'Sí, cargar',
                cancelButtonText: 'Cancelar',
                confirmButtonColor: '#13A438',
                cancelButtonColor: '#084F21',
            }).then(async (result) => {
                if (result.isConfirmed) {
                    
                    const formData = new FormData();
                    formData.append('file', file);
                    formData.append('model_name', modelName); 

                    try {
                        // Hacer la petición al endpoint con fetch
                        const response = await fetch('/cargue-archivos', {
                            method: 'POST',
                            body: formData, 
                        });

                        if (response.ok) {
                            Swal.fire('Cargado', 'El archivo se ha cargado exitosamente', 'success').then((result) => {
                                if (result.isConfirmed){
                                    window.location.reload();
                                }
                            });
                        } else {
                            const errorData = await response.json(); 
                            Swal.fire('Error', errorData.detail || 'Hubo un problema al cargar el archivo', 'error').then((result) => {
                                if (result.isConfirmed){
                                    window.location.reload();
                                }
                            });
                        }
                    } catch (error) {
                        Swal.fire('Error', 'Error en la solicitud: ' + error.message, 'error');
                    }
                } else {
                    Swal.fire('Cancelado', 'La carga de archivo fue cancelada', 'info').then((result) => {
                        if (result.isConfirmed){
                            window.location.reload();
                        }
                    });
                }
            });
        }
    });

// cierre del DOM
});

