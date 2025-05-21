$(document).ready(function () {

var country=$("#select_country").val();
var category=$("#select_category").val();
var brand=$("#select_brand").val();

String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

//   var country='market1';
//   var category='category1';
//   var brand='brand1';
    var Info={};
    Info.country = country;
    Info.category = category;
    Info.brand = brand;
    Info.csrfmiddlewaretoken = csrftoken;
    var resp=autoresponse("chartdata",Info);
    doAjax(resp);
    doughnut1(resp);
    chart2(resp);
    chart3(resp);
    chart4(resp);
    chart5(resp);
    chart6(resp);
    chart7(resp);
	$('.dropdown-toggle').dropdown();

	$('#select_country').on('change', function() {

    var country=$("#select_country").val();
    var category=$("#select_category").val();
    var brand=$("#select_brand").val();
    var Info={};
    Info.country = country;
    Info.category = category;
    Info.brand = brand;
    Info.csrfmiddlewaretoken = csrftoken;
    var resp=autoresponse("chartdata",Info);

		$('#select_country').html($(this).find('a').html());
		doAjax(resp);
		doughnut1(resp);
		chart2(resp);
        chart3(resp);
        chart4(resp);
        chart5(resp);
        chart6(resp);
        chart7(resp);
		});
	$('#select_category').on('change', function() {

        var country=$("#select_country").val();
        var category=$("#select_category").val();
        var brand=$("#select_brand").val();
        var Info={};
        Info.country = country;
        Info.category = category;
        Info.brand = brand;
        Info.csrfmiddlewaretoken = csrftoken;
        var resp=autoresponse("chartdata",Info);


		$('#select_category').html($(this).find('a').html());
		doAjax(resp);
		doughnut1(resp);
		chart2(resp);
        chart3(resp);
        chart4(resp);
        chart5(resp);
        chart6(resp);
        chart7(resp);
		});
	$('#select_brand').on('change', function() {

        var country=$("#select_country").val();
        var category=$("#select_category").val();
        var brand=$("#select_brand").val();
        var Info={};
        Info.country = country;
        Info.category = category;
        Info.brand = brand;
        Info.csrfmiddlewaretoken = csrftoken;
        var resp=autoresponse("chartdata",Info);

		$('#select_brand').html($(this).find('a').html());
		doAjax(resp);
		doughnut1(resp);
		chart2(resp);
        chart3(resp);
        chart4(resp);
        chart5(resp);
        chart6(resp);
        chart7(resp);
		});
	$('#periodDrop li').on('click', function() {

        var country=$("#select_country").val();
        var category=$("#select_category").val();
        var brand=$("#select_brand").val();
        var Info={};
        Info.country = country;
        Info.category = category;
        Info.brand = brand;
        Info.csrfmiddlewaretoken = csrftoken;
        var resp=autoresponse("chartdata",Info);

		$('#select_period').html($(this).find('a').html());
		doAjax(resp);
		doughnut1(resp);
		chart2(resp);
        chart3(resp);
        chart4(resp);
        //remove imagnery chart data start here
        $('#radar-chart').remove();
        $('#radar-chart-panel').append('<canvas id="radar-chart" width="800" height="600"></canvas>');
        //end heer
        chart5(resp);
        chart6(resp);
        chart7(resp);



		});
	$('#shardata').on('change', function() {
		doughnut1(resp);
	});

 function doAjax() {
          //q1 api
		$.each(resp.q111, function (k, v) {
		var period_val=$("#select_period").text();
		var vol_val = (period_val=="YTDTY")?v.fields.ytdty:v.fields.var3mmtty;
        var per1=parseFloat(vol_val);
        var per=per1.toFixed(1);
				$("#volume_label").text(per);
		});
 }

 });//document end here


//chart start here

