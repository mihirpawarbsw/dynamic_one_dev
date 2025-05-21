// var API_URL='https://forecasting.azurewebsites.net/';
var API_URL='https://127.0.0.1:8000/';
// var API_URL='https://127.0.0.1:8000/';
// var API_URL='http://127.0.0.1:8000/';
// var API_URL='http://127.0.0.1:8000/';
// var API_URL='https://ietool.brand-scapes.com/';


function autoresponse(zurl,data) {
    var resultobj;
    var result;
    var zapiurl = API_URL + zurl;
    var formData = data;
    $.ajax({
        type: "POST",
        url: zapiurl,
        data: formData,
        dataType: 'json',
        async: !1,
         success: function (data) {
                resultobj = data;
            },
            error: function (textStatus, errorThrown) {
              // alert
               // swal({title: "Error!",
               //    text: "No Data Found Try Another filter!",
               //    type: "error",
               //    confirmButtonText: "OK"
               //  });
               hidePreloader();
            }
    });
   return resultobj;
}

function showPreloader() {
$("#preloader").show();
}

function hidePreloader() {
$("#preloader").hide();
}

// $("#logout").click(function(){
//   // alert("The paragraph was clicked.");
//    flagcheck=window.localStorage.setItem('flag', '0');
//    // window.location.replace("https://forecasting.azurewebsites.net/");
//    window.location.replace("http://127.0.0.1:8000");
// });


$("#holt_winter_forecast_line_chart_download_ppt,#Arima_forecast_line_chart_download_ppt").click(function(event) {
    
  model_type = $("#nav-tab a.active").attr('id');
  // alert(model_type);
  ppt_download_forecast_line_common();

      
});

$("#holt_winter_actual_fitted_lin_chart_download_ppt,#Arima_arima_actual_fitted_linee_chart_download_ppt").click(function(event) {
    
  model_type = $("#nav-tab a.active").attr('id');
  // alert(model_type);
  ppt_download_Actual_vs_fitted_common();

      
});

function ppt_download_forecast_line_common(){
  // forecast_line_chart ppt code  // 
  var pptx = new PptxGenJS();
  var slide = pptx.addNewSlide();
  var opts = { x:1.0, y:1.0, fontSize:42, color:'00FF00' };
  // slide.addImage({ data: dataURL, x:1, y:1, w:8, h:4 });
  var forecast_line_chart_ppt_download = localStorage.getItem('forecast_line_chart');
  slide.addImage({ path: forecast_line_chart_ppt_download, x:1, y:1, w:8, h:4  });
  // slide.addImage({ path: "https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg" });
  pptx.writeFile({ fileName: 'forecast_line' });

}

function ppt_download_Actual_vs_fitted_common(){
  // Actual_vs_fitted_line_chart ppt code  // 
  var pptx = new PptxGenJS();
  var slide = pptx.addNewSlide();
  var opts = { x:1.0, y:1.0, fontSize:42, color:'00FF00' };
  // slide.addImage({ data: dataURL, x:1, y:1, w:8, h:4 });
  var Actual_vs_fitted_line_chart_ppt_download = localStorage.getItem('Actual_vs_fitted_line_chart');
  slide.addImage({ path: Actual_vs_fitted_line_chart_ppt_download, x:1, y:1, w:8, h:4  });
  // slide.addImage({ path: "https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg" });
  pptx.writeFile({ fileName: 'Actual_vs_fitted_line' });

}




