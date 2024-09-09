document.addEventListener("DOMContentLoaded", function() {
    const canvas = document.getElementById('grafica-productos');

    if (canvas && canvas.getContext) {
        const ctx = canvas.getContext('2d');

        const meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"];
        const andes = "#13A438";

        const getColors = opacity => {
            const colors = [andes, '#000000'];
            return colors.map(color => opacity ? `${color}${opacity}` : color);
        };

        const estadosCerradosPorMes = [65, 359, 180, 81, 256, 255, 40, 60, 290, 170, 410, 200]; 
        const estadosNegadosPorMes = [335, 49, 760, 271, 36, 45, 330, 40, 290, 110, 600, 100]; 

        const data = {
            labels: meses,
            datasets: [
                {
                    label: 'cerradas',
                    data: estadosCerradosPorMes,
                    tension: .4,
                    fill: 1,
                    borderColor: getColors()[0],
                    backgroundColor: getColors(50)[0],
                    pointRadius: 3,
                    pointBorderColor: andes,
                    pointBackgroundColor: andes,
                },
                {
                    label: 'negadas',
                    data: estadosNegadosPorMes,
                    tension: .4,
                    fill: true,
                    borderColor: getColors()[1],
                    backgroundColor: getColors(50)[1],
                    pointRadius: 3,
                    pointBorderColor: '#000000',
                    pointBackgroundColor: '#000000',
                },
            ],
        };

        const options = {
            maintainAspectRatio: false,
            responsive: true,
            resizeDelay: 200,
            animation: true,
            scales: {
                y: {
                    beginAtZero: true,
                    min: 0,
                },
                x: {
                    // Configuraciones adicionales para el eje x si es necesario
                }
            },
            plugins: {
                legend: {
                    display: true
                },
                title: {
                    // display: true,
                    // text: 'Estadísticas de Reportes'
                }
            }
        };

        new Chart(ctx, {
            type: 'line',
            data: data,
            options: options
        });
    } else {
        console.error('El canvas no se encontró o no es válido.');
    }

    var ctx = document.getElementById('grafica-productos-2').getContext('2d');
    var myDonutChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
            datasets: [{
                label: 'Colors',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                    'rgba(251, 68, 100, 0.6)',
                    'rgba(119, 182, 254, 0.6)',
                    'rgba(234, 252, 64, 0.6)',
                    'rgba(67, 247, 69, 0.6)',
                    'rgba(217, 44, 254, 0.6)',
                    'rgba(255, 151, 0, 0.6)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.label || '';
                            let value = context.raw || '';
                            return `${label}: ${value}`;
                        }
                    }
                }
            }
        }
    });

});
