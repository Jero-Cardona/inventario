document.addEventListener("DOMContentLoaded", function() {
    // Función para obtener los datos del endpoint
    async function fetchData() {
        try {
            const response = await fetch('/productos-all-fk/');
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching data:', error);
            return [];
        }
    }

    // Función para construir el gráfico de líneas
    async function buildChart() {
        const data = await fetchData();
        
        if (!data.length) {
            console.error('No hay datos para construir el gráfico.');
            return;
        }

        const canvas = document.getElementById('grafica-productos');
        if (canvas && canvas.getContext) {
            const ctx = canvas.getContext('2d');

            const meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"];
            const andes = "#13A438";

            const getColors = opacity => {
                const colors = [andes, '#000000'];
                return colors.map(color => opacity ? `${color}${opacity}` : color);
            };

            const cantidadProductos = new Array(12).fill(0);
            const costoProductos = new Array(12).fill(0);

            // Procesa los datos recibidos
            data.forEach(item => {
                const fecha = new Date(item.fecha_ingreso);
                const month = fecha.getMonth();
                if (month >= 0 && month < 12) {
                    cantidadProductos[month] += item.cantidad || 0;
                    costoProductos[month] += item.costo_inicial || 0;
                }
            });

            const chartData = {
                labels: meses,
                datasets: [
                    {
                        label: 'Cantidad',
                        data: cantidadProductos,
                        tension: .4,
                        fill: 1,
                        borderColor: getColors()[0],
                        backgroundColor: getColors(50)[0],
                        pointRadius: 3,
                        pointBorderColor: andes,
                        pointBackgroundColor: andes,
                    },
                    {
                        label: 'Costo Inicial',
                        data: costoProductos,
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
                }
            };

            // Destruye el gráfico anterior si existe
            if (window.myChart) {
                window.myChart.destroy();
            }

            window.myChart = new Chart(ctx, {
                type: 'line',
                data: chartData,
                options: options
            });
        } else {
            console.error('El canvas no se encontró o no es válido.');
        }
    }

    // Función para construir el gráfico de dona
    async function buildChartDonut() {
        try {
            const data = await fetchData();

            if (!data.length) {
                console.error('No hay datos para construir el gráfico de dona.');
                return;
            }

            // Mapea los usos de los productos y sus cantidades
            const usoCounts = {};
            data.forEach(product => {
                const uso = product.uso || 'Desconocido';
                if (usoCounts[uso]) {
                    usoCounts[uso] += product.cantidad;
                } else {
                    usoCounts[uso] = product.cantidad;
                }
            });

            // Extrae las etiquetas y los valores para el gráfico
            const labels = Object.keys(usoCounts);
            const values = Object.values(usoCounts);

            // Gráfico de dona (pie)
            const ctx = document.getElementById('grafica-productos-2').getContext('2d');
            const myDonutChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Cantidad de productos por uso',
                        data: values,
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
                                    return `${label}: ${value} productos`;
                                }
                            }
                        }
                    }
                }
            });
        } catch (error) {
            console.error('Error al construir el gráfico de dona:', error);
        }
    }

    // Llamadas para construir los gráficos
    buildChart();
    buildChartDonut();
});
