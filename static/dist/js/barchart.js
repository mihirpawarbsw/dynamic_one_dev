var csrfmiddlewaretoken=csrftoken;
var myChart;

$("#chart_div").click(function (e) {
   // alert('Ooo bhai');
    var chart_type=$('#Chart_type').val();
    var Timeperiod_chart=$('#Timeperiod_chart').val();
    var Facts_chart=$('#Facts_chart').val();
    var Other_chart=$('#Other_chart').val();
    var dict_selected_measures_lst=$('#dict_selected_measures_lst').html();
    console.log('dict_selected_measures_lst chart',dict_selected_measures_lst)

	var checkData = "csrfmiddlewaretoken=" + csrfmiddlewaretoken+"&Timeperiod_chart=" + Timeperiod_chart+"&Facts_chart=" + Facts_chart+"&Other_chart=" + Other_chart+"&dict_selected_measures_lst=" + dict_selected_measures_lst;
      respdata = autoresponse("bar_chart", checkData);
      if (respdata.status  == 200)
      {
        barchart(respdata);
      }
      else
      {
      alert('Something went wrong')
      }

    $("#chart_Modal").modal("toggle")
});




$("#Export_ppt11").click(function (e) {
   // alert('Ooo bhai');

    var checkData = "csrfmiddlewaretoken=" + csrfmiddlewaretoken;
      respdata = autoresponse("bar_chart", checkData);
      if (respdata.status  == 200)
      {
        ppt_dwn(respdata);
        // ppt_img()
      }
      else
      {
      alert('Something went wrong')
      }


});




$("#Timeperiod_chart,#Facts_chart,#Chart_type").change(function(){
    Other_chart_filter();
   
    

    setTimeout(function () {
            
    
     var chart_type=$('#Chart_type').val();
    var Timeperiod_chart=$('#Timeperiod_chart').val();
    var Facts_chart=$('#Facts_chart').val();
    var Other_chart=$('#Other_chart').val();
    var dict_selected_measures_lst=$('#dict_selected_measures_lst').html();

    var checkData4 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken+"&Timeperiod_chart=" + Timeperiod_chart+"&Facts_chart=" + Facts_chart+"&Other_chart=" + Other_chart+"&dict_selected_measures_lst=" + dict_selected_measures_lst;
        respdata = autoresponse("bar_chart", checkData4);
    if (respdata.status  == 200){

        if (chart_type=='bar_chart') {
            barchart(respdata);
        }else if (chart_type=='line_chart') {
            linechart(respdata);
        }

    }


        }, 600);
    
    
});

$("#Other_chart").change(function(){

   

    setTimeout(function () {
    
     var chart_type=$('#Chart_type').val();
    var Timeperiod_chart=$('#Timeperiod_chart').val();
    var Facts_chart=$('#Facts_chart').val();
    var Other_chart=$('#Other_chart').val();
    var dict_selected_measures_lst=$('#dict_selected_measures_lst').html();

    var checkData4 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken+"&Timeperiod_chart=" + Timeperiod_chart+"&Facts_chart=" + Facts_chart+"&Other_chart=" + Other_chart+"&dict_selected_measures_lst=" + dict_selected_measures_lst;
        respdata = autoresponse("bar_chart", checkData4);
    if (respdata.status  == 200){

        if (chart_type=='bar_chart') {
            barchart(respdata);
        }else if (chart_type=='line_chart') {
            linechart(respdata);
        }

    }


        }, 600);
    
    
});


function Other_chart_filter(){

     var Facts_chart=$('#Facts_chart').val();
     if (Facts_chart=="Volume" || Facts_chart=="Volume" || Facts_chart=="Volume") {
        var resp=['Absolutes','Share','Growth','bps change'];
     }else if(Facts_chart=="TDP"){
        var resp=['Absolutes','Share','Growth','bps change'];
     }else if(Facts_chart=="WD" || Facts_chart=="ND" || Facts_chart=="API"){
        var resp=['Absolutes','bps change'];
     }else if(Facts_chart=="Avg Price"){
        var resp=['Absolutes','Growth'];
     }


    $("#Other_chart").empty();
    var i=0;
     $.each(resp, function (key2, value2) {

            if (i==0) {
                $("#Other_chart").append('<option select  style="width: 100px" value="'+value2+'" >'+value2+'</option>'); 
            }else{
                $("#Other_chart").append('<option  style="width: 100px" value="'+value2+'" >'+value2+'</option>'); 
            }
            
            i++ 

  });

   $("#Other_chart").multiselect('rebuild');  
    $("#Other_chart").multiselect({
        search   : true,
    });


} 	

