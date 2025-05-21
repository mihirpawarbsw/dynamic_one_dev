 // $(document).ready(function(){

 //   callback_drag_and_drop_function();
 //     drag_and_drop_intial_fun();
 // });
var csrfmiddlewaretoken=csrftoken;
var data11 = ["A1","A2","A3","A3","A4","A5","A6","A7","A8","A9","A10","A11","A12", "A13","A14", "A14","A15", "A16","A17", "A18","A19", "A20","A21", "A22","A23", "A24","A25", "A26","A27", "A28","A29", "A30","A31", "A32","A33", "A34"]

// var data=['LinkID', 'Country', 'Are_you_comfortable_in_taking_following_survey_in_English_or_any_other_language', 'Do_you_work_in_any_of_these_industries', 'Gender', 'Age', 'Age_:_Post_code', 'Please_select_Items_you_have_at_home_in_working_condition_::_Electricity_connection', 'Please_select_Items_you_have_at_home_in_working_condition_::_Ceiling_fan', 'Please_select_Items_you_have_at_home_in_working_condition_::_LPG_stove','LinkID', 'Country', 'Are_you_comfortable_in_taking_following_survey_in_English_or_any_other_language', 'Do_you_work_in_any_of_these_industries', 'Gender', 'Age', 'Age_:_Post_code', 'Please_select_Items_you_have_at_home_in_working_condition_::_Electricity_connection', 'Please_select_Items_you_have_at_home_in_working_condition_::_Ceiling_fan', 'Please_select_Items_you_have_at_home_in_working_condition_::_LPG_stove','Please_select_Items_you_have_at_home_in_working_condition_::_LPG_stove', 'Please_select_Items_you_have_at_home_in_working_condition_::_Two-wheeler', 'Please_select_Items_you_have_at_home_in_working_condition_::_Colour_TV', 'Please_select_Items_you_have_at_home_in_working_condition_::_Refrigerator', 'weighting'];


    let limit;
    var selectControl; 
    var selectionContainer;
    var ul;
    var searchText;
    var deleteSelectedText;
    var selectedText;



  setTimeout(function () { 
      var checkData2 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken;  
      respdata2 = autoresponse("display_all_data1", checkData2);   
      if (respdata2.status  == 200)
      {
      display_leftside_menu(respdata2);
      }
      else
      {
      alert('Something went wrong')
      } 
      
    }, 100);



function display_leftside_menu(resp){

  console.log('resp',resp)
  var html= '';
  var i=0;
  var ii=0;
  var j=0;
  var resp_len=Object.keys(resp['list_all_files']).length;

    var get_all_column_name=Object.keys(resp['list_all_files']);
   $.each(resp['list_all_files'], function(key1, val1){
      console.log('val1',val1)
      
      i++;
      html +='<ul class="subb-menu collapse" id="getting">';
      html +='<li class="child sub-main collapsed" data-toggle="collapse" data-target="#intro'+i+'">';
      html +='<a class="child dealerDetails" href="#" data-get_table_name="Electrolux- India filled_less_rows_respondent"  onclick="get_all_column_data(this);" data-get_id_name="dealerDropdown'+i+'" data-filename="'+val1+'">'+val1+'</a>';
      html +='</li>';
      html +='<ul id="intro'+i+'"  class="child-sub collapse">';
      html +='<li class="pl-4">';
      html +='<div id="dealerDropdown'+i+'" class="dropdown-container child  hide bg-transparent border-0">';
      html +='<div class="search bg-transparent" >';
      html +='<input type="text" class="search-box"/>';
      html +='</div>';
      html +='<div class="search-result bg-transparent ">';
      html +='<ul class="search-results-list border-0">';
      html +='</ul>';
      html +='</div>';
      html +='</div> ';
      html +='</li></ul></ul>';

      $('#display_leftside_menu').html(html);
      
     });


  }//function end here


