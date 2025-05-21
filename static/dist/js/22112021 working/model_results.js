$(document).ready(function(){
	var myChart1; 
	var myChart;
// // alert('yes!!');
// flag=window.localStorage.getItem('flag');
// if (flag==0) {
//    window.location.replace("https://forecasting.azurewebsites.net/");
//    // window.location.replace("http://127.0.0.1:8000");
// }
showPreloader();
var csrfmiddlewaretoken=csrftoken;



setTimeout(function () {
	var checkData2 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken;
	resp_histotic_filter = autoresponse("Historic_filename_Filtery", checkData2);
	if (resp_histotic_filter.status  == 200)
	// if (respdata2.status  == 200)
	{
	 Historic_Filtery(resp_histotic_filter)

	 data_type_append_common();
	 common_prediction_points_show();
	 
	 model_result_main()
	 	// alert('yes');
	}
	else
	{
		// alert('no');
		$('#HOLT_WINTER_NA_ID_id').css("display","block")//#MODIFICATION DONE BY PRANIT ON 25-05-2021
		hidePreloader();//#MODIFICATION DONE BY PRANIT ON 25-05-2021
	}

}, 100);



function data_type_append_common(){
	setTimeout(function () {
		var historic_data_file_name = $("#historic_data_file_name").val();
	var checkData2 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken+"&historic_data_file_name=" + historic_data_file_name;
	resp = autoresponse("data_type_append_common", checkData2);
	if (resp.status  == 200)
	// if (respdata2.status  == 200)
	{
	 
	 	// alert('yes');
	 	data_type_filter_common(resp.data_type.trim());
	}
	else
	{
		alert('no');
		
		hidePreloader();//#MODIFICATION DONE BY PRANIT ON 25-05-2021
	}

}, 100);

}
function Historic_Filtery(resp){
    var i = 1;
    $.each(resp.data, function (k, v) {
    	json_file_name=v[0].slice(0, -5);
    	console.log('========================',json_file_name);
        if(i == 1){
            $("#historic_data_file_name").append('<option value="' + v + '" selected>' + json_file_name + '</option>');
        }else{
            $("#historic_data_file_name").append('<option value="' + v + '" >' +json_file_name + '</option>');
        }
        i++;
    });
    
}

// setTimeout(function () {
// 			// var social_media_type = $("#social_media_type").val();
// 			var analyzeInput = $("#analyzeInput").val();
// 			var historic_data = $("#historic_data").val();
// 			var model_type = "Holt_Winter_Model";
// 			// alert(historic_data);
// 			var checkData2 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken+"&analyzeInput=" + analyzeInput+"&model_type=" + model_type;
// 			respdata2 = autoresponse("model_results", checkData2);
// 			if (respdata2.status  == 200)
// 			// if (respdata2.status  == 200)
// 			{
// 			    // hidePreloader();
// 				model_summary_div_table1(respdata2);
// 				EvaluationMetrics_div_table1(respdata2);
// 				arima_actual_fitted_chart(respdata2);
// 				forecast_fitted_chart(respdata2);
// 			// alert('yes');
// 			}
// 			else
// 			{
// 				// alert('no holt winter model');
// 				$('#HOLT_WINTER_NA_ID_id').css("display","block")//#MODIFICATION DONE BY PRANIT ON 25-05-2021
// 				hidePreloader();//#MODIFICATION DONE BY PRANIT ON 25-05-2021
// 			}

// 		}, 100);

$('#historic_data_file_name').change(function ()
    {
    	var model_type = $("#nav-tab a.active").attr('id');
    	// alert(model_type);
    	if (model_type=='Arimax_model') {
			var historic_data_file_name = $("#historic_data_file_name").val();
			var checkData2 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken+"&analyzeInput=" + analyzeInput+"&model_type=" + model_type+"&historic_data_file_name=" + historic_data_file_name;
			respdata2 = autoresponse("input_file_dimension_check", checkData2);
			if (respdata2.status  == 200)
				{
					if(respdata2.column_size>0){
						$(".notification_mssg_1").show();
						$(".notification_mssg").show();
						$(".Arimax_cls_hide").hide();
						$(".notification_mssg_2").hide();
						independent_prediction_point_btn_show();
						// alert(1);
					}
					else{
						// alert(2);
						independent_prediction_point_btn_hide();
						$(".notification_mssg_2").show();
						$(".notification_mssg_1").hide();
						$(".Arimax_cls_hide").hide();
						$(".notification_mssg").hide();
					}
				}
			else
			{
				$(".notification_mssg_2").show();
				$(".notification_mssg_1").hide();
				$(".Arimax_cls_hide").hide();
				$(".notification_mssg").hide();
			}
    	}
		else{
			data_type_append_common();
    		model_result_main();

		}
		
		

       // model_result_main();
	});	



$('#upload_data_type_id').change(function ()
    {
    	var model_type = $("#nav-tab a.active").attr('id');
    	// alert(model_type);
    	if (model_type=='Arimax_model') {
			var historic_data_file_name = $("#historic_data_file_name").val();
			var checkData2 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken+"&analyzeInput=" + analyzeInput+"&model_type=" + model_type+"&historic_data_file_name=" + historic_data_file_name;
			respdata2 = autoresponse("input_file_dimension_check", checkData2);
			if (respdata2.status  == 200)
				{
					if(respdata2.column_size>0){
						$(".notification_mssg_1").show();
						$(".notification_mssg").show();
						$(".Arimax_cls_hide").hide();
						$(".notification_mssg_2").hide();
						independent_prediction_point_btn_show();
						// alert(1);
					}
					else{
						// alert(2);
						independent_prediction_point_btn_hide();
						$(".notification_mssg_2").show();
						$(".notification_mssg_1").hide();
						$(".Arimax_cls_hide").hide();
						$(".notification_mssg").hide();
					}
				}
			else
			{
				$(".notification_mssg_2").show();
				$(".notification_mssg_1").hide();
				$(".Arimax_cls_hide").hide();
				$(".notification_mssg").hide();
			}
    	}
		else{
    		model_result_main();

		}
		
		

       // model_result_main();
	});	

function model_result_main() {

    showPreloader();
	setTimeout(function () {
			// var social_media_type = $("#social_media_type").val();
			var analyzeInput = $("#analyzeInput").val();
			var historic_data_file_name = $("#historic_data_file_name").val();
			var upload_data_type_id = $("#upload_data_type_id").val();
			// var model_type = "Holt_Winter_Model";
			var model_type = $("#nav-tab a.active").attr('id');
			var arimamape = localStorage.getItem('Arimax_mape');
			if (arimamape == null){
			    var value1="N.A";
			}
			else{
				var value1=parseFloat(arimamape).toFixed(4);
			}
			// alert(model_type);
			var checkData2 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken+"&analyzeInput=" + analyzeInput+"&model_type=" + model_type+"&historic_data_file_name=" + historic_data_file_name+"&arimamape=" + arimamape+"&upload_data_type_id=" + upload_data_type_id;
			respdata2 = autoresponse("model_results", checkData2);
			if (respdata2.status  == 200)
			// if (respdata2.status  == 200)
			{
				if(model_type  == "ALL_MODEL_SUMMARY"){
					common_prediction_points_hide();
					independent_prediction_point_btn_hide();
					ALL_MODEL_SUMMARY_table(respdata2);
					hidePreloader();
				}
				// else if((model_type=="ARIMAX_Model") && (respdata2.column_size==0)){
				// 	alert('yes');
				// 	hidePreloader();
				// }
				else{
                   // hidePreloader();
					model_summary_div_table1(respdata2);
					EvaluationMetrics_div_table1(respdata2);
					arima_actual_fitted_chart(respdata2);
					forecast_fitted_chart(respdata2);
	                hidePreloader();
				}
			    
			// alert('yes');
			}
			else
			{
				// alert('no holt winter model');
				$('#HOLT_WINTER_NA_ID_id').css("display","block")//#MODIFICATION DONE BY PRANIT ON 25-05-2021
				hidePreloader();//#MODIFICATION DONE BY PRANIT ON 25-05-2021
			}

		}, 100);
}

   
function model_result_independent_main(){
   // alert('ssssssssss');

	model_summary_div_table1(respdata2);
	EvaluationMetrics_div_table1(respdata2);
	arima_actual_fitted_chart(respdata2);
	forecast_fitted_chart(respdata2);

}


$("#independent_model_submit_btn").click(function(){
	showPreloader();
setTimeout(function () {
	var number_of_prediction_point = $("#number_of_prediction_point").val();
	var data_column_size = localStorage.getItem('data_column_size');
	// var data_column_size_1 = data_column_size-2;
	var setRows    = number_of_prediction_point;
	// var setColumns = 2;
	var setColumns = data_column_size;
	var TotalObj= [];
	var Data_Obj= [];

	// console.log('llllllllllllll',displayRecords);

	// alert('llllllllllllll');
	for (var i = 1; i <=setRows ; i++) {
		// var Data_Obj= [];
		$("#Month"+i+" td input").each(function(){
		  var input_val = $(this).val();

		  console.log('llllllllllllll',input_val);
		  Data_Obj.push([input_val]);
		  // Data_Obj.push({input_val:input_val});
		  });


	}

	  console.log('Data_Obj',Data_Obj.length);

	      
	  var analyzeInput = $("#analyzeInput").val();
	  var historic_data_file_name = $("#historic_data_file_name").val();
	  // var model_type = "Holt_Winter_Model";
	  var model_type = $("#nav-tab a.active").attr('id');
	  var csrfmiddlewaretoken=csrftoken;
	  // alert(model_type);
	  var checkData2 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken+"&number_of_prediction_point=" + number_of_prediction_point+"&model_type=" + model_type+"&historic_data_file_name=" + historic_data_file_name+"&Data_Obj=" + Data_Obj+"&setColumns=" + setColumns;
	  respdata2 = autoresponse("model_results_for_indepedent_model", checkData2);
	  if (respdata2.status  == 200)
	  {
	    
	    // alert('yes');
	    localStorage.setItem('Arimax_mape', respdata2.Data1.table2.mape);
	    $('.Arimax_cls_hide').show();
	    model_result_independent_main(respdata2);
	    $('#Please_select_no_of_prediction_points').hide();
	    $('#staticBackdrop').modal('toggle');
	    hidePreloader();
	  }
	  else
	  {
	    alert('Something went wrong');
	    hidePreloader();//#MODIFICATION DONE BY PRANIT ON 25-05-2021
	  }

    }, 100);

  });

$("#analyzeInput_btn").click(function(){
  // alert("The paragraph was clicked.");
  
    showPreloader();
    setTimeout(function () {
			var analyzeInput = $("#analyzeInput").val();
			// alert(analyzeInput);
			model_type = $("#nav-tab a.active").attr('id');
			var historic_data_file_name = $("#historic_data_file_name").val();
			var checkData2 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken+"&analyzeInput=" + analyzeInput+"&model_type=" + model_type+"&historic_data_file_name=" + historic_data_file_name;
			respdata2 = autoresponse("model_results", checkData2);
			if (respdata2.status  == 200)
			{

			model_summary_div_table1(respdata2);
			EvaluationMetrics_div_table1(respdata2);
			arima_actual_fitted_chart(respdata2);
			forecast_fitted_chart(respdata2);

			// alert('yes');
			}
			else
			{
			alert('Something went wrong');
			}

		}, 100);


});

$("#Arimax_model").click(function(){
    // alert("nav-ARIMA-tab");
    var data_column_size = localStorage.getItem('data_column_size');
    common_prediction_points_hide();
    independent_prediction_point_btn_show();
     // if (data_column_size>0)
     // {
     // // alert('yes');
     // $("#common_prediction_points").hide();

     // }
     // else
     // {
     // // alert('no');
     // $("#Please_select_no_of_prediction_points").hide();
     // $("#Arimax_analysis_btn").hide();
     // $("#Arimax_error_NA_id").show();
     //  // hidePreloader();

     // }

     if(data_column_size>0){
			$(".notification_mssg_1").show();
			$(".notification_mssg").show();
			$(".Arimax_cls_hide").hide();
			$(".notification_mssg_2").hide();
			// alert(1);
		}
		else{
			// alert(2);
			$(".notification_mssg_2").show();
			$(".notification_mssg_1").hide();
			$(".Arimax_cls_hide").hide();
			$(".notification_mssg").hide();
		}


});



$("#SARIMA_Model").click(function(){
    // alert("nav-ARIMA-tab");
    // model_result_main()
    common_prediction_points_show();
    independent_prediction_point_btn_hide();
    // $("#common_prediction_points").hide();
    showPreloader();
    setTimeout(function () {
			var analyzeInput = $("#analyzeInput").val();
			model_type = $("#nav-tab a.active").attr('id');
			var historic_data_file_name = $("#historic_data_file_name").val();
			var checkData2 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken+"&analyzeInput=" + analyzeInput+"&model_type=" + model_type+"&historic_data_file_name=" + historic_data_file_name;
			respdata2 = autoresponse("model_results", checkData2);
			var myJSON = JSON.stringify(respdata2);
			if (respdata2.status  == 200)
			{
				localStorage.setItem('data_column_size', respdata2.column_size);

			model_summary_div_table1(respdata2);
			EvaluationMetrics_div_table1(respdata2);
			arima_actual_fitted_chart(respdata2);
			forecast_fitted_chart(respdata2);

			// alert('yes');
			hidePreloader();
			}
			else
			{
			// alert('no');
			$('#SARIMA_NA_ID_id').css("display","block")//#MODIFICATION DONE BY PRANIT ON 25-05-2021
		    hidePreloader();//#MODIFICATION DONE BY PRANIT ON 25-05-2021

			}

		}, 100);


});


$("#UCM_Model").click(function(){
    // alert("nav-ARIMA-tab");
    // model_result_main()
    common_prediction_points_show();
    independent_prediction_point_btn_hide();
    // $("#common_prediction_points").hide();
    showPreloader();
    setTimeout(function () {
			var analyzeInput = $("#analyzeInput").val();
			model_type = $("#nav-tab a.active").attr('id');
			var historic_data_file_name = $("#historic_data_file_name").val();
			var checkData2 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken+"&analyzeInput=" + analyzeInput+"&model_type=" + model_type+"&historic_data_file_name=" + historic_data_file_name;
			respdata2 = autoresponse("model_results", checkData2);
			var myJSON = JSON.stringify(respdata2);
			if (respdata2.status  == 200)
			{
				localStorage.setItem('data_column_size', respdata2.column_size);

			model_summary_div_table1(respdata2);
			EvaluationMetrics_div_table1(respdata2);
			arima_actual_fitted_chart(respdata2);
			forecast_fitted_chart(respdata2);

			// alert('yes');
			hidePreloader();
			}
			else
			{
			// alert('no');
			$('#UCM_NA_ID_id').css("display","block")//#MODIFICATION DONE BY PRANIT ON 25-05-2021
		    hidePreloader();//#MODIFICATION DONE BY PRANIT ON 25-05-2021

			}

		}, 100);


});

$("#ARIMA_Model").click(function(){
    // alert("nav-ARIMA-tab");
    // model_result_main()
    common_prediction_points_show();
    independent_prediction_point_btn_hide()
    showPreloader();
    setTimeout(function () {
			var analyzeInput = $("#analyzeInput").val();
			model_type = $("#nav-tab a.active").attr('id');
			var historic_data_file_name = $("#historic_data_file_name").val();
			var checkData2 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken+"&analyzeInput=" + analyzeInput+"&model_type=" + model_type+"&historic_data_file_name=" + historic_data_file_name;
			respdata2 = autoresponse("model_results", checkData2);
			var myJSON = JSON.stringify(respdata2);
			// alert('wwwwwwwwwwwwwww');
			console.log('ARIMA_Model_respdata2============',typeof(respdata2));
			if (respdata2.status  == 200)
			{

			model_summary_div_table1(respdata2);
			EvaluationMetrics_div_table1(respdata2);
			arima_actual_fitted_chart(respdata2);
			forecast_fitted_chart(respdata2);

			// alert('yes');
			}
			else
			{
			// alert('no');
			$('#ARIMA_NA_ID_id').css("display","block")//#MODIFICATION DONE BY PRANIT ON 25-05-2021
		    hidePreloader();//#MODIFICATION DONE BY PRANIT ON 25-05-2021

			}

		}, 100);


});

$("#Holt_Winter_Model").click(function(){
    // alert("nav-ARIMA-tab");
    // model_result_main()
    common_prediction_points_show();
    independent_prediction_point_btn_hide()
    showPreloader();
    setTimeout(function () {
			var analyzeInput = $("#analyzeInput").val();
			model_type = $("#nav-tab a.active").attr('id');
			var historic_data_file_name = $("#historic_data_file_name").val();
			var checkData2 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken+"&analyzeInput=" + analyzeInput+"&model_type=" + model_type+"&historic_data_file_name=" + historic_data_file_name;
			respdata2 = autoresponse("model_results", checkData2);
			if (respdata2.status  == 200)
			{

			model_summary_div_table1(respdata2);
			EvaluationMetrics_div_table1(respdata2);
			arima_actual_fitted_chart(respdata2);
			forecast_fitted_chart(respdata2);

			// alert('yes');
			}
			else
			{
			// alert('no');
			$('#HOLT_WINTER_NA_ID_id').css("display","block")//#MODIFICATION DONE BY PRANIT ON 25-05-2021
		    hidePreloader();//#MODIFICATION DONE BY PRANIT ON 25-05-2021
			}

		}, 100);


});

$("#ALL_MODEL_SUMMARY").click(function(){
    // alert("ALL_MODEL_SUMMARY");
    common_prediction_points_hide();
    independent_prediction_point_btn_hide();
    showPreloader();
    setTimeout(function () {
			var analyzeInput = $("#analyzeInput").val();
			model_type = $("#nav-tab a.active").attr('id');
			var historic_data_file_name = $("#historic_data_file_name").val();
			var arimamape = localStorage.getItem('Arimax_mape');
		   if (arimamape == null){
			    var value1="N.A";
			}
			else{
				var value1=parseFloat(arimamape).toFixed(4);
			}
			// alert(model_type)
			// alert(analyzeInput)
			var checkData2 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken+"&analyzeInput=" + analyzeInput+"&model_type=" + model_type+"&historic_data_file_name=" + historic_data_file_name+"&arimamape=" + arimamape;
			respdata2 = autoresponse("model_results", checkData2);
			if (respdata2.status  == 200)
			{
			// model_summary_div_table1(respdata2);
			// EvaluationMetrics_div_table1(respdata2);
			// arima_actual_fitted_chart(respdata2);
			ALL_MODEL_SUMMARY_table(respdata2);
			hidePreloader();
			// alert('yes');
			}
			else
			{
			$('#ALL_MODEL_SUMMARY_NA_ID_id').css("display","block")//#MODIFICATION DONE BY PRANIT ON 25-05-2021
		    hidePreloader();//#MODIFICATION DONE BY PRANIT ON 25-05-2021
			}

		}, 100);


});

// working function ALL_MODEL_SUMMARY_table
// function ALL_MODEL_SUMMARY_table(displayRecords) {
// // alert('okay');
// var percent_val='%';
// $('#Arima_mape').html((displayRecords.Data1.arima).toFixed(4)+' '+percent_val+'');
// $('#holt_winter_mape').html((displayRecords.Data1.holt_winter).toFixed(4)+' '+percent_val+'');
// $('#ucm_mape').html(displayRecords.Data1.ucm);
// $('#Bayesia_mape').html(displayRecords.Data1.bayesia);
// $('#Sarima_mape').html(displayRecords.Data1.sarima);
// }

function ALL_MODEL_SUMMARY_table(displayRecords) {
	// alert('okay');
	// console.log('llllllllllllll',displayRecords);

	var html=i= '';
	html +='<table class="table table-striped table-responsive-sm">';
	html +='<thead>';
	html +='<tr class="table-font-hd">';
	html +='<th scope="col" colspan="4" class="px-1">Summary Data</th>';
	html +='</tr>';
	html +='</thead>';
	html +='<tbody>';
	html +='<tr>';
	html +='<td class="text-center"><b>METHOD</b></td>';
	html +='<td class="text-center"><b>MAPE</b></td>';
	html +='</tr>';
	// console.log('sort array', displayRecords.Data1);
	// var masterList=displayRecords.Data1;
	// var masterList_ = {}


	// var masterList=Object.values(masterList).sort()
	// // console.log(masterList_)
	// console.log('sort arraymasterList', masterList);
	// var masterList=displayRecords.Data1;
	var masterList1=Object.entries(displayRecords.Data1).sort((a,b) => a[1]-b[1])
	console.log('sort arraymasterList', masterList1);

	// $.each(masterList1, function (k1, value1) {
	// 		console.log('sort arraymasterList new', value1[0],value1[1]);

	// 	html +='<tr>';
	// 	   var k11=value1[0].replace(/[^a-zA-Z ]/g, " ");
		   
	// 	   if (value1[0]=='arimax') {
	// 	   		var arimamape = localStorage.getItem('Arimax_mape');
	// 		   if (arimamape == null){
	// 			    value1[1]="N.A";
	// 			}
	// 			else{
	// 				value1[1]=parseFloat(arimamape).toFixed(4);

	// 			}
	// 	   }
		
	// 	});
	// // var masterList1=Object.entries(displayRecords.Data1).sort((a,b) => a[1]-b[1])
	// console.log('sort arraymasterList new array', masterList1);



	$.each(masterList1, function (k1, value1) {
		html +='<tr>';
		   var k11=value1[0].replace(/[^a-zA-Z ]/g, " ");
			mape_color=model_mape_value_check(value1[1]);
			html +='<td class="text-center">'+k11.capitalize();+' </td>';
			html +='<td class="text-center"  style="background:'+mape_color+';color:white">'+parseFloat(value1[1]).toFixed(4);+'</td>';
        html +='</tr>';
		});


	html +='</tbody>';
	html +='</table>';
	$('#ALL_MODEL_SUMMARY_div_table1').html(html);
     hidePreloader();

}

String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

function model_summary_div_table1(displayRecords) {
	var html=i= '';
	
	
    $("#forecast_line_img_div img:last-child").remove();
    $("#actual_fitted_img_div img:last-child").remove();
    $("#arima_forecast_line_img_div img:last-child").remove();
    $("#arima_actual_fitted_img_div img:last-child").remove();
	html +='<table class="table table-striped table-responsive-sm">';
	html +='<thead>';
	html +='<tr class="table-font-hd">';
	// html +='<th scope="col" colspan="4" class="px-1">Model Summary</th>';
	html +='<th scope="col" colspan="2" class="px-1">Model Summary</th>';
	html +='<th scope="col" class="px-1" colspan="4" style="text-align: end;"><a  class="btn bg-red" data-toggle="modal" data-target="#Help_section" style="float: right;"><i class="fas fa-info"></i></a></th>';
	html +='</tr>';
	html +='</thead>';
	html +=' <tbody>';
	// for (var i = 0;i<7; i++) {
		html +='<tr>';
	
		$.each(displayRecords.Data1.table1, function (k1, value1) {
            // console.log('ssssssssssss',value1);
			html +='<td class="text-center">'+value1.Dep+'</td>';
			html +='<td class="text-center">'+value1.Sales+'</td>';
			html +='<td class="text-center">'+value1.Observations+'</td>';
			html +='<td class="text-center">'+value1.val+'</td>';
        html +='</tr>';
		});

	html +='</tbody>';
	html +='</table>';
    
        $("#forecast_line_img_div").append("<img src='/static/images/forecast_line/"+displayRecords.Data1.forecast_line_img+".jpg' class='img-fluid'  /> ");
        $("#actual_fitted_img_div").append("<img src='/static/images/actual_fitted/"+displayRecords.Data1.actual_fitted_img+".jpg' class='img-fluid'  /> ");
        $("#arima_forecast_line_img_div").append("<img src='/static/images/forecast_line/"+displayRecords.Data1.forecast_line_img+".jpg' class='img-fluid'  /> ");
        $("#arima_actual_fitted_img_div").append("<img src='/static/images/actual_fitted/"+displayRecords.Data1.actual_fitted_img+".jpg' class='img-fluid'  /> ");

        model_type = $("#nav-tab a.active").attr('id');
        if (model_type=='Holt_Winter_Model') {
        	$('#model_summary_div_table1').html(html);
        	hidePreloader();
        }
        else if(model_type=='ARIMA_Model'){
        	$('#Arima_model_summary_div_table1').html(html);
        	hidePreloader();
        }
        else if(model_type=='SARIMA_Model'){
        	$('#Sarima_model_summary_div_table1').html(html);
        	hidePreloader();
        }
        else if(model_type=='UCM_Model'){
        	$('#UCM_model_summary_div_table1').html(html);
        	hidePreloader();
        }
        else if(model_type=='Arimax_model'){
        	$('#Arimax_model_summary_div_table1').html(html);
        	hidePreloader();
        }
		// $('#model_summary_div_table1').html(html);
		//  hidePreloader();
  }


function EvaluationMetrics_div_table1(displayRecords) {
	var html=i= '';
	html +='<table class="table table-striped table-responsive-sm">';
	html +='<thead>';
	html +='<tr class="table-font-hd">';
	html +='<th scope="col" colspan="4" class="px-1">Evaluation Metrics</th>';
	html +='<th scope="col" class="px-1" colspan="4" style="text-align: end;"><span class="px-2  pr-1 mr-1" style="background-color:green"></span> Excellent  <span class="px-2  pr-1 mr-1" style="background-color:#ffb100"></span> Good  <span class="px-2  pr-1 mr-1" style="background-color:red"></span> Poor</th>';
	// html +='<th scope="col" class="px-1"><span class="px-2  pr-1 mr-1" style="background-color:#D8BFD8"></span> Poor</th>';
	html +='</tr>';
	html +='</thead>';
	html +='<tbody>';
	html +='<tr>';
	html +='<td class="text-center">mape: </td>';
	html +='<td class="text-center">me: </td>';
	html +='<td class="text-center">mae: </td>';
	html +='<td class="text-center">mpe: </td>';
	html +='<td class="text-center">rsme: </td>';
	html +='<td class="text-center">corr:</td>';
	html +='<td class="text-center">minmax:</td>';
	html +='</tr>';
	html +='<tr>';
	$.each(displayRecords.Data1.table2, function (k1, value1) {
		var mape_color="white";
		var percent_val='';
		var bg='black';

       if (k1=="mape") {
       	mape_color=model_mape_value_check(value1);
       	   percent_val="%";
       	   bg='white';
       }
        html +='<td class="text-center" style="background: '+mape_color+';color:'+bg+'">'+value1.toFixed(4)+ ' '+ percent_val+'</td>';
        // console.log('k11111111111111',k1);

	});	
	html +='</tr>';
	html +='</tbody>';
	html +='</table>';

	model_type = $("#nav-tab a.active").attr('id');
    if(model_type=='Holt_Winter_Model') {
    	$('#EvaluationMetrics_div_table1').html(html);
    	hidePreloader();
    }
    else if(model_type=='ARIMA_Model'){
    	$('#Arima_EvaluationMetrics_div_table1').html(html);
    	hidePreloader();
    }
    else if(model_type=='SARIMA_Model'){
    	$('#Sarima_EvaluationMetrics_div_table1').html(html);
    	hidePreloader();
    }
    else if(model_type=='UCM_Model'){
    	$('#UCM_EvaluationMetrics_div_table1').html(html);
    	hidePreloader();
    }
    else if(model_type=='Arimax_model'){
        	$('#Arimax_EvaluationMetrics_div_table1').html(html);
        	hidePreloader();
    }

	// $('#EvaluationMetrics_div_table1').html(html);
	//  hidePreloader();
  }


var myChart1;  
function arima_actual_fitted_chart(resp){
	if (myChart1) {
        myChart1.destroy();
    }
 var label = [],dataset_red=[];dataset_blue=[];
	model_type = $("#nav-tab a.active").attr('id');
	// alert(model_type);
	if(model_type=='Holt_Winter_Model') {
		var ctx = document.getElementById("holt_winter_actual_fitted_line_chart1").getContext('2d');
		// save as image code start here
		function done(){
		  // alert("haha");
		  var url=myChart1.toBase64Image();
		  localStorage.setItem('Actual_vs_fitted_line_chart', url);
		  // alert(url);
		  document.getElementById("holt_winter_actual_fitted_lin_chart_img_save_as").href=url;
		}
		// save as image code end here
	}
	else if(model_type=='ARIMA_Model'){
       var ctx = document.getElementById("arima_actual_fitted_line_chart2").getContext('2d');
       // save as image code start here
		function done(){
		  // alert("haha");
		  var url=myChart1.toBase64Image();
		  localStorage.setItem('Actual_vs_fitted_line_chart', url);
		  // alert(url);
		  document.getElementById("arima_actual_fitted_line_chart_img_save_as").href=url;
		}
		// save as image code end here
	}
	else if(model_type=='SARIMA_Model'){
       var ctx = document.getElementById("Sarima_actual_fitted_line_chart2").getContext('2d');
       // save as image code start here
		function done(){
		  // alert("haha");
		  var url=myChart1.toBase64Image();
		  localStorage.setItem('Actual_vs_fitted_line_chart', url);
		  // alert(url);
		  document.getElementById("Sarima_actual_fitted_line_chart_img_save_as").href=url;
		}
		// save as image code end here
	}
	else if(model_type=='UCM_Model'){
       var ctx = document.getElementById("UCM_actual_fitted_line_chart2").getContext('2d');
       // save as image code start here
		function done(){
		  // alert("haha");
		  var url=myChart1.toBase64Image();
		  localStorage.setItem('Actual_vs_fitted_line_chart', url);
		  // alert(url);
		  document.getElementById("UCM_actual_fitted_line_chart_img_save_as").href=url;
		}
		// save as image code end here
	}
	else if(model_type=='Arimax_model'){
       var ctx = document.getElementById("Arimax_actual_fitted_line_chart2").getContext('2d');
       // save as image code start here
		function done(){
		  // alert("haha");
		  var url=myChart1.toBase64Image();
		  localStorage.setItem('Actual_vs_fitted_line_chart', url);
		  // alert(url);
		  document.getElementById("Arimax_actual_fitted_line_chart_img_save_as").href=url;
		}
		// save as image code end here
	}

	// console.log('dataset_blue',dataset_blue);
	// console.log('dataset_red',dataset_red);
	// console.log('label',label);
	// console.log('totalRecords',(totalRecords/ 12));
	$.each(resp.Data1.pred_actual_dict.data_blue_line, function(key, value) {
           var getMonth_resp=value.Month;
			var d = new Date(getMonth_resp);
			var n = d.getMonth();
			var y = d.getFullYear();
			getMonth_name=get_month_name(n);
			dataset_blue.push(value.Sales);
			label.push(getMonth_name+'-'+y);
			
	});
	$.each(resp.Data1.pred_actual_dict.data_red_line, function(key, value) {
			dataset_red.push(value.Sales);
	});
	// console.log('dataset_blue',dataset_blue);
	// console.log('dataset_blue',dataset_red);

	
	if(model_type=="ARIMA_Model"){
		// dataset_blue.shift();
		// dataset_red.shift();
		first_dataset_blue=dataset_blue[0]
		let replacedItem = dataset_red.splice(dataset_red.indexOf(0), 1, first_dataset_blue)

	}
	// console.log('dataset_blue remove',dataset_blue);
	console.log('dataset_red remove',dataset_red);
	var totalRecords = Object.keys(resp.Data1.pred_actual_dict.data_blue_line).length;
	  
	  myChart1 = new Chart(ctx, {
	  type: 'line',
	  data: {
		   
		    labels: label,
		    datasets: [
		    {
		      label: '# Actual Line',
		      data: dataset_blue,
		      // backgroundColor: 'rgba(255, 99, 132, 0.2)',
		      borderColor: 'blue',
		      borderWidth: 2,
		      fill: false
		    },
		    {
		      label: '# Fitted Line',
		      data: dataset_red,
		      // backgroundColor: 'red',
		      borderColor: 'red',
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
		          // stepSize: 100, // this worked as expected
		          // min:3000000,
		          // max:1900          
		        }
		      }],
		      xAxes: [{
		        ticks: {
		          maxTicksLimit: (totalRecords/ 12),
		           maxRotation:-120
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
  
var myChart;

function forecast_fitted_chart(resp){
	if (myChart) {
        myChart.destroy();
    }
 var label = [];dataset_red=[];dataset_blue=[];label_red = [];color_array=[];
	model_type = $("#nav-tab a.active").attr('id');
    var url;
	if (model_type=='Holt_Winter_Model') {
		var ctx = document.getElementById("holt_winter_forecast_line_chart").getContext('2d');
		// save as image code start here
		function done(){
		  // alert("haha");
		  url=myChart.toBase64Image();
		  localStorage.setItem('forecast_line_chart', url);
		  // alert(url);
		  // console.log('ggggggggggggggggggggggggggggggg',url)
		  document.getElementById("holt_winter_forecast_line_chart_img_save_as").href=url;
		}
		// save as image code end here
	}
	else if(model_type=='ARIMA_Model')  {
       var ctx = document.getElementById("arima_forecast_line_chart").getContext('2d');
       // save as image code start here
		function done(){
		  // alert("haha");
		  url=myChart.toBase64Image();
		  localStorage.setItem('forecast_line_chart', url);
		  
		  document.getElementById("Arima_forecast_line_chart_img_save_as").href=url;
		}
		// save as image code end here
	}
	else if(model_type=='SARIMA_Model')  {
       var ctx = document.getElementById("Sarima_forecast_line_chart").getContext('2d');
       // save as image code start here
		function done(){
		  // alert("haha");
		  url=myChart.toBase64Image();
		  localStorage.setItem('forecast_line_chart', url);
		  
		  document.getElementById("Sarima_forecast_line_chart_img_save_as").href=url;
		}
		// save as image code end here
	}
	else if(model_type=='UCM_Model')  {
       var ctx = document.getElementById("UCM_forecast_line_chart").getContext('2d');
       // save as image code start here
		function done(){
		  // alert("haha");
		  url=myChart.toBase64Image();
		  localStorage.setItem('forecast_line_chart', url);
		  
		  document.getElementById("UCM_forecast_line_chart_img_save_as").href=url;
		}
		// save as image code end here
	}
	else if(model_type=='Arimax_model')  {
       var ctx = document.getElementById("Arimax_forecast_line_chart").getContext('2d');
       // save as image code start here
		function done(){
		  // alert("haha");
		  url=myChart.toBase64Image();
		  localStorage.setItem('forecast_line_chart', url);
		  
		  document.getElementById("Arimax_forecast_line_chart_img_save_as").href=url;
		}
		// save as image code end here
	}
    // console.log('ggggggggggggggggggggggggggggggg',url)



	var len_color_blue = Object.keys(resp.Data1.forecast_actual_dict.data_blue_line).length;
	var len_color_red = Object.keys(resp.Data1.forecast_actual_dict.data_red_line).length;


	for (let j = 0; j < len_color_blue; j++) {
        color_name_blue='blue';
        color_array.push(color_name_blue);
    }
    for (let j = 0; j < len_color_red; j++) {
        color_name_red='red';
        color_array.push(color_name_red);
    }



	// console.log('color_array',color_array);
	// console.log('dataset_red',dataset_red);
	// console.log('label',label);
	// console.log('totalRecords',(totalRecords/ 12));
	$.each(resp.Data1.forecast_actual_dict.data_blue_line, function(key, value) {
           var getMonth_resp=value.Month;
			var d = new Date(getMonth_resp);
			var n = d.getMonth();
			var y = d.getFullYear();
			getMonth_name=get_month_name(n);
			dataset_blue.push(value.Sales);
			label.push(getMonth_name+'-'+y);
			
	});

	$.each(resp.Data1.forecast_actual_dict.data_red_line, function(key1, value1) {
			var red_getMonth_resp=value1.Month;
			var red_d = new Date(red_getMonth_resp);
			var red_n = red_d.getMonth();
			var red_y = red_d.getFullYear();
			var red_getMonth_name=get_month_name(red_n);
			dataset_red.push(value1.Sales);
			label_red.push(red_getMonth_name+'-'+red_y);
	});

	$.each(dataset_red, function(key2, value2) {
			dataset_blue.push(value2);
	});
	$.each(label_red, function(key3, value3) {
			label.push(value3);
	});
	 


	var totalRecords = Object.keys(dataset_blue).length;
	// var ctx = document.getElementById("holt_winter_actual_fitted_line_chart1").getContext('2d');
	  myChart = new Chart(ctx, {
	  type: 'line',
	  plugins: [{
			    afterLayout: chart => {
			      var ctx = chart.chart.ctx;
			      var xAxis = chart.scales['x-axis-0'];
			      var gradientStroke = ctx.createLinearGradient(xAxis.left, 0, xAxis.right, 0);
			      var dataset = chart.data.datasets[0];
			      dataset.colors.forEach((c, i) => {
			        var stop = 1 / (dataset.colors.length - 1) * i;
			        gradientStroke.addColorStop(stop, dataset.colors[i]);
			      });
			      dataset.backgroundColor = gradientStroke;
			      dataset.borderColor = gradientStroke;
			      dataset.pointBorderColor = gradientStroke;
			      dataset.pointBackgroundColor = gradientStroke;
			      dataset.pointHoverBorderColor = gradientStroke;
			      dataset.pointHoverBackgroundColor = gradientStroke;
			    }
	    }],
	  data: {
		   
		    labels: label,
		    datasets: [
		    {
		      label: '#Forecast Line',
		      data: dataset_blue,
		      // backgroundColor: 'rgba(255, 99, 132, 0.2)',
		      // borderColor: 'blue',
		      borderWidth: 2,
		      fill: false,
		       colors: color_array
		    },

		    
		    ]
		  },
		  options: {
		    scales: {
		      yAxes: [{
		        ticks: {
		          beginAtZero: false,
		          // min:3000000,          
		          // stepSize: 100, // this worked as expected
		          // min:1500          
		        }
		      }],
		      xAxes: [{
		        ticks: {
		          maxTicksLimit: (totalRecords/ 12),
		           maxRotation:-120
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
// var url111=myChart.toBase64Image();  
myChart.render();
var canvas = myChart.canvas;
var dataURL = canvas.toDataURL();
 // console.log('kkkkkkkkkkkkkkkkkkkkkkkkkkkkk',url111);	



}








function get_month_name(month) {
	const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
	  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
	const monthNames1 = ["January", "February", "March", "April", "May", "June",
	  "July", "August", "September", "October", "November", "December"];
	var getMonth_val=monthNames[month];
    return getMonth_val

}
// console.log('sssssssss',get_month_name(12));

});





//document close