//VALUE SHARE, SOURCE: RA js start here
function doughnut1(resp){
var v1=$("#select_period").text();
var v2=$("#shardata").val();
var label = [], data = [];

if(v2=='Volume Share' && v1=='YTDTY'){
       $.each(resp.q222, function (k, v) {
        data[k]= parseFloat(v.fields.ytdty).toFixed(1);
        });
   }
  if(v2=='Volume Share' && v1=='3MMTTY'){
       $.each(resp.q222, function (k, v) {
        data[k]= parseFloat(v.fields.var3mmtty).toFixed(1);
        });
   }
   if(v2=='Value Share' && v1=='YTDTY'){
       $.each(resp.q1000, function (k, v) {
        data[k]=parseFloat(v.fields.ytdty).toFixed(1);
        });
   }
   if(v2=='Value Share' && v1=='3MMTTY'){
       $.each(resp.q1000, function (k, v) {
        data[k]= parseFloat(v.fields.var3mmtty).toFixed(1);
        });
   }
   var per1=[],per=[];
   var per2=[],perr=[];
 var per1=parseFloat(data);
 var per=parseFloat(per1).toFixed(1);

 var per2=parseFloat(label);
 var perr=v2;


 new Chart(document.getElementById("doughnut-chart"), {
                type: 'doughnut',
                data: {
                  labels: [perr],
                  datasets: [
                    {
                      label: "Population (millions)",
                      backgroundColor: ["red", "#d3d3d3"],
                      data:[data, 100 - data]
                    }
                  ]
                },
                options: {
                  title: {
                    display: true,
                    text: perr
                  },
                elements: {
                    center: {
                    text: data,
                    color: 'red', //Default black
                    fontStyle: 'Helvetica', //Default Arial
                    sidePadding: 15 //Default 20 (as a percentage)
                    }
                },
                  legend: {
                    display: false,
                    labels: {
                        text: perr,
                        fontColor: 'rgb(255, 99, 132)'
                    }
                }
               ,tooltips: false,
                }
            });
    Chart.pluginService.register({
      beforeDraw: function (chart) {
        if (chart.config.options.elements.center) {
          //Get ctx from string
          var ctx = chart.chart.ctx;

          //Get options from the center object in options
          var centerConfig = chart.config.options.elements.center;
          var fontStyle = centerConfig.fontStyle || 'Arial';
          var txt = centerConfig.text;
          var color = centerConfig.color || '#000';
          var sidePadding = centerConfig.sidePadding || 20;
          var sidePaddingCalculated = (sidePadding/100) * (chart.innerRadius * 2)
          //Start with a base font of 30px
          ctx.font = "50px " + fontStyle;

          //Get the width of the string and also the width of the element minus 10 to give it 5px side padding
          var stringWidth = ctx.measureText(txt).width;
          var elementWidth = (chart.innerRadius * 2) - sidePaddingCalculated;

          // Find out how much the font can grow in width.
          var widthRatio = elementWidth / stringWidth;
          var newFontSize = Math.floor(30 * widthRatio);
          var elementHeight = (chart.innerRadius * 2);

          // Pick a new font size so it will not be larger than the height of label.
          var fontSizeToUse = Math.min(newFontSize, elementHeight);

          //Set font settings to draw it correctly.
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';
          var centerX = ((chart.chartArea.left + chart.chartArea.right) / 2);
          var centerY = ((chart.chartArea.top + chart.chartArea.bottom) / 2);
          ctx.font = fontSizeToUse+"px " + fontStyle;
          ctx.fillStyle = color;

          //Draw text in center
          ctx.fillText(txt, centerX, centerY);
        }
      }
    });
}
//end here