var data1=[];
var get_id_name;
function get_all_column_data(e) {
  // alert('get_all_column_data')
      // var filename='Electrolux_India'; 
      var filename=$(e).attr("data-filename");
      console.log('data-filename',filename)
      var checkData2 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken+"&filename=" + filename;;
      get_id_name=$(e).attr("data-get_id_name"); 

      respdata = autoresponse("display_all_data", checkData2);   
      if (respdata.status  == 200)
      {
        // console.log('table_name',table_name)
        // console.log('get_id_name',get_id_name)
        // console.log('respdata',respdata)
        // console.log('respdata finale',respdata['colname_dict_final'][table_name]['colname_obj'])
        data=[];
        data=respdata['data_column_names']['filename'];
        display_all_column_name(filename);
        // drag_and_drop_intial_fun();
        callback_drag_and_drop_function();

      }
      else
      {
      alert('Something went wrong')
      }

}



function display_all_column_name(filename) {
    // alert('display_all_column_name')


   limit = Math.min(data.length, 5);
   selectControl = $('#delaerDetails');
   selectionContainer = $('.select-container');
   ul = $('#'+get_id_name+' .search-results-list');
   searchText = $('#'+get_id_name+' .search-box');
   console.log('searchText',searchText)
   deleteSelectedText = $(".dealerDetails .delete-selected-text");
   selectedText = $(".dealerDetails .selected-text");

   function debounce(fn, wait) {
    let timeout;
    return function() {
      let context = this;
      let argument = arguments
      clearTimeout(timeout);
        timeout = setTimeout(function() {
        fn.apply(context, argument);
        }, wait);
      }
    }

      var displayArray = data.slice(0, limit);
      let debouncedCreateElements = debounce(createAndAppend, 300);



      function createAndAppend(dataToAppend) {
        // console.log("called, " , dataToAppend);
        // createElement('li', dataToAppend);
        var dataToCreate=dataToAppend

        ul.html('');

        var listHTML = '';
        console.log(dataToCreate, limit);
        dataToCreate.forEach(function(item, index) {
          console.log('item=== line 145',item)
          // listHTML += `<li class="drag" id=${index}>${dataToCreate[index]}</li>`;
           listHTML += `<li class="text-left drag child  collapsed text-break border-bottom" data-filename=${filename} data-toggle="collapse" data-target="#intro2"  id=${index}><a href="#" class="text-wrap">${dataToCreate[index]}</a></li>`;
           // alert('rrr')
        });
        ul.append(listHTML);

    }

    function filterValues() {
      let searchedResults = filterArray(data, getSearchBoxValue(), 0);
      debouncedCreateElements(searchedResults);
    }

    let filterArray = (function filteringFunction() {
      let lastIndex = 0;
      function filterArray(arr, text, retainIndex) {
        var indexMax = Math.min(arr.length, limit);
        let filteredElements = 0;
        let start = retainIndex ? lastIndex : 0;
        if (start==0) {
          start=0
        }else{
          start=start+1
        }
        displayArray = [];
        for(var filteredIndex = start; (filteredIndex < arr.length || filteredElements > indexMax); filteredIndex++) {
          if(arr[filteredIndex].indexOf(text) != -1) {
             filteredElements++;
             displayArray.push(arr[filteredIndex]);
          }
          if(filteredElements >= indexMax) {
            
            break;
          }
        }
        lastIndex = filteredIndex;
        return displayArray;
      }
      return filterArray;
    })();

    filterValues();




ul.on('click', function(event) {
  selectedText.html(event.target.innerHTML);
  selectionContainer.addClass("render-selected-text");
  // alert('8')
  // deleteSelectedText.removeClass("hide");
  // $("#dealerDropdown").toggle();
});

deleteSelectedText.on('click', function() {
  setSearchBoxValue('');
  selectedText.html('');
  selectionContainer.removeClass("render-selected-text");
  filterValues();
  deleteSelectedText.addClass("hide");
  // alert('1')

})

searchText.on('keyup', function() {
  // alert('3')
  console.log('keyup=== called',searchText)
  filterValues();
});

function getSearchBoxValue() {
  // alert('33');
  // drag_and_drop_intial_fun();
  // callback_drag_and_drop_function();
  return searchText.val();
}

function setSearchBoxValue(value) {
  // alert('34');
  // drag_and_drop_intial_fun();
  // callback_drag_and_drop_function();
  return searchText.val(value);


}

    $('#'+get_id_name+' .search-result').on('scroll', function() {
      if($(this).scrollTop() + $(this).innerHeight() >= $(this)[0].scrollHeight) {
        console.log('line 186',this)
        let filteredData = filterArray(data, getSearchBoxValue(), 1)
        // addElementsToUL(filteredData);
        var dataToCreate=filteredData
        var listHTML = '';
        console.log(dataToCreate, limit);
        dataToCreate.forEach(function(item, index) {
          // listHTML += `<li class="drag" id=${index}>${dataToCreate[index]}</li>`;
           listHTML += `<li class="text-left drag child  collapsed text-break border-bottom" data-filename=${filename} data-toggle="collapse" data-target="#intro2"  id=${index}><a href="#" class="text-wrap">${dataToCreate[index]}</a></li>`;
           // alert('222')
        });
        ul.append(listHTML);
        callback_drag_and_drop_function();
      }
    })
   $('#'+get_id_name).show();





  }//display_all_column_name end here