// not using this function
function ppt_download(dataset_blue,dataURL,label,color_array) {
   
   
    // alert('hello');
   showPreloader();
   var chartname='line chart';
   var chartname='line chart';
   // var chartname=$(this).attr("chart");
      // alert(chartname);
   setTimeout(function(){

 

       var pptx = new PptxGenJS();
       pptx.layout ='LAYOUT_WIDE';
       var slide = pptx.addNewSlide();

 

      //  var elements=$('.'+chartname+'-panel').parent().find('.chart-title').html();
      // var  charttitle= elements.replace(/<i.*>.*?<\/i>/ig,'');

 
     // static data
      // var dataChartAreaLine = [
      //     {
      //         name: "Actual Sales",
      //         labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
      //         values: [1500, 4600, 5156, 3167, 8510, 8009, 6006, 7855, 12102, 12789, 10123, 15121],
      //     },
      //     {
      //         name: "Projected Sales",
      //         labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
      //         values: [1000, 2600, 3456, 4567, 5010, 6009, 7006, 8855, 9102, 10789, 11123, 12121],
      //     },
      // ];

      var dataChartAreaLine = [
          {
              name: "Forecast Line",
              labels: label,
              values: dataset_blue,
              chartColors: color_array,
          }
      ];



 

       // Bullets with indent levels
       // var text='CONTINENTS='+$('#dash-sel-continent  option:selected').text()+', COUNTRY='+$('#dash-sel-country  option:selected').text()+', DIVISIONS='+$('#dash-sel-category  option:selected').text()+', EXPERIMENT (CAMPAIGN) OBJECTIVE='+$('#dash-sel-objective  option:selected').text()+', DATE='+$('#reportrange span').html()+', SIZE OF EXPERIMENT (# IMPRESSIONS)='+$('#imp-min').val()+'-'+$('#imp-max').val();
       // slide.addText(
       //     text,
       //     { x:'10%', y:0.15, w:'100%', color:'9F9F9F',fontSize:10.3, margin:1, border:[0,0,{pt:'2',color:'CFCFCF'},0] }
       // );

 

       // slide.addText(
       //     charttitle,
       //     { x:'30%', y:0.15, w:'100%', h:1, align:'c', fontSize:24, color:'0088CC'  }
       // );

 

      slide.addChart(pptx.ChartType.line, dataChartAreaLine, { x: 1, y: 1, w: 10, h: 5 });
      pptx.writeFile({ fileName: 'charttitle' });
      hidePreloader();
   },500);

}



function model_mape_value_check(mape_val){
  var mape_color;
  if (mape_val <= 10) {
    mape_color='green';//Excellent_
  }
  else if(mape_val <= 20) {
    mape_color='#ffb100';//Good_
  }
  else {
    mape_color='red';//Poor_
  }
  return mape_color;
}
// model_mape_value_check(10);



// $("#number_of_prediction_point").change(function(){
$("#Arimax_analysis_btn").click(function(){
  var number_of_prediction_point = $("#number_of_prediction_point").val();
  var data_column_size = localStorage.getItem('data_column_size');
  var data_column_size_1 = data_column_size-2;
  var setRows    = number_of_prediction_point;
  // var setColumns = 3;
  var setColumns = data_column_size;

  // console.log('llllllllllllll',displayRecords);

  var html=i= '';
  html +='<table class="table table-striped table-responsive-sm" id="number_of_prediction_point_tbl">';
  html +='<thead>';
  html +='<tr class="table-font-hd">';
  html +='<th scope="col" colspan="4" class="px-1">No. of prediction points</th>';
  html +='</tr>';
  html +='</thead>';
  html +='<tbody id="tableBody">';
  html +='<tr>';
  html +='<td class="text-center"><b>Month</b></td>';
  // html +='<td class="text-center"><b>Col 1</b></td>';
  // html +='<td class="text-center"><b>Col 2</b></td>';
  for (var jj = 1; jj <= setColumns; jj++) {
      html += '<td class="text-center" >Col '+jj+'</td>';
    }
  html +='</tr>';

  
  for (var i=1; i<=setRows; i++){
    html += '<tr style="background-color: rgba(0, 0, 0, 0.05);" id="Month'+i+'"> ';
    html +='<td class="text-center">Month '+i+' </td>';
    for (var j = 1; j <= setColumns; j++) {
      // html += '<td class="text-center"  contenteditable="true"></td>';
      html += '<td class="text-center" i><input type="text" name="name'+i+' " required></td>';
    }
    html += '</tr>';
  }



  html +='</tbody>';
  html +='</table>';
  $('#number_of_prediction_point_input_table').html(html);
     hidePreloader();

});