// Bar chart VOLUME, SOURCE: INTERNAL SALES start here
function chart2(resp){
var label = [], data = [], datakey=[],data9=[],data10=[],dataset=[];
var dataset = resp.q555[0].fields;
var lable1 =["jul2014", "aug2014"];
    $.each(resp.q555, function (k, v) {
     datakey[k]= v.fields.jul2014;
    });

    var data1 = [],data2 = [];

for (var property in dataset) {

   if ( ! dataset.hasOwnProperty(property)) {
      continue;
   }

   data1.push(property);
   data2.push(dataset[property]);

}

var i=9;
for(i = 9;i<=21;i++){
data9[i-9] = data1[i].capitalize();
data10[i-9] = parseFloat(data2[i]).toFixed(1);
}
//data9=parseFloat(data9).toFixed(1);
//data10=parseFloat(data10).toFixed(1);


new Chart(document.getElementById("bar-chart"), {
    type: 'bar',
    data: {
      labels: data9,
      datasets: [
        {
          label: "Population (millions)",
          backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850", "#8e5ea2","#3cba9f","#e8c3b9","#c45850",, "#8e5ea2","#3cba9f","#e8c3b9"],
          data: data10
        }
      ]
    },
     options: {

          legend: { display: false
           },
          title: {
            display: false,
            text: 'Predicted world population (millions) in 2050'
          },
           layout: {
                  	padding: {
                                left: 0,
                                right: 0,
                                top: 100,
                                bottom: 0
                        }
                },
//          animation: {easing:'easeInCubic',duration:600},
           animation: {
            onComplete: function () {
                var chartInstance = this.chart,
                    ctx = chartInstance.ctx;
                ctx.textAlign = 'left';
                ctx.fillStyle = "#000";
                ctx.textBaseline = 'top';

                this.data.datasets.forEach(function (dataset, i) {
                    var meta = chartInstance.controller.getDatasetMeta(i);
                    meta.data.forEach(function (bar, index) {
                        var data = dataset.data[index];
                        ctx.fillText(data, bar._model.x - 8, bar._model.y - 15);

                    });
                });
            }
                },
					tooltips: {
						enabled: true
				   },
					 plugins: {
						datalabels: {
							display: true,

						}
					     },
//					     tooltips: false,
         scales: {
        yAxes: [{
                  gridLines: {
                    drawBorder: false,
                  },
                  scaleLabel: {
                    display: false,
                },
                 ticks: {
                    display: false,
                }
        }],
          xAxes: [{
                  gridLines: {
                    drawBorder: false,
                  },
                  scaleLabel: {
                    display: false,
                },
//                ticks: {
//                fontSize: 8
//            }
        }]
        }
    }
});
}
//end here


//Vol Gain/Loss, Source: HH Panel js start here
function chart6(resp){
var label = [], data = [];
$.each(resp.q666, function (k, v) {
//parseFloat(v.fields.ytdty).toFixed(1);
 data[k]= parseFloat(v.fields.value).toFixed(1);
 label[k] =v.fields.brand.capitalize();
});
new Chart(document.getElementById("bar-chart-horizontal-vol_gain"), {
    type: 'horizontalBar',
    data: {
      labels: label,
      datasets: [
        {
          label: "Population (millions)",
          backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
          data: data
        }
      ]
    },
    options: {
      legend: { display: false },
      title: {
        display: false,
        text: 'Predicted world population (millions) in 2050'
      },
        layout: {
          	padding: {
                    left: 0,
                    right: 30,
                    top: 30,
                    bottom: 0
                }
            },
       animation: {
        onComplete: function () {
            var chartInstance = this.chart,
                ctx = chartInstance.ctx;
            ctx.textAlign = 'left';
            ctx.fillStyle = "#000";
            ctx.textBaseline = 'top';

            this.data.datasets.forEach(function (dataset, i) {
                var meta = chartInstance.controller.getDatasetMeta(i);
                meta.data.forEach(function (bar, index) {
                    var data = dataset.data[index];
                    ctx.fillText(data, bar._model.x, bar._model.y - 5);

                });
            });
        }
            }
    }
});
}

//end here


//IMAGERY, SOURCE: BRAND TRACK js start here

