$(document).ready(function(){
    $("button").click(function(){
        $("#test").hide()
    });
});


let myChart = document.getElementById('myChart').getContext('2d');
// Global Options
Chart.defaults.global.defaultFontFamily = 'Lato';
Chart.defaults.global.defaultFontSize = 18;
Chart.defaults.global.defaultFontColor = '#777';

let massPopChart = new Chart(myChart, {
  type:'doughnut', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
  data:{
    labels:['찬성', '중립','반대'],
    datasets:[{
      label:'doughnut',
      data:[
        forCount,
        neutralCount,
        againstCount,
      ],
      //backgroundColor:'green',
      backgroundColor:[
        'rgba(30, 149, 237, 0.6)',
        'rgba(169, 169, 169, 0.6)',
        'rgba(220, 20, 60, 0.6)',
      ],
      borderWidth:1,
      borderColor:'#777',
      hoverBorderWidth:3,
      hoverBorderColor:'#000'
    }]
  },
  options:{
    maintainAspectRatio: false,
    rotation: 1 * Math.PI,
    circumference: 3.14,

    title:{
      display:true,
      text:'투표결과',
      fontSize:25,
      position: 'top'
    },
    legend:{
      display:true,
      position:'bottom',
      labels:{
        fontColor:'#000'
      }
    },
    layout:{
      padding:{
        left:50,
        right:0,
        bottom:0,
        top:0
      }
    },
    tooltips:{
      enabled:true
    }
    
  }
});