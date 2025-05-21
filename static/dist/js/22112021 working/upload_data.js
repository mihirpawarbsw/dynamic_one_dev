$(document).ready(function(){
// flag=window.localStorage.getItem('flag');
// if (flag==0) {
//    // window.location.replace("https://forecasting.azurewebsites.net/");
//    window.location.replace("http://127.0.0.1:8000/");
// }

// alert('aa');

 $("#docfile1").change(function(e){
            var fileName = e.target.files[0].name;
            $("#country_upload_file1").html(fileName);

   });

var csrfmiddlewaretoken=csrftoken;
   showPreloader();
   setTimeout(function () { 
            var upload_data_type_flag=0;  
            var upload_data_type=0;
			// var social_media_type = $("#social_media_type").val();
			// var checkData2 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken;
			var checkData2 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken+"&upload_data_type=" + upload_data_type+"&upload_data_type_flag=" + upload_data_type_flag;
			// var upload_data_type = $("#upload_data_type").val();
   //          alert(upload_data_type);	
			respdata2 = autoresponse("displaydata", checkData2);		
			if (respdata2.status  == 200)
			{
			display_table1_div(respdata2);
			data_type_filter_common(respdata2.data_type.trim());
			Trend_line_chart(respdata2);
			
			// alert('yes');
			}
			else
			{
			// alert('no');
			$('#DATA_table_id').css("display","block");//function modification done by pranit on 25-05-2021
			$('#trend_chart_id').css("display","block");//function modification done by pranit on 25-05-2021
			hidePreloader();//#function modification done by pranit on 25-05-2021
			} 
			
		}, 100);



	$("#Upload_data_btn").click(function(){
		showPreloader();
		$("#country_upload_file1").html("");
	  // alert("The paragraph was clicked.");
	    // alert('dd');
	    var retrievedObject = localStorage.getItem('upload-items');
	    var filename =  $('input:file').val().match(/[^\\/]*$/)[0];
	    var new_filename=filename.split('.').slice(0, -1).join('.')
	    // alert(new_filename);
	    var parsedObject_upload_item1 = JSON.stringify(retrievedObject);
	    var parsedObject_upload_item = JSON.parse(parsedObject_upload_item1);
	    var upload_data_type = $("#upload_data_type").val();
	    // console.log('upload-items',parsedObject_upload_item)
	    setTimeout(function () {
				// var Country = $("#Country").val();
				// var docfile1 = $("#docfile1").val();
				var checkData2 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken+"&parsedObject_upload_item=" + parsedObject_upload_item+"&new_filename=" + new_filename+"&upload_data_type=" + upload_data_type;
				respdata2 = autoresponse("upload_data", checkData2);
				if (respdata2.status  == 200)
				{
					var checkData3 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken;	
			        respdata3 = autoresponse("displaydata", checkData3);
			        $('#trend_chart_id').css("display","none");
			        window.location.reload();
			        // display_table1_div(respdata3);
			        // Trend_line_chart(respdata3);

				// model_summary_div_table1(respdata2);
				// alert('yes');
				}
				else
				{
				alert('Something Went Wrong');
				}

			}, 100);


	});



});	


function display_table1_div(displayRecords) {
	var html=i= '';
    $("#trend_line_chart_div img:last-child").remove();
	html +='<table class="table table-striped table-responsive-sm mt-4">';
	html +='<thead>';
	html +='<tr class="bg-danger table-font-hd">';
	html +='<th scope="col" class="text-center px-0">Month</th>';
	html +='<th scope="col" class="text-center px-2">Sale</th>';
	html +='</tr>';
	html +='</thead>';
	html +=' <tbody>';
	$.each(displayRecords.Data, function (k1, value1) {
    	// console.log('displayRecordsdisplayRecords',k1,value1);
    	html +='<tr>';
    	
			html +='<td class="text-center">'+value1.Month+'</td>';
			html +='<td class="text-center">'+value1.Sales+'</td>';
	    	// html +='<td>12</td>';
    	
    	


	});
	html +='</tr>';
	html +='</tbody>';
	html +='</table>';

    
    $("#trend_line_chart_div").append("<img src='/static/images/trend_line/"+displayRecords.trend_line+".jpg' class='img-fluid'  /> ");
    $('#display_table1_div').html(html);
     hidePreloader();
  }

