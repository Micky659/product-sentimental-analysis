// Produces a chart.js histogram with product ratings on the product details page

var options = { responsive: true };

//var ctx_bar = $("#barChart").get(0).getContext("2d");
//
//console.log("calling bar chart");
//  var myBarChart = new Chart(ctx_bar, {
//      type: 'bar',
//      data: ['Negative', 'Negative', 'Positive', 'Positive', 'Negative', 'Positive', 'Positive'],
//      options: {
//        legend: {
//            display: false
//        },
//        scales: {
//            xAxes: [{
//                gridLines: {
//                    display: false
//                }
//            }],
//            yAxes: [{
//                gridLines: {
//                    display: false
//                }
//            }]
//
//        } //scales
//
//      } //options
//  });
const ctx = document.getElementById('histogram').getContext('2d');

$.get("/product-bar-data", function(data) {
const chart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Positive', 'Negative'],
    datasets: [{
      label: 'Percentage of Positive and Negative reviews',
      data: [(data['numpos']/(data['numpos']+data['numneg']))*100, (data['numneg']/(data['numpos']+data['numneg']))*100],
      backgroundColor: ['green', 'red'],
    }]
  },
  options: {
    scales: {
      xAxes: [{
        display: false,
        barPercentage: 1.3,
        ticks: {
          max: 3,
        }
      }, {
        display: true,
        ticks: {
          autoSkip: false,
          max: 4,
        }
      }],
      yAxes: [{
        ticks: {
          beginAtZero: false
        }
      }]
    }
  }
});
});