function chart5(resp){
var period_val=$("#select_period").text();


var label = [], data1 = [],data2 = [];
  if(period_val=='YTDTY'){
     $.each(resp.q999, function (k, v) {
     data1[k]= (v.fields.ytdty).replace('%', '');
     data2[k]= (v.fields.var3mmtty).replace('%', '');
     label[k] =v.fields.fact.capitalize();
    });
  }
  else if(period_val=='3MMTTY'){
      $.each(resp.q999, function (k, v) {
         data1[k]= (v.fields.ytdly).replace('%', '');
         data2[k]= (v.fields.var3mmtly).replace('%', '');
         label[k] =v.fields.fact.capitalize();
        });
   }



new Chart(document.getElementById("radar-chart"), {
    type: 'radar',
    data: {
      labels: label,
      datasets: [
        {
          label: "1950",
          fill: true,
          backgroundColor: "rgba(179,181,198,0.2)",
          borderColor: "rgba(179,181,198,1)",
          pointBorderColor: "#fff",
          pointBackgroundColor: "rgba(179,181,198,1)",
          data: data1
        }, {
          label: "2050",
          fill: true,
          backgroundColor: "rgba(255,99,132,0.2)",
          borderColor: "rgba(255,99,132,1)",
          pointBorderColor: "#fff",
          pointBackgroundColor: "rgba(255,99,132,1)",
          pointBorderColor: "#fff",
          data: data2
        }
      ]
    },
    options: {
      title: {
        display: false,
        text: 'Distribution in % of world population'
      },
      legend: { display: false }
    }
});
}
//end here



//PYRAMID, SOURCE: BRAND TRACK js start here
function chart7(resp){
var label = [], data = [];
var v1=$("#select_period").text();
 if(v1=='YTDTY'){
   $.each(resp.q777, function (k, v) {
    data[k]= (v.fields.ytdty).replace('%', '');
    label[k] =v.fields.fact.capitalize();
    });
   }
  if(v1=='3MMTTY'){
   $.each(resp.q777, function (k, v) {
    data[k]= (v.fields.ytdty).replace('%', '');
    label[k] =v.fields.fact.capitalize();
    });
   }
//parseFloat(v.fields.ytdty).toFixed(1);
new Chart(document.getElementById("bar-chart-horizontal"), {
    type: 'horizontalBar',
    data: {
      labels: ["Presence", "Relevance", "Performance", "Advantage", "Bonding"],
      datasets: [
        {
          label: "Population (millions)",
          backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
          data: data
        }
      ]
    },
    options: {
      legend: { display: false },
      title: {
        display: false,
        text: 'Predicted world population (millions) in 2050'
      },
        layout: {
          	padding: {
                    left: 0,
                    right: 40,
                    top: 30,
                    bottom: 0
                }
            },
     animation: {
            onComplete: function () {
                var chartInstance = this.chart,
                    ctx = chartInstance.ctx;
                ctx.textAlign = 'left';
                ctx.fillStyle = "#000";
                ctx.textBaseline = 'top';

                this.data.datasets.forEach(function (dataset, i) {
                    var meta = chartInstance.controller.getDatasetMeta(i);
                    meta.data.forEach(function (bar, index) {
                        var data = dataset.data[index];
                        ctx.fillText(data, bar._model.x, bar._model.y - 5);

                    });
                });
            }
                }


    }
});
}
//end here


//CONSUMPTION FREQUENCY, SOURCE: BRAND TRACK js start here
function chart4(resp){
var v2=$("#select_period").text();
var label = [], data = [];

  if(v2=='3MMTTY'){
       $.each(resp.q888, function (k, v) {
        data[k]= (v.fields.var3mmtty).replace('%', '');
        label[k] =v.fields.fact.capitalize();
        });
   }
  if(v2=='YTDTY'){
      $.each(resp.q888, function (k, v) {
        data[k]= (v.fields.ytdty).replace('%', '');
        label[k] =v.fields.fact.capitalize();
    });
  }

console.log('labelissues',label);
new Chart(document.getElementById("bar-chart-Consumption"), {
    type: 'bar',
    data: {
      labels: label,
      datasets: [
        {
          label: "Population (millions)",
          backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
          data: data
        }
      ]
    },
   options: {
      legend: { display: false },
      title: {
        display: false,
        text: 'Predicted world population (millions) in 2050'
      },
        layout: {
          	padding: {
                    left: 0,
                    right: 0,
                    top: 30,
                    bottom: 0
                }
            },
       animation: {
        onComplete: function () {
            var chartInstance = this.chart,
                ctx = chartInstance.ctx;
            ctx.textAlign = 'left';
            ctx.fillStyle = "#000";
            ctx.textBaseline = 'top';

            this.data.datasets.forEach(function (dataset, i) {
                var meta = chartInstance.controller.getDatasetMeta(i);
                meta.data.forEach(function (bar, index) {
                    var data = dataset.data[index];
                    ctx.fillText(data, bar._model.x - 8, bar._model.y - 15);

                });
            });
        }
            },
     scales: {
    yAxes: [{
      gridLines: {
        drawBorder: false,
      },
      scaleLabel: {
        display: false,
    },
     ticks: {
        display: false,
    }
    }],
      xAxes: [{
      gridLines: {
        drawBorder: false,
      },
      scaleLabel: {
        display: false,
    },

//    ticks: {
//                fontSize: 8

//            }
    }]
  }
    }
});
}
//end here

