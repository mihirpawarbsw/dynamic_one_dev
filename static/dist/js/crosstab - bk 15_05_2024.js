$(document).ready(function(){
	$.LoadingOverlay("show");	
// flag=window.localStorage.getItem('flag');
// if (flag==0) {
//    // window.location.replace("https://forecasting.azurewebsites.net/");
//    window.location.replace("http://127.0.0.1:8000/");
// }



var csrfmiddlewaretoken=csrftoken;

var final_row_col_array_grp1 = localStorage.getItem('final_row_col_array_grp');
var final_row_col_array_grp2 = JSON.parse(final_row_col_array_grp1);

	// get row and column value from localstorage
	setTimeout(function () { 
			
			var column_name_list_object_1 = localStorage.getItem('column_name_list_object');
			var column_name_list_object_2 = JSON.parse(column_name_list_object_1);

			var row_name_list_object_1 = localStorage.getItem('row_name_list_object');
			var row_name_list_object_2 = JSON.parse(row_name_list_object_1);

			var remaining_other_list_object_1 = localStorage.getItem('remaining_other_list_object');
			var remaining_other_list_object_2 = JSON.parse(remaining_other_list_object_1);

			append_data_menu_list();

			//console.log('column_name_list_object_2 21' ,);
			//console.log('row_name_list_object_2 21',row_name_list_object_2.length);
			//console.log('remaining_other_list_object_2 21' ,remaining_other_list_object_2);

			if (column_name_list_object_2.length==1 && row_name_list_object_2.length==1) {
				// $(".significant_div").show();
				$("#chart_div").show();
				// alert(1)
				// $("#significant_div").css({"display":"block"});
			}else{
				// alert(2)
				// $(".significant_div").hide();
				$("#chart_div").hide();
			}
			var table_data_type_respone = localStorage.getItem('tbl_name');
			table_data_type_respone = table_data_type_respone.replace(/^"(.*)"$/, '$1');
			row_and_column_filter(row_name_list_object_2,column_name_list_object_2)

			
			if (table_data_type_respone=="respondent" || table_data_type_respone=="concat" ) {
				var measure_array=['People']
			}else{
				var measure_array=['People','Volume','Occasion']
			}
   			$('#weight_volume_type').find('option').remove();
			$.each(measure_array, function (kh1, kv1) {

		        $("#weight_volume_type").append('<option value="' + kv1 + '" >' +kv1+ '</option>');
			});
			$('#weight_volume_type option:first').attr('selected', true);
			$('#weight_volume_type').multiselect('rebuild');


			

			
			filename=Object.keys(final_row_col_array_grp2[0]);

			// time period filter start
			var time_range='QUARTER';
			var checkData5={'csrfmiddlewaretoken': csrfmiddlewaretoken,'filename':filename[0],'time_range':time_range};		
			resp_filter = autoresponse("current_time_period_resp", checkData5);
			if (resp_filter['status']==200) {
				// console.log('resp_filter',resp_filter)
				// time_period_filters(resp_filter['current_time_period_resp']);
				time_period_filters(resp_filter);
				comparative_time_period_resp();
			}
				
			// time period filter end
			

			
			
		}, 100);


   setTimeout(function () {
   			// alert('aa')
   			var column_name_list_object_1 = localStorage.getItem('column_name_list_object');
			var column_name_list_object_2 = JSON.parse(column_name_list_object_1);

			var row_name_list_object_1 = localStorage.getItem('row_name_list_object');
			var row_name_list_object_2 = JSON.parse(row_name_list_object_1);

			var seperated_flag_row_1 = localStorage.getItem('seperated_flag_row');
			var seperated_flag_row_2 = JSON.parse(seperated_flag_row_1);

			var seperated_flag_col_1 = localStorage.getItem('seperated_flag_col');
			var seperated_flag_col_2 = JSON.parse(seperated_flag_col_1);


			

			var wt_measures_1 = localStorage.getItem('wt_measures');
			var wt_measures_2 = JSON.parse(wt_measures_1);

			var table_data_type_respone = localStorage.getItem('tbl_name');
			table_data_type_respone = table_data_type_respone.replace(/^"(.*)"$/, '$1');


			calculation_type_name=$('input[name="calculation_type"]:checked').val();
			weight_type_name=$('input[name="weight_type"]:checked').val();
			Total_column_filter=$('input[name="Total_column"]:checked').val();
			weight_volume_type_name=$('input[name="weight_volume_type"]:checked').val();
			// decimal_point_filter=5
			var decimal_point_filter=$('#decimal_filter_new').val();



			var checkData4={'csrfmiddlewaretoken': csrfmiddlewaretoken,'final_row_col_array_grp':JSON.stringify(final_row_col_array_grp2),'columnfilter_val':column_name_list_object_1,'rowfilter_val':row_name_list_object_1,'calculation_type_name':calculation_type_name,'weight_type_name':weight_type_name,'table_data_type_respone':table_data_type_respone,'seperated_flag_row_2':0,'seperated_flag_col_2':0,'weight_volume_type_name':weight_volume_type_name,'decimal_point_filter':decimal_point_filter,'Total_column_filter':Total_column_filter,'wt_measures':JSON.stringify(wt_measures_2)};

			// respdata4 = autoresponse("crosstab_dash/crosstab_resp", checkData4);		
			respdata4 = autoresponse("crosstab_table", checkData4);	
			//console.log('respdata4 line 66',respdata4);
			$('#table_name').html(respdata4.merge_filename)	
			if (respdata4.status  == 200)
			{
			// display_significant_column_ftr(respdata4['unique_groups_level1_resp']['unique_groups_level1']);
			filters_assign_fun(respdata4['filter_dict_resp']);
			facts_assign_fun(respdata4['dict_selected_measures_lst'],respdata4['dict_selected_measures_filtered_lst'],respdata4['current_time_period_resp'],respdata4['comparative_time_period_resp']);
			facts_range_filter_fun(respdata4['dict_selected_measures_lst']);
			// time_period_filters(respdata4['time_period_vals']);
			Facts_chart(respdata4['dict_selected_measures_lst']);
			Timeperiod_chart(respdata4['time_period_filter_val_resp']['selected_time_period']);
			weighting_filter();
			base_column_filter_refresh(respdata4['all_categories_vals']);
			display_crosstab_table(respdata4,calculation_type_name,respdata4['dict_selected_measures_filtered_lst']);
			display_crosstab_table_xls_download(respdata4,calculation_type_name,respdata4['dict_selected_measures_filtered_lst']);
			// display_facts_colorizer_values();
			$.LoadingOverlay("hide",true);
			// alert('yes crosstab_table');
			}
			else
			{
			alert('no');
			$.LoadingOverlay("hide",true);
			// hidePreloader();//#function modification done by pranit on 25-05-2021
			} 
			
		}, 100);


function base_column_filter_refresh(resp) {
	
	var json_stringify=JSON.stringify(resp);
	$('#base_column_value').empty();
	$("#base_column_value").append(json_stringify);

}
// function filters_assign_fun(filter_dict_resp){
// 	var i=1;
// 	$.each(filter_dict_resp, function (key1, value1) {
//             console.log('filter_dict_resp====','key1===>',key1,'values1===>',value1)
// 		html='';
// 		html +='<div class="col-sm-2">';
// 		html +='<div class="form-group">';
// 		html +='<label for="example-post" data-toggle="tooltip" title='+key1+' class="mr-2 mb-0 text-truncate" style="width: 100%;">'+key1+'</label><br>';
// 		html +='<select id="filter'+i+'" class="w-75" name="multiselect[]" multiple="multiple">';
// 			$.each(value1, function (key2, value2) {
// 		            console.log('filter_dict_resp====','key2===>',key2,'values2===>',value2)
// 		        html +='<option value='+value2+' selected>'+value2+'</option>';         
// 		  });
// 		 html +='</select>';
// 		  html +='</div></div>';

// 		  $('#display_filter_section').append(html);  
		           
 
// 		    i++;     
//   });

//    $("#filter1").multiselect('rebuild');  
//    $("#filter2").multiselect('rebuild');  
//    $("#filter3").multiselect('rebuild');  
//    $("#filter4").multiselect('rebuild');  
//    $("#filter5").multiselect('rebuild');  
// }

function display_significant_column_ftr(resp) {
	// console.log('line 300 display_significant_column_ftr',resp);
	// console.log('string==>150',resp.toString());
	$("#store_unique_column_name").append(resp.toString());
	var selectd_sig_col=$("#significant_base_col").val();
//console.log('selectd_sig_col==>150',selectd_sig_col);
$("#significant_base_col").empty();
	$.each(resp, function (k, value) {

			if (value=='Total') {
					$("#significant_base_col").append('<option selected value="'+value+'" >'+value+'</option>');
				}else{
						$("#significant_base_col").append('<option value="'+value+'" >'+value+'</option>');
				}
       

		  });

			$('#significant_base_col [value="'+selectd_sig_col+'"]').attr('selected', 'true');
		  $("#significant_base_col").multiselect('rebuild');  


}

function weighting_filter(){
			var wt_measures_1 = localStorage.getItem('wt_measures');
			var wt_measures_obj = JSON.parse(wt_measures_1);
			// console.log('wt_measures_obj length',wt_measures_obj.length)
			if (wt_measures_obj.length>0) {
				$("#weighting_filter").show();
				 $.each(wt_measures_obj, function (key2, value2) {

	       	$("#Weighted").append('<option selected  value="'+value2+'" >'+value2+'</option>');

			  });

		     $("#Weighted").multiselect('rebuild');  
		      $("#Weighted").multiselect({
			        includeSelectAllOption: true
			    });
		     $("#Weighted").multiselect('selectAll', true);
			}
      


  
}
function time_period_filters(resp_filter){

		$("#time_period").empty();
 		// var i=
 		// $.each(resp, function (key1, value) {
 		// 		$("#time_period").append('<optgroup label="'+key1+'" id="'+key1.replace(/[^a-zA-Z0-9]/g, '')+'" class="dropmenu">');
		// 	$.each(value, function (key2, value1) {

					
		// 			$("#time_period").append('<option class="dropmenu" value="'+value1+'" >'+value1.replace("QUARTER", "")+'</option>');
					
		// 	});
		// 	$("#time_period").append('</optgroup>');
		// });


		//   $("#time_period").multiselect('rebuild'); 
		//    $("#time_period").multiselect({
        //       includeSelectAllOption: true,
        //       selectAll: true,
        //       search   : true,
        //       enableCaseInsensitiveFiltering: true
		// 	    });


	// new code started

	let newData = [];
 
    if (resp_filter['status'] == 200) {
        const data = resp_filter['current_time_period_resp'];
 
        // Sort the years in descending order and then reverse the quarters, store in array for guaranteed order
        Object.keys(data).sort((a, b) => b - a).forEach(year => {
            newData.push({
                year: year,
                quarters: data[year].slice().reverse()
            });
        });
        // console.log('Reversed and re-ordered data', newData);
 
        // var tp_active = $("#time_period").val();
        // var lastDigits = tp_active.match(/\d{4}$/);
        // var newYear = parseInt(lastDigits[0]) - 1;
        // var newString = tp_active.replace(/\d{4}$/, newYear);
        // console.log('newString------->', newString);
 
        newData.forEach(item => {
            $("#time_period").append('<optgroup label="' + item.year + '" id="' + item.year.replace(/[^a-zA-Z0-9]/g, '') + '" class="dropmenu">');
            item.quarters.forEach(quarter => {
                var quarterDisplay = quarter.replace("QUARTER ", "");
                // var selected = quarterDisplay === newString.replace("QUARTER ", "") ? ' selected' : '';
                selected= '';
                $("#time_period").append('<option style="width: 100px"' + selected + ' value="' + quarter + '">' + quarterDisplay + '</option>');
            });
            $("#time_period").append('</optgroup>');
        });
 
        $("#time_period").multiselect('rebuild');
        $("#time_period").multiselect({
            includeSelectAllOption: true,
            selectAll: true,
            search: true,
            enableCaseInsensitiveFiltering: true
        });
    }
      
}

function comparative_time_period_resp() { 

     var final_row_col_array_grp1 = localStorage.getItem('final_row_col_array_grp');
    var final_row_col_array_grp2 = JSON.parse(final_row_col_array_grp1);
    var filename = Object.keys(final_row_col_array_grp2[0]);
    var current_timeperiod = $("#time_period").val();
    var checkData5 = {
        'csrfmiddlewaretoken': csrfmiddlewaretoken,
        'current_timeperiod': current_timeperiod,
        'filename': filename[0]
    };
    var resp_filter = autoresponse("comparative_time_period_resp", checkData5);
 
    // Assuming `autoresponse` is synchronous and `resp_filter` is immediately available
    let newData = [];
 
    if (resp_filter['status'] == 200) {
        const data = resp_filter['comparative_time_period_resp'];
 
        // Sort the years in descending order and then reverse the quarters, store in array for guaranteed order
        Object.keys(data).sort((a, b) => b - a).forEach(year => {
            newData.push({
                year: year,
                quarters: data[year].slice().reverse()
            });
        });
        // console.log('Reversed and re-ordered data', newData);
 
        var tp_active = $("#time_period").val();
        var lastDigits = tp_active.match(/\d{4}$/);
        var newYear = parseInt(lastDigits[0]) - 1;
        var newString = tp_active.replace(/\d{4}$/, newYear);
        // console.log('newString------->', newString);
 
        newData.forEach(item => {
            $("#comparison_time_period").append('<optgroup label="' + item.year + '" id="' + item.year.replace(/[^a-zA-Z0-9]/g, '') + '" class="dropmenu">');
            item.quarters.forEach(quarter => {
                var quarterDisplay = quarter.replace("QUARTER ", "");
                var selected = quarterDisplay === newString.replace("QUARTER ", "") ? ' selected' : '';
                $("#comparison_time_period").append('<option style="width: 100px"' + selected + ' value="' + quarter + '">' + quarterDisplay + '</option>');
            });
            $("#comparison_time_period").append('</optgroup>');
        });
 
        $("#comparison_time_period").multiselect('rebuild');
        $("#comparison_time_period").multiselect({
            includeSelectAllOption: true,
            selectAll: true,
            search: true,
            enableCaseInsensitiveFiltering: true
        });
    }
 
    var get_val_ctp = $("#comparison_time_period").val();
    $("#store_selected_comparison_time_period_value").html(get_val_ctp);
}







$('#time_range').change(function (e){
	
	// $("#time_period").empty();
	// alert('hii')
    	//  var rowfilter_val=$('#rowfilter').val();
    	$.LoadingOverlay("show");	
        	setTimeout(function () {

			var csrfmiddlewaretoken=csrftoken;
			var final_row_col_array_grp1 = localStorage.getItem('final_row_col_array_grp');
			var final_row_col_array_grp2 = JSON.parse(final_row_col_array_grp1);
        	filename=Object.keys(final_row_col_array_grp2[0]);
        	var time_range=$("#time_range").val();
			// time period filter start
			var checkData5={'csrfmiddlewaretoken': csrfmiddlewaretoken,'filename':filename[0],'time_range':time_range};		
			resp_filter1 = autoresponse("current_time_period_resp", checkData5);
			if (resp_filter1['status']=200) {
				// console.log('resp_filter--->',resp_filter1)
				$("#time_period").empty();
				$("#comparison_time_period").empty();
        		time_period_filters(resp_filter1);
        		comparative_time_period_resp();


				calculation_type_name=$('input[name="calculation_type"]:checked').val();
				weight_type_name=$('input[name="weight_type"]:checked').val();
				Total_column_filter=$('input[name="Total_column"]:checked').val();
				weight_volume_type_name=$('input[name="weight_volume_type"]:checked').val();
				var r_text_val=$('#example2-left').sortableListsToArray()
				var c_text_val=$('#example2-right').sortableListsToArray()
				var rowfilter_sort=exract_one_array_object_by_labels(r_text_val);
				var columnfilter_sort=exract_one_array_object_by_labels(c_text_val);
				filter_data=crosstable_filterdata();
				callback_onchnage(rowfilter_sort,columnfilter_sort,calculation_type_name,weight_type_name,weight_volume_type_name,Total_column_filter,r_text_val,c_text_val,filter_data);
			}
			

			}, 500);
        	$.LoadingOverlay("hide",true);
     

});


$('#time_period').change(function (e){
	
	$("#comparison_time_period").empty();
	// alert('hii')
    	//  var rowfilter_val=$('#rowfilter').val();
    	$.LoadingOverlay("show");	
        	setTimeout(function () {
        		comparative_time_period_resp();
				calculation_type_name=$('input[name="calculation_type"]:checked').val();
				weight_type_name=$('input[name="weight_type"]:checked').val();
				Total_column_filter=$('input[name="Total_column"]:checked').val();
				weight_volume_type_name=$('input[name="weight_volume_type"]:checked').val();
				var r_text_val=$('#example2-left').sortableListsToArray()
				var c_text_val=$('#example2-right').sortableListsToArray()
				var rowfilter_sort=exract_one_array_object_by_labels(r_text_val);
				var columnfilter_sort=exract_one_array_object_by_labels(c_text_val);
				filter_data=crosstable_filterdata();
				callback_onchnage(rowfilter_sort,columnfilter_sort,calculation_type_name,weight_type_name,weight_volume_type_name,Total_column_filter,r_text_val,c_text_val,filter_data);

			}, 500);
        	$.LoadingOverlay("hide",true);
     

});

$('#comparison_time_period').change(function (e){
	
	// alert('yes')
	$.LoadingOverlay("show");
	setTimeout(function () {
		calculation_type_name=$('input[name="calculation_type"]:checked').val();
		weight_type_name=$('input[name="weight_type"]:checked').val();
		Total_column_filter=$('input[name="Total_column"]:checked').val();
		weight_volume_type_name=$('input[name="weight_volume_type"]:checked').val();


		var r_text_val=$('#example2-left').sortableListsToArray()
		var c_text_val=$('#example2-right').sortableListsToArray()
		var rowfilter_sort=exract_one_array_object_by_labels(r_text_val);
		var columnfilter_sort=exract_one_array_object_by_labels(c_text_val);
		filter_data=crosstable_filterdata();


		callback_onchnage(rowfilter_sort,columnfilter_sort,calculation_type_name,weight_type_name,weight_volume_type_name,Total_column_filter,r_text_val,c_text_val,filter_data);

	}, 500);
	$.LoadingOverlay("hide",true);

});


function Timeperiod_chart(resp){
	$('#Timeperiod_chart').empty();
	// console.log('Timeperiod_chart 1000',resp)
		 if (resp.length>0) {

				 $.each(resp, function (key2, value2) {

				 	if (value2=="MAT") {
				 		$("#Timeperiod_chart").append('<option style="width: 100px" selected  value="'+value2+'" >'+value2+'</option>');
				 	}else{
				 		$("#Timeperiod_chart").append('<option  style="width: 100px" value="'+value2+'" >'+value2+'</option>');
				 	}
			  });

		     $("#Timeperiod_chart").multiselect('rebuild');  
		      $("#Timeperiod_chart").multiselect({
              includeSelectAllOption: true,
              selectAll: true,
              search   : true,
              enableCaseInsensitiveFiltering: true,

			    });
		   
		     
			}

}

function Facts_chart(resp){

	var keys=Object.keys(resp);

	 $.each(keys, function (key2, value2) {

	 		$("#Facts_chart").append('<option  style="width: 100px" value="'+value2+'" >'+value2+'</option>');	

  });

   $("#Facts_chart").multiselect('rebuild');  
    $("#Facts_chart").multiselect({
        search   : true,
    });


}

 function facts_assign_fun(resp,selected_resp1,current_time_period_resp,comparative_time_period_resp) {
 	$("#dict_selected_measures_lst").text(JSON.stringify(resp))
 	$("#facts_group_filter").empty();
 	// console.log('facts_assign_fun==328',selected_resp1)
 	var i=
 		$.each(resp, function (key1, value) {
 				$("#facts_group_filter").append('<optgroup label="'+key1+'" id="'+key1.replace(/[^a-zA-Z0-9]/g, '')+'" class="dropmenu">');
			$.each(value, function (key2, value1) {
				// console.log('facts_assign_fun inner==328',selected_resp1[key1])
				const found = selected_resp1[key1].find(element => element === value1);
				// var  {replace_string,original_string} = replace_CY_YA_string(value1,current_time_period_resp,comparative_time_period_resp);
						
					if (found) {
						
						$("#facts_group_filter #"+key1.replace(/[^a-zA-Z0-9]/g, '') ).append('<option selected class="dropmenu" value="'+value1+'" >'+value1.replace("QUARTER", "")+'</option>');
					}
					else{
						$("#facts_group_filter #"+key1.replace(/[^a-zA-Z0-9]/g, '') ).append('<option class="dropmenu" value="'+value1+'" >'+value1.replace("QUARTER", "")+'</option>');
					}
			});
			$("#facts_group_filter").append('</optgroup>');
		});


		  $("#facts_group_filter").multiselect('rebuild'); 
		   $("#facts_group_filter").multiselect({
			        //  enableClickableOptGroups: true,
              // enableCollapsibleOptGroups: true,
              includeSelectAllOption: true,
              selectAll: true,
              search   : true,
              enableCaseInsensitiveFiltering: true,
              // maxHeight: 200,
              // buttonWidth: '100px'
			    });
 }

 function facts_range_filter_fun(resp) {
 	
 	// console.log('facts_range_filter_fun===> 10000',resp)
 	 html='';

	$.each(resp, function (key1, value1) {
		$.each(value1, function (key2, value2) {


			// to check if a string contains any element of an array start
			var factsArr_condition = ['Share', 'Growth', 'Chg'];
			// var myString = "I have an apple and a watermelon.";
			var stringIncludes_found = factsArr_condition.some(check => value2.includes(check));

			// to check if a string contains any element of an array end
			if (stringIncludes_found) {
				var value2_name = value2.split(" ").join("");
				var min=value2_name+'_min';
				var max=value2_name+'_max';
				// console.log('facts_range_filter_fun value1===> 10000',value2)
				html +='<a class="dropdown-item" href="#">';
				html +='<input class="form-check-input" type="checkbox" value="'+value2+'" id='+value2_name+'><b style="font-size:12px">'+value2+'</b><div class="d-flex">';
				html +='<input type="number" class="form-control w-50" id='+min+' aria-describedby="number" placeholder="min" style="height: 30px;">';
				html +='<input type="number" class="form-control mx-1 w-50" id='+max+' aria-describedby="number" placeholder="max" style="height: 30px;"></div></a>';
			}
			
			
		});
	});
	$("#facts_range_filter").append(html);
	
		  
 }



function filters_assign_fun(filter_dict_resp){
	$("#filter1").empty();
	$("#filter2").empty();
	$("#filter3").empty();
	$("#filter4").empty();
	$("#filter5").empty();
	$("#filter_div1").hide();
	$("#filter_div2").hide();
	$("#filter_div3").hide();
	$("#filter_div4").hide();
	$("#filter_div5").hide();

	// console.log('200 filter_dict_resp',filter_dict_resp)

	var i=1;
	$.each(filter_dict_resp, function (key1, value1) {
		  // console.log('filter_dict_resp====','key1===>',key1,'values1===>',value1)
		  // Reordering the array
			var filter_object;
			if (key1=='Category') {
				filter_object = reorderArray(value1);
			}else{
				filter_object=value1;
			}
			
			
			// console.log('filter_dict_resp====','key1===>',reorderedArray)
		  $("#filter_div"+i).show();
		  $(".filter"+i).html(key1);
		  $(".filter"+i).addClass(['label_width','text-truncate']);
		  $(".filter"+i).attr({'data-toggle':'tooltip','title':key1});
		  $("#filter"+i).attr({'data-filtername':key1});
      $.each(filter_object, function (key2, value2) {

       	$("#filter"+i).append('<option selected value="'+value2+'" >'+value2+'</option>');

		  });

		     $("#filter"+i).multiselect('rebuild');  
		      
		     $("#filter"+i).multiselect('selectAll', false); 
		    i++;     
  });
  
}

function append_data_menu_list2(){
	
	var row_name_list_object_1 = localStorage.getItem('row_name_list_object');
	var row_data = JSON.parse(row_name_list_object_1);

	var column_name_list_object_1 = localStorage.getItem('column_name_list_object');
	var column_data = JSON.parse(column_name_list_object_1);

	var remaining_other_list_object_1 = localStorage.getItem('remaining_other_list_object');
	var remaining_other_list = JSON.parse(remaining_other_list_object_1);
	
	// console.log('remaining_other_list',remaining_other_list)
	var ret_data = removeItemOnce(remaining_other_list, 'Time');
	// var listarray=checkDuplicate(remaining_other_list);
	// console.log('ret_data',ret_data)

// var html2='';
// html2+='<li class="list-group-item"><div>Item 11</div></li>';
// html2+='<li class="list-group-item"><div><span class="clickable">Item 5 - clickable text</span></div></li>';
// html2+='<li class="list-group-item"><div>Item 13</div></li>';
// html2+='<li class="list-group-item"><div>Item 14</div></li>';
// $("#example2-left").append(html2);
	$("#example2-left").append(' <li class="list-group-item"  id="item_a" data-module="a" data-value="'+row_data[0]+'"><div>'+row_data[0]+'</div></li>');
	$("#example2-right").append('<li class="list-group-item tinted"  id="item_b" data-module="a" data-value="'+column_data[0]+'"><div>' +column_data[0]+ '</div></li>');
	$.each(remaining_other_list, function (key, val) {
		
		$("#example33").append('<li class="list-group-item tinted"  id="item_c" data-module="a" data-value="'+val+'"><div>' +val+ '</div></li>');
	});


	
	// drag_drop_menu_list();
	// drag_drop_menu_list_method1();



}



function append_data_menu_list(){
	// alert('hlw')


	var row_name_list_object_1 = localStorage.getItem('row_name_list_object');
	var row_data = JSON.parse(row_name_list_object_1);

	var column_name_list_object_1 = localStorage.getItem('column_name_list_object');
	var column_data = JSON.parse(column_name_list_object_1);

	var remaining_other_list_object_1 = localStorage.getItem('remaining_other_list_object');
	var remaining_other_list = JSON.parse(remaining_other_list_object_1);
	 console.log('row_data',row_data)
	 console.log('column_data',column_data)
	// console.log('remaining_other_list',remaining_other_list)
	var ret_data = removeItemOnce(remaining_other_list, 'Time');
	// var listarray=checkDuplicate(remaining_other_list);
	// console.log('ret_data',ret_data)

// var html2='';
// html2+='<li class="list-group-item"><div>Item 11</div></li>';
// html2+='<li class="list-group-item"><div><span class="clickable">Item 5 - clickable text</span></div></li>';
// html2+='<li class="list-group-item"><div>Item 13</div></li>';
// html2+='<li class="list-group-item"><div>Item 14</div></li>';
// $("#example2-left").append(html2);
	$("#example2-left").append(' <li class="list-group-item"  id="item_a" data-module="a" data-value="'+row_data[0]+'"><div>'+row_data[0]+'</div></li>');
	$("#example2-right").append('<li class="list-group-item tinted"  id="item_b" data-module="a" data-value="'+column_data[0]+'"><div>' +column_data[0]+ '</div></li>');
	$.each(remaining_other_list, function (key, val) {
		
		$("#example33").append('<li class="list-group-item tinted"  id="item_c" data-module="a" data-value="'+val+'"><div>' +val+ '</div></li>');
	});


	
	drag_drop_menu_list();
	var other_via_len=$('ul#example33 li').length;
	if (other_via_len==1) {
		$('#other_variable_id').text('Other Variable')
	}else{
		$('#other_variable_id').text('Other Variable(s)')
	}
	// alert(other_via_len)
	// drag_drop_menu_list_method1();


}

function removeItemOnce(arr, value) {
  var index = arr.indexOf(value);
  if (index > -1) {
    arr.splice(index, 1);
  }
  return arr;
}

function drag_drop_menu_list(){

  var options = {
    placeholderCss: {'background-color': '#ff8'},
    hintCss: {'background-color':'#bbf'},
    onChange: function( cEl )
    {
      // console.log( 'onChange 600',cEl );
    },
    complete: function( cEl )
    {
      // console.log( 'complete 600',cEl );
    },
    isAllowed: function( cEl, hint, target )
    {
    	// console.log( 'isAllowed 600',cEl );
      // Be carefull if you test some ul/ol elements here.
      // Sometimes ul/ols are dynamically generated and so they have not some attributes as natural ul/ols.
      // Be careful also if the hint is not visible. It has only display none so it is at the previous place where it was before(excluding first moves before showing).
      if( target.data('module') === 'c' && cEl.data('module') !== 'c' )
      {
        hint.css('background-color', '#ff9999');
        return false;
      }
      else
      {
        hint.css('background-color', '#99ff99');
        return true;
      }
    },
    opener: {
      active: true,
      as: 'html',  // if as is not set plugin uses background image
      close: '<i class="fa fa-minus c3"></i>',  // or 'fa-minus c3'
      open: '<i class="fa fa-plus"></i>',  // or 'fa-plus'
      openerCss: {
        'display': 'inline-block',
        //'width': '18px', 'height': '18px',
        'float': 'left',
        'margin-left': '-35px',
        'margin-right': '5px',
        //'background-position': 'center center', 'background-repeat': 'no-repeat',
        'font-size': '1.1em'
      }
    },
    ignoreClass: 'clickable'
  };

  var optionsPlus = {
    insertZonePlus: true,
    placeholderCss: {'background-color': '#ff8'},
    hintCss: {'background-color':'#bbf'},
    opener: {
      active: true,
      as: 'html',  // if as is not set plugin uses background image
      close: '<i class="fa fa-minus c3"></i>',
      open: '<i class="fa fa-plus"></i>',
      openerCss: {
        'display': 'inline-block',
        'float': 'left',
        'margin-left': '-35px',
        'margin-right': '5px',
        'font-size': '1.1em'
      }
    }
  };

  // $('#sTree2').sortableLists( options );
  // $('#sTreePlus').sortableLists( optionsPlus );
  $('#example2-left').sortableLists( options );
  $('#example2-right').sortableLists( options );
  $('#othersection11').sortableLists( options );
  
 //  $('#row_clear').on( 'click', function(){
 //   console.log( $('#example2-left').sortableListsToArray() ); 
 //  	// alert('ee');
 // } );
  // $('#toArrBtn').on( 'click', function(){ console.log( $('#sTree2').sortableListsToArray() ); } );
  $('#toHierBtn').on( 'click', function() { console.log( $('#sTree2').sortableListsToHierarchy() ); } );
  $('#toStrBtn').on( 'click', function() { console.log( $('#sTree2').sortableListsToString() ); } );
  $('.descPicture').on( 'click', function(e) { $(this).toggleClass('descPictureClose'); } );

	// $('#row_section').on('click', function(e) {
	// 	// alert($(this).attr("data-textval")); 
	// 	var text_val=$(this).attr("data-textval");
	// 	$("#example33").append('<li class="list-group-item tinted wwww"><div>' +text_val+ '<span class="clickable c3" style="float:right"  id="other_section" data-textval="'+text_val+'"><i class="fa fa-trash" aria-hidden="true"></i></span></div></li>');
	// 	$("#example2-left").empty();

	// });

	// $('#col_section').on('click', function(e) {
	// 	var text_val=$(this).attr("data-textval");
	// 	$("#example33").append('<li class="list-group-item tinted wwww"><div>' +text_val+ '</div></li>');
	// 	$("#example2-right").empty();
	// });

  // 	$('.clickable').on('click', function(e) {
	// 	// alert($(this).attr("id")); 
	// 	// alert($(this).closest('ul').attr("id")); 
  // 	var text_val=$(this).attr("data-textval");
	// 	var id_name=$(this).attr("id");
	// 	var closest_id=$(this).closest('ul').attr("id");
	// 	if (id_name=='row_section' || id_name=='col_section') {
	// 		var text_val=$(this).attr("data-textval");

	// 		$("#example33").append('<li class="list-group-item tinted wwww"><div>' +text_val+ '<span class="clickable c3" style="float:right"  id="'+id_name+'" data-textval="'+text_val+'"><i class="fa fa-trash" aria-hidden="true"></i></span></div></li>');
	// 			$(this).closest('li').remove();
	// 		alert(1)
	// 	}else{
	// 		alert(2)
	// 	}

	// });

		

  /* Scrolling anchors */
  $('#toPictureAnch').on( 'mousedown', function( e ) { scrollToAnch( 'pictureAnch' ); return false; } );
  $('#toBaseElementAnch').on( 'mousedown', function( e ) { scrollToAnch( 'baseElementAnch' ); return false; } );
  $('#toBaseElementAnch2').on( 'mousedown', function( e ) { scrollToAnch( 'baseElementAnch' ); return false; } );
  $('#toCssPatternAnch').on( 'mousedown', function( e ) { scrollToAnch( 'cssPatternAnch' ); return false; } );

  function scrollToAnch( id )
  {
    return true;
    $('html, body').animate({
      scrollTop: '-=-' + $("#" + id).offset().top + 'px'
    }, 750);
    return false;
  }

}
$("#row_clear").click(function(q){
 	var text_val=$('#example2-left').sortableListsToArray()
 	$(text_val).each(function(k,v)
	{
		$("#example33").append('<li class="list-group-item tinted"  id="item_a" data-module="a" data-value="'+v['value']+'"><div>' +v['value']+ '</div></li>')
	});
	$("#example2-left").empty();
});
$("#col_clear").click(function(q){
 	var text_val=$('#example2-right').sortableListsToArray()
 	$(text_val).each(function(k,v)
	{
		$("#example33").append('<li class="list-group-item tinted"  id="item_a" data-module="a" data-value="'+v['value']+'"><div>' +v['value']+ '</div></li>')
	});
	$("#example2-right").empty();
});

// $("#pdf_download").click(function(q){
// 		html2canvas($('#crosstab_data')[0], {
//         onrendered: function (canvas) {
//             var data = canvas.toDataURL();
//             var docDefinition = {
//                 content: [{
//                     image: data,
//                     width: 500
//                 }]
//             };
//             pdfMake.createPdf(docDefinition).download("Crosstab_Table.pdf");
//         }
//     });
// });
$("#pdf_download").click(function(q){
	// $('#crosstab_data').addClass('test3').removeClass('hide_class');
	// $('#crosstab_data').find('.hide_class').removeClass("hide_class");
	// $('#crosstab_data').find('.hide_class').addClass('show_class').removeClass('hide_class');
		html2canvas($('#crosstab_data')[0], {
                onrendered: function (canvas) {
                    var data = canvas.toDataURL();
                    // console.log('pdf data 300',data)
                    var docDefinition = {
                        content: [{
                            image: data,
                            width: 500,
                            // height: 700,
                        }]
                    };
                    pdfMake.createPdf(docDefinition).download("Table.pdf");
                }
            });
		// $('#crosstab_data').find('.show_class').addClass('hide_class').removeClass('show_class');
});		
// $("#image_download").click(function(q){
// 		html2canvas($('#crosstab_data')[0], {
//          onrendered: function(canvas) {
//                    img = canvas.toDataURL("image/png");
//                   //console.log('img1',img)
//                   const link = document.createElement("a");
//                   link.href = img;
//                   link.download = 'filename';
//                   link.click();
//                   }
//     });
//   });
$("#image_download").on('click', function () {
		html2canvas(document.getElementById("crosstab_data"),		{
			allowTaint: true,
			useCORS: true
		}).then(function (canvas) {
			var anchorTag = document.createElement("a");
			document.body.appendChild(anchorTag);
			document.getElementById("previewImg").appendChild(canvas);			anchorTag.download = "filename.jpg";
			anchorTag.href = canvas.toDataURL();
			anchorTag.target = '_blank';
			anchorTag.click();
		});
});;


$("#reset_fun").click(function(){
 	// alert('reset_fun');
 	$("#example2-left,#example2-right,#example33").empty();
 	// $("#sTreePlus").empty();
 	// $("#sTreePlus").empty();
 	 append_data_menu_list2()

});

$("#Total_column_disable111").click(function(){
 alert('hello');
});




// $('.Total_column_filter1 input:radio').click(function() {
//     // alert('Hlw')
// 	var text_val=$(this).closest(".tcd").val();

//   });

// $('.calculation_type_filter1 input:radio').click(function() {
//     // alert('Hlw')
// 	var text_val=$(this).closest(".tcd").val();
// 	alert(text_val)

//   });
// $('.weight_type_filter1 input:radio').click(function() {
//     // alert('Hlw')
// 	var text_val=$(this).closest(".tcd").val();
// 	alert(text_val)

//   });

function drag_drop_menu_list_method1(){

	$('.drag').draggable({ 
	  appendTo: 'body',
	  helper: 'clone'
	});

	$('#sTree2').droppable({
	  activeClass: 'active',
	  hoverClass: 'hover',
	  accept: ":not(.ui-sortable-helper)", // Reject clones generated by sortable
	  drop: function (e, ui) {
 
        // var table_name=ui.draggable[0].getAttribute("data-filename");
        // console.log('line no 277 tab_ui==>','tab_ui');
        var $el = $('<li class="drop-item " id="item_b1" data-module="b" data-filename="" data-value="' + ui.draggable.text() + '"><div><span id="clickable">' + ui.draggable.text() + '</span></div></li>');
        // $el.append($('<button type="button" onclick="myFunction()" class="btn btn-default btn-xs remove "><i class="fa fa-minus-square" aria-hidden="true"></i></button>').click(function () { $(this).parent().detach(); }));
        $(this).append($el);
        // console.log('Table section',e);
       
      }
	}).sortable({
	  items: '.drop-item',
	  sort: function() {
	    // gets added unintentionally by droppable interacting with sortable
	    // using connectWithSortable fixes this, but doesn't allow you to customize active/hoverClass options
	    $( this ).removeClass( "active" );
	  }
	});

	$('#sTreePlus').droppable({
	  activeClass: 'active',
	  hoverClass: 'hover',
	  accept: ":not(.ui-sortable-helper)", // Reject clones generated by sortable
	  drop: function (e, ui) {
 
        // var table_name=ui.draggable[0].getAttribute("data-filename");
        // console.log('line no 277 tab_ui==>','tab_ui');
        var $el = $('<li class="drop-item " id="item_b1" data-module="b" data-filename="" data-value="' + ui.draggable.text() + '"><div><span id="clickable">' + ui.draggable.text() + '</span></div></li>');
        // $el.append($('<button type="button" onclick="myFunction()" class="btn btn-default btn-xs remove "><i class="fa fa-minus-square" aria-hidden="true"></i></button>').click(function () { $(this).parent().detach(); }));
        $(this).append($el);
        // console.log('Table section',e);
       
      }
	}).sortable({
	  items: '.drop-item',
	  sort: function() {
	    // gets added unintentionally by droppable interacting with sortable
	    // using connectWithSortable fixes this, but doesn't allow you to customize active/hoverClass options
	    $( this ).removeClass( "active" );
	  }
	});
	
}//end 

function row_and_column_filter(row_data,column_data) {

	// alert('working bhava')
	$("#rowfilter").empty();
	$("#columnfilter").empty();
	$.each(row_data, function (k1, val2) {

		$("#rowfilter").append('<option value="'+val2+'"  selected="">'+val2+'</option>');
	});
	$.each(column_data, function (k1, val2) {
		//console.log('line no 105',val2)
		$("#columnfilter").append('<option value="'+val2+'" selected="">'+val2+'</option>');
	});

	$('#rowfilter').multiselect('rebuild');
	$('#columnfilter').multiselect('rebuild');
	
}


function display_crosstab_table(resp,calculation_type_name,facts_selected_value){

	// facts selected logic
	const fcats_key = Object.keys(facts_selected_value)[0];
	const modified_Fcats_Array = facts_selected_value[fcats_key].map(item => item.replace("QUARTER ", ""));
	const modified_Fcats_Array1 = modified_Fcats_Array.map(item => item.replace(/\s/g, ''));
	// const modified_Fcats_Array = facts_selected_value[fcats_key].map(item => item.replace("QUARTER ", ""));

	// var find_color_code=match_facts_value_return_true_false(modified_Fcats_Array1,'Sales(MJPY)_Q42023',3204.6)

	// console.log('fcats_key main',facts_selected_value)
	// console.log('fcats_key main join',modified_Fcats_Array1)
	// console.log('resp column',resp['df_cross_json']['columns'][0],'type',typeof(resp['df_cross_json']['columns'][0]))

	var decimal_point_filter=$("#decimal_filter").val();
	const groupBy = (x,f)=>x.reduce((a,b,i)=>((a[f(b,i,x)]||=[]).push(b),a),{});

	if (typeof(resp['df_cross_json']['index'][0])==='string') {
		var row_data=string_to_array_convert(resp['df_cross_json']['index']);
	}else{
		var row_data=resp['df_cross_json']['index'];
	}

	if (typeof(resp['df_cross_json']['columns'][0])==='string') {
		var columns_data=string_to_array_convert(resp['df_cross_json']['columns']);
	}else{
		var columns_data=resp['df_cross_json']['columns'];
	}
	percent_sign='%';
	if (calculation_type_name=='actual_count' || calculation_type_name=='Indices') {
		percent_sign='';
	}

	// console.log('columns_data[0]',columns_data)
	// console.log('row_data[0]',row_data)
	var total_row_length=Object.keys(resp['df_cross_json']['index']).length;
	var total_column_length=Object.keys(columns_data[0]).length;
	var single_row_length=Object.keys(row_data[0]).length;
	//console.log('total_column_length',total_column_length)
	//console.log('single_row_length',single_row_length)
	// console.log('columns_data',columns_data)
	var group_column_resp=groupBy(columns_data, v => v[0]);

	var r_text_val=$('#example2-left').sortableListsToArray()
	var rowfilter_sort=exract_one_array_object_by_labels(r_text_val);
	var row_str = rowfilter_sort.toString();
 	row_str = row_str.replaceAll(",", " & ");


 	// get dropdown  range filter value start 
 	var selectedValues = [];
 	// var dropdown_match_index_key=[];

	$('#facts_range_filter').find('a').each(function (index, element) {
	    var checkbox = $(element).find('input[type="checkbox"]');
	    var minValueInput = $(element).find('input[type="number"]').eq(0);
	    var maxValueInput = $(element).find('input[type="number"]').eq(1);

	    if (checkbox.prop('checked')) {
	        var item = {
	            value: checkbox.val(),
	            min: minValueInput.val(),
	            max: maxValueInput.val()
	        };

	        selectedValues.push(item);
	    }
	});

	// console.log('Selected Values 1000:', selectedValues);

 	// get dropdown  range filter value end 

  // console.log('row_str 682==',row_str)
  var copy_variable=total_column_length;
	var html= '';
	var html1= '';
	var html2= '';
	html +='<table class="table table-bordered"  id="crosstab_data">';

	// if (resp['seperated_flag_col']==0) {
	// 	html= header_nested_logic(html,group_column_resp,single_row_length,row_str,columns_data,resp);
	// }else{
	// 	html= header_stacked_logic(html,group_column_resp,single_row_length,row_str,columns_data,resp);
	// }
	
	html= header_stacked_logic(html,group_column_resp,single_row_length,row_str,columns_data,resp);
// header cloumn name end here
	// $("#dropdown_range_filter").html(JSON.stringify(dropdown_match_index_key));
	html +='<tbody>';




	// row each data loop
	var group_row_resp=groupBy(row_data, v => v[0]);
	var group_row_resp_len=Object.keys(group_row_resp).length;
	// row each data loop
	var group_row_resp11=groupBy(row_data, v => v[1]);
  // console.log('group_row_resp11 500==',group_row_resp11)
  html +='</tr>';

  // console.log('total_row_length 100==',total_row_length)
  // console.log('group_row_resp 500==',group_row_resp)
  
  // row each data loop
  const group_row_resp_result = createNestedStructure(row_data);
  const numberOfLevels = getNestedLevels(group_row_resp_result);
  // console.log('group_row_resp_result 500==',group_row_resp_result)
  // console.log('numberOfLevels 500==',numberOfLevels)
  var get_facts_colorizer_object=$("#facts_coorizer_div_array").html();	
  if (get_facts_colorizer_object != "") {
        var facts_coorizer_div_array_1=JSON.parse(get_facts_colorizer_object);
    }
  var counter_i=0;
	$.each(group_row_resp_result, function (row_k, row_val) {
			var row_val_len=Object.keys(group_row_resp[row_k]).length;
			// console.log(' tbody start 500============================================')
			// console.log('row_val_len 500==',row_val_len)
			// console.log('row_k 500==',row_k)
			// console.log('row_val 500==',row_val)
			// console.log('row_val lenght 500==',row_val[0].length)

			
	 	html +='<tr >';


		html +='<th scope="row" class="bg-info L1 row_l1"  rowspan='+row_val_len+'>'+row_k+'</th>';
		
		// for loop code start section 
		// for loop code end section
		
		var ct_1=0;
		$.each(row_val, function (row_k1, row_val1) {
			// console.log('####################### start ##################')
			// console.log('2nd loop 500==row_k1',row_k1,'row_val1--->',row_val1 ,'counter_i',counter_i)
			if (numberOfLevels===1) {
				html +='<th scope="row" class="bg-info L2">'+row_k1+'</th>';

					// if (ct_1===0) {
					// 		counter_i=counter_i;
					// 	}if (counter_i===0) {
					// 		counter_i=ct_1;
					// 	}
					

					$.each(resp['df_cross_json']['data'][counter_i], function (k1, val2) {


						// $.each(resp['df_cross_json']['data'][i], function (k1, val2) {
							// console.log('value  1138===>',val2)
							// console.log('value  1138 type===>',typeof(val2))
							// var val_text= Math.round(val2)
							if (typeof val2 === 'string') {
							    
							    var val_text= val2;
							}else{
								var val_text= val2.toFixed(1);
							}

							
							if (decimal_point_filter>1 && typeof val2 != 'string') {
								// var dec_pt=decimal_point_filter+1;
									// console.log('dec_pt 641',dec_pt)
								 val_text= val2.toFixed(parseInt(decimal_point_filter)+1).slice(0,-1)
							}

							var check_stored_object=$("#dropdown_range_filter").html();
							var check_stored_object_json=JSON.parse(check_stored_object);
							// console.log('check_stored_object-------------->',typeof(check_stored_object_json))
							// adding default color code for GR and BR logic start
								var find_color_code=match_facts_value_return_true_false(modified_Fcats_Array1,resp['df_cross_json']['columns'][k1][2].replace(/\s/g, ''),val_text)
							// adding default color code for GR and BR logic end
							
							if (Object.keys(check_stored_object_json).length !== 0) {

								
			                    // console.log('check_stored_object_json---> 1000',check_stored_object_json)
								var matchingValues1 = getMatchingValues(k1,check_stored_object_json,'','','',1,'');
								// console.log(k1,'1079 matchingValues---> 1000',matchingValues1)
								if (typeof(matchingValues1) !== 'undefined' && matchingValues1 !== null) {
									var get_color=set_color_range_val(val_text,matchingValues1);
									html +='<th scope="row" class="text-right" style="color:'+get_color[1]+';" >'+addThousandSeparators(val_text)+'</th>';
								}
								else{
									html +='<th scope="row" class="text-right" style="color:'+find_color_code[0]+';">'+addThousandSeparators(val_text)+'</th>';
								}

							}
							else{

									html +='<th scope="row" class="text-right" style="color:'+find_color_code[0]+';">'+addThousandSeparators(val_text)+'</th>';
								}
		                    
					
							// html +='<th scope="row" class="text-right" >'+addThousandSeparators(val_text)+'</th>';

						});
					// console.log('####################### END ##################')
					counter_i++;
			}
			if (numberOfLevels===2) {
				var row_val1_count=Object.keys(row_val1).length;
				html +='<th scope="row" class="bg-info" rowspan="'+row_val1_count+'" >'+row_k1+'</th>';

				$.each(row_val1, function (row_k2, row_val2) {

					html +='<th scope="row" class="bg-info L3 row_l3">'+row_k2+'</th>';
					// console.log('start ####################################################')
					// console.log('row_k1==>',row_k1)
					// console.log('Measures==>',row_k2)

					$.each(resp['df_cross_json']['data'][counter_i], function (k1, val2) {

						// $.each(resp['df_cross_json']['data'][i], function (k1, val2) {
							// console.log('value  788===> index',i,'value==>',val2)
							// var val_text= Math.round(val2)
							if (typeof val2 === 'string') {
							    
							    var val_text= val2;
							}else{
								var val_text= val2.toFixed(1);
							}
							if (decimal_point_filter>1  && typeof val2 != 'string') {
								// var dec_pt=decimal_point_filter+1;
									// console.log('dec_pt 641',dec_pt)
								 val_text= val2.toFixed(parseInt(decimal_point_filter)+1).slice(0,-1)
							}
								                   
		                     // console.log('facts_coorizer_div_array_1---> type 1000',typeof(get_facts_colorizer_object))
							// adding default color code for GR and BR logic start
								var find_color_code=match_facts_value_return_true_false(modified_Fcats_Array1,resp['df_cross_json']['index'][counter_i][2].replace(/\s/g, ''),val_text)
							// adding default color code for GR and BR logic end

		                    if (get_facts_colorizer_object != "") {
		                    	console.log('facts_coorizer_div_array_1---> 1000',facts_coorizer_div_array_1)
			                   var matchingValues = getMatchingValues_facts_in_row_level(facts_coorizer_div_array_1,row_k1,row_k2);
			                    console.log('getMatchingValues_facts_in_row_level---> 1000',matchingValues)
			                    if (Object.keys(matchingValues).length !== 0) {
			                    	var get_color=set_color_range_val(val_text,matchingValues);
			                    	html +='<th scope="row" class="text-right" style="color:'+get_color[1]+';">'+addThousandSeparators(val_text)+'</th>';

			                    }else{
									html +='<th scope="row" class="text-right" style="color:'+find_color_code[0]+';">'+addThousandSeparators(val_text)+'</th>';
								}
							
		                	}
		                	else{
									html +='<th scope="row" class="text-right" style="color:'+find_color_code[0]+';" >'+addThousandSeparators(val_text)+'</th>';
								}
					
							
							// html +='<th scope="row" class="text-right" >'+addThousandSeparators(val_text)+'</th>';
						});
					// console.log('end ####################################################')
					counter_i++;

					html +='</tr>';
				});

			}
			
			html +='</tr>';
			html +='</tr>';
			ct_1++;
		});
		html +='</tr>';
	 // console.log(' tbody end============================================')
	 });
	

	// ###########################################################################################
	// ###########################################################################################
	// filter code start

	// filter code end
	// ###########################################################################################
	// ###########################################################################################

	// html +=html2+'</tr>'; 
	html +='</tbody>'; 
	html +='</table>';
	$('#cross_tab_data_table').html(html);
	// $("#facts_coorizer_div_array").empty()
}


function display_crosstab_table_xls_download(resp,calculation_type_name,facts_selected_value){

	// facts selected logic
	const fcats_key = Object.keys(facts_selected_value)[0];
	const modified_Fcats_Array = facts_selected_value[fcats_key].map(item => item.replace("QUARTER ", ""));
	const modified_Fcats_Array1 = modified_Fcats_Array.map(item => item.replace(/\s/g, ''));
	// console.log('display_crosstab_table resp',resp['seperated_flag_col'])
	// console.log('resp column',resp['df_cross_json']['columns'][0],'type',typeof(resp['df_cross_json']['columns'][0]))

	var decimal_point_filter=$("#decimal_filter").val();
	const groupBy = (x,f)=>x.reduce((a,b,i)=>((a[f(b,i,x)]||=[]).push(b),a),{});

	if (typeof(resp['df_cross_json']['index'][0])==='string') {
		var row_data=string_to_array_convert(resp['df_cross_json']['index']);
	}else{
		var row_data=resp['df_cross_json']['index'];
	}

	if (typeof(resp['df_cross_json']['columns'][0])==='string') {
		var columns_data=string_to_array_convert(resp['df_cross_json']['columns']);
	}else{
		var columns_data=resp['df_cross_json']['columns'];
	}
	percent_sign='%';
	if (calculation_type_name=='actual_count' || calculation_type_name=='Indices') {
		percent_sign='';
	}

	// console.log('columns_data[0]',columns_data)
	// console.log('row_data[0]',row_data)
	var total_row_length=Object.keys(resp['df_cross_json']['index']).length;
	var total_column_length=Object.keys(columns_data[0]).length;
	var single_row_length=Object.keys(row_data[0]).length;
	//console.log('total_column_length',total_column_length)
	//console.log('single_row_length',single_row_length)
	// console.log('columns_data',columns_data)
	var group_column_resp=groupBy(columns_data, v => v[0]);

	var r_text_val=$('#example2-left').sortableListsToArray()
	var rowfilter_sort=exract_one_array_object_by_labels(r_text_val);
	var row_str = rowfilter_sort.toString();
 	row_str = row_str.replaceAll(",", " & ");


 	// get dropdown  range filter value start 
 	var selectedValues = [];
 	// var dropdown_match_index_key=[];

	$('#facts_range_filter').find('a').each(function (index, element) {
	    var checkbox = $(element).find('input[type="checkbox"]');
	    var minValueInput = $(element).find('input[type="number"]').eq(0);
	    var maxValueInput = $(element).find('input[type="number"]').eq(1);

	    if (checkbox.prop('checked')) {
	        var item = {
	            value: checkbox.val(),
	            min: minValueInput.val(),
	            max: maxValueInput.val()
	        };

	        selectedValues.push(item);
	    }
	});

	// console.log('Selected Values 1000:', selectedValues);

 	// get dropdown  range filter value end 

  // console.log('row_str 682==',row_str)
  var copy_variable=total_column_length;
	var html= '';
	var html1= '';
	var html2= '';
	html +='<table class="table table-bordered"  id="crosstab_data_xls_download">';

	// if (resp['seperated_flag_col']==0) {
	// 	html= header_nested_logic(html,group_column_resp,single_row_length,row_str,columns_data,resp);
	// }else{
	// 	html= header_stacked_logic(html,group_column_resp,single_row_length,row_str,columns_data,resp);
	// }
	
	html= header_stacked_logic(html,group_column_resp,single_row_length,row_str,columns_data,resp);
// header cloumn name end here
	// $("#dropdown_range_filter").html(JSON.stringify(dropdown_match_index_key));
	html +='<tbody>';




	// row each data loop
	var group_row_resp=groupBy(row_data, v => v[0]);
	var group_row_resp_len=Object.keys(group_row_resp).length;
	// row each data loop
	var group_row_resp11=groupBy(row_data, v => v[1]);
  // console.log('group_row_resp11 500==',group_row_resp11)
  html +='</tr>';

  // console.log('total_row_length 100==',total_row_length)
  // console.log('group_row_resp 500==',group_row_resp)
  
  // row each data loop
  const group_row_resp_result = createNestedStructure(row_data);
  const numberOfLevels = getNestedLevels(group_row_resp_result);
  // console.log('group_row_resp_result 500==',group_row_resp_result)
  // console.log('numberOfLevels 500==',numberOfLevels)
  var get_facts_colorizer_object=$("#facts_coorizer_div_array").html();	
  if (get_facts_colorizer_object != "") {
        var facts_coorizer_div_array_1=JSON.parse(get_facts_colorizer_object);
    }
  var counter_i=0;
	$.each(group_row_resp_result, function (row_k, row_val) {
			var row_val_len=Object.keys(group_row_resp[row_k]).length;
			// console.log(' tbody start 500============================================')
			// console.log('row_val_len 500==',row_val_len)
			// console.log('row_k 500==',row_k)
			// console.log('row_val 500==',row_val)
			// console.log('row_val lenght 500==',row_val[0].length)

			
	 	html +='<tr >';


		html +='<th scope="row" class="bg-info L1"  rowspan='+row_val_len+' style="background-color:#e0e1dd !important">'+row_k+'</th>';
		
		// for loop code start section 
		// for loop code end section
		
		var ct_1=0;
		$.each(row_val, function (row_k1, row_val1) {
			// console.log('####################### start ##################')
			// console.log('2nd loop 500==row_k1',row_k1,'row_val1--->',row_val1 ,'counter_i',counter_i)
			if (numberOfLevels===1) {
				html +='<th scope="row" class="bg-info L2"  style="background-color:#e0e1dd !important">'+row_k1+'</th>';

					// if (ct_1===0) {
					// 		counter_i=counter_i;
					// 	}if (counter_i===0) {
					// 		counter_i=ct_1;
					// 	}
					

					$.each(resp['df_cross_json']['data'][counter_i], function (k1, val2) {


						// $.each(resp['df_cross_json']['data'][i], function (k1, val2) {
							// console.log('value  788===> index',i,'value==>',val2)
							// var val_text= Math.round(val2)
							if (typeof val2 === 'string') {
							    
							    var val_text= val2;
							}else{
								var val_text= val2.toFixed(1);
							}
							
							if (decimal_point_filter>1  && typeof val2 != 'string') {
								// var dec_pt=decimal_point_filter+1;
									// console.log('dec_pt 641',dec_pt)
								 val_text= val2.toFixed(parseInt(decimal_point_filter)+1).slice(0,-1)
							}
							var check_stored_object=$("#dropdown_range_filter").html();
							var check_stored_object_json=JSON.parse(check_stored_object);
							// adding default color code for GR and BR logic start
								var find_color_code=match_facts_value_return_true_false(modified_Fcats_Array1,resp['df_cross_json']['columns'][k1][2].replace(/\s/g, ''),val_text)
							// adding default color code for GR and BR logic end

							// console.log('check_stored_object-------------->',typeof(check_stored_object_json))
							if (Object.keys(check_stored_object_json).length !== 0) {

								
			                    // console.log('check_stored_object_json---> 1000',check_stored_object_json)
								var matchingValues1 = getMatchingValues(k1,check_stored_object_json,'','','',1,'');
								// console.log(k1,'1079 matchingValues---> 1000',matchingValues1)
								if (typeof(matchingValues1) !== 'undefined' && matchingValues1 !== null) {
									var get_color=set_color_range_val(val_text,matchingValues1);
									html +='<th scope="row" class="text-right" style="color:'+get_color[1]+';" >'+addThousandSeparators(val_text)+'</th>';
								}
								else{
									html +='<th scope="row" class="text-right"  style="color:'+find_color_code[0]+';">'+addThousandSeparators(val_text)+'</th>';
								}

							}
							else{
									html +='<th scope="row" class="text-right"  style="color:'+find_color_code[0]+';">'+addThousandSeparators(val_text)+'</th>';
								}
		                    
					
							// html +='<th scope="row" class="text-right" >'+addThousandSeparators(val_text)+'</th>';

						});
					// console.log('####################### END ##################')
					counter_i++;
			}
			if (numberOfLevels===2) {
				var row_val1_count=Object.keys(row_val1).length;
				html +='<th scope="row" class="bg-info " rowspan="'+row_val1_count+'" >'+row_k1+'</th>';

				$.each(row_val1, function (row_k2, row_val2) {

					html +='<th scope="row" class="bg-info L3"  style="background-color:#e0e1dd !important">'+hasMatchingSubstring(row_k2)+'</th>';
					// console.log('start ####################################################')
					// console.log('row_k1==>',row_k1)
					// console.log('Measures==>',row_k2)
					$.each(resp['df_cross_json']['data'][counter_i], function (k1, val2) {

						// $.each(resp['df_cross_json']['data'][i], function (k1, val2) {
							// console.log('value  788===> index',i,'value==>',val2)
							// var val_text= Math.round(val2)
							if (typeof val2 === 'string') {
							    
							    var val_text= val2;
							}
							else{
								var val_text= val2.toFixed(1);
							}
							if (decimal_point_filter>1  && typeof val2 != 'string') {
								// var dec_pt=decimal_point_filter+1;
									// console.log('dec_pt 641',dec_pt)
								 val_text= val2.toFixed(parseInt(decimal_point_filter)+1).slice(0,-1)
							}
							// adding default color code for GR and BR logic start
								var find_color_code=match_facts_value_return_true_false(modified_Fcats_Array1,resp['df_cross_json']['index'][k1][2].replace(/\s/g, ''),val_text)
							// adding default color code for GR and BR logic end
		                     // console.log('facts_coorizer_div_array_1---> type 1000',typeof(get_facts_colorizer_object))
		                    if (get_facts_colorizer_object != "") {
		                    	// console.log('facts_coorizer_div_array_1---> 1000',facts_coorizer_div_array_1)
			                   var matchingValues = getMatchingValues_facts_in_row_level(facts_coorizer_div_array_1,row_k1,row_k2);
			                    // console.log('getMatchingValues_facts_in_row_level---> 1000',matchingValues)
			                    if (Object.keys(matchingValues).length !== 0) {
			                    	var get_color=set_color_range_val(val_text,matchingValues);
			                    	html +='<th scope="row" class="text-right" style="color:'+get_color[1]+';" >'+addThousandSeparators(val_text)+'</th>';

			                    }else{
									html +='<th scope="row" class="text-right" style="color:'+find_color_code[0]+';">'+addThousandSeparators(val_text)+'</th>';
								}
								// var matchingValues1 = getMatchingValues(k1,'',check_stored_object_json,1,'');
								// // console.log(k1,'1079 matchingValues---> 1000',matchingValues1)
								// if (matchingValues1) {
								// 	var get_color=set_color_range_val(val_text,matchingValues1);
								// 	html +='<th scope="row" class="text-right" style="color:'+get_color[1]+'" >'+addThousandSeparators(val_text)+'</th>';
								// }else{
								// 	html +='<th scope="row" class="text-right" >'+addThousandSeparators(val_text)+'</th>';
								// }
		                	}
		                	else{
									html +='<th scope="row" class="text-right" style="color:'+find_color_code[0]+';">'+addThousandSeparators(val_text)+'</th>';
								}
					
							
							// html +='<th scope="row" class="text-right" >'+addThousandSeparators(val_text)+'</th>';
						});
					// console.log('end ####################################################')
					counter_i++;

					html +='</tr>';
				});

			}
			
			html +='</tr>';
			html +='</tr>';
			ct_1++;
		});
		html +='</tr>';
	 // console.log(' tbody end============================================')
	 });
	
	var r_text_val=$('#example2-left').sortableListsToArray()
	var rowfilter_sort=exract_one_array_object_by_labels(r_text_val);
	var row_str = rowfilter_sort.toString();
 	row_str = row_str.replaceAll(",", " & ");

 	var c_text_val=$('#example2-right').sortableListsToArray()
	var columnfilter_sort=exract_one_array_object_by_labels(c_text_val);
	var col_str = columnfilter_sort.toString();
 	col_str = col_str.replaceAll(",", " & ");

 	var time_period_filter=$("#time_period").val();
 	var comparison_time_period=$("#comparison_time_period").val();
 	// console.log('time_period_filter 700',time_period_filter)

 	var other_variableArray = [];
		$('#example33 li').each(function(){
		    other_variableArray.push($(this).attr('data-value'));
		});

// console.log('other_variableArray 700',other_variableArray)
	var final_row_col_array_grp1 = localStorage.getItem('final_row_col_array_grp');
	var final_row_col_array_grp2 = JSON.parse(final_row_col_array_grp1);
	var datbaseName=Object.keys( final_row_col_array_grp2[0])
	var filter_data=crosstable_filterdata();
	var filter_data_text=''
	if (filter_data.length==0) {
		// alert('1')
		 filter_data_text='<th>None</th>';
	}else{
		// alert(2)
		// console.log('filter_data 888',filter_data[0]);
		// console.log('filter_data 888 len',filter_data[0]['Brand'].length);
			$.each(filter_data[0], function (kh11, kv11) {
				// console.log('filter_data 888',kv11);
				var filter_data_len=filter_data[0][kh11].length
				if(filter_data_len<=3){
					var value_filter=filter_data[0][kh11].slice(0, 3);
				}else{
					var value_filter='multiple';
				}
				filter_data_text +='<th style="width: 90px;">'+kh11+' : '+value_filter +'</th>';
		});
	}

// get selected value from facts_group_filter start here
var releasearr = {};
var theSelect = document.getElementById('facts_group_filter');
var optgroups = theSelect.getElementsByTagName('optgroup');
// console.log('optgroups',optgroups.length)
var arr = {};
for (var i = 0; i < optgroups.length; i++) {
    l=optgroups[i].getAttribute('label');
    // console.log('iiiiiiiiiiii',i)
    // console.log('lllllllllllllllll',l)
    releasearr[l] = [];
    arr[l]= [];
    var options = optgroups[i].getElementsByTagName('option');
    // console.log('options',options)
 
    
    for (var j = 0; j < options.length; j++) {
    	// console.log('selected options',options[j].selected)
        releasearr[l].push(options[j].innerHTML);
        if(options[j].selected){
        	// console.log('line 1774',l,'value',options[j].innerHTML)
            
            arr[l].push(options[j].innerHTML);
        }
    }
}
var Facts_keys = Object.keys(arr);
	
	// html +='<tr class="hide_class2"><th></th></tr><tr class="hide_class2"><th></th></tr><tr class="hide_class2"><th></th></tr>';
	// html +='<tr class="hide_class2"><th colspan="0">Database </th><th>'+datbaseName[0]+'</th></tr>';
	// html +='<tr class="hide_class2"><th colspan="0">Other Variable</th><th>'+other_variableArray+'</th></tr>';
	// html +='<tr class="hide_class2"><th colspan="0">Dimensions </th><th>'+row_str+'</th></tr>';
	// html +='<tr class="hide_class2"><th colspan="0">Time Period </th><th>'+time_period_filter+'</th></tr>';
	// html +='<tr class="hide_class2"><th colspan="0">Filter </th>'+filter_data_text+'</tr>';
	// html +='<tr class="hide_class2"><th colspan="0">Facts </th><th>'+Facts_keys+'</th></tr>';



	// html +='<tr class="hide_class2"><th></th></tr><tr class="hide_class2"><th></th></tr><tr class="hide_class2"><th></th></tr>';
	// html +='<tr class="hide_class2" ><th colspan="0" style="background-color:#dee2e6">Name of Database </th><th>'+datbaseName[0]+'</th></tr>';
	// html +='<tr class="hide_class2" ><th colspan="0" style="background-color:#dee2e6">Column </th><th>'+col_str+'</th></tr>';
	// html +='<tr class="hide_class2" ><th colspan="0" style="background-color:#dee2e6">Row </th><th>'+row_str+'</th></tr>';
	// html +='<tr class="hide_class2" ><th colspan="0" style="background-color:#dee2e6">Current Time Period </th><th>'+time_period_filter+'</th></tr>';
	// html +='<tr class="hide_class2" ><th colspan="0" style="background-color:#dee2e6">Comparative Time Period </th><th>'+comparison_time_period+'</th></tr>';
	// html +='<tr class="hide_class2" ><th colspan="0" style="background-color:#dee2e6">Facts </th><th>'+Facts_keys+'</th></tr>';
	// html +='<tr class="hide_class2" ><th colspan="0" style="background-color:#dee2e6">Filter </th>'+filter_data_text+'</tr>';

	






	html +='</tbody>'; 
	html +='</table>';
	 $('#cross_tab_data_table_xls_download').html(html);
}


// Function to check if a given string matches any value in the array

function getMatchingValues2(index,dataArray) {
	

	// console.log('flag 0 condition-->index',index,'factsvalue',factsvalue,'flag',flag)
	for (var i = 0; i < dataArray.length; i++) {
    if ( factsvalue === dataArray[i].factsvalue &&  tpname === dataArray[i].tp_name) {
        return {
            tp_name: dataArray[i].tp_name,
            factsheader: dataArray[i].factsheader,
            factsvalue: dataArray[i].factsvalue,
            input1: dataArray[i].input1,
            input2: dataArray[i].input2
            };
        }
    }
    return null;
	
	
    
}
function set_color_range_val(text_val,matchingValues1) {

	// console.log('set_color_range_val 1590-->',matchingValues1)
	// console.log('set_color_range_val 1590-->',text_val,'min val-->',matchingValues1['input1'],'max--->',matchingValues1['input2'])
	if (parseFloat(text_val) < parseFloat(matchingValues1['input1'])) {
		var bg_color='white';
		var color='red';
	}
	else if (parseFloat(text_val) >= parseFloat(matchingValues1['input2'])) {

		var bg_color='white';
		var color='green';
	}
	else if (parseFloat(text_val) >= parseFloat(matchingValues1['input1']) && parseFloat(text_val) < parseFloat(matchingValues1['input2'])) {

		var bg_color='white';
		var color='#FFBF00';
	}else {

		// var bg_color='white';
		var color='black';
	}

	return [bg_color,color];
}


function sigificant_tail_1(sig_val) {

	var selected_sig_value=$('#significant :selected').val();
	// console.log('sig_val-==>',typeof(sig_val))
		if (sig_val===777) {
		// var bg_color='blue';
		// var color='white';
		var bg_color='white';
		var color='blue';
	}
	else if (sig_val<(-selected_sig_value)) {
		// var bg_color='red';
		// var color='white';
		var bg_color='white';
		var color='red';
	}
	else if ((sig_val > (-selected_sig_value)) && (sig_val < selected_sig_value)) {
		// var bg_color='black';
		// var color='white';
		var bg_color='white';
		var color='black';
	}
	else if (sig_val>selected_sig_value) {
		// var bg_color='green';
		// var color='white';
		var bg_color='white';
		var color='green';
	}
	return [bg_color,color];
}

function sigificant_tail_2(sig_val) {
	var selected_sig_value=$('#significant :selected').val();
	// console.log('sig_val-==>',typeof(sig_val))
	if (sig_val===777) {
		// var bg_color='blue';
		// var color='white';
			var bg_color='white';
		var color='blue';
	}
	else if (sig_val<(-selected_sig_value)) {
		// var bg_color='red';
		// var color='white';
		var bg_color='white';
		var color='red';
	}
	else if ((sig_val > (-selected_sig_value)) && (sig_val < selected_sig_value)) {
		// var bg_color='black';
		// var color='white';
		var bg_color='white';
		var color='black';
	}
	else if (sig_val>selected_sig_value) {
		// var bg_color='green';
		// var color='white';
		var bg_color='white';
		var color='green';
	}
	return [bg_color,color];
}



function column_name_merge_fun(columns_data,index){
	// console.log('column_name_merge_fun',columns_data)
	// console.log('index',index)

	var columns_data_resp=[];
	$.each(columns_data, function (k1, val2) {
			columns_data_resp.push(val2[index])
		});
	const counts = {};
	columns_data_resp.forEach(function (x) { counts[x] = (counts[x] || 0) + 1; });
	// console.log('columns_data_resp',columns_data_resp)
	// console.log('counts',counts)
	return counts;
}

function string_to_array_convert(resp) {
	// console.log('oooooooooooo',resp)
	var array_resp=[];
	$.each(resp, function (k1, val2) {
			array_resp.push([val2])
		});
	return array_resp;
	// console.log('array_resp',array_resp)
}



// $('#rowfilter').change(function (e){
	
//     	 var rowfilter_val=$('#rowfilter').val();
//     	 var columnfilter_val=$('#columnfilter').val();
//       	console.log('rowfilter_val type of',typeof(rowfilter_val))
//       	console.log('rowfilter_val',rowfilter_val)
//       	console.log('rowfilter_val this',$(this).val())
//         setTimeout(function () {
//              callback_onchnage(rowfilter_val,columnfilter_val);
    
     
//         }, 10);

// });

// $('#columnfilter').change(function ()
//     {
//     	 var rowfilter_val=$('#rowfilter').val();
//     	 var columnfilter_val=$('#columnfilter').val();
//       	console.log('columnfilter_val',columnfilter_val)
//       	console.log('rowfilter_sort column chnage',rowfilter_sort)
//         setTimeout(function () {
//              callback_onchnage(rowfilter_val,columnfilter_val);
     
//         }, 10);

// });

var vals = [];
var vals1 = [];
var rowfilter_sort = [];
var columnfilter_sort = [];


$('#rowfilter').change(function (e){
	

   		rowfilter_sort=row_func_sort();
   		calculation_type_name=$('#calculation_type').val();
		weight_type_name=$('#weight_type').val();
		weight_volume_type_name=$('#weight_volume_type').val();
		if (weight_volume_type_name=='' || weight_volume_type_name=== undefined) {
   			// alert('weight_volume_type undefined')
   			weight_volume_type_name="weighting";
   		}
   		// col_len=columnfilter_sort.length;
   		// if (col_len==0) {
   		// 	columnfilter_sort=$('#columnfilter').val();
   		// }
   		columnfilter_sort=$('#columnfilter').val();
   		filter_data=crosstable_filterdata();
   		setTimeout(function () {
             callback_onchnage(rowfilter_sort,columnfilter_sort,calculation_type_name,weight_type_name,weight_volume_type_name,filter_data);
        }, 10);
        // console.log('rowfilter->weight_volume_type==========',weight_volume_type)
   		// console.log('rowfilter_sort row 306',rowfilter_sort)
   		// console.log('rowfilter_sort column 306',columnfilter_sort)

});

$('#columnfilter').change(function (){

		columnfilter_sort=column_func_sort();
		// console.log('columnfilter_sort===',columnfilter_sort)
		calculation_type_name=$('#calculation_type').val();
		weight_type_name=$('#weight_type').val();
		weight_volume_type_name=$('#weight_volume_type').val();
		if (weight_volume_type_name=='' || weight_volume_type_name=== undefined) {
   			// alert('weight_volume_type undefined')
   			weight_volume_type_name="weighting";
   		}
		
   		rowfilter_sort=$('#rowfilter').val();
   		
   		filter_data=crosstable_filterdata();
   		setTimeout(function () {
             callback_onchnage(rowfilter_sort,columnfilter_sort,calculation_type_name,weight_type_name,weight_volume_type_name,filter_data);
        }, 10);
   		// console.log('columnfilter->weight_volume_type==========',weight_volume_type)
   		// console.log('columnfilter_sort column',columnfilter_sort)
   		// console.log('columnfilter_sort row ',rowfilter_sort)

    
});


$('.calculation_type_filter1 input:radio').click(function() {

		$.LoadingOverlay("show");
		calculation_type_name=$('input[name="calculation_type"]:checked').val();
			weight_type_name=$('input[name="weight_type"]:checked').val();
			Total_column_filter=$('input[name="Total_column"]:checked').val();
			weight_volume_type_name=$('input[name="weight_volume_type"]:checked').val();

		// calculation_type_name=$('#calculation_type').val();
		// weight_type_name=$('#weight_type').val();
		// weight_volume_type_name=$('#weight_volume_type').val();
		if (weight_volume_type_name=='' || weight_volume_type_name=== undefined) {
   			// alert('weight_volume_type undefined')
   			weight_volume_type_name="weighting";
   		}
			// console.log('weight_volume_type################',weight_volume_type)
	   	var r_text_val=$('#example2-left').sortableListsToArray()
	 	var c_text_val=$('#example2-right').sortableListsToArray()
	 	var rowfilter_sort=exract_one_array_object_by_labels(r_text_val);
	 	var columnfilter_sort=exract_one_array_object_by_labels(c_text_val);
	 	filter_data=crosstable_filterdata();
	   		// console.log('calculation_type->weight_volume_type==========',weight_volume_type)
	   		setTimeout(function () {
	             callback_onchnage(rowfilter_sort,columnfilter_sort,calculation_type_name,weight_type_name,weight_volume_type_name,Total_column_filter,r_text_val,c_text_val,filter_data);
	             // $.LoadingOverlay("hide",true);
	        }, 300);
	   		$.LoadingOverlay("hide",true);

});

$('.weight_type_filter1 input:radio').click(function() {
	$.LoadingOverlay("show");
		 var i = 1;
		calculation_type_name=$('input[name="calculation_type"]:checked').val();
		weight_type_name=$('input[name="weight_type"]:checked').val();
		Total_column_filter=$('input[name="Total_column"]:checked').val();
		weight_volume_type_name=$('input[name="weight_volume_type"]:checked').val();
		// calculation_type_name=$('#calculation_type').val();
		// weight_type_name=$('#weight_type').val();
		// weight_volume_type_name=$('#weight_volume_type').val();
		var table_data_type_respone = localStorage.getItem('tbl_name');
		table_data_type_respone = table_data_type_respone.replace(/^"(.*)"$/, '$1');
		
		// if (rowfilter_sort.length==0) {
   	// 		rowfilter_sort=$('#rowfilter').val();
   	// 	}
   	// 	if (columnfilter_sort.length==0) {
   	// 		columnfilter_sort=$('#columnfilter').val();
   	// 	}
		var r_text_val=$('#example2-left').sortableListsToArray()
		var c_text_val=$('#example2-right').sortableListsToArray()
		var rowfilter_sort=exract_one_array_object_by_labels(r_text_val);
		var columnfilter_sort=exract_one_array_object_by_labels(c_text_val);
   		// alert(weight_type_name)

   		// adding weight and volumn base filter start here
   		if (weight_type_name=='weighted') {
   			var measure_array=['People','Volume','Occasion']
   			if (table_data_type_respone=="respondent" || table_data_type_respone=="concat") {
				var measure_array=['People']
			}
   			// var measure_array=['People','Volume','Occasion']
   			$('#weight_volume_type').find('option').remove();
			$.each(measure_array, function (kh1, kv1) {

		        $("#weight_volume_type").append('<option value="' + kv1 + '" >' +kv1+ '</option>');
			});
			$('#weight_volume_type option:first').attr('selected', true);

   			// append_weighted_volume_filter();
   			// $('#weight_volume_type_div').show();
   		}else if(weight_type_name=='unweighted'){
   			var measure_array1=['People','Volume','Occasion']
   			if (table_data_type_respone=="respondent" || table_data_type_respone=="concat") {
				var measure_array1=['People']
			}
   			$('#weight_volume_type').find('option').remove();
			$.each(measure_array1, function (kh1, kv1) {

		        $("#weight_volume_type").append('<option value="' + kv1 + '" >' +kv1+ '</option>');
			});
			$('#weight_volume_type option:first').attr('selected', true);
   			// $('#weight_volume_type_div').hide();
   			// $("#weight_volume_type_div").empty();
   		}
   		
   		 $('#weight_volume_type').multiselect('rebuild');
   		

   		
		if (weight_volume_type_name=='' || weight_volume_type_name=== undefined) {
   			// alert('weight_volume_type undefined')
   			weight_volume_type_name="weighting";
   		}
   			filter_data=crosstable_filterdata();
   		// console.log('weight_type->weight_volume_type==========',weight_volume_type_name)
   		// adding weight and volumn base filter end here
   		setTimeout(function () {
             callback_onchnage(rowfilter_sort,columnfilter_sort,calculation_type_name,weight_type_name,weight_volume_type_name,Total_column_filter,r_text_val,c_text_val,filter_data);
        }, 300);

			$.LoadingOverlay("hide",true);
});

$('.weight_volume_type1 input:radio').click(function() {
	$.LoadingOverlay("show");
	// alert('working')
		// calculation_type_name=$('#calculation_type').val();
		// weight_type_name=$('#weight_type').val();
		// weight_volume_type_name=$('#weight_volume_type').val();

		calculation_type_name=$('input[name="calculation_type"]:checked').val();
			weight_type_name=$('input[name="weight_type"]:checked').val();
			Total_column_filter=$('input[name="Total_column"]:checked').val();
			weight_volume_type_name=$('input[name="weight_volume_type"]:checked').val();

		var r_text_val=$('#example2-left').sortableListsToArray()
		var c_text_val=$('#example2-right').sortableListsToArray()
		var rowfilter_sort=exract_one_array_object_by_labels(r_text_val);
		var columnfilter_sort=exract_one_array_object_by_labels(c_text_val);
		filter_data=crosstable_filterdata();
   		// alert(weight_type_name)
   		
   		
   		// console.log('weight_volume_type==========',weight_volume_type)
   		setTimeout(function () {
             callback_onchnage(rowfilter_sort,columnfilter_sort,calculation_type_name,weight_type_name,weight_volume_type_name,Total_column_filter,r_text_val,c_text_val,filter_data);
        }, 300);

   		$.LoadingOverlay("hide",true);
});

$("#clickbtn").click(function(){
	       // alert('hh')
        const toggleButton = document.getElementById("clickbtn");
        const icon = document.getElementById("icon");
        if (icon.classList.contains("fa-level-down")) {
          icon.classList.remove("fa-level-down");
          icon.classList.add("fa-chevron-up");
            $("#clickbtn").attr("title","Time");
           $("#clickbtn").attr("data-original-title","Measure in Row");
           $('#updown_toggle').attr('src', '/static/dist/img/up-chevron.png');
          // changeTextON.classList.add("d-none");
          // changeTextOFF.classList.remove("d-none");
          $("#hiddevalue").empty();
          $("#hiddevalue").text('measure_in_column');
        } else {
          icon.classList.remove("fa-chevron-up");
          icon.classList.add("fa-level-down");
          
           $("#clickbtn").attr("title","Facts");
           $("#clickbtn").attr("data-original-title","Measure in Column");
           $('#updown_toggle').attr('src', '/static/dist/img/down-chevron.png');
          // changeTextON.classList.remove("d-none");
          // changeTextOFF.classList.add("d-none");
          $("#hiddevalue").empty();
          $("#hiddevalue").text('measure_in_row');
        }

        $.LoadingOverlay("show");
		 		setTimeout(function () {
				calculation_type_name=$('input[name="calculation_type"]:checked').val();
				weight_type_name=$('input[name="weight_type"]:checked').val();
				Total_column_filter=$('input[name="Total_column"]:checked').val();
				weight_volume_type_name=$('input[name="weight_volume_type"]:checked').val();


				var r_text_val=$('#example2-left').sortableListsToArray()
				var c_text_val=$('#example2-right').sortableListsToArray()
				var rowfilter_sort=exract_one_array_object_by_labels(r_text_val);
				var columnfilter_sort=exract_one_array_object_by_labels(c_text_val);
				filter_data=crosstable_filterdata();
				

	       callback_onchnage(rowfilter_sort,columnfilter_sort,calculation_type_name,weight_type_name,weight_volume_type_name,Total_column_filter,r_text_val,c_text_val,filter_data);
	       
	       }, 500);
		 		$.LoadingOverlay("hide",true);

	});




$(".plus").click(function(){
		// alert('hh');
		var ct_val=$('.count').val();
				// console.log('plus ct_val be',ct_val)
		$('.count').val(parseInt($('.count').val()) + 1 );
			var counter_val=$("#counter").html(4)
				// console.log('plus ct_val af',ct_val)
		 	$.LoadingOverlay("show");
	 		setTimeout(function () {
			calculation_type_name=$('input[name="calculation_type"]:checked').val();
			weight_type_name=$('input[name="weight_type"]:checked').val();
			Total_column_filter=$('input[name="Total_column"]:checked').val();
			weight_volume_type_name=$('input[name="weight_volume_type"]:checked').val();


			var r_text_val=$('#example2-left').sortableListsToArray()
			var c_text_val=$('#example2-right').sortableListsToArray()
			var rowfilter_sort=exract_one_array_object_by_labels(r_text_val);
			var columnfilter_sort=exract_one_array_object_by_labels(c_text_val);
			filter_data=crosstable_filterdata();
			

       callback_onchnage(rowfilter_sort,columnfilter_sort,calculation_type_name,weight_type_name,weight_volume_type_name,Total_column_filter,r_text_val,c_text_val,filter_data);
       
       }, 500);
	 		$.LoadingOverlay("hide",true);
		   

	});


$(".minus").click(function(){
		// alert('hh');
		$('.count').val(parseInt($('.count').val()) - 1 );
		if ($('.count').val() == 0) {
			$('.count').val(1);
			// var ct_val=$('.count').val();
			// console.log('minus ct_val',ct_val)
		}

		 	$.LoadingOverlay("show");
	 		setTimeout(function () {
			calculation_type_name=$('input[name="calculation_type"]:checked').val();
			weight_type_name=$('input[name="weight_type"]:checked').val();
			Total_column_filter=$('input[name="Total_column"]:checked').val();
			weight_volume_type_name=$('input[name="weight_volume_type"]:checked').val();


			var r_text_val=$('#example2-left').sortableListsToArray()
			var c_text_val=$('#example2-right').sortableListsToArray()
			var rowfilter_sort=exract_one_array_object_by_labels(r_text_val);
			var columnfilter_sort=exract_one_array_object_by_labels(c_text_val);
			filter_data=crosstable_filterdata();
			

       callback_onchnage(rowfilter_sort,columnfilter_sort,calculation_type_name,weight_type_name,weight_volume_type_name,Total_column_filter,r_text_val,c_text_val,filter_data);
       
       }, 500);
	 		$.LoadingOverlay("hide",true);
		   

	});


$('#decimal_filter').change(function (){
// $('#decimal_filter').onChange(function() {
	 	$.LoadingOverlay("show");
	 		setTimeout(function () {
			calculation_type_name=$('input[name="calculation_type"]:checked').val();
			weight_type_name=$('input[name="weight_type"]:checked').val();
			Total_column_filter=$('input[name="Total_column"]:checked').val();
			weight_volume_type_name=$('input[name="weight_volume_type"]:checked').val();


			var r_text_val=$('#example2-left').sortableListsToArray()
			var c_text_val=$('#example2-right').sortableListsToArray()
			var rowfilter_sort=exract_one_array_object_by_labels(r_text_val);
			var columnfilter_sort=exract_one_array_object_by_labels(c_text_val);
			filter_data=crosstable_filterdata();
			

       callback_onchnage(rowfilter_sort,columnfilter_sort,calculation_type_name,weight_type_name,weight_volume_type_name,Total_column_filter,r_text_val,c_text_val,filter_data);
       
       }, 500);
	 		$.LoadingOverlay("hide",true);
});

function numberWithCommas(x) {
    return x.toString().split('.')[0].length > 3 ? x.toString().substring(0,x.toString().split('.')[0].length-3).replace(/\B(?=(\d{2})+(?!\d))/g, ",") + "," + x.toString().substring(x.toString().split('.')[0].length-3): x.toString();
}

function addThousandSeparators(number) {
    const parts = number.toString().split('.');
    const integerPart = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    const decimalPart = parts.length > 1 ? parts[1] : '';
    return decimalPart.length > 0 ? `${integerPart}.${decimalPart}` : integerPart;
}


// $('#Weighted').change(function (){
// // $('#decimal_filter').onChange(function() {
// 	 	$.LoadingOverlay("show");
// 	 		setTimeout(function () {
// 			calculation_type_name=$('input[name="calculation_type"]:checked').val();
// 			weight_type_name=$('input[name="weight_type"]:checked').val();
// 			Total_column_filter=$('input[name="Total_column"]:checked').val();
// 			weight_volume_type_name=$('input[name="weight_volume_type"]:checked').val();


// 			var r_text_val=$('#example2-left').sortableListsToArray()
// 			var c_text_val=$('#example2-right').sortableListsToArray()
// 			var rowfilter_sort=exract_one_array_object_by_labels(r_text_val);
// 			var columnfilter_sort=exract_one_array_object_by_labels(c_text_val);
// 			filter_data=crosstable_filterdata();
			

//        callback_onchnage(rowfilter_sort,columnfilter_sort,calculation_type_name,weight_type_name,weight_volume_type_name,Total_column_filter,r_text_val,c_text_val,filter_data);
       
//        }, 500);
// 	 		$.LoadingOverlay("hide",true);
// });

// $('#filter1,#filter2,#filter3,#filter4,#filter5').change(function (e){
$("#filter_submit").click(function(){
		$.LoadingOverlay("show");
      setTimeout(function () {
		filter_data=crosstable_filterdata();
		var json_stringify=JSON.stringify(filter_data[0]);
		$("#filter_data_object").html(json_stringify);


  var r_text_val=$('#example2-left').sortableListsToArray()
 	var c_text_val=$('#example2-right').sortableListsToArray()
 	var rowfilter_sort=exract_one_array_object_by_labels(r_text_val);
 	var columnfilter_sort=exract_one_array_object_by_labels(c_text_val);


 	if (rowfilter_sort.length==0) {
 		// alert('Please select atleast one variable in row');
 		swal({
                  title: "Opps!",
                  text: "Please select atleast one variable in row!",
                  icon: "warning",
                });
 		return false;
 	}
 	if (columnfilter_sort.length==0) {
 		swal({
                  title: "Opps!",
                  text: "Please select atleast one variable in column!",
                  icon: "warning",
                });
 		return false;
 	}


 	calculation_type_name=$('#calculation_type').val();
	weight_type_name=$('#weight_type').val();
	weight_volume_type_name=$('#weight_volume_type').val();
	Total_column_filter=$('input[name="Total_column"]:checked').val();


             callback_onchnage(rowfilter_sort,columnfilter_sort,calculation_type_name,weight_type_name,weight_volume_type_name,Total_column_filter,r_text_val,c_text_val,filter_data);
             	var get_json_stringify=$("#filter_data_object").text();
      				var json_obj=JSON.parse(get_json_stringify);
      				filter_length=Object.keys(json_obj).length;
      				filter_keys=Object.keys(json_obj);

			      	var q=1;
			      	for (var i = 0; i<=filter_length; i++) {

			      		$("#filter"+q).val(json_obj[filter_keys[i]]);
								$("#filter"+q).multiselect('rebuild');
								q++;
			      	}

        	}, 500);

      $.LoadingOverlay("hide",true);
});


$("#toArrBtn").click(function(){
	var other_via_len=$('ul#example33 li').length;
	if (other_via_len==1) {
		$('#other_variable_id').text('Other Variable')
	}else{
		$('#other_variable_id').text('Other Variable(s)')
	}
	// alert(other_via_len)
 	// alert('Go');
 	$.LoadingOverlay("show");
  setTimeout(function () {
	 	var r_text_val=$('#example2-left').sortableListsToArray()
	 	var c_text_val=$('#example2-right').sortableListsToArray()
	 	var rowfilter_sort=exract_one_array_object_by_labels(r_text_val);
	 	var columnfilter_sort=exract_one_array_object_by_labels(c_text_val);


	 	console.log('r_text_val 800',r_text_val)
	 	console.log('c_text_val 800',c_text_val)



	 	// Calculate the total length of the array
		const totalLength = c_text_val.length;

		// Calculate the count of objects that have a defined 'parentId'
		const countWithParentId = c_text_val.reduce((count, item) => {
		    if ('parentId' in item && item.parentId !== undefined) {
		        return count + 1;
		    }
		    return count;
		}, 0);

		// Output the results
		console.log("Total length of the array:", totalLength); // Output: 3
		console.log("Number of elements with 'parentId':", countWithParentId); // Output: 2


	 	if (rowfilter_sort.length==0) {
	 		// alert('Please select atleast one variable in row');
	 		swal({
                  title: "Opps!",
                  text: "Please select atleast one variable in row!",
                  icon: "warning",
                });
	 		return false;
	 	}
	 	if (columnfilter_sort.length==0) {
	 		swal({
                  title: "Opps!",
                  text: "Please select atleast one variable in column!",
                  icon: "warning",
                });
	 		return false;
	 		
	 	}

	 	if (columnfilter_sort.length>1 && rowfilter_sort.length>1) {
	 		$('.condition_dropdown').hide();
	 	}else{
	 		$('.condition_dropdown').show();
	 	}

	 	calculation_type_name=$('#calculation_type').val();
		weight_type_name=$('#weight_type').val();
		weight_volume_type_name=$('#weight_volume_type').val();
		Total_column_filter=$('input[name="Total_column"]:checked').val();
		// filter_data=crosstable_filterdata();
		filter_data=[];

             callback_onchnage(rowfilter_sort,columnfilter_sort,calculation_type_name,weight_type_name,weight_volume_type_name,Total_column_filter,r_text_val,c_text_val,filter_data);
             // $.LoadingOverlay("hide",true);
        }, 500);
  $.LoadingOverlay("hide",true);

 	$("#store_unique_column_name").empty();

});//end toArrBtn

// $('#Total_column_filter').change(function (){
// 	// alert('working')
// 			calculation_type_name=$('#calculation_type').val();
// 			weight_type_name=$('#weight_type').val();
// 			var r_text_val=$('#example2-left').sortableListsToArray()
// 			var c_text_val=$('#example2-right').sortableListsToArray()
// 			var rowfilter_sort=exract_one_array_object_by_labels(r_text_val);
// 			var columnfilter_sort=exract_one_array_object_by_labels(c_text_val);
   		
//    		weight_volume_type_name=$('#weight_volume_type').val();
//    		console.log('weight_volume_type==========',weight_volume_type)
//    		setTimeout(function () {
//              callback_onchnage(rowfilter_sort,columnfilter_sort,calculation_type_name,weight_type_name,weight_volume_type_name);
//         }, 10);


// });
$('.Total_column_filter1 input:radio').click(function() {
		$.LoadingOverlay("show");
      setTimeout(function () {
					// calculation_type_name=$('#calculation_type').val();
					// $.LoadingOverlay("show");
					calculation_type_name=$('input[name="calculation_type"]:checked').val();
					// weight_type_name=$('#weight_type').val();
					weight_type_name=$('input[name="weight_type"]:checked').val();
					Total_column_filter=$('input[name="Total_column"]:checked').val();
					var r_text_val=$('#example2-left').sortableListsToArray()
					var c_text_val=$('#example2-right').sortableListsToArray()
					var rowfilter_sort=exract_one_array_object_by_labels(r_text_val);
					var columnfilter_sort=exract_one_array_object_by_labels(c_text_val);
		   		// var Total_column_filter=$(this).closest(".tcd").val();
		   		// weight_volume_type_name=$('#weight_volume_type').val();
		   		weight_volume_type_name=$('input[name="weight_volume_type"]:checked').val();
		   		filter_data=crosstable_filterdata();
		   		console.log('Total_column_filter========== 812',Total_column_filter)
		   		console.log('calculation_type_name========== 812',calculation_type_name)
		   		console.log('weight_type_name========== 812',weight_type_name)
		   		console.log('weight_volume_type_name========== 812',weight_volume_type_name)
   	
             callback_onchnage(rowfilter_sort,columnfilter_sort,calculation_type_name,weight_type_name,weight_volume_type_name,Total_column_filter,r_text_val,c_text_val,filter_data);
             // $.LoadingOverlay("hide",true);
        }, 500);

      $.LoadingOverlay("hide",true);
});//end Total_column_filter1

window.exract_one_array_object_by_labels = function(text_val){  
// function exract_one_array_object_by_labels(text_val){
   var array_nodes = [];
   text_val.forEach(function(d) {
                array_nodes.push({
                  value: d.value
                });
    });
   // // From an array of objects, extract value of a property as array
   let array_nodes1 = array_nodes.map(a => a.value);
    // console.log('text_val 758 final',array_nodes1);
   return array_nodes1;
} 


function exract_one_array_object_nested_ct(text_val){
   var array_nodes = [];
   text_val.forEach(function(d) {
   	if (d.parentId===undefined || d.parentId=='' ) {
   		
   	}
   	else{
   			array_nodes.push({
                  parentId: d.parentId
                });
   	}
   	//console.log('line 868',d.parentId)
                
    });
   // // From an array of objects, extract value of a property as array
   let array_nodes1 = array_nodes.map(a => a.parentId);
   return array_nodes1;
}
// $('#toArrBtn').change(function (){
// 	alert('Go')
	// exract_one_array_object_by_labels();
		// calculation_type_name=$('#calculation_type').val();
		// weight_type_name=$('#weight_type').val();
		// // if (rowfilter_sort.length==0) {
   		// 	rowfilter_sort=$('#rowfilter').val();
   		// // }
   		// // if (columnfilter_sort.length==0) {
   		// 	columnfilter_sort=$('#columnfilter').val();
   		// // }
   		// // alert(weight_type_name)
   		
   		// weight_volume_type_name=$('#weight_volume_type').val();
   		// console.log('weight_volume_type==========',weight_volume_type)
   		// setTimeout(function () {
        //      callback_onchnage(rowfilter_sort,columnfilter_sort,calculation_type_name,weight_type_name,weight_volume_type_name);
        // }, 10);


// });

$('#toggle-event').change(function (){
	$.LoadingOverlay("show");
  // setTimeout(function () {
			var toggle_value=$(this).prop('checked');
			var row_object=[];
			var col_object=[];
			// alert(toggle_value)
			// calculation_type_name=$('#calculation_type').val();
			// 	weight_type_name=$('#weight_type').val();
			// 	weight_volume_type_name=$('#weight_volume_type').val();
				calculation_type_name=$('input[name="calculation_type"]:checked').val();
				weight_type_name=$('input[name="weight_type"]:checked').val();
				Total_column_filter=$('input[name="Total_column"]:checked').val();
				weight_volume_type_name=$('input[name="weight_volume_type"]:checked').val();
				var r_text_val=$('#example2-left').sortableListsToArray()
				var c_text_val=$('#example2-right').sortableListsToArray()
				var rowfilter_sort=exract_one_array_object_by_labels(r_text_val);
				var columnfilter_sort=exract_one_array_object_by_labels(c_text_val);
				// if (rowfilter_sort.length==0) {
		   	// 		rowfilter_sort=$('#rowfilter').val();
		   	// 	}
		   	// 	if (columnfilter_sort.length==0) {
		   	// 		columnfilter_sort=$('#columnfilter').val();
		   	// 	}

				// $("#rowfilter option").each(function(){
				//     var r=$(this).val();
				//     row_object.push(r)
				// });
				// $("#columnfilter option").each(function(){
				//     var r=$(this).val();
				//     col_object.push(r)
				// });

		   		
		   		// console.log('row_object 444',row_object)
		   		// console.log('rowfilter_sort line no 480 old',rowfilter_sort)
		   		// console.log('columnfilter_sort line no 481 old',columnfilter_sort)
		filter_data=crosstable_filterdata();
   		if(toggle_value==true) {
   			setTimeout(function () {
	             callback_onchnage(columnfilter_sort,rowfilter_sort,calculation_type_name,weight_type_name,weight_volume_type_name,Total_column_filter,r_text_val,c_text_val,filter_data);
	        }, 500);
   			// alert('on')
   			// rowfilter_sort=columnfilter_sort;
   			
   		}
   		else if(toggle_value==false){
   			// columnfilter_sort=rowfilter_sort
   			// alert('off')
   			setTimeout(function () {
	             callback_onchnage(rowfilter_sort,columnfilter_sort,calculation_type_name,weight_type_name,weight_volume_type_name,Total_column_filter,r_text_val,c_text_val,filter_data);
	        }, 500);
   		}
 
		// rowfilter_sort1=$('#rowfilter').val();
		// columnfilter_sort1=$('#columnfilter').val();
   		
   	// 	console.log('rowfilter_sort line no 495 new filter',rowfilter_sort1)
   	// 	console.log('columnfilter_sort line no 496 new filter',columnfilter_sort1)
   		filter_data=crosstable_filterdata();
   		setTimeout(function () {
	             callback_onchnage(columnfilter_sort,rowfilter_sort,calculation_type_name,weight_type_name,weight_volume_type_name,Total_column_filter,r_text_val,c_text_val,filter_data);
	             // $.LoadingOverlay("hide",true);
	        }, 500);
   		
   		// console.log('weight_volume_type==========',weight_volume_type)
   		$.LoadingOverlay("hide",true);

});




function append_weighted_volume_filter() {
	// alert('yes')
	var html='';
	html +='<div class="form-inline">';
	html +='<label for="example-post" class="mr-2">Weight/Volume</label>';
	html +='<select id="weight_volume_type">';
	html +='<option value="weighting" selected>Weighted</option>';
	html +='<option value="Volume" >Volume</option>';
	html +='</select>';
	html +='</div>';
	$('#weight_volume_type_div').html(html);
	$('#weight_volume_type').multiselect('rebuild');
}




function row_func_sort() {
	for(var i=0; i <$('#rowfilter option').length; i++) {
	      if ($($('#rowfilter option')[i]).prop('selected') ) {
	        if (!vals.includes(i)) {
	          vals.push(i);
	        }
	      } else {
	        if (vals.includes(i)) {
	          vals.splice(vals.indexOf(i), 1);
	        }
	      }
	    }
	    var order = '';
	    vals.forEach(function(ele) {
	      order += $($('#rowfilter option')[ele]).val() + ',';
	    })
	    order = order.replace(/,\s*$/, "");
	    var rowfilter_sort1 = order.split(",");
	    // console.log('order',array);
	    return rowfilter_sort1;
}

function column_func_sort() {
	for(var i=0; i <$('#columnfilter option').length; i++) {
	      if ($($('#columnfilter option')[i]).prop('selected') ) {
	        if (!vals1.includes(i)) {
	          vals1.push(i);
	        }
	      } else {
	        if (vals1.includes(i)) {
	          vals1.splice(vals1.indexOf(i), 1);
	        }
	      }
	    }
	    var order1 = '';
	    vals1.forEach(function(ele) {
	      order1 += $($('#columnfilter option')[ele]).val() + ',';
	    })
	    order1 = order1.replace(/,\s*$/, "");
	    var columnfilter_sort1 = order1.split(",");
	    // console.log('order',array);
	    return columnfilter_sort1;
}


$('#significant').change(function (){
	$("#significant_flag").val(1)
	 	$.LoadingOverlay("show");
	 		setTimeout(function () {
			calculation_type_name=$('input[name="calculation_type"]:checked').val();
			weight_type_name=$('input[name="weight_type"]:checked').val();
			Total_column_filter=$('input[name="Total_column"]:checked').val();
			weight_volume_type_name=$('input[name="weight_volume_type"]:checked').val();


			var r_text_val=$('#example2-left').sortableListsToArray()
			var c_text_val=$('#example2-right').sortableListsToArray()
			var rowfilter_sort=exract_one_array_object_by_labels(r_text_val);
			var columnfilter_sort=exract_one_array_object_by_labels(c_text_val);
			filter_data=crosstable_filterdata();
			

       callback_onchnage(rowfilter_sort,columnfilter_sort,calculation_type_name,weight_type_name,weight_volume_type_name,Total_column_filter,r_text_val,c_text_val,filter_data);
       	$("#significant_flag").val(0)
       }, 500);
	 		$.LoadingOverlay("hide",true);
	 	
});

$('#significant_base_col').change(function (){
	$("#significant_flag").val(1)

		// var base_column=$('#significant_base_col :selected').val();
		// var base_column="Total";
		// console.log('base_column==>1400',base_column)
	 	$.LoadingOverlay("show");
	 		setTimeout(function () {
			calculation_type_name=$('input[name="calculation_type"]:checked').val();
			weight_type_name=$('input[name="weight_type"]:checked').val();
			Total_column_filter=$('input[name="Total_column"]:checked').val();
			weight_volume_type_name=$('input[name="weight_volume_type"]:checked').val();


			var r_text_val=$('#example2-left').sortableListsToArray()
			var c_text_val=$('#example2-right').sortableListsToArray()
			var rowfilter_sort=exract_one_array_object_by_labels(r_text_val);
			var columnfilter_sort=exract_one_array_object_by_labels(c_text_val);
			filter_data=crosstable_filterdata();

			if(c_text_val.length==1){
				var get_current_column_text=c_text_val[0]['value'];
				$("#base_column_varible_selected").html(get_current_column_text);
			}



			// console.log('c_text_val 700',c_text_val);
			// console.log('c_text_val 700',c_text_val[0]['value']);
			

       callback_onchnage(rowfilter_sort,columnfilter_sort,calculation_type_name,weight_type_name,weight_volume_type_name,Total_column_filter,r_text_val,c_text_val,filter_data);
       	$("#significant_flag").val(0)
       }, 500);
	 		$.LoadingOverlay("hide",true);
	 	
});
// This function is global variable 
 window.callback_onchnage = function(rowfilter_val,columnfilter_val,calculation_type_name,weight_type_name,weight_volume_type_name,Total_column_filter,r_text_val,c_text_val,filter_data){  
// function callback_onchnage(rowfilter_val,columnfilter_val,calculation_type_name,weight_type_name,weight_volume_type_name,Total_column_filter,r_text_val,c_text_val,filter_data) {
	
	// console.log('1400 rowfilter_val===',rowfilter_val)
	// console.log('1400 columnfilter_val===',columnfilter_val)
	// console.log('1400 calculation_type_name===',calculation_type_name)

	var tbl_name = localStorage.getItem('tbl_name');

	// var seperated_flag_row_1 = localStorage.getItem('seperated_flag_row');
	// var seperated_flag_row_2 = JSON.parse(seperated_flag_row_1);
	// var final_row_col_array_grp=0;

	var final_row_col_array_grp1 = localStorage.getItem('final_row_col_array_grp');
	var final_row_col_array_grp2 = JSON.parse(final_row_col_array_grp1);


	// var seperated_flag_col_1 = localStorage.getItem('seperated_flag_col');
	// var seperated_flag_col_2 = JSON.parse(seperated_flag_col_1);

	var toggle_value=$("#toggle-event").prop('checked');
	// alert(toggle_value)
	

		var get_parent_nested_ct_row=exract_one_array_object_nested_ct(r_text_val);
 		var get_parent_nested_ct_col=exract_one_array_object_nested_ct(c_text_val);
 		// console.log('get_parent_nested_ct_col line 1057',get_parent_nested_ct_col)
 		// console.log('columnfilter_val line 1057',columnfilter_val.length)
 		// console.log('condition 1 line 1057',get_parent_nested_ct_col.length)
 		// console.log('condition 2 line 1057',(columnfilter_val.length-1))
 		if (rowfilter_val.length==1) {
 			var seperated_flag_row_2=1;
 		}
 		else if (rowfilter_val.length>1 && get_parent_nested_ct_row.length==1) {
 			var seperated_flag_row_2=0;
 		}else{
 			var seperated_flag_row_2=1;
 		}

 		if (columnfilter_val.length==1) {
 			var seperated_flag_col_2=1;
 			//console.log('if seperated_flag_col_2',seperated_flag_col_2)
 		}
 		else if (columnfilter_val.length>1 && get_parent_nested_ct_col.length>=1) {
 			var seperated_flag_col_2=0;
 			//console.log('if seperated_flag_col_2',seperated_flag_col_2)
 		}else{
 			var seperated_flag_col_2=1;
 			//console.log('else seperated_flag_col_2',seperated_flag_col_2)
 		}
 		// console.log('rowfilter_val.length 4444',rowfilter_val.length);
 		// console.log('columnfilter_val.length 4444',columnfilter_val.length);
 		$("#chart_div").hide();
 		if (columnfilter_val.length==1 && rowfilter_val.length==1 ) {
				// $(".significant_div").show();
				$("#chart_div").show();
		}

		$(".significant_div").hide();
		$(".base_column_div").hide();
		if (columnfilter_val.length==1 && rowfilter_val.length==1 && calculation_type_name=='Significance') {
				$(".significant_div").show();
				$(".base_column_div").show();
		}
		if (columnfilter_val.length==1 && rowfilter_val.length==1 && calculation_type_name=='Indices') {
				$(".base_column_div").show();
		}
		var row_flag=0
		var column_flag=0

		// toggle-event function start here
		if(toggle_value==true) {
   			var seperated_flag_row_2=seperated_flag_col_2
   			var seperated_flag_col_2=seperated_flag_row_2
   		}
   		else if(toggle_value==false){
   			var seperated_flag_row_2=seperated_flag_row_2
   			var seperated_flag_col_2=seperated_flag_col_2
   		}
   		//console.log('toggle_value line 589',toggle_value)
   		//console.log('seperated_flag_col_2 line 1074',seperated_flag_col_2)
   		//console.log('seperated_flag_row_2 1074',seperated_flag_row_2)
	// toggle-event function end here

	table_name=$('#table_name').text();
	// table_name=$('#table_name').text();
	//console.log(' table_name line 466',table_name)
	var table_data_type_respone = localStorage.getItem('tbl_name');
	// var decimal_point_filter=5
	var decimal_point_filter=$('#decimal_filter').val();
	// var decimal_point_filter=$('#decimal_filter_new').val();
	// console.log('decimal_point_filter',decimal_point_filter)
	// Total_column_filter=$('#Total_column_filter').val();

	calculation_type_name=$('input[name="calculation_type"]:checked').val();
	weight_type_name=$('input[name="weight_type"]:checked').val();
	Total_column_filter=$('input[name="Total_column"]:checked').val();
	weight_volume_type_name=$('input[name="weight_volume_type"]:checked').val();

	var wt_measures=$('#Weighted').val();
	var time_val=$('#time_period').val();
	var measure_type=$('#hiddevalue').text();
	// alert(measure_time_toggle)

	
	if (calculation_type_name==undefined || calculation_type_name== null) {
		calculation_type_name='column_percent';
		// $("input:radio[name=calculation_type][disabled=false]:first").attr('checked', true);
		$("input[id='calculation_type1']:checked").prop("checked", true);
			$("#calculation_type1").attr( 'checked', true )
	}
	var get_base_column_variable=$("#base_column_varible_selected").text();

	// && (calculation_type_name=='Significance' || calculation_type_name=='Indices')
	if ((columnfilter_val.length==1) && (calculation_type_name=='Significance' || calculation_type_name=='Indices') && (get_base_column_variable!=columnfilter_val[0])) {
		// console.log('columnfilter_val 500',columnfilter_val);
		var json_stringify = $('#base_column_value').text();
		var json_obj=JSON.parse(json_stringify);
		// console.log('base_column_value 500',json_obj);

		// filtering array data to get selected column name start here
		const filtered_base_column = Object.keys(json_obj)
    .filter(key => columnfilter_val.includes(key))
    .reduce((obj, key) => {
        obj[key] = json_obj[key];
        return obj;
  	}, {});
  	// filtering array data to get selected column name end here
    $("#significant_base_col").find('option').remove();
    $("#significant_base_col").multiselect('rebuild');  
		// console.log('filtered_base_column',filtered_base_column);

		$.each(filtered_base_column[columnfilter_val[0]], function (k, value) {

				if (value=='Total') {
					$("#significant_base_col").append('<option selected value="'+value+'" >'+value+'</option>');
				}else{
						$("#significant_base_col").append('<option value="'+value+'" >'+value+'</option>');
				}
		  });
		$("#significant_base_col").multiselect('rebuild');  

	}


	if ((columnfilter_val.length>1 || rowfilter_val.length>1) && (calculation_type_name=='Significance' || calculation_type_name=='Indices')) {
			calculation_type_name='column_percent';
			swal({
				  text: "Please select one Row and one Column for Indices and Significance!",
				  icon: "warning",
				  // buttons: true,
				  dangerMode: true,
				});
				$("input[id='calculation_type5']:checked").prop("checked", false);
				$("#calculation_type1").attr( 'checked', true )
				// $("input:radio[name=calculation_type][disabled=false]:first").attr('checked', true);
			// $('input:radio[name="calculation_type"]').attr('checked', 'checked');

	}

	get_significat_flag=$("#significant_flag").val();
		var base_column=$("#significant_base_col").val();
	if (base_column === undefined || base_column === null) { 
		var base_column='Total';
	 }
		else{
			var base_column=$("#significant_base_col").val();
	}


// ============================================================================

var getSelectedValues_facts = getSelectedValues_facts_filter();
var getSelectedValues_facts_all = getSelectedIndex_facts_filter_all();
// console.log('getSelectedValues_facts_filter',getSelectedValues_facts_filter);

	// var releasearr = {};
	// var theSelect = document.getElementById('facts_group_filter');
	// var optgroups = theSelect.getElementsByTagName('optgroup');
	// // console.log('optgroups',optgroups.length)
	// var arr = {};
	// for (var i = 0; i < optgroups.length; i++) {
	// l=optgroups[i].getAttribute('label');
	// // console.log('iiiiiiiiiiii',i)
	// // console.log('lllllllllllllllll',l)
	// releasearr[l] = [];
	// arr[l]= [];
	// var options = optgroups[i].getElementsByTagName('option');
	// // console.log('options',options)


	// for (var j = 0; j < options.length; j++) {
	// 	// console.log('selected options',options[j].selected)
	//     releasearr[l].push(options[j].innerHTML);
	//     if(options[j].selected){
	//     	// console.log('line 1774',l,'value',options[j].innerHTML)
	        
	//         arr[l].push(options[j].innerHTML);
	//     }
	// }
	// }
	// console.log('line 2740 arr',arr)
	// ============================================================================
	
	var filter_data_new=JSON.stringify(filter_data);
	filter_data_new = filter_data_new.replace(/'/g, "\\'");
	// console.log('filter_data_new1 ',filter_data_new);
	// console.log('filter_data_new 2189 encode',encodeURIComponent(filter_data_new));
	var comparative_time_period=$("#comparison_time_period").val();

	

		// var checkData4 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken+"&rowfilter_val=" + rowfilter_val+"&columnfilter_val=" + columnfilter_val+"&calculation_type_name=" + calculation_type_name+"&weight_type_name=" + weight_type_name+"&tbl_name=" + tbl_name+"&seperated_flag_row_2=" + seperated_flag_row_2+"&seperated_flag_col_2=" + seperated_flag_col_2+"&weight_volume_type_name=" + weight_volume_type_name+"&final_row_col_array_grp=" + JSON.stringify(final_row_col_array_grp2)+"&filename_merged=" + table_name+"&table_data_type_respone=" + table_data_type_respone+"&decimal_point_filter=" + parseInt(decimal_point_filter)+"&Total_column_filter=" + Total_column_filter+"&filter_data='" + filter_data_new+"'&base_column=" + base_column+"&wt_measures=" + JSON.stringify(wt_measures)+"&Time_val=" + time_val+"&measure_time_toggle=" + measure_time_toggle+"&facts_object=" + JSON.stringify(arr);



	var checkData4 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken+"&rowfilter_val=" + rowfilter_val+"&columnfilter_val=" + columnfilter_val+"&calculation_type_name=" + calculation_type_name+"&weight_type_name=" + weight_type_name+"&tbl_name=" + tbl_name+"&seperated_flag_row_2=" + seperated_flag_row_2+"&seperated_flag_col_2=" + seperated_flag_col_2+"&weight_volume_type_name=" + weight_volume_type_name+"&final_row_col_array_grp=" + JSON.stringify(final_row_col_array_grp2)+"&filename_merged=" + table_name+"&table_data_type_respone=" + table_data_type_respone+"&decimal_point_filter=" + parseInt(decimal_point_filter)+"&Total_column_filter=" + Total_column_filter+"&filter_data='" + encodeURIComponent(filter_data_new)+"'&base_column=" + base_column+"&wt_measures=" + JSON.stringify(wt_measures)+"&Time_val=" + time_val+"&measure_type=" + measure_type+"&facts_object=" + JSON.stringify(getSelectedValues_facts)+"&facts_object_index=" + JSON.stringify(getSelectedValues_facts_all)+"&comparative_time_period=" + comparative_time_period;

	
		respdata4 = autoresponse("crosstab_table_page2", checkData4);


				if (respdata4.status  == 200)
					{
						// console.log('respdata4',respdata4);
						// console.log('respdata4',typeof(respdata4['base_column_names_resp']));
						// console.log('respdata4',respdata4['base_column_names_resp']['type']);
						if (respdata4['base_column_names_resp']['type']=='Significance') {
								$(".significant_div").show();
								$(".base_column_div").show();
								display_significant_column_ftr(respdata4['base_column_names_resp']['base_column_names_resp']);

						}
						if (respdata4['base_column_names_resp']['type']=='Indices') {
								$(".significant_div").hide();
								$(".base_column_div").show();
								display_significant_column_ftr(respdata4['base_column_names_resp']['base_column_names_resp']);
						}
					display_crosstab_table(respdata4,calculation_type_name,respdata4['dict_selected_measures_filtered_lst']);
					display_crosstab_table_xls_download(respdata4,calculation_type_name,respdata4['dict_selected_measures_filtered_lst']);
					
					// filters_assign_fun();
					// filters_assign_fun(respdata4['filter_dict_resp']);
					Timeperiod_chart(respdata4['time_period_filter_val_resp']['selected_time_period']);
					facts_assign_fun(respdata4['dict_selected_measures_lst'],respdata4['dict_selected_measures_filtered_lst'],respdata4['current_time_period_resp'],respdata4['comparative_time_period_resp']);
					// display_significant_column_ftr(respdata4['unique_groups_level1_resp']['unique_groups_level1']);
					// alert('yes crosstab_table');
					}
					else
					{
						swal({
				              title: "Opps!",
				              text: "No Data is Available for this Filter combination!",
				              icon: "warning",
				          });
				      return false;
					// hidePreloader();
					}


	// console.log('respdata4 line 461',respdata4)		


	$.LoadingOverlay("hide",true); 
}



});// document closed


function submit_colorizer_data() {
	// alert('hi')
	$.LoadingOverlay("show");
	var data=[];

	// find card class name start here
	const element = document.getElementById("accordion_facts_colorizer1");
	const nodes = element.getElementsByClassName("card");
	let card_len = nodes.length;
	// console.log('number--->',card_len)

	// alert('hiii')
	for (var i =0; i<card_len; i++) {
		
	
		$("#collapse"+i+" .card-body .d-flex").each(function(e){

			var htmlString=$(this).html();
			var tempDiv = $('<div>').html(htmlString);
			var factsheader = tempDiv.find('input').data('factsheader');
			var tp_name = tempDiv.find('input').data('tp_name');
			var inputId = tempDiv.find('input[type="checkbox"]').attr('id');

			// console.log('inputId--->',card_len)
			var check_selected=$("#" + inputId).is(":checked");
			var factsvalue=$(this).text();
			// Find the index of the second underscore
			var secondUnderscoreIndex = inputId.indexOf('_', inputId.indexOf('_'));
			// Extract the substring starting from the character after the second underscore
			var resultString = inputId.substring(secondUnderscoreIndex + 1);
			var input1=$("#c1_" + resultString).val();
			var input2=$("#c2_" + resultString).val();
			var input1_ck = (input1=="") ? '0' : input1 ;
			var input2_ck = (input2=="") ? '0' : input2 ;
			// console.log('factsheader--->',factsheader)
			// console.log('isChecked--->',inputId)
			// console.log('resultString--->',resultString)
			

			if (check_selected==true || check_selected=='true') {
			  
			   data.push({['id']: inputId,['tp_name']:tp_name,['factsheader']:factsheader,['factsvalue']:factsvalue,['input1']:input1_ck,['input2']:input2_ck});
			  // console.log('True checked checkbox found.');
			}



		});//each loop closed here
	}//for loop closed here	
	$("#facts_coorizer_div_array").empty();
	$("#facts_coorizer_div_array").html(JSON.stringify(data))
	// console.log('final data',data);

// ========================================================================================================================
// ========================================================================================================================
	// common code start here

	   setTimeout(function () {
		filter_data=crosstable_filterdata();
		var json_stringify=JSON.stringify(filter_data[0]);
		$("#filter_data_object").html(json_stringify);


	  	var r_text_val=$('#example2-left').sortableListsToArray()
	 	var c_text_val=$('#example2-right').sortableListsToArray()
	 	var rowfilter_sort=exract_one_array_object_by_labels(r_text_val);
	 	var columnfilter_sort=exract_one_array_object_by_labels(c_text_val);


	 	if (rowfilter_sort.length==0) {
	 		alert('Please select atleast one variable in row');
	 		return false;
	 	}
	 	if (columnfilter_sort.length==0) {
	 		alert('Please select atleast one variable in column');
	 		return false;
	 	}


	 	calculation_type_name=$('#calculation_type').val();
		weight_type_name=$('#weight_type').val();
		weight_volume_type_name=$('#weight_volume_type').val();
		Total_column_filter=$('input[name="Total_column"]:checked').val();


         callback_onchnage(rowfilter_sort,columnfilter_sort,calculation_type_name,weight_type_name,weight_volume_type_name,Total_column_filter,r_text_val,c_text_val,filter_data);
         	var get_json_stringify=$("#filter_data_object").text();
  				var json_obj=JSON.parse(get_json_stringify);
  				filter_length=Object.keys(json_obj).length;
  				filter_keys=Object.keys(json_obj);

		      	var q=1;
		      	for (var i = 0; i<=filter_length; i++) {

		      		$("#filter"+q).val(json_obj[filter_keys[i]]);
							$("#filter"+q).multiselect('rebuild');
							q++;
		      	}

    	}, 500);
	   $('#facts_colorizer1').modal('hide');
      $.LoadingOverlay("hide",true);
// common code end here
// ========================================================================================================================
// ========================================================================================================================
}


function display_facts_colorizer_values() {
	// alert('hii')
	// get all selected facts name and values start here
	var releasearr = {};
	var theSelect = document.getElementById('facts_group_filter');
	var optgroups = theSelect.getElementsByTagName('optgroup');
	// console.log('optgroups',optgroups.length)
	var arr = {};
	for (var i = 0; i < optgroups.length; i++) {
	    l=optgroups[i].getAttribute('label');
	    // console.log('iiiiiiiiiiii',i)
	    // console.log('lllllllllllllllll',l)
	    releasearr[l] = [];
	    arr[l]= [];
	    var options = optgroups[i].getElementsByTagName('option');
	    // console.log('options',options)
	 
	    
	    for (var j = 0; j < options.length; j++) {
	    	// console.log('selected options',options[j].selected)
	        releasearr[l].push(options[j].innerHTML);
	        if(options[j].selected){
	        	// console.log('line 1774',l,'value',options[j].innerHTML)
	            
	            arr[l].push(options[j].innerHTML);
	        }
	    }
	}
	// get all selected facts name and values end here
	var get_tp_name=$("#time_period").val()
	if (typeof get_tp_name === 'string') {
		get_tp_name=[get_tp_name];
	}
	console.log('get_tp_name--->',get_tp_name)
	console.log('get_tp_name arr--->',arr)
	// console.log('get_tp_name---> typeof',typeof(get_tp_name))
	

var html='';

	$.each(get_tp_name, function (tp_key, tp_value) {
		var class_sh='';
		if (tp_key==0 || tp_key=='0') {
			class_sh='show';
		}
		// card class start here
		html+='<div class="card">';
		html+='<div class="card-header py-1" id="headingOne" data-toggle="collapse" data-target="#collapse'+tp_key+'" aria-expanded="true" aria-controls="collapse'+tp_key+'" style="cursor: pointer">';
		html+='<h5 class="mb-0"><button class="btn text-light"><span id="iconOne" class="plus-minus">+</span> '+tp_value+' </button></h5>';
		html+='</div>';
		html+='<div id="collapse'+tp_key+'" class="collapse '+class_sh+'" aria-labelledby="headingOne">';
		// console.log('arr--->',arr)
		let arr_length = Object.keys(arr).length;
		// console.log('arr length--->',arr_length)

		$.each(arr, function (facts_key, facts_values) {
			var get_facts_colorizer_object=$("#facts_coorizer_div_array").html();
			
			console.log('facts_values--->',facts_values)
			const filteredData = facts_values.filter(item => item.includes("vs"));
			let filteredData1 = filteredData.filter(element => !element.includes('GR'));
			console.log('filteredData==>',filteredData)
			console.log('filteredData1==>',filteredData1)
			// collapseOne class start here
			var modifiedText = facts_key.replace(/[()_]/g, ""); // Remove parentheses and underscores
			var joinedText = modifiedText.replace(/\s+/g, "_"); // Replace spaces with underscores
			html+='<h6 class="pl-2 mt-2">'+facts_key+'</h6>';
				$.each(filteredData1, function (key1, value2) {
					//card-body class start here


					if (get_facts_colorizer_object!="") {
		               var get_facts_colorizer_json=JSON.parse(get_facts_colorizer_object);
		               // console.log('get_facts_colorizer_json 4000',get_facts_colorizer_json);
		               get_result=find_match_facts_colorizer_value(get_facts_colorizer_json,value2);
		               // console.log('get_result 4000',get_result);
		               // console.log('get_result factsvalue 4000',get_result.factsvalue);

		               	html+='<div class="card-body p-2 px-4">';
						html+='<div class="d-flex justify-content-between pl-3 w-100">';
						html+='<input type="checkbox" class="form-check-input" id="checkbox_'+joinedText+'_'+tp_key+'_'+key1+'" data-tp_name="'+tp_value+'"  data-factsheader="'+facts_key+'">';
						html+='<label class="form-check-label" for="exampleCheck1">'+value2+'</label>';
						html+='<input type="number" class="form-control ml-auto" id="c1_'+joinedText+'_'+tp_key+'_'+key1+'" aria-describedby="number" placeholder="min" style="height: 27px; width: 70px !important;" />';
						html+='<input type="number" class="form-control mx-1" id="c2_'+joinedText+'_'+tp_key+'_'+key1+'" aria-describedby="number" placeholder="max" style="height: 27px; width: 70px !important;" />';
						html+='</div></div>';
						$('#checkbox_'+joinedText+'_'+tp_key+'_'+key1+'').prop('checked', true);

		            }else{

		            	html+='<div class="card-body p-2 px-4">';
						html+='<div class="d-flex justify-content-between pl-3 w-100">';
						html+='<input type="checkbox" class="form-check-input" id="checkbox_'+joinedText+'_'+tp_key+'_'+key1+'" data-tp_name="'+tp_value+'"  data-factsheader="'+facts_key+'">';
						html+='<label class="form-check-label" for="exampleCheck1">'+value2+'</label>';
						html+='<input type="number" class="form-control ml-auto" id="c1_'+joinedText+'_'+tp_key+'_'+key1+'" aria-describedby="number" placeholder="min" style="height: 27px; width: 70px !important;" />';
						html+='<input type="number" class="form-control mx-1" id="c2_'+joinedText+'_'+tp_key+'_'+key1+'" aria-describedby="number" placeholder="max" style="height: 27px; width: 70px !important;" />';
						html+='</div></div>';
		            }

					
					//card-body class end

					

				});
			
			

		});
		html+='</div>';// collapseOne class end
		html+='</div>';// card class end
	});

	$("#accordion_facts_colorizer1").empty()
	$("#accordion_facts_colorizer1").append(html)


	// tesing code not started for stored checked item
	// var get_stored_object=$("#facts_coorizer_div_array").html();
	// if (get_stored_object!="") {
		
	// 	var get_stored_object_json=JSON.parse(get_stored_object);
	// 	$.each(group_column_resp, function (k1, val1) {
	// 	// var matchingValues = getMatchingValues2(text,get_stored_object_json);

	// 	 });
	// }
}


function column_click_func(obj) {
	// alert($(obj).attr("data-class_name"))
	var get_class_name=$("#significant").val();
	// alert(get_class_name)
	// var get_class_name=$(obj).attr("data-class_name");
	
}

// $('#significant').change(function (){
// 	var sig_value=$('#significant :selected').val();
// 	var sig_id=$('#significant :selected').parent().attr('label');
//     // console.log('label',label);
// });

//original excel to export function star here
//    var tableToExcel = (function() {
//   var uri = 'data:application/vnd.ms-excel;base64,'
//     , template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--><meta http-equiv="content-type" content="text/plain; charset=UTF-8"/></head><body><table>{table}</table></body></html>'
//     , base64 = function(s) { return window.btoa(unescape(encodeURIComponent(s))) }
//     , format = function(s, c) { return s.replace(/{(\w+)}/g, function(m, p) { return c[p]; }) }
//   return function(table, name) {
//     if (!table.nodeType) table = document.getElementById(table)
//     var ctx = {worksheet: name || 'Worksheet', table: table.innerHTML}
//     window.location.href = uri + base64(format(template, ctx))
//   }
// })()


 var tableToPDF = function(table, name) {
  if (!table.nodeType) table = document.getElementById(table);
  
  // Add inline styles for borders and colors
  table.style.borderCollapse = 'collapse';
  table.style.width = '100%';
  // table.style.border = '1px solid black'; // border style
  table.style.color = '#333'; // font color
  // table.style.backgroundColor = '#f5f5f5'; // background color
  table.style.backgroundColor = '#fff'; // background color
  table.querySelectorAll('td, th').forEach(function(cell) {
    cell.style.border = '1px solid #dddddd'; // cell border style
    cell.style.padding = '8px'; // cell padding
  });

  // Open a new window with the table content
  var win = window.open('', '', 'width=800,height=600');
  win.document.write('<html><head><title>' + (name || 'Document') + '</title></head><body>');
  // win.document.write('<h1 style="color: #333;">' + (name || 'Document') + '</h1>');
  win.document.write('<h1 style="color: #333;">' + ('Document') + '</h1>');
  win.document.write(table.outerHTML);
  win.document.write('</body></html>');
  win.document.close(); // Close the document to render

  // After rendering, trigger the print functionality
  win.print();

  return true;
};

var tableToImage = function(table, name) {
  if (!table.nodeType) table = document.getElementById(table);
  
  // Add inline styles for borders and colors
  table.style.borderCollapse = 'collapse';
  table.style.width = '100%';
  table.style.border = '1px solid black'; // border style
  table.style.color = '#333'; // font color
  table.style.backgroundColor = '#f5f5f5'; // background color
  table.querySelectorAll('td, th').forEach(function(cell) {
    cell.style.border = '1px solid #dddddd'; // cell border style
    cell.style.padding = '8px'; // cell padding
  });

  // Use dom-to-image to convert the table to an image
  domtoimage.toBlob(table)
    .then(function(blob) {
      // Create a link element to trigger download
      var link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = name || 'image.png';
      document.body.appendChild(link);
      link.click();

      // Clean up
      document.body.removeChild(link);
    })
    .catch(function(error) {
      console.error('Error converting table to image:', error);
    });
};

// working for pdf without color code
// var tableToExcel = function(table, name) {
//   if (!table.nodeType) table = document.getElementById(table);
  
//   // Open a new window with the table content
//   var win = window.open('', '', 'width=800,height=600');
//   win.document.write('<html><head><title>' + (name || 'Document') + '</title></head><body>');
//   win.document.write('<h1>' + (name || 'Document') + '</h1>');
//   win.document.write(table.outerHTML);
//   win.document.write('</body></html>');
//   win.document.close(); // Close the document to render

//   // After rendering, trigger the print functionality
//   win.print();

//   return true;
// };

//color code not working 
var tableToExcel = function() {
    return function(table, name) {
        if (!table.nodeType) table = document.getElementById(table);

        // Create a workbook
        var workbook = XLSX.utils.book_new();

        // Add worksheet
        var ws = XLSX.utils.table_to_sheet(table);

        // Add the worksheet to the workbook
        XLSX.utils.book_append_sheet(workbook, ws, name || "Sheet1");

        // Write the workbook to a file
        XLSX.writeFile(workbook, (name || "table") + ".xlsx");
    };
}();


// excel to export function end here