var myChart;  
function Trend_line_chart(resp){


	if (myChart) {
        myChart.destroy();
    }
 var label = [],dataset_red=[];dataset=[];
	
	
	$.each(resp.Data, function(key, value) {
           var getMonth_resp=value.Month;
			var d = new Date(getMonth_resp);
			var n = d.getMonth();
			var y = d.getFullYear();
			getMonth_name=get_month_name(n);
			dataset.push(value.Sales);
			label.push(getMonth_name+'-'+y);
			
	});
	var totalRecords = Object.keys(resp.Data).length;

	console.log('dataset_blue',dataset);
	// console.log('label',label);
	console.log('totalRecords monthly',(totalRecords/ 12));
	console.log('totalRecords quaterly',(totalRecords/ 3));
	console.log('totalRecords value',totalRecords);
	// var totalRecords = Object.keys(resp.Data1.pred_actual_dict.data_blue_line).length;
	// save as image code start here
		function done(){
		  // alert("haha");
		  var url=myChart.toBase64Image();
		  // alert(url);
		  document.getElementById("trend_line_chart_img_save_as").href=url;
		}
		// save as image code end here
		var data_type=$('#upload_data_type_id').val().trim();

		// var data_type=resp.data_type.trim();
		var totalRecords_final=get_total_month_output(data_type,totalRecords);
		// alert(totalRecords_final);
	  var ctx = document.getElementById("canvas_trend_line_chart").getContext('2d');
	  myChart = new Chart(ctx, {
	  type: 'line',
	  data: {
		   
		    labels: label,
		    datasets: [
		    {
		      label: '# Trend Line Chart',
		      data: dataset,
		      // backgroundColor: 'rgba(255, 99, 132, 0.2)',
		      borderColor: 'blue',
		      borderWidth: 2,
		      fill: false
		    }
		    ]
		  },
		  options: {
		    scales: {
		      yAxes: [{
		        ticks: {
		          beginAtZero: false,          
		          // stepSize: 20 // this worked as expected          
		        }
		      }],
		      xAxes: [{
		        ticks: {
		          maxTicksLimit: totalRecords_final,
		          // maxTicksLimit: (totalRecords/ 12),//monthly spilte data
		          // maxTicksLimit: (totalRecords/ 3), //Quaterly spilte data
		          // minRotation:12,
		          maxRotation:60
		          // maxTicksLimit: 5
		        }
		      }]
		    },
		     bezierCurve : false,
			  animation: {
			    onComplete: done
			  }	
		  }
		});


}

 

function get_month_name(month) {
	const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
	  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
	const monthNames1 = ["January", "February", "March", "April", "May", "June",
	  "July", "August", "September", "October", "November", "December"];
	var getMonth_val=monthNames[month];
    return getMonth_val

}



$('#upload_data_type_id').on('change', function() {
   // showPreloader();
// alert('sss')
   setTimeout(function () {
   		var csrfmiddlewaretoken=csrftoken;  
   		var upload_data_type = $("#upload_data_type_id").val();
   		var upload_data_type_flag=1;
            // alert(upload_data_type); 
			// var social_media_type = $("#social_media_type").val();
			var checkData2 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken+"&upload_data_type=" + upload_data_type+"&upload_data_type_flag=" + upload_data_type_flag;	
			
			respdata2 = autoresponse("displaydata", checkData2);		
			if (respdata2.status  == 200)
			{
			display_table1_div(respdata2);
			Trend_line_chart(respdata2);
			
			// alert('yes');
			}
			else
			{
			// alert('no');
			$('#DATA_table_id').css("display","block");//function modification done by pranit on 25-05-2021
			$('#trend_chart_id').css("display","block");//function modification done by pranit on 25-05-2021
			hidePreloader();//#function modification done by pranit on 25-05-2021
			} 
			
		}, 100);

});