let filterArray = (function filteringFunction() {
  let lastIndex = 0;
  function filterArray(arr, text, retainIndex) {
    var indexMax = Math.min(arr.length, limit);
    let filteredElements = 0;
    let start = retainIndex ? lastIndex : 0;
    displayArray = [];
    for(var filteredIndex = start; (filteredIndex < arr.length || filteredElements > indexMax); filteredIndex++) {
      if(arr[filteredIndex].indexOf(text) != -1) {
         filteredElements++;
         displayArray.push(arr[filteredIndex]);
      }
      if(filteredElements >= indexMax) {
        
        break;
      }
    }
    lastIndex = filteredIndex;
    return displayArray;
  }
  return filterArray;
})();

// filterValues();



// $('.dealerDetails').on('click', function() {
//   $('#'+get_id_name).show();
// });

function getSearchBoxValue() {
  // drag_and_drop_intial_fun();
  callback_drag_and_drop_function();
  return searchText.val();
}

function setSearchBoxValue(value) {
  // drag_and_drop_intial_fun();
  callback_drag_and_drop_function();
  return searchText.val(value);
}




// $(".dealerDetails").click(function(){
//  alert('hhh')
//   // callback_drag_and_drop_function();
// });
// ==========================================================
// ==========================================================

function callback_drag_and_drop_function() {
    
  // alert(' callback_drag_and_drop_function')
   $('.drag').draggable({ 
      appendTo: 'body',
      helper: 'clone'
    });

      //SECTION 1  clickable
    $('#sTreePlus').droppable({
      activeClass: 'active',
      hoverClass: 'hover',
      accept: ":not(.ui-sortable-helper)", // Reject clones generated by sortable
       drop: function (e, ui) {
          var table_name=ui.draggable[0].getAttribute("data-filename");
          console.log('table_name 334',ui);
          // console.log('ui.draggable.text() 334',ui.draggable.text());
          var $el = $('<p class="drop-item"  data-module="b" data-filename="'+table_name+'" data-value="' + ui.draggable.text() + '" style="color: black;">' + ui.draggable.text() + '</p>');
          $el.append($('<button type="button" class="btn btn-default btn-xs remove" style="background-color: black;height: 15px;"><span class="glyphicon glyphicon-trash"></span></button>').click(function () { $(this).parent().detach(); }));
          $(this).append($el);
           // alert('helloo')
           Row_array_data=grouping_div_element();
           // var Row_array_data=$('#sTreePlus').sortableListsToArray();
        find_table_name_dy(Row_array_data);
        // console.log('line 343 Row_array_data',Row_array_data)
        }
    }).sortable({
      items: '.drop-item',
      sort: function() {
        // gets added unintentionally by droppable interacting with sortable
        // using connectWithSortable fixes this, but doesn't allow you to customize active/hoverClass options
        $( this ).removeClass( "active" );
      }
    });

   



    


}

