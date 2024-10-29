document.addEventListener('DOMContentLoaded', function () {

    const qrButtons = document.querySelectorAll('.codigoQR');
    const qrModal = document.getElementById('qrModal');
    const qrImage = document.getElementById('qrImage');
    const closeModalQR = document.getElementById('closeModalQR');

    const showModal = () => {
            qrModal.classList.remove('opacity-0', 'pointer-events-none');
            qrModal.classList.add('opacity-100');
    };

    const hideModal = () => {
            qrModal.classList.add('opacity-0', 'pointer-events-none');
            qrModal.classList.remove('opacity-100');
    };

    qrButtons.forEach(button => {
        button.addEventListener('click', async function () {
            const producto_id = this.getAttribute('data-id');

            try {
                const response = await fetch(`/generar-codigoqr-producto/${producto_id}`);

                if (response.ok) {
                    // Actualizar la imagen del QR
                    const blob = await response.blob();
                    const imageUrl = URL.createObjectURL(blob);
                    qrImage.src = imageUrl;

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

    // Función para descargar todos los QR como un archivo ZIP
    async function downloadAllQRs() {
        try {
            const response = await fetch('/productos-imagen-qr');

            if (response.ok) {
                const blob = await response.blob();
                const zipUrl = URL.createObjectURL(blob);

                const link = document.createElement('a');
                link.href = zipUrl;
                link.download = 'productos_codigos_qr.zip';

                document.body.appendChild(link);
                link.click();

                document.body.removeChild(link);
                URL.revokeObjectURL(zipUrl);

                Swal.fire({
                    icon: 'success',
                    title: 'Descarga completada',
                    text: 'Se han descargado todos los códigos QR correctamente.',
                    confirmButtonText: 'Aceptar',
                    confirmButtonColor: '#13A438',
                });
            } else {
                const errorData = await response.json()
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: errorData.detail || 'No se pudo descargar los códigos QR.',
                    confirmButtonText: 'Aceptar',
                    confirmButtonColor: '#13A438',
                });
            }
        } catch (error) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text:'Ocurrió un error al intentar descargar los códigos QR.',
                confirmButtonText: 'Aceptar',
                confirmButtonColor: '#13A438',
            });
            console.error('Error:', error);
        }
    }

    document.getElementById('downloadAllQrButton').addEventListener('click', function () {
        Swal.fire({
            title: '¿Estás seguro?',
            text: "Se descargará un archivo ZIP con todos los códigos QR de los productos.",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Sí, descargar',
            cancelButtonText: 'Cancelar',
            confirmButtonColor: '#13A438',
            cancelButtonColor: '#084F21',
        }).then((result) => {
            if (result.isConfirmed) {
                downloadAllQRs();
            }
        });
    });


});