//DISTRIBUTION, SOURCE: RA js start here
function chart3(resp){
var label = [], data1 = [],data2 = [];

//parseFloat(per1).toFixed(1);

   $.each(resp.q333, function (k, v) {
//   data1[k]= v.fields.ytdly;
//    data1.push(v.fields.ytdty);
    data1[k]= Math.round(parseFloat(v.fields.ytdly));
     var ss=  Math.round(parseFloat(v.fields.ytdty));
    data1.push(ss);
    });

    $.each(resp.q444, function (k, v) {

    data2[k]=  Math.round(parseFloat(v.fields.ytdly));
    var sss=  Math.round(parseFloat(v.fields.ytdty));
    data2.push(sss);
// data2[k]= v.fields.ytdly;
//    data2.push(v.fields.ytdty);
    });

var q1=[],q2=[];
for(var i=0; i< data1.length; i++){
    if(i%2){
        q2.push(data1[i]);
        q2.push(data2[i]);
    }else{
        q1.push(data1[i]);
        q1.push(data2[i]);
    }
}
console.log('dataq1',q1);
console.log('dataq2',q2);
//console.log('data3',data3);
new Chart(document.getElementById("bar-chart-Distribution"), {

    type: 'bar',
    data: {
     labels: ["Numeric Distribution", "Weighted Distribution"],
       datasets: [
        {
          label: "data1",
          backgroundColor: ["#3e95cd", "#3e95cd"],
          data: q1
        },
        {
          label: "data2",
          backgroundColor: ["#8e5ea2", "#8e5ea2"],
          data: q2
        }
      ]
    },



    options: {
      legend: { display: false },
      title: {
        display: false,
        text: 'Predicted world population (millions) in 2050'
      },
      layout: {
              	padding: {
                            left: 0,
                            right: 0,
                            top: 30,
                            bottom: 0
                    }
                },
       animation: {
                    duration: 1,
                    onComplete: function () {
                        var chartInstance = this.chart,
                            ctx = chartInstance.ctx;
                        ctx.textAlign = 'left';
                        ctx.fillStyle = "#000";
                        ctx.textBaseline = 'top';

                        this.data.datasets.forEach(function (dataset, i) {
                            var meta = chartInstance.controller.getDatasetMeta(i);
                            meta.data.forEach(function (bar, index) {
                                var data = dataset.data[index];
                                ctx.fillText(data, bar._model.x - 8, bar._model.y - 15);

                            });
                        });
                    }
                },
     scales: {
    yAxes: [{
      gridLines: {
        drawBorder: false,
      },
      scaleLabel: {
        display: false,
    },
     ticks: {
        min: 10,
        display: false,
    }
    }],
      xAxes: [{
      gridLines: {
        drawBorder: false,
      },
      scaleLabel: {
        display: false,
    }
    }]
  }
    },
    animation: {
        duration: 1,
        onComplete: function () {
            var chartInstance = this.chart,
                ctx = chartInstance.ctx;
            ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, Chart.defaults.global.defaultFontStyle, Chart.defaults.global.defaultFontFamily);
            ctx.textAlign = 'center';
            ctx.textBaseline = 'bottom';

            this.data.datasets.forEach(function (dataset, i) {
                var meta = chartInstance.controller.getDatasetMeta(i);
                meta.data.forEach(function (bar, index) {
                    var data = dataset.data[index];
                    ctx.fillText(data, bar._model.x, bar._model.y - 5);
                });
            });
        }
    }
});
}
//end here