window.onload = formChart
function formChart() {const xValues = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  const yValues = [8, 25, 15, 10, 22, 33, 48];
  const barColors = ["red", "green","blue","orange","brown", "purple", "black"];
  
  new Chart("myChart", {
    type: "bar",
    data: {
      labels: xValues,
      datasets: [{
        backgroundColor: barColors,
        data: yValues
      }]
    },
    options: {
      legend: {display: false},
      title: {
        display: true,
        text: "Number of 341s pulled [date range]"
      }
    }
  });
}