function grouping_div_element() {
  var body_object=[];
  $('#sTreePlus p').each(function() {
    // var data = $(this).attr('data-id'); 
    var filename=$(this).attr('data-filename'); 
    var value=$(this).attr('data-value'); 
    console.log('grouping_div_element 1',$(this));
    // console.log('grouping_div_element 2',$(this).attr('data-filename'),$(this).attr('data-value'));
    body_object.push({['filename']:filename,['value']:value});
    console.log('body_object',body_object);
    
  });
  return body_object;
}

$("#dealerDetails111").click(function(){
 alert('hhh')
  // callback_drag_and_drop_function();
});


function find_table_name_dy(Row_array_data){
      console.log('=================find_table_name_dy start===============')
      console.log('Row_array_data row 250',Row_array_data)
      // console.log('Column_array_data col 250' ,Column_array_data)

      var final_combine_array=[];
      var final_combine_array2=[];
      console.log('length Row',Row_array_data.length)
      // console.log('length col',Column_array_data.length)

        if (Row_array_data.length>0) {
          $.each(Row_array_data, function (key1, value1) {
            // console.log('final_col_array_grp====',key1,value1)
                final_combine_array.push({[key1]:value1});
                // z++;
          });
        }
        // if (Column_array_data.length>0) {
        //   $.each(Column_array_data, function (key1, value1) {
        //     // console.log('final_col_array_grp====',key1,value1)
        //         final_combine_array.push({[key1]:value1});
        //         // z++;
        //   });
        // }
        // console.log('final_combine_array ==== 808',final_combine_array)
        for (var i = 0 ;i < final_combine_array.length; i++) {
          $.each(final_combine_array[i], function (key1, value1) {
            // console.log('final_row_array_grp====',key1,value1)
                final_combine_array2.push(value1);
          });
        }

        let row_array_group = final_combine_array2.reduce((r, a) => {
         r[a.filename] = [...r[a.filename] || [], a];
         return r;
        }, {});

        var keys = Object.keys(row_array_group);
        if (keys.length>0) {
          $('#dropzone').empty();
          $.each(keys, function (k1, v1) {
            // var html='<li class="drop-item" id="item_b1" data-module="b" data-value="cbl_respondent_level"><div>'+v1+'</div></li>'
            var html='<div class="bg-white border m-2 p-3 pt-2 shadow-sm">'+v1+'</div>'
            $('#dropzone').append(html)
          });
          
        }
        console.log('final_combine_array2 ==== 269',final_combine_array2)
        console.log('row_array_group ==== 276',row_array_group)
        console.log('keys',keys)
        // console.log('final_combine_array ==== 262',final_combine_array)
        console.log('=================find_table_name_dy end===============')

}

$('#clear_all_row').click(function(){
 // alert('yes11')
 $('#sTreePlus').empty();
});


$('#clear_all_column').click(function(){
 // alert('yes11')
 $('#sTree2').empty();
});