var myChart1;
function linechart(respdata){
    // alert('line')
	
    column=[];datarow=[];row=[];code_frame=[];code_frame1=[];data=[];
	var color_code=['purple', 'orange', 'blue', 'yellow','silver','maroon', "fushsia", "teal"];



    var label_arra=respdata.res_data.index;

    const index = label_arra.indexOf('AAAATotal'); // 👉️  0

    if (index !== -1) {
      label_arra[index] = 'Total';
    }

    if(myChart1){
        myChart1.destroy();
    }


    //filter collection start
    var dimensions  = $("#example2-left li");
    var other_variable = $("#example33 li");
    var row_text;var col_text;
    other_variable.each(function(idx, li) {
         other_variable = $(li).text();
    });
    dimensions.each(function(idx, li) {
         dimensions = $(li).text();
    });
    

    // var join_r_and_c=other_variable+ " Vs " +dimensions;
    var join_r_and_c=dimensions+ " Vs  Time";
    //filter collection end

	for (var r =0; r<respdata.res_data.columns.length ; r++) {
			ccol1=[];
			for (var c =0; c<respdata.res_data.index.length ; c++) {
				// console.log('data col',c,'row data',r);
				ccol1.push(respdata.res_data.data[c][r].toFixed(1));
			}
			// console.log('labels',respdata.res_data.columns[r],'col1',ccol1);
			// data.push({['label']:respdata.res_data.columns[r],['data']:ccol1,['backgroundColor']:randColor(),['fill']:false,['borderWidth']:1,['borderColor']:randColor()});
            data.push({['label']:respdata.res_data.columns[r],['data']:ccol1,['backgroundColor']:color_code[r],['fill']:false,['borderWidth']:1,['borderColor']:randColor()});
	}

    // console.log('chart data 70',data)
    $('#BarChart').remove();
	$("#barchartdiv").append('<canvas id="BarChart"></canvas>');

    var min_num=respdata['min_max_dict']['min_value'];

    if (min_num > 0) {
        min_num=0;
    }else{
         min_num=respdata['min_max_dict']['min_value'];
    }


	const ctx = document.getElementById('BarChart');
  	myChart1 = new Chart(ctx, {
    type: 'line',
    data: {
      labels: label_arra,
	  datasets:data,
     //  datasets: [{
     //    label: '# Male',
     //    data: [12, 19, 3, 5, 2, 3],
     //    borderWidth: 1,
     //    backgroundColor: ['green'],
     //    borderColor: "#3e95cd",
     //    fill: false

     //  },
     //  {
     //    label: '# Female',
     //    data: [25, 23, 9, 36, 9, 7],
     //    borderWidth: 1,
     //    backgroundColor: ['yellow'],
     //     borderColor: "#8e5ea2",
     //    fill: false
     //  },
     //  {
     //    label: '# Total',
     //    data: [17, 23, 18, 19, 12, 13],
     //    borderWidth: 2,
     //    backgroundColor: ['red'],
     //     borderColor: "#3cba9f",
     //    fill: false
     //  }
     // ]
    },
    options: {
      elements: {
              rectangle: {
                  // borderWidth: 2,
                  // borderColor: '#98c4f9',
                  borderSkipped: 'bottom'
              }
          },
      responsive: true,
      legend: {
          position: 'bottom',
      },
      title: {
          display: true,
          text: join_r_and_c
      },
      scales: {
                yAxes: [{
                     gridLines: {
                        display:false
                    },
                     ticks: {
                        beginAtZero: true,
                         // stepSize: 500000,
                        // min: respdata['min_max_dict']['min_value'],
                        min: min_num,
                        max: respdata['min_max_dict']['max_value'],

                     
                        userCallback: function(value, index, values) {
                        // Convert the number to a string and splite the string every 3 charaters from the end
                        // value = value.toString();
                        // value = value.split(/(?=(?:...)*$)/);
                        // Convert the array to a string and format the output
                        // value = value.join(',');
                            // return  value ;
         
                        if (value >= 1000000000) {
                            return (value / 1000000000).toFixed(1).replace(/\.0$/, '') + 'G';
                         }
                         else if (value >= 1000000) {
                            return (value / 1000000).toFixed(1).replace(/\.0$/, '') + 'M';
                         }
                        else if (value >= 1000) {
                            return (value / 1000).toFixed(1).replace(/\.0$/, '') + 'K';
                         }
                         else  {
                            return value;
                         }
                        // return (value / 1000).toFixed(1).replace(/\.0$/, '') + 'K';
                        // return value;
                        
                       
                        }

                    }
                }],
                xAxes: [{
                     gridLines: {
                        display:false
                    },
                    ticks: {
                        // Show all labels
                        autoSkip: false,
                        callback: function(tick) {
                            var characterLimit = 7;
                            if (tick.length >= characterLimit) {
                                return tick.slice(0, tick.length).substring(0, characterLimit - 1).trim() + '...';;
                            }
                            return tick;
                        }
                    }
                }]
            },
			tooltips: {
            	callbacks: {
                	title: function(tooltipItem){
                    	return this._data.labels[tooltipItem[0].index];
                    }
                }
            },
          plugins: {
            zoom: {
                // Container for pan options
                pan: {
                    // Boolean to enable panning
                    enabled: true,

                    // Panning directions. Remove the appropriate direction to disable 
                    // Eg. 'y' would only allow panning in the y direction
                    mode: 'xy'
                },

                // Container for zoom options
                zoom: {
                    // Boolean to enable zooming
                    enabled: true,

                    // Zooming directions. Remove the appropriate direction to disable 
                    // Eg. 'y' would only allow zooming in the y direction
                    mode: 'xy',
                }
            }
        },
           animation: {
      	onComplete: function () {
      		$("#download_img").removeAttr("href");
        // console.log('image line cchart 143',myChart.toBase64Image());
        document.getElementById('download_img').href = myChart.toBase64Image();
      },
    },
    }
  });
  	var image = myChart.toBase64Image();
}


