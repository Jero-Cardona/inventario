document.addEventListener('DOMContentLoaded', function() {
    const swalldownloand = document.querySelectorAll('.descargar');

    swalldownloand.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const url = this.getAttribute('href');
            const modelo = this.getAttribute('data-endpoint');
            const tipoarchivo = this.getAttribute('data-tipo');

            console.log(url, modelo); 
            console.log(tipoarchivo); 

            Swal.fire({
                title: 'Descargar archivo',
                text: 'Al aceptar, descargarás todos los registros de esta tabla',
                icon: 'info',
                showCancelButton: true,
                confirmButtonText: 'Descargar',
                cancelButtonText: 'Cancelar',
                confirmButtonColor: '#13A438',
                cancelButtonColor: '#084F21',
            }).then((result) => {
                if (result.isConfirmed) {
                    // Determinar la extensión del archivo
                    const extension = tipoarchivo === 'archivoExcel' ? 'xlsx' : 'csv';

                    // Hacer fetch para descargar el archivo
                    fetch(`${url}/${modelo}?tipo_archivo=${extension}`, {
                        method: 'GET',
                    })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Error al descargar el archivo');
                        }
                        // Cambiamos a arrayBuffer para manejar binarios correctamente
                        return response.arrayBuffer();
                    })
                    .then(buffer => {
                        // Definir el tipo MIME correcto basado en la extensión
                        const mimeType = extension === 'xlsx' 
                            ? 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                            : 'text/csv';
                        
                        // Crear un Blob con el arrayBuffer
                        const blob = new Blob([buffer], { type: mimeType });

                        // Crear un enlace de descarga
                        const link = document.createElement('a');
                        link.href = window.URL.createObjectURL(blob);
                        link.download = `reportes-${modelo}.${extension}`;
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                    })
                    .catch(error => {
                        Swal.fire('Error', 'Hubo un problema al descargar el archivo', 'error');
                        console.error('Error:', error);
                    });
                }
            });
        });
    });
});