$('#toArrBtn').on( 'click', function(){ 
  // alert('hmm')
      var final_combine_array2=grouping_div_element();
      console.log('final_combine_array2 454',final_combine_array2);

      final_row_col_array_grp1=comparing_array_object(final_combine_array2);
      final_row_col_array_grp=sorting_comparing_object(final_row_col_array_grp1)
      console.log('final_row_col_array_grp 8451 ',final_row_col_array_grp1);
      console.log('final_row_col_array_grp 845',final_row_col_array_grp);

      var Row_array_data_len = Object.keys(final_combine_array2).length;
      var row_object_grp_len = Object.keys(final_combine_array2).length;
      console.log('Row_array_data_len lenght11' ,Row_array_data_len);
      console.log('Value1_size row lenght' ,row_object_grp_len);
       //row condition list
      // if (row_object_grp_len===1) {
      //   var seperated_flag_row=0;
      //   // alert('seperated_flag_row 0')
      // }
      // else if(row_object_grp_len>1 && Row_array_data_len==row_object_grp_len){
      //   var seperated_flag_row=1;
      //   // alert('seperated_flag_row 1')
      // }
       var seperated_flag_row=1;
       var seperated_flag_col=1;

      

      var body_data= exract_one_array_object_by_data(final_combine_array2);
      console.log('Row_array_new 548' ,body_data);
       var table_name1 = [];
      if ( $('#dropzone div').length > 1 ) {
        
        // $(function() {

          $('#dropzone div').each(function(){
              var tbl_name=$(this).text();
               table_name1.push($(this).text());
          });
        // });
        
      }else{
            table_name1.push($('#dropzone div').text())
      }
      // console.log('table_name1 563' ,table_name1);
      if (table_name1.length>1) {
        // table_name1='merged'
        if ((table_name1.length)=2) {
          var t1=table_name1[0].split("_").splice(-1)[0]
          var t2=table_name1[1].split("_").splice(-1)[0]
          if (t1==t2) {
              // console.log('t1 is  equal to t2')
              table_name1='concat'
          }
          else if (t1!=t2) {
             table_name1='merged'
            // console.log('t1 not  equal to t2')
          }
          // console.log('table_name1 951 qq',t1)
          // console.log('table_name1 952 ee',t2)
          
        }
      
      }else{
        // console.log('table string',table_name1[0].split("_").splice(-1));
        table_name1=table_name1[0].split("_").splice(-1)[0]
        // console.log('table string' ,table_name1);
      }
    // console.log('Row_array_new' ,Row_array_new);
    // console.log('Col_array_new' ,Col_array_new);
    // console.log('table_name1 949' ,table_name1);
    console.log('body_data lenght 520' ,Object.keys(body_data).length);
      // Object.keys(body_data).length;
    if (Object.keys(body_data).length<2) {
      alert('Please select atleast 2 variable')
    }else if(Object.keys(body_data).length>5){
      alert('Variable should not greater then 5')
    }else{
      // var Row_array_new=
      const Row_array_new = body_data.splice(0, 1);   
      const Col_array_new = body_data.splice(0, 1);

      console.log('firstHalf' ,Row_array_new);
      console.log('secondHalf' ,Col_array_new);
      console.log('body_data 533' ,body_data);
      get_table_resp(Row_array_new,Col_array_new,body_data,seperated_flag_row,seperated_flag_col,final_row_col_array_grp,table_name1);
    }



  
    // get_table_resp(Row_array_new,seperated_flag_row,seperated_flag_col,final_row_col_array_grp,table_name1);



  
});//end toArrBtn


function sorting_comparing_object(final_row_col_array_grp) {
  console.log('sorting_comparing_object start',final_row_col_array_grp)
  var respondent=[]
  var response=[]
  var main_object=[]
  $.each(final_row_col_array_grp, function (k11, val22) {
    var last_val_obj=Object.keys(val22)

    var last_val = last_val_obj[0].split("_").pop()
    console.log('last_val start',last_val)
    if (last_val==='respondent') {
      respondent.push(val22)
    }else if(last_val==='response'){
      response.push(val22)
    }
  });

  console.log('respondent start',respondent)
  console.log('response start',response)

    var respondent1 = Object.keys(respondent).length;
    var response1 = Object.keys(response).length;

    console.log('respondent1 lenght',respondent1)
    console.log('response1 lenght',response1)
    if ((respondent1>=2 && response1==0)) {main_object=respondent}
    else if((response1>=2 && respondent1==0)) {main_object=response}
    else{
      if (respondent1>0) {main_object.push(respondent[0])}
      if (response1>0) {main_object.push(response[0])}
    }
    
    // if (respondent1>0) {main_object.push(respondent)}
    // if (response1>0) {main_object.push(response)}
    
    // main_object.push(response[0])
    console.log('sorting_comparing_object main obj',main_object)
    return main_object
    
}