var myChart;
function barchart(respdata){
	// alert('barchart funcction called')
	// var checkData = "csrfmiddlewaretoken=" + csrfmiddlewaretoken;
	// respdata = autoresponse("bar_chart", checkData);
	column=[];datarow=[];row=[];code_frame=[];code_frame1=[];data=[];
	var color_code=['purple', 'orange', 'blue', 'yellow','silver','maroon', "fushsia", "teal"];
    if(myChart){
        myChart.destroy();
    }



    // const index = label_arra.indexOf('AAAATotal'); //   0

    // if (index !== -1) {
    //   label_arra[index] = 'Total';
    // }


    //filter collection start
    var dimensions  = $("#example2-left li");
    var other_variable = $("#example33 li");
    var row_text;var col_text;
    other_variable.each(function(idx, li) {
         other_variable = $(li).text();
    });
    dimensions.each(function(idx, li) {
         dimensions = $(li).text();
    });
    

    // var join_r_and_c=other_variable+ " Vs " +dimensions;
     var join_r_and_c=dimensions+ " Vs  Time";
    //filter collection end

     console.log('charts 400',respdata)
     // console.log('charts 400',respdata.res_data.columns)


	for (var r =0; r<respdata.res_data.columns.length ; r++) {
			ccol1=[];
			for (var c =0; c<respdata.res_data.index.length ; c++) {
				// console.log('data col',c,'row data',r);
				ccol1.push(respdata.res_data.data[c][r].toFixed(1));
			}
			// console.log('labels',respdata.res_data.columns[r],'col1',ccol1);
			// data.push({['label']:respdata.res_data.columns[r],['data']:ccol1,['backgroundColor']:randColor()});
            data.push({['label']:respdata.res_data.columns[r],['data']:ccol1,['backgroundColor']:color_code[r]});
	}	

	// for (var x = 0; x < respdata.res_data.index.length; x++) {
	// 	code_frame.push('A'+x);
	// }


	console.log('dataset1',data);
	// console.log('label_arra',label_arra);
	$('#BarChart').remove();
	$("#barchartdiv").append('<canvas id="BarChart"></canvas>');

    var min_num=respdata['min_max_dict']['min_value'];

    if (min_num > 0) {
        min_num=0;
    }else{
         min_num=respdata['min_max_dict']['min_value'];
    }


	
	const ctx = document.getElementById('BarChart');
	myChart = new Chart(ctx, {
	type: 'bar',
	data: {
	  labels: respdata.res_data.index,
	  // labels: label_arra,
	   datasets:data,
	
	},
	   options: {

            // Elements options apply to all of the options unless overridden in a dataset
            // In this case, we are setting the border of each bar to be 2px wide and green
            elements: {
                rectangle: {
                    // borderWidth: 2,
                    // borderColor: '#98c4f9',
                    borderSkipped: 'bottom'
                }
            },
            responsive: true,
            legend: {
                position: 'bottom',
            },
            title: {
                display: true,
                text: join_r_and_c
            },
            scales: {
                yAxes: [{
                     gridLines: {
                        display:false
                    },
                    ticks: {
                        beginAtZero: true,
                         // stepSize: 500000,
                        // min: respdata['min_max_dict']['min_value'],
                        min: min_num,
                        max: respdata['min_max_dict']['max_value'],

                     
                        userCallback: function(value, index, values) {
                        // Convert the number to a string and splite the string every 3 charaters from the end
                        // value = value.toString();
                        // value = value.split(/(?=(?:...)*$)/);
                        // Convert the array to a string and format the output
                        // value = value.join(',');
                            // return  value ;
         
                        if (value >= 1000000000) {
                            return (value / 1000000000).toFixed(1).replace(/\.0$/, '') + 'G';
                         }
                         else if (value >= 1000000) {
                            return (value / 1000000).toFixed(1).replace(/\.0$/, '') + 'M';
                         }
                        else if (value >= 1000) {
                            return (value / 1000).toFixed(1).replace(/\.0$/, '') + 'K';
                         }
                         else  {
                            return value;
                         }
                         // return (value / 1000).toFixed(1).replace(/\.0$/, '') + 'K';
                        // return value;
                        
                       
                        }

                    }
                }],
                xAxes: [{
                    gridLines: {
                        display:false
                    },
                    ticks: {
                        // Show all labels
                        autoSkip: false,
                        callback: function(tick) {
                            var characterLimit = 7;
                            if (tick.length >= characterLimit) {
                                return tick.slice(0, tick.length).substring(0, characterLimit - 1).trim() + '...';;
                            }
                            return tick;
                        }
                    }
                }]
            },
			tooltips: {
            	callbacks: {
                	title: function(tooltipItem){
                    	return this._data.labels[tooltipItem[0].index];
                    }
                }
            },
            plugins: {
	            zoom: {
	                // Container for pan options
	                pan: {
	                    // Boolean to enable panning
	                    enabled: true,

	                    // Panning directions. Remove the appropriate direction to disable 
	                    // Eg. 'y' would only allow panning in the y direction
	                    mode: 'xy'
	                },

	                // Container for zoom options
	                zoom: {
	                    // Boolean to enable zooming
	                    enabled: true,

	                    // Zooming directions. Remove the appropriate direction to disable 
	                    // Eg. 'y' would only allow zooming in the y direction
	                    mode: 'xy',
	                }
	            }
        },
        animation: {
      	onComplete: function () {
        // console.log('image line 143',myChart.toBase64Image());
        document.getElementById('download_img').href = myChart.toBase64Image();
      },
    },
        }
	});

	var image = myChart.toBase64Image();
	// console.log('image',image);


  
}