// working  function comment by pranit
// $("#independent_model_submit_btn").click(function(){
//   var number_of_prediction_point = $("#number_of_prediction_point").val();
//   var data_column_size = localStorage.getItem('data_column_size');
//   // var data_column_size_1 = data_column_size-2;
//   var setRows    = number_of_prediction_point;
//   // var setColumns = 2;
//   var setColumns = data_column_size;
//   var TotalObj= [];
//   var Data_Obj= [];

//   // console.log('llllllllllllll',displayRecords);

//   // alert('llllllllllllll');
//   for (var i = 1; i <=setRows ; i++) {
//     // var Data_Obj= [];
//     $("#Month"+i+" td input").each(function(){
//       var input_val = $(this).val();
//       console.log('llllllllllllll',input_val);
//       Data_Obj.push([input_val]);
//       // Data_Obj.push({input_val:input_val});
//       });
    
    
//   }

//   console.log('Data_Obj',Data_Obj);

      
//   var analyzeInput = $("#analyzeInput").val();
//   var historic_data_file_name = $("#historic_data_file_name").val();
//   // var model_type = "Holt_Winter_Model";
//   var model_type = $("#nav-tab a.active").attr('id');
//   var csrfmiddlewaretoken=csrftoken;
//   // alert(model_type);
//   var checkData2 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken+"&number_of_prediction_point=" + number_of_prediction_point+"&model_type=" + model_type+"&historic_data_file_name=" + historic_data_file_name+"&Data_Obj=" + Data_Obj+"&setColumns=" + setColumns;
//   respdata2 = autoresponse("model_results_for_indepedent_model", checkData2);
//   if (respdata2.status  == 200)
//   {
//     // $('#staticBackdrop').modal('toggle');
//     alert('yes');
//     model_result_independent_main();
//     hidePreloader();
//   }
//   else
//   {
//     alert('Something went wrong');
//     hidePreloader();//#MODIFICATION DONE BY PRANIT ON 25-05-2021
//   }

    

//   });

function common_prediction_points_show(){
   $("#common_prediction_points").show();

}
function common_prediction_points_hide(){
   $("#common_prediction_points").hide();

}

function independent_prediction_point_btn_show(){
   $("#independent_prediction_point_btn").show();

}
function independent_prediction_point_btn_hide(){
   $("#independent_prediction_point_btn").hide();

}

// New code added by pranit
function data_type_filter_value(data_type){

  const arr1 =  ["Daily","Weekly","Monthly","Quarterly"];
  var arr2=[];
  if(data_type=="Daily"){
    var arr2 = [];
  }
  else if(data_type=="Weekly"){
    var arr2 = ["Daily"];
  }
  else if(data_type=="Monthly"){
    var arr2=["Daily","Weekly"];
  }
  else if(data_type=="Quarterly"){
    var arr2=["Daily","Weekly","Monthly"];
  }

  let unique1 = arr1.filter((o) => arr2.indexOf(o) === -1);
  let unique2 = arr2.filter((o) => arr1.indexOf(o) === -1);
  var data_type_filter_array = unique1.concat(unique2);

  // console.log('data_type_filter_array',data_type_filter_array);
  // console.log('data_type',data_type,'aaaaaaaaaaaaaaa');
  // console.log('arr2',arr2);
  return data_type_filter_array
}

function data_type_filter_common(data_type){
  var historic_data_file_name = $("#upload_data_type_id").val();
// alert(historic_data_file_name)
  $('#upload_data_type_id').children().remove().end()
  data_type_filter_array=data_type_filter_value(data_type);



  $.each(data_type_filter_array, function(key, value) {
  // $('#upload_data_type_id').append($("<option></option>").attr("value", value).text(value));
  if(value == historic_data_file_name){
  // data_type=historic_data_file_name;
  }



  if(value == data_type){
  $("#upload_data_type_id").append('<option value="' + value + '" selected>' + value + '</option>');
  }else{
  $("#upload_data_type_id").append('<option value="' + value + '" >' +value + '</option>');
  }

  });
  }