function comparing_array_object(Row_array_data){
      // group by table name start
      // console.log('line 899',Row_array_data)
      let row_array_group = Row_array_data.reduce((r, a) => {
       r[a.filename] = [...r[a.filename] || [], a];
       return r;
      }, {});
      // console.log("Row_array_group 973", row_array_group);
      // group by table name end

      var final_row_array_grp=[];
      var final_row_array_grp1=[];
      $.each(row_array_group, function (k11, val22) {
        console.log("each loop start",k11, val22);
        var column_arr=[];
          $.each(val22, function (k111, val222) {
            column_arr.push(val222['value'])
          });
          final_row_array_grp.push({[k11]:column_arr})
      });
      // for (var i = 0; i <final_row_array_grp.length; i++) {
      //    $.each(final_row_array_grp[i], function (k111, val222) {
      //      // console.log('line 903==>',val222);
      //    });
      // }

      // console.log( 'final_row_array_grp line 943',final_row_array_grp); 
      // group by table name end
      return final_row_array_grp;

}

function get_table_resp(Row_array_new,Col_array_new,remaining_other_array,seperated_flag_row,seperated_flag_col,final_row_col_array_grp,table_name1) {
  console.log('table_name22 ==' ,table_name1);
  console.log('Row_array_new 444==' ,Row_array_new);
  console.log('Col_array_new 444==' ,Col_array_new);
  console.log('remaining_other_array 444==' ,remaining_other_array);
  console.log('seperated_flag_row 444==' ,seperated_flag_row);
  console.log('seperated_flag_col 444==' ,seperated_flag_col);
  console.log('final_row_col_array_grp 444==' ,final_row_col_array_grp);
  console.log('table_name1 444==' ,table_name1);

  localStorage.clear(); //all items
  var tbl_name=$('#source_name').html();
   // alert(tbl_name)
   if (tbl_name!='') {
    //console.log('sss',column_name_list)
    

    // Column name array stored in local strorage
    var column_name_list_object = JSON.stringify(Col_array_new);
    localStorage.removeItem("column_name_list_object");
    localStorage.setItem('column_name_list_object', column_name_list_object);

    // row name array stored in local strorage
    var row_name_list_object = JSON.stringify(Row_array_new);
    localStorage.removeItem("row_name_list_object");
    localStorage.setItem('row_name_list_object', row_name_list_object);

    // Column name array stored in local strorage
    var remaining_other_list_object = JSON.stringify(remaining_other_array);
    localStorage.removeItem("remaining_other_list_object");
    localStorage.setItem('remaining_other_list_object', remaining_other_list_object);


    localStorage.removeItem("seperated_flag_row");
    localStorage.setItem('seperated_flag_row', seperated_flag_row);

    localStorage.removeItem("seperated_flag_col");
    localStorage.setItem('seperated_flag_col', seperated_flag_col);

    var final_row_col_array_grp1 = JSON.stringify(final_row_col_array_grp);
    localStorage.removeItem("final_row_col_array_grp");
    localStorage.setItem('final_row_col_array_grp', final_row_col_array_grp1);


    var table_name11 = JSON.stringify(table_name1);
    localStorage.removeItem("tbl_name");
    localStorage.setItem('tbl_name', table_name11);


    // localStorage.removeItem("tbl_name");
    // localStorage.setItem('tbl_name', tbl_name);
    // window.location.href = API_URL+'crosstab_dash/';
    window.open(API_URL+'crosstab_dash/', '_blank');
    // alert('yes') 
      return false;
   }
   else{
    alert('please select data source')
   }
  

}




