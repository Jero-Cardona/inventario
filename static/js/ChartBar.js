import Chart from "chart.js";

var barChart = new Chart(densityCanvas, {
    type: 'bar',
    data: densityData,
    options: chartOptions
});

var densityData = {
    label: 'Density of Planets (kg/m3)',
    data: [5427, 5243, 5514, 3933, 1326, 687, 1271, 1638]
  };
  var barChart = new Chart(densityCanvas, {
    type: 'bar',
    data: {
      labels: ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"],
      datasets: [densityData]
    }
  });