// function data_type_filter_common(data_type){
//   data_type_filter_array=data_type_filter_value(data_type);

//        $.each(data_type_filter_array, function(key, value) {
//          // $('#upload_data_type_id').append($("<option></option>").attr("value", value).text(value));
//           if(value == data_type){
//             $("#upload_data_type_id").append('<option value="' + value + '" selected>' + value + '</option>');
//           }else{
//               $("#upload_data_type_id").append('<option value="' + value + '" >' +value + '</option>');
//           }
        
//        });
// }

function get_total_month_output(data_type,totalRecords) {
  if(data_type=="Daily"){
    var totalRecords_final =(totalRecords);
    // var totalRecords_final =(totalRecords/12);
  }
  else if(data_type=="Weekly"){
    // var totalRecords_final = (totalRecords/ 12);
    var totalRecords_final = (totalRecords);
  }
  else if(data_type=="Monthly"){
    var totalRecords_final=(totalRecords);
    // alert('Monthly');
  }
  else if(data_type=="Quarterly"){
    var totalRecords_final=(totalRecords);
    // var totalRecords_final=(totalRecords/3);
    // alert('Quarterly');
  }
   return totalRecords_final

} 
// function ppt_download(dataset_blue,dataURL) {
   
//    // showPreloader();
//    var chartname='line chart';
//    var charttitle='line chart';
//      // console.log('helloooooooooooooooooooooooooooooooooo',dataURL);
//   // console.log('helloooooooooooooooodataset_blue',dataset_blue);
//    // var data_str = $(this).attr("data-value");
//    // var my_object = JSON.parse(decodeURIComponent(data_str));
//    // console.log(my_object);

 


//    setTimeout(function(){

 

//        var pptx = new PptxGenJS();
//        pptx.layout ='LAYOUT_WIDE';
//        var slide = pptx.addNewSlide();

 

//       // var c = document.getElementById(chartname);
//       // var elements=$('.'+chartname+'-panel').parent().find('.chart-title').html();
//       // var  charttitle= elements.replace(/<i.*>.*?<\/i>/ig,'');
      
//       // var dataURL = c.toDataURL();

 

//       // var dataChartAreaLine = [];
//       var dataChartAreaLine = [];


//       // $.each(dataset_blue,function(kk,vv){
       
//               dataChartAreaLine.push({
//                   name: 'line chart',
//                   chartColors: 'red',
//                   labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
//                   values: [1500, 4600, 5156, 3167, 8510, 8009, 6006, 7855, 12102, 12789, 10123, 15121],
//                   // labels: 'hello',
//                   // values: vv,
//               });
//       // });
//        console.log('helloooooooooooooooodataset_blue',dataChartAreaLine);
 

//        // Bullets with indent levels
//        // var text='CONTINENTS='+$('#dash-sel-continent  option:selected').text()+', COUNTRY='+$('#dash-sel-country  option:selected').text()+', DIVISIONS='+$('#dash-sel-category  option:selected').text()+', EXPERIMENT (CAMPAIGN) OBJECTIVE='+$('#dash-sel-objective  option:selected').text()+', DATE='+$('#reportrange span').html()+', SIZE OF EXPERIMENT (# IMPRESSIONS)='+$('#imp-min').val()+'-'+$('#imp-max').val();
//        // slide.addText(
//        //     text,
//        //     { x:'10%', y:0.15, w:'100%', color:'9F9F9F',fontSize:10.3, margin:1, border:[0,0,{pt:'2',color:'CFCFCF'},0] }
//        // );

 

//        // slide.addText(
//        //     charttitle,
//        //     { x:'30%', y:0.15, w:'100%', h:1, align:'c', fontSize:24, color:'0088CC'  }
//        // );

 

//       // slide.addImage({x:'5%', y:'15%', w:'90%', h:6, align:'c', data: dataURL});
//       slide.addChart(pptx.ChartType.line, dataChartAreaLine, { x:'5%', y:'15%', w:'90%', h:6, align:'c'});
      
//       pptx.writeFile({ fileName: charttitle });
//       // hidePreloader();
//    },500);

// }