function groupArrayOfObjects(list, key) {
  return list.reduce(function(rv, x) {
    (rv[x[key]] = rv[x[key]] || []).push(x);
    return rv;
  }, {});
};


function exract_one_array_object_by_data(resp){
   var array_nodes = [];
   resp.forEach(function(d) {
                array_nodes.push({
                  value: d.value
                });
    });
   // From an array of objects, extract value of a property as array
   let array_nodes1 = array_nodes.map(a => a.value);
   return array_nodes1;
}



$("#insert_data").click(function(){
      var data_type_file=$('#calculation_type').val();
      console.log('data_type_file',data_type_file)
      var retrievedObject = localStorage.getItem('upload-items');
      var filename =  $('input:file').val().match(/[^\\/]*$/)[0];
      var new_filename=filename.split('.').slice(0, -1).join('.')
      // alert(new_filename);
      var parsedObject_upload_item1 = JSON.stringify(retrievedObject);
      var parsedObject_upload_item = JSON.parse(parsedObject_upload_item1);


      // get object form inner html
    let text = document.getElementById("json_resp").innerText;
    var barchart_JsonString = JSON.parse(text);
    console.log('barchart_JsonString',text)


      var upload_data_type = $("#upload_data_type").val();
      // //console.log('upload-items',parsedObject_upload_item)
      setTimeout(function () {

        var checkData2 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken+"&excel_data=" + parsedObject_upload_item+"&new_filename=" + new_filename+"&upload_data_type=" + upload_data_type;

          // data={'csrfmiddlewaretoken':csrfmiddlewaretoken,'excel_data':text,'new_filename':new_filename,'data_type_file':data_type_file,'brand_report_data': JSON.stringify(parsedObject_upload_item1)};
          data={'csrfmiddlewaretoken':csrfmiddlewaretoken,'new_filename':new_filename,'data_type_file':data_type_file,'excel_data':text};
          // data={'csrfmiddlewaretoken':csrfmiddlewaretoken,'excel_data':text,'new_filename':new_filename,'data_type_file':data_type_file};
          // data={'csrfmiddlewaretoken':csrfmiddlewaretoken,'excel_data':text,'new_filename':new_filename,'data_type_file':data_type_file,'brand_report_data': JSON.stringify(barchart_JsonString)};
          // data={'csrfmiddlewaretoken':csrfmiddlewaretoken,'excel_data':parsedObject_upload_item,'new_filename':new_filename,'brand_report_data': JSON.stringify(parsedObject_upload_item1)};

        respdata2 = autoresponse("upload_data", data);
        // if (respdata2.status  == 200)
        // {
        //   var checkData3 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken;
        //   respdata3 = autoresponse("display_all_data", checkData3);
        //   if (respdata3){
        //    window.location.reload();
        //   }
        
        // }
        // else
        // {
        // alert('Something Went Wrong');
        // }

      }, 100);


});


function drag_and_drop_intial_fun() {
  var options = {
        placeholderCss: {'background-color': '#ff8'},
        hintCss: {'background-color':'#bbf'},
        onChange: function( cEl )
        {
            console.log( 'onChange' );
        },
        complete: function( cEl )
        {
            console.log( 'complete' );
        },
        isAllowed: function( cEl, hint, target )
        {
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

    $('#sTree2').sortableLists( options );
    $('#sTreePlus').sortableLists( optionsPlus );

    $('#toArrBtn').on( 'click', function(){ console.log( $('#sTree2').sortableListsToArray() ); } );
    $('#toHierBtn').on( 'click', function() { console.log( $('#sTree2').sortableListsToHierarchy() ); } );
    $('#toStrBtn').on( 'click', function() { console.log( $('#sTree2').sortableListsToString() ); } );
    $('.descPicture').on( 'click', function(e) { $(this).toggleClass('descPictureClose'); } );

    $('.clickable').on('click', function(e) { alert('Click works fine! IgnoreClass stopped onDragStart event.'); });

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