function kFormatter(num) {
    return Math.abs(num) > 999 ? Math.sign(num)*((Math.abs(num)/1000).toFixed(1)) + 'k' : Math.sign(num)*Math.abs(num)
}

$('#reset_zoom').click(function(){
    myChart.resetZoom();
});



 function ppt_dwn(respdata_new){

    var chart_type=$("#Chart_type").val();
    // alert(chart_type)
    
    var label_arra=respdata_new.res_data.index;
    column=[];datarow=[];row=[];code_frame=[];code_frame1=[];data=[];
    for (var r =0; r<respdata_new.res_data.columns.length ; r++) {
            ccol1=[];
            for (var c =0; c<respdata_new.res_data.index.length ; c++) {
                // console.log('data col',c,'row data',r);
                ccol1.push(respdata_new.res_data.data[c][r]);
            }
            // console.log('labels',respdata_new.res_data.columns[r],'col1',ccol1);
            // data.push({['label']:respdata_new.res_data.columns[r],['data']:ccol1,['backgroundColor']:randColor()});
            data.push({['labels']:label_arra,['values']:ccol1,['name']:respdata_new.res_data.columns[r]});
    }   

    console.log('ppt dataset1',data);

    let pres = new PptxGenJS();
    let slide = pres.addSlide();
    let dataChartAreaLine = data;


    if (chart_type=='bar_chart') {
        slide.addChart(pres.ChartType.bar, dataChartAreaLine, { x: 1, y: 1, w: 8, h: 4 });
        pres.writeFile("Sample Presentation.pptx");
    }else if(chart_type=='line_chart'){
        slide.addChart(pres.ChartType.line, dataChartAreaLine, { x: 1, y: 1, w: 8, h: 4 });
        pres.writeFile("Sample Presentation.pptx");
    }


    

  }

  function ppt_img(){

   var img;
            var resultDiv = document.getElementById("result");
            html2canvas(document.getElementById("BarChart"),
             {
                onrendered: function(canvas) {
                   img = canvas.toDataURL("image/png");
                  console.log('img1',img)
                  let pres = new PptxGenJS();
                  let slide1 = pres.addSlide();
                  let slide2 = pres.addSlide();
                  slide1.addImage({  data:img,x: 0,
                                    // y: 1,
                                    // w: "100%",
                                    // h: 2,
                                    // align: "center",
                                    // color: "0088CC",
                                    // fill: "F1F1F1",
                                    // fontSize: 24,
                                    y: 1,
                                    w: "100%",
                                    h: 3.5,
                                    align: "center",
                                    color: "0088CC",
                                    fill: "F1F1F1",
                                    fontSize: 24,
                                  });
                  slide2.addImage({  data:img,x: 0,
                                    // y: 1,
                                    // w: "100%",
                                    // h: 2,
                                    // align: "center",
                                    // color: "0088CC",
                                    // fill: "F1F1F1",
                                    // fontSize: 24,
                                    y: 1,
                                    w: "100%",
                                    h: 3.5,
                                    align: "center",
                                    color: "0088CC",
                                    fill: "F1F1F1",
                                    fontSize: 24,
                                  });
                  pres.writeFile("Sample Presentation.pptx");



                  }
            });

  }


const randColor = () =>  {
    return "#" + Math.floor(Math.random()*16777215).toString(16).padStart(6, '0').toUpperCase();
}


// console.log('data=======',data)

// function barchart_bk(){
// // alert('hii')

// 	$('#BarChart').remove();
// 	$("#barchartdiv").append('<canvas id="BarChart"></canvas>');
// 	const ctx = document.getElementById('BarChart');

//   new Chart(ctx, {
//     type: 'bar',
//     data: {
//       labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
//       datasets: [{
//         label: '# of Votes',
//         data: [12, 19, 3, 5, 2, 3],
//         borderWidth: 1,
//                 backgroundColor: [
//           "rgba(10,20,30,0.3)",
//           "rgba(10,20,30,0.3)",
//           "rgba(10,20,30,0.3)",
//           "rgba(10,20,30,0.3)",
//           "rgba(10,20,30,0.3)"
//         ],
//         borderColor: [
//           "rgba(10,20,30,1)",
//           "rgba(10,20,30,1)",
//           "rgba(10,20,30,1)",
//           "rgba(10,20,30,1)",
//           "rgba(10,20,30,1)"
//         ],

//       },
//       {
//         label: '# of Votes',
//         data: [12, 19, 3, 5, 2, 3],
//         borderWidth: 1,
//         backgroundColor: [
//           "rgba(50,150,200,0.3)",
//           "rgba(50,150,200,0.3)",
//           "rgba(50,150,200,0.3)",
//           "rgba(50,150,200,0.3)",
//           "rgba(50,150,200,0.3)"
//         ],
//         borderColor: [
//           "rgba(50,150,200,1)",
//           "rgba(50,150,200,1)",
//           "rgba(50,150,200,1)",
//           "rgba(50,150,200,1)",
//           "rgba(50,150,200,1)"
//         ],
//       }
//      ]
//     },
//        options: {
//       scales: {
//         y: {
//           beginAtZero: true
//         }
//       }
//     }
//   });
  
// }