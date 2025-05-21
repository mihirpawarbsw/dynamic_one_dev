$(document).ready(function (e) {
  // if (!$(e.target).closest('.modal').length) {
  //         alert('click outside1!');
  //     }
  //   callback_drag_and_drop_function();
  //     drag_and_drop_intial_fun();
});

var csrfmiddlewaretoken = csrftoken;
var data11 = ["A1", "A2", "A3", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10", "A11", "A12", "A13", "A14", "A14", "A15", "A16", "A17", "A18", "A19", "A20", "A21", "A22", "A23", "A24", "A25", "A26", "A27", "A28", "A29", "A30", "A31", "A32", "A33", "A34"]

var color_code_object = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0];

// var data=['LinkID', 'Country', 'Are_you_comfortable_in_taking_following_survey_in_English_or_any_other_language', 'Do_you_work_in_any_of_these_industries', 'Gender', 'Age', 'Age_:_Post_code', 'Please_select_Items_you_have_at_home_in_working_condition_::_Electricity_connection', 'Please_select_Items_you_have_at_home_in_working_condition_::_Ceiling_fan', 'Please_select_Items_you_have_at_home_in_working_condition_::_LPG_stove','LinkID', 'Country', 'Are_you_comfortable_in_taking_following_survey_in_English_or_any_other_language', 'Do_you_work_in_any_of_these_industries', 'Gender', 'Age', 'Age_:_Post_code', 'Please_select_Items_you_have_at_home_in_working_condition_::_Electricity_connection', 'Please_select_Items_you_have_at_home_in_working_condition_::_Ceiling_fan', 'Please_select_Items_you_have_at_home_in_working_condition_::_LPG_stove','Please_select_Items_you_have_at_home_in_working_condition_::_LPG_stove', 'Please_select_Items_you_have_at_home_in_working_condition_::_Two-wheeler', 'Please_select_Items_you_have_at_home_in_working_condition_::_Colour_TV', 'Please_select_Items_you_have_at_home_in_working_condition_::_Refrigerator', 'weighting'];


let limit;
var selectControl;
var selectionContainer;
var ul;
var searchText;
var deleteSelectedText;
var selectedText;



setTimeout(function () {
  let type = getUrlParameter('type');
  var checkData2 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken + "&type=" + type;;
  respdata2 = autoresponse("display_all_data1", checkData2);
  if (respdata2.status == 200) {
    display_leftside_menu(respdata2);
  }
  else {
    alert('Something went wrong')
  }

}, 100);


// Function to get URL parameters
function getUrlParameter(name) {
  let url = window.location.href;
  name = name.replace(/[\[\]]/g, '\\$&');
  let regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)');
  let results = regex.exec(url);
  if (!results) return null;
  if (!results[2]) return '';
  return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

function display_leftside_menu(resp) {

  console.log('resp', resp)

  var i = 0;
  var ii = 0;
  var j = 0;
  var resp_len = Object.keys(resp['list_all_files']).length;

  var get_all_column_name = Object.keys(resp['list_all_files']);
  // console.log('val1 51',get_all_column_name)
  for (let db = 1; db < 2; db++) {
    var html = '';
    // $('#display_leftside_menu2').empty();
    // console.log('foor loop start ##########################')
    $.each(resp['list_all_files'], function (key1, val1) {

      new_val1 = val1.replace('Consolidated_', ''); // Remove 'Consolidated_' including the trailing underscore
      new_val1 = new_val1.replace('Marketwise_', ''); // Remove 'Marketwise_' if present
      // console.log('id',db)
      // console.log('key1',key1)
      // console.log('val1',val1)
      i++;
      html += '<ul class="subb-menu collapse" id="getting_' + db + '">';
      html += '<li class="child sub-main collapsed" data-toggle="collapse" data-target="#intro' + db + i + '" aria-expanded="false" aria-controls="intro' + db + i + '">';
      html += '<a class="child dealerDetails" aria-expanded="false" aria-controls="dealerDropdown' + db + i + '" href="#dealerDropdown' + db + i + '" data-get_table_name="Electrolux-India filled_less_rows_respondent" onclick="get_all_column_data(this);" data-get_id_name="dealerDropdown' + db + i + '" data-filename="' + val1 + '">' + new_val1 + '</a>';
      html += '</li>';
      html += '<ul id="intro' + db + i + '" class="child-sub collapse" aria-labelledby="intro' + db + i + '" data-parent="#display_leftside_menu1">';  // data-parent attribute links to the accordion container
      html += '<li class="pl-4">';
      html += '<div id="dealerDropdown' + db + i + '" class="dropdown-container child hide bg-transparent border-0">';
      html += '<div class="search bg-transparent">';
      html += '<input type="text" class="search-box"/>';
      html += '</div>';
      html += '<div class="search-result bg-transparent ">';
      html += '<ul class="search-results-list border-0">';
      html += '</ul>';
      html += '</div>';
      html += '</div>';
      html += '</li></ul></ul>';


      $('#display_leftside_menu' + db).html(html);
      // console.log('foor loop end ##########################')
    });
  }

}//function end here


var data1 = [];
var get_id_name;
function get_all_column_data(e) {
  // alert('get_all_column_data')

  $('#sTreePlus').empty();
  $(".blue_class").prop("checked", false);
  $('#sTree2').empty();
  $(".red_class").prop("checked", false);

  // var filename='Electrolux_India'; 
  var filename = $(e).attr("data-filename");
  console.log('data-filename', filename)
  var checkData2 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken + "&filename=" + filename;
  get_id_name = $(e).attr("data-get_id_name");

  respdata = autoresponse("display_all_data", checkData2);
  console.log('respdata 90', respdata)
  if (respdata.status == 200) {
    // console.log('table_name',table_name)
    // console.log('get_id_name',get_id_name)
    // console.log('respdata',respdata)
    // console.log('respdata finale',respdata['colname_dict_final'][table_name]['colname_obj'])
    data = [];
    data = respdata['data_column_names']['filename'];
    // data=respdata['data_column_names_groups'];
    display_all_column_name(filename);
    // drag_and_drop_intial_fun();
    callback_drag_and_drop_function();

  }
  else {
    alert('Something went wrong')
  }

}



function display_all_column_name(filename) {
  // alert('display_all_column_name')


  limit = Math.min(data.length, 100);
  selectControl = $('#delaerDetails');
  selectionContainer = $('.select-container');
  ul = $('#' + get_id_name + ' .search-results-list');
  searchText = $('#' + get_id_name + ' .search-box');
  console.log('searchText', searchText)
  deleteSelectedText = $(".dealerDetails .delete-selected-text");
  selectedText = $(".dealerDetails .selected-text");

  function debounce(fn, wait) {
    let timeout;
    return function () {
      let context = this;
      let argument = arguments
      clearTimeout(timeout);
      timeout = setTimeout(function () {
        fn.apply(context, argument);
      }, wait);
    }
  }

  var displayArray = data.slice(0, limit);
  console.log('==data 139', data)
  let debouncedCreateElements = debounce(createAndAppend, 300);



  function createAndAppend(dataToAppend) {
    // console.log("called, " , dataToAppend);
    // createElement('li', dataToAppend);
    var dataToCreate = dataToAppend

    ul.html('');


    // console.log(dataToCreate, limit);
    console.log('dataToCreate', dataToCreate);

    let main_array = {
      'Fields': [],
      'Values': [],
    };
    dataToCreate.forEach(function (item, index) {
      // console.log('item=== line 145',item)
      // console.log('index=== line 145',index)
      // console.log('color_code_object=== line 145',color_code_object);

      var text_val = item;
      // console.log('text_val',text_val)
      // var check_text_type = text_val.substr(text_val.length - 2); 
      var check_text_type = text_val.substr(text_val.length - 3);
      // console.log('159 check_text_type==',check_text_type)
      if (check_text_type == 'NUM') {

        main_array['Values'].push(item);
        // console.log('check_text_type if');
      } else {

        main_array['Fields'].push(item);
        // console.log('check_text_type elsre');
      }

    });

    loop_id = 0;

    $.each(main_array, function (key_1, val_1) {
      var listHTML = '';
      var listHTML1 = '';
      var random_val = Math.floor(1000 + Math.random() * 9000);
      $.each(val_1, function (key_2, val_2) {

        // console.log('key_1------>',key_1)
        // console.log('val_1------>',val_1)

        var text_val = val_2;
        // console.log('text_val',text_val)
        // var check_text_type = text_val.substr(text_val.length - 2); 
        var check_text_type = text_val.substr(text_val.length - 3);
        // console.log('159 check_text_type==',check_text_type)
        if (check_text_type == 'NUM') {
          var color_code = 'red !important';
          var flag_id = 1;
          var red_class = 'red_class';

          // console.log('check_text_type if');
        } else {
          var color_code = 'blue !important';
          var flag_id = 0;
          var red_class = 'blue_class';

          // console.log('check_text_type elsre');
        }
        var text_val2 = text_val.slice(0, -4);
        // data-target="#intro2"
        // listHTML += `<li class="drag" id=${index}>${dataToCreate[index]}</li>`;
        if (key_1 == 'Fields') {
          listHTML += `<li class="text-left drag child  collapsed text-break border-bottom pl-2" data-filename=${filename}   id=${text_val2}><input   type="checkbox" class="dropdown_text_checkbox ${red_class}" onChange="dropdown_text_checkbox(this)"   data-filename=${filename}  data-color_code="${flag_id}" name="" value="${text_val2}" style="display:inline"><a href="#" data-flag=${flag_id} class="text-wrap" style="color:${color_code}">${text_val2}</a></li>`;
        }
        if (key_1 == 'Values') {
          // type="radio" add for single select Values logic
          listHTML += `<li class="text-left drag child collapsed text-break border-bottom pl-2" data-filename=${filename}   id=${text_val2}><input type="checkbox" class="dropdown_text_checkbox ${red_class}" onChange="dropdown_text_checkbox(this)"   data-filename=${filename}  data-color_code="${flag_id}" name="${random_val}" value="${text_val2}" style="display:inline"><a href="#" data-flag=${flag_id} class="text-wrap" style="color:${color_code}">${text_val2}</a></li>`;
        }



      });

      console.log('main_array------>', main_array)
      // dimension and Values added as a header
      listHTML1 += '<li class="child collapse font-weight-bold py-1 show sub-main text-left" style="font-size:14px;margin-right:6px !important;" data-toggle="collapse" data-target="#subchild_id_' + random_val + '" aria-expanded="true"><a class="child dealerDetails" aria-expanded="false" aria-controls="dealerDropdown1" href="#dealerDropdown1">' + key_1 + '</a></li>';
      ul.append(listHTML1);
      ul.append('<ul id="subchild_id_' + random_val + '" class="collapse search-results-list show sub-menu style-2" style="overflow-y: scroll;height:auto;">' + listHTML + '</ul>');
      // ul.append(listHTML);

      loop_id++;
    });



    callback_drag_and_drop_function()

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
      if (start == 0) {
        start = 0
      } else {
        start = start + 1
      }
      displayArray = [];
      for (var filteredIndex = start; (filteredIndex < arr.length || filteredElements > indexMax); filteredIndex++) {
        // console.log('arr--->',arr)
        // if(arr[filteredIndex].indexOf(text) != -1) {
        if (arr[filteredIndex].search(new RegExp(text, "i")) != -1) {//new code added
          filteredElements++;
          displayArray.push(arr[filteredIndex]);
        }
        if (filteredElements >= indexMax) {

          break;
        }
      }
      lastIndex = filteredIndex;
      return displayArray;
    }
    return filterArray;
  })();

  filterValues();




  ul.on('click', function (event) {
    selectedText.html(event.target.innerHTML);
    selectionContainer.addClass("render-selected-text");
    // alert('8')
    // deleteSelectedText.removeClass("hide");
    // $("#dealerDropdown").toggle();
  });

  deleteSelectedText.on('click', function () {
    setSearchBoxValue('');
    selectedText.html('');
    selectionContainer.removeClass("render-selected-text");
    filterValues();
    deleteSelectedText.addClass("hide");
    // alert('1')

  })

  searchText.on('keyup', function () {
    // alert('3')
    console.log('keyup=== called', searchText)
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

  $('#' + get_id_name + ' .search-result').on('scroll', function () {

    if ($(this).scrollTop() + $(this).innerHeight() >= $(this)[0].scrollHeight) {

      console.log('line 186', this)
      let filteredData = filterArray(data, getSearchBoxValue(), 1)
      // addElementsToUL(filteredData);
      var dataToCreate = filteredData
      var listHTML = '';
      console.log(dataToCreate, limit);

      dataToCreate.forEach(function (item, index) {
        var text_val = dataToCreate[index];
        var check_text_type = text_val.substr(text_val.length - 3);
        var text_val2 = text_val.slice(0, -4);
        if (check_text_type == 'NUM') {
          var color_code = 'red !important';
          var flag_id = 1;
        } else {
          var color_code = 'blue !important';
          var flag_id = 0;
        }
        // data-target="#intro2"
        // listHTML += `<li class="drag" id=${index}>${dataToCreate[index]}</li>`;
        listHTML += `<li class="text-left drag child  collapsed text-break border-bottom" data-filename=${filename}    id=${index}><input   type="checkbox" class="dropdown_text_checkbox" onChange="dropdown_text_checkbox(this)" data-filename=${filename}  data-color_code="${flag_id}" name="${text_val2}" value="${text_val2}" style="display:inline"><a href="#" data-flag=${flag_id} class="text-wrap" style="color:${color_code}">${text_val2}</a></li>`;
        // alert('222')
      });
      ul.append(listHTML);
      callback_drag_and_drop_function();
    }
  })
  $('#' + get_id_name).show();





}//display_all_column_name end here


function dropdown_text_checkbox(e) {
  // alert('hii')
  var get_text = $(e).attr('value');
  var get_color_flag = $(e).attr("data-color_code")
  var get_data_filename = $(e).attr("data-filename")
  // data-color_code="${flag_id}"
  // alert(get_data_filename)

  if ($(e).is(':checked')) {
    // alert('checkd ');
    // Append element start
    // blue color section
    if (get_color_flag == 0) {

      // check where to move column logic start here

      swal({
        title: "Where to move variable filed?",
        buttons: {
          
          moveRow: {
            text: "Add to Row",
            value: "row"
          },
          moveColumn: {
            text: "Add to Column",
            value: "column"
          },
           moveOther: {
            text: "Add to Other",
            value: "other"
          },
          cancel: {
            text: "Cancel",
            value: null, // No specific value for cancel
            visible: true,
            closeModal: true // This closes the modal when cancel is clicked
          }
        }
      }).then((value) => {
        switch (value) {
          case "row":
            // swal("Moving to row section!", "", "success");
            var html = '<p class="drop-item" data-module="b" data-filename=' + get_data_filename + ' data-value="' + get_text + '" style="color: blue;">' + get_text + '<button onclick="delete_element_dimension(this.parentNode)" type="button" class="btn btn-default btn-xs remove" style="color: #fb0000;height: 15px;"><i class="fa fa-times" aria-hidden="true"></i></button></p>';
            $('#sTreePlus').append(html);

            break;
          case "column":
            // swal("Moving to column section!", "", "success");
            var html = '<p class="drop-item" data-module="b" data-filename=' + get_data_filename + ' data-value="' + get_text + '" style="color: blue;">' + get_text + '<button onclick="delete_element_dimension(this.parentNode)" type="button" class="btn btn-default btn-xs remove" style="color: #fb0000;height: 15px;"><i class="fa fa-times" aria-hidden="true"></i></button></p>';
            $('#sTree3').append(html);

            break;
         case "other":
          // swal("Moving to column section!", "", "success");
          var html = '<p class="drop-item" data-module="b" data-filename=' + get_data_filename + ' data-value="' + get_text + '" style="color: blue;">' + get_text + '<button onclick="delete_element_dimension(this.parentNode)" type="button" class="btn btn-default btn-xs remove" style="color: #fb0000;height: 15px;"><i class="fa fa-times" aria-hidden="true"></i></button></p>';
          $('#othervariable').append(html);

          break;
          // default:
          //   swal("Action canceled!");
        }
      });


      // check where to move column logic end here
      // var html = '<p class="drop-item" data-module="b" data-filename=' + get_data_filename + ' data-value="' + get_text + '" style="color: blue;">' + get_text + '<button onclick="delete_element_dimension(this.parentNode)" type="button" class="btn btn-default btn-xs remove" style="color: #fb0000;height: 15px;"><i class="fa fa-times" aria-hidden="true"></i></button></p>';
      // $('#sTreePlus').append(html);
    }
    // Red color section
    else if (get_color_flag == 1) {
      // $('#sTree2').empty(); uncomment for single select Values logic
      var html = '<p class="drop-item" data-module="b" data-filename=' + get_data_filename + ' data-value="' + get_text + '" style="color: red;">' + get_text + '<button onclick="delete_element_facts(this.parentNode)"  type="button" class="btn btn-default btn-xs remove" style="color: #fb0000;height: 15px;"><i class="fa fa-times" aria-hidden="true"></i></button></p>';
      $('#sTree2').append(html);
    }
    // Append element end

  } else {
    // alert('uncheckd ');
    // uncheckd condition start here
    // remove element from dimension section start
    if (get_color_flag == 0) {

      var sTreePlusArray = [];
      $('#row_section ul p').each(function () {

        sTreePlusArray.push($(this).text());
      })
      // console.log('sTreePlus=======> 300',sTreePlusArray)

      // removing matcing element from array
      sTreePlusArray = sTreePlusArray.filter(function (item) {
        return item !== get_text
      })
      // console.log('after removing sTreePlus=======> 300',sTreePlusArray)

      // resetting array in row_section section
      $("#row_section ul").empty();
      $.each(sTreePlusArray, function (key2, value1) {
        $("#row_section ul").append('<p class="drop-item" data-module="b" data-filename=' + get_data_filename + ' data-value="' + value1 + '" style="color: blue;">' + value1 + '<button onclick="delete_element_dimension(this.parentNode)" type="button" class="btn btn-default btn-xs remove" style="color: #fb0000;height: 15px;"><i class="fa fa-times" aria-hidden="true"></i></button></p>');
      });

    }
    // remove element from dimension section end
    // remove element from facts section start
    else if (get_color_flag == 1) {

      var sTree2Array = [];
      $('#column_section ul p').each(function () {

        sTree2Array.push($(this).text());
      })
      // console.log('sTreePlus=======> 300',sTree2Array)

      // removing matcing element from array
      sTree2Array = sTree2Array.filter(function (item) {
        return item !== get_text
      })
      // console.log('after removing sTreePlus=======> 300',sTree2Array)

      // resetting array in row_section section
      $("#column_section ul").empty();
      $.each(sTree2Array, function (key2, value1) {
        $("#column_section ul").append('<p class="drop-item" data-module="b" data-filename=' + get_data_filename + ' data-value="' + value1 + '" style="color: red;">' + value1 + '<button onclick="delete_element_facts(this.parentNode)" type="button" class="btn btn-default btn-xs remove" style="color: #fb0000;height: 15px;"><i class="fa fa-times" aria-hidden="true"></i></button></p>');
      });
    }
    // remove element from facts section end

  }
  callback_drag_and_drop_function();
}//function closed

function delete_element_dimension(parentNode) {
  var dataValue = parentNode.getAttribute('data-value');
  parentNode.remove();
  // $(".red_class").prop("checked", false);
}

function delete_element_facts(parentNode) {
  var dataValue = parentNode.getAttribute('data-value');
  parentNode.remove();
  $(".red_class").prop("checked", false);
}



let filterArray = (function filteringFunction() {
  let lastIndex = 0;
  function filterArray(arr, text, retainIndex) {
    var indexMax = Math.min(arr.length, limit);
    let filteredElements = 0;
    let start = retainIndex ? lastIndex : 0;
    displayArray = [];
    for (var filteredIndex = start; (filteredIndex < arr.length || filteredElements > indexMax); filteredIndex++) {
      if (arr[filteredIndex].indexOf(text) != -1) {
        filteredElements++;
        displayArray.push(arr[filteredIndex]);
      }
      if (filteredElements >= indexMax) {

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
      var table_name = ui.draggable[0].getAttribute("data-filename");
      console.log('table_name 334', ui);
      console.log('ui.draggable.text() 334', ui.draggable);
      var $el = $('<p class="drop-item"  data-module="b" data-filename="' + table_name + '" data-value="' + ui.draggable.text() + '" style="color: black;">' + ui.draggable.text() + '</p>');
      $el.append($('<button type="button" class="btn btn-default btn-xs remove" style="color: #fb0000;height: 15px;"><i class="fa fa-times" aria-hidden="true"></i></button>').click(function () { $(this).parent().detach(); }));
      $(this).append($el);
      // alert('helloo')
      Row_array_data = grouping_div_element();
      // var Row_array_data=$('#sTreePlus').sortableListsToArray();
      find_table_name_dy(Row_array_data);
      // console.log('line 343 Row_array_data',Row_array_data)
    }
  }).sortable({
    items: '.drop-item',
    sort: function () {
      // gets added unintentionally by droppable interacting with sortable
      // using connectWithSortable fixes this, but doesn't allow you to customize active/hoverClass options
      $(this).removeClass("active");
    }
  });

  //SECTION 1  clickable
  $('#sTree2').droppable({
    activeClass: 'active',
    hoverClass: 'hover',
    accept: ":not(.ui-sortable-helper)", // Reject clones generated by sortable
    drop: function (e, ui) {
      var table_name = ui.draggable[0].getAttribute("data-filename");
      console.log('table_name 334', ui);
      // console.log('ui.draggable.text() 334',ui.draggable.text());
      var $el = $('<p class="drop-item"  data-module="b" data-filename="' + table_name + '" data-value="' + ui.draggable.text() + '" style="color: black;">' + ui.draggable.text() + '</p>');
      $el.append($('<button type="button" class="btn btn-default btn-xs remove" style="color: #fb0000;height: 15px;"><i class="fa fa-times" aria-hidden="true"></i></button>').click(function () { $(this).parent().detach(); }));
      $(this).append($el);
      // alert('helloo')
      Measures = measures_div_element();
      // console.log('Measures',Measures)
      // var Row_array_data=$('#sTreePlus').sortableListsToArray();
      find_table_name_dy(Measures);
      // console.log('line 343 Row_array_data',Row_array_data)
    }
  }).sortable({
    items: '.drop-item',
    sort: function () {
      // gets added unintentionally by droppable interacting with sortable
      // using connectWithSortable fixes this, but doesn't allow you to customize active/hoverClass options
      $(this).removeClass("active");
    }
  });



  //SECTION 3  clickable
  $('#sTree3').droppable({
    activeClass: 'active',
    hoverClass: 'hover',
    accept: ":not(.ui-sortable-helper)", // Reject clones generated by sortable
    drop: function (e, ui) {
      var table_name = ui.draggable[0].getAttribute("data-filename");
      console.log('table_name 334', ui);
      // console.log('ui.draggable.text() 334',ui.draggable.text());
      var $el = $('<p class="drop-item"  data-module="b" data-filename="' + table_name + '" data-value="' + ui.draggable.text() + '" style="color: black;">' + ui.draggable.text() + '</p>');
      $el.append($('<button type="button" class="btn btn-default btn-xs remove" style="color: #fb0000;height: 15px;"><i class="fa fa-times" aria-hidden="true"></i></button>').click(function () { $(this).parent().detach(); }));
      $(this).append($el);
      // alert('helloo')
      Measures = measures_div_element();
      // console.log('Measures',Measures)
      // var Row_array_data=$('#sTreePlus').sortableListsToArray();
      find_table_name_dy(Measures);
      // console.log('line 343 Row_array_data',Row_array_data)
    }
  }).sortable({
    items: '.drop-item',
    sort: function () {
      // gets added unintentionally by droppable interacting with sortable
      // using connectWithSortable fixes this, but doesn't allow you to customize active/hoverClass options
      $(this).removeClass("active");
    }
  });


  //SECTION 3  clickable
  $('#sTree4').droppable({
    activeClass: 'active',
    hoverClass: 'hover',
    accept: ":not(.ui-sortable-helper)", // Reject clones generated by sortable
    drop: function (e, ui) {
      var table_name = ui.draggable[0].getAttribute("data-filename");
      console.log('table_name 334', ui);
      // console.log('ui.draggable.text() 334',ui.draggable.text());
      var $el = $('<p class="drop-item"  data-module="b" data-filename="' + table_name + '" data-value="' + ui.draggable.text() + '" style="color: black;">' + ui.draggable.text() + '</p>');
      $el.append($('<button type="button" class="btn btn-default btn-xs remove" style="color: #fb0000;height: 15px;"><i class="fa fa-times" aria-hidden="true"></i></button>').click(function () { $(this).parent().detach(); }));
      $(this).append($el);
      // alert('helloo')
      Measures = measures_div_element();
      // console.log('Measures',Measures)
      // var Row_array_data=$('#sTreePlus').sortableListsToArray();
      find_table_name_dy(Measures);
      // console.log('line 343 Row_array_data',Row_array_data)
    }
  }).sortable({
    items: '.drop-item',
    sort: function () {
      // gets added unintentionally by droppable interacting with sortable
      // using connectWithSortable fixes this, but doesn't allow you to customize active/hoverClass options
      $(this).removeClass("active");
    }
  });

}

// use for both row and column 
function grouping_div_element() {
  var body_object = [];
  var filename1 = $('#sTreePlus p').attr('data-filename');

  $('#sTreePlus p').each(function () {
    // var data = $(this).attr('data-id'); 
    var filename = $(this).attr('data-filename');
    var value = $(this).attr('data-value');
    var ct = 0;
    if (value != "") {
      body_object.push({ ['filename']: filename, ['value']: value });
    }
    // if (ct!=2) {
    //   body_object.push({['filename']:filename,['value']:value});
    // }else{
    //   ct=0;
    // }


    //console.log('body_object deminsion',body_object);

  });
  // body_object.push({['filename']:filename1,['value']:'Time'});
  return body_object;
}

function grouping_div_element_different() {
  var body_object = [];
  var column_section_object = [];
  var othervariable_section_object = [];
  var all_object = [];
  var filename1 = $('#sTreePlus p').attr('data-filename');
  var column_section = $('#sTree3 p').attr('data-filename');
  var othervariable_section = $('#othervariable p').attr('data-filename');

  $('#sTreePlus p').each(function () {
    // var data = $(this).attr('data-id'); 
    var filename = $(this).attr('data-filename');
    var value = $(this).attr('data-value');
    var ct = 0;
    if (value != "") {
      body_object.push({ ['filename']: filename, ['value']: value });
      all_object.push({ ['filename']: filename, ['value']: value });
    }
    //console.log('body_object deminsion',body_object);
  });
  $('#sTree3 p').each(function () {
    // var data = $(this).attr('data-id'); 
    var filename = $(this).attr('data-filename');
    var value = $(this).attr('data-value');
    var ct = 0;
    if (value != "") {
      column_section_object.push({ ['filename']: filename, ['value']: value });
      all_object.push({ ['filename']: filename, ['value']: value });

    }
    //console.log('body_object deminsion',body_object);
  });
  $('#othervariable p').each(function () {
    // var data = $(this).attr('data-id'); 
    var filename = $(this).attr('data-filename');
    var value = $(this).attr('data-value');
    var ct = 0;
    if (value != "") {
      othervariable_section_object.push({ ['filename']: filename, ['value']: value });
      all_object.push({ ['filename']: filename, ['value']: value });
    }
    //console.log('body_object deminsion',body_object);
  });

  // body_object.push({['filename']:filename1,['value']:'Time'});
  return [body_object,column_section_object,othervariable_section_object,all_object];
}
function measures_div_element() {
  var body_object = [];
  $('#sTree2 p').each(function () {
    // var data = $(this).attr('data-id'); 
    var filename = $(this).attr('data-filename');
    var value = $(this).attr('data-value');
    console.log('601 line -->', value)
    // console.log('grouping_div_element 2',$(this).attr('data-filename'),$(this).attr('data-value'));
    body_object.push({ ['filename']: filename, ['value']: value });
    //console.log('body_object meausre',body_object);

  });
  return body_object;
}

$("#dealerDetails111").click(function () {
  // alert('hhh')
  // callback_drag_and_drop_function();
});


function find_table_name_dy(Row_array_data) {
  // console.log('=================find_table_name_dy start===============')
  //console.log('Row_array_data row 250',Row_array_data)
  // console.log('Column_array_data col 250' ,Column_array_data)

  var final_combine_array = [];
  var final_combine_array2 = [];
  //console.log('length Row',Row_array_data.length)
  // console.log('length col',Column_array_data.length)

  if (Row_array_data.length > 0) {
    $.each(Row_array_data, function (key1, value1) {
      // console.log('final_col_array_grp====',key1,value1)
      final_combine_array.push({ [key1]: value1 });
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
  for (var i = 0; i < final_combine_array.length; i++) {
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
  if (keys.length > 0) {
    $('#dropzone').empty();
    $.each(keys, function (k1, v1) {
      // var html='<li class="drop-item" id="item_b1" data-module="b" data-value="cbl_respondent_level"><div>'+v1+'</div></li>'
      var html = '<div class="bg-white border m-2 p-3 pt-2 shadow-sm">' + v1 + '</div>'
      $('#dropzone').append(html)
    });

  }
  // console.log('final_combine_array2 ==== 269',final_combine_array2)
  // console.log('row_array_group ==== 276',row_array_group)
  // console.log('keys',keys)
  // console.log('final_combine_array ==== 262',final_combine_array)
  // console.log('=================find_table_name_dy end===============')

}

$('#clear_all_row').click(function () {
  // alert('yes11')
  $('#sTreePlus').empty();
  $(".blue_class").prop("checked", false);

});


$('#clear_all_column').click(function () {
  // alert('yes11')
  $('#sTree2').empty();
  $(".red_class").prop("checked", false);
});

var measures_div_element4;
$('#toArrBtn').on('click', function () {
  // alert('hmm')
  // var final_combine_array2 = grouping_div_element();
  var resp_object = grouping_div_element_different();
  var final_combine_array2=resp_object[0];
  var column_section_object=resp_object[1];
  var othervariable_section_object=resp_object[2];
  var all_section_object=resp_object[3];
  console.log('final_combine_array2 538', final_combine_array2);
  console.log('column_section_object 538', column_section_object);
  console.log('othervariable_section_object 538', othervariable_section_object);
  // console.log('final_combine_array2 length 538', final_combine_array2.length);
  if (final_combine_array2.length == 0 && column_section_object.length == 0) {
    // alert('Please select atleast one variable in row');
    swal({
      title: "Opps!",
      text: "Please select atleast one variable in Fields!",
      icon: "warning",
    });
    return false;
  }
  final_row_col_array_grp1 = comparing_array_object(final_combine_array2);
  final_row_col_array_grp = sorting_comparing_object(final_row_col_array_grp1)
  console.log('main final_row_col_array_grp1==> 300', final_row_col_array_grp1);
  console.log('main final_row_col_array_grp==> 300', final_row_col_array_grp);

  all_section_object1 = comparing_array_object(all_section_object);
  all_section_object_grp = sorting_comparing_object(all_section_object1);
   console.log('main all_section_object1==> 300', all_section_object1);
  console.log('main all_section_object_grp==> 300', all_section_object_grp);

  // return false;
  var measures_div_element1 = measures_div_element();
  if (measures_div_element1.length == 0) {
    // alert('Please select atleast one variable in row');
    swal({
      title: "Opps!",
      text: "Please select atleast one variable in Facts!",
      icon: "warning",
    });
    return false;
  }
  console.log('main measures_div_element1==> 300', measures_div_element1)
  console.log('main measures_div_element1==> lenght', measures_div_element1.length)
  measures_div_element2 = comparing_array_object(measures_div_element1);
  measures_div_element3 = sorting_comparing_object(measures_div_element2)

  // console.log('measures_div_element2==> 300',measures_div_element2)
  // console.log('measures_div_element3==> 300',measures_div_element3)
  var measures_div_element3_key = Object.keys(measures_div_element3[0]);
  measures_div_element4 = measures_div_element3[0][measures_div_element3_key[0]];

  // console.log('measures_div_element3 300 ',measures_div_element3);
  console.log('measures_div_element3_key 300 ',measures_div_element3_key);
  console.log('measures_div_element4 300 ',measures_div_element4);
  // console.log('final_row_col_array_grp 8451 ',final_row_col_array_grp1);
  // console.log('final_row_col_array_grp 845',final_row_col_array_grp);

  var Row_array_data_len = Object.keys(final_combine_array2).length;
  var row_object_grp_len = Object.keys(final_combine_array2).length;
  console.log('Row_array_data_len lenght11', Row_array_data_len);
  console.log('Value1_size row lenght', row_object_grp_len);
  //row condition list
  // if (row_object_grp_len===1) {
  //   var seperated_flag_row=0;
  //   // alert('seperated_flag_row 0')
  // }
  // else if(row_object_grp_len>1 && Row_array_data_len==row_object_grp_len){
  //   var seperated_flag_row=1;
  //   // alert('seperated_flag_row 1')
  // }
  // var seperated_flag_row = 0;
  // var seperated_flag_col = 0;

  // for stack logic
   var seperated_flag_row = 1;
  var seperated_flag_col = 1;



  var body_data = exract_one_array_object_by_data(final_combine_array2);
  var columnsection_data = exract_one_array_object_by_data(column_section_object);
  var othersection_data = exract_one_array_object_by_data(othervariable_section_object);
  console.log('Row_array_new 548', body_data);
  console.log('columnsection_data 548', columnsection_data);
  console.log('othersection_data 548', othersection_data);
  var table_name1 = [];
  if ($('#dropzone div').length > 1) {

    // $(function() {

    $('#dropzone div').each(function () {
      var tbl_name = $(this).text();
      table_name1.push($(this).text());
    });
    // });

  } else {
    table_name1.push($('#dropzone div').text())
  }
  // console.log('table_name1 563' ,table_name1);
  if (table_name1.length > 1) {
    // table_name1='merged'
    if ((table_name1.length) = 2) {
      var t1 = table_name1[0].split("_").splice(-1)[0]
      var t2 = table_name1[1].split("_").splice(-1)[0]
      if (t1 == t2) {
        // console.log('t1 is  equal to t2')
        table_name1 = 'concat'
      }
      else if (t1 != t2) {
        table_name1 = 'merged'
        // console.log('t1 not  equal to t2')
      }

    }

  } else {
    // console.log('table string',table_name1[0].split("_").splice(-1));
    table_name1 = table_name1[0].split("_").splice(-1)[0]
    // console.log('table string' ,table_name1);
  }
  // console.log('Row_array_new' ,Row_array_new);
  // console.log('Col_array_new' ,Col_array_new);
  // console.log('table_name1 949' ,table_name1);
  // console.log('body_data lenght 520' ,Object.keys(body_data).length);
  // Object.keys(body_data).length;
  // if (Object.keys(body_data).length<2) {

  //    swal({
  //           title: "Opps!",
  //           text: "Please select atleast 2 variable",
  //           icon: "warning",
  //       });
  //     return false;

  // }


  if (Object.keys(body_data).length > 5) {
    // swal({
    //         title: "Warning!",
    //         text: "Please avoid adding >5 variables.",
    //         icon: "warning",
    //     });
    // return false;
    swal({
      title: "Warning",
      text: "Please avoid adding >5 variables.",
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: '#DD6B55',
      confirmButtonText: 'Yes, I am sure!',
      cancelButtonText: "No, cancel it!"
    }).then(
      function () {

        // const Row_array_new = body_data.splice(0, 1);
        // const Col_array_new = body_data.splice(0, 1);
        // const Col_array_new = ['Time'];
          console.log('columnsection_data 548', columnsection_data);
  console.log('othersection_data 548', othersection_data);

        const Row_array_new = body_data;
        const Col_array_new = columnsection_data;
        // body_data = [...new Set(body_data)];//remove duplicates
        othersection_data = [...new Set(othersection_data)];//remove duplicates
        get_table_resp(Row_array_new, Col_array_new, othersection_data, seperated_flag_row, seperated_flag_col, final_row_col_array_grp, table_name1);

      },
      function () { return false; });
  }
  else {

    // const Row_array_new = body_data.splice(0, 1);
    // const Col_array_new = body_data.splice(0, 1);
    // const Col_array_new = ['Time'];
    const Row_array_new = body_data;
    const Col_array_new = columnsection_data;

    // body_data = [...new Set(body_data)];//remove duplicates
    othersection_data = [...new Set(othersection_data)];//remove duplicates
    get_table_resp(Row_array_new, Col_array_new, othersection_data, seperated_flag_row, seperated_flag_col, all_section_object_grp, table_name1);

  }




});//end toArrBtn

function uniqByKeepLast(data, key) {

  return [

    ...new Map(

      data.map(x => [key(x), x])

    ).values()

  ]

}


function sorting_comparing_object(final_row_col_array_grp) {
  // console.log('sorting_comparing_object start', final_row_col_array_grp)
  var respondent = []
  var response = []
  var main_object = []
  $.each(final_row_col_array_grp, function (k11, val22) {
    var last_val_obj = Object.keys(val22)

    var last_val = last_val_obj[0].split("_").pop()
    // console.log('last_val start', last_val)
    if (last_val === 'respondent') {
      respondent.push(val22)
    } else if (last_val === 'response') {
      response.push(val22)
    }
  });

  var respondent1 = Object.keys(respondent).length;
  var response1 = Object.keys(response).length;

  // console.log('respondent lenght', respondent)
  // console.log('respondent lenght', respondent)
  if ((respondent1 >= 2 && response1 == 0)) { main_object = respondent }
  else if ((response1 >= 2 && respondent1 == 0)) { main_object = response }
  else {
    if (respondent1 > 0) { main_object.push(respondent[0]) }
    if (response1 > 0) { main_object.push(response[0]) }
  }


  // console.log('sorting_comparing_object main obj',main_object)
  // return main_object
  return final_row_col_array_grp

}


function comparing_array_object(Row_array_data) {
  // group by table name start
  // console.log('line 300',Row_array_data)
  let row_array_group = Row_array_data.reduce((r, a) => {
    r[a.filename] = [...r[a.filename] || [], a];
    return r;
  }, {});
  // console.log("Row_array_group 973", row_array_group);
  // group by table name end

  var final_row_array_grp = [];
  var final_row_array_grp1 = [];
  $.each(row_array_group, function (k11, val22) {
    // console.log("each loop start",k11, val22);
    var column_arr = [];
    $.each(val22, function (k111, val222) {
      column_arr.push(val222['value'])
    });
    final_row_array_grp.push({ [k11]: column_arr })
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

function get_table_resp(Row_array_new, Col_array_new, remaining_other_array, seperated_flag_row, seperated_flag_col, final_row_col_array_grp, table_name1) {
  // console.log('measures_div_element4 end ',measures_div_element4);
  // console.log('table_name22 ==' ,table_name1);
  // console.log('Row_array_new 444==' ,Row_array_new);
  // console.log('Col_array_new 444==' ,Col_array_new);
  // console.log('remaining_other_array 444==' ,remaining_other_array);
  // console.log('seperated_flag_row 444==' ,seperated_flag_row);
  // console.log('seperated_flag_col 444==' ,seperated_flag_col);
  // console.log('final_row_col_array_grp 444==' ,final_row_col_array_grp);
  // console.log('table_name1 444==' ,table_name1);

  localStorage.clear(); //all items
  var tbl_name = $('#source_name').html();
  // alert(tbl_name)
  if (tbl_name != '') {
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
    // console.log('remaining_other_array old',remaining_other_array)
    // var remaining_other_array1 = [...new Set(remaining_other_array)];
    // console.log('remaining_other_array1 new',remaining_other_array1)
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

    var measures_div_element1 = JSON.stringify(measures_div_element4);
    localStorage.removeItem("wt_measures");
    localStorage.setItem('wt_measures', measures_div_element1);


    var table_name11 = JSON.stringify(table_name1);
    localStorage.removeItem("tbl_name");
    localStorage.setItem('tbl_name', table_name11);


    // localStorage.removeItem("tbl_name");
    // localStorage.setItem('tbl_name', tbl_name);
    // window.location.href = API_URL+'crosstab_dash/';
    window.open(API_URL + 'crosstab_dash/', '_blank');
    // alert('yes') 
    return false;
  }
  else {
    alert('please select data source')
  }


}




function groupArrayOfObjects(list, key) {
  return list.reduce(function (rv, x) {
    (rv[x[key]] = rv[x[key]] || []).push(x);
    return rv;
  }, {});
};


function exract_one_array_object_by_data(resp) {
  var array_nodes = [];
  resp.forEach(function (d) {
    array_nodes.push({
      value: d.value
    });
  });
  // From an array of objects, extract value of a property as array
  let array_nodes1 = array_nodes.map(a => a.value);
  return array_nodes1;
}


// old upload data working commented by pranit
// $("#insert_data").click(function(){
//       var data_type_file=$('#calculation_type').val();
//       console.log('data_type_file',data_type_file)
//       var retrievedObject = localStorage.getItem('upload-items');
//       var filename =  $('input:file').val().match(/[^\\/]*$/)[0];
//       var new_filename=filename.split('.').slice(0, -1).join('.')
//       var parsedObject_upload_item1 = JSON.stringify(retrievedObject);
//       var parsedObject_upload_item = JSON.parse(parsedObject_upload_item1);
//     let text = document.getElementById("json_resp").innerText;
//     var barchart_JsonString = JSON.parse(text);
//       var upload_data_type = $("#upload_data_type").val();
//       setTimeout(function () {
//         var checkData2 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken+"&excel_data=" + parsedObject_upload_item+"&new_filename=" + new_filename+"&upload_data_type=" + upload_data_type;
//           data={'csrfmiddlewaretoken':csrfmiddlewaretoken,'new_filename':new_filename,'data_type_file':data_type_file,'excel_data':text};
//         respdata2 = autoresponse("upload_data", data);
//         if (respdata2.status  == 200)
//         {
//            window.location.reload();
//         }
//         else
//         {
//         alert('Something Went Wrong');
//         }
//       }, 100);
// });


function drag_and_drop_intial_fun() {
  var options = {
    placeholderCss: { 'background-color': '#ff8' },
    hintCss: { 'background-color': '#bbf' },
    onChange: function (cEl) {
      console.log('onChange');
    },
    complete: function (cEl) {
      console.log('complete');
    },
    isAllowed: function (cEl, hint, target) {
      // Be carefull if you test some ul/ol elements here.
      // Sometimes ul/ols are dynamically generated and so they have not some attributes as natural ul/ols.
      // Be careful also if the hint is not visible. It has only display none so it is at the previous place where it was before(excluding first moves before showing).
      if (target.data('module') === 'c' && cEl.data('module') !== 'c') {
        hint.css('background-color', '#ff9999');
        return false;
      }
      else {
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
    placeholderCss: { 'background-color': '#ff8' },
    hintCss: { 'background-color': '#bbf' },
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

  $('#sTree2').sortableLists(options);
  $('#sTreePlus').sortableLists(optionsPlus);

  $('#toArrBtn').on('click', function () { console.log($('#sTree2').sortableListsToArray()); });
  $('#toHierBtn').on('click', function () { console.log($('#sTree2').sortableListsToHierarchy()); });
  $('#toStrBtn').on('click', function () { console.log($('#sTree2').sortableListsToString()); });
  $('.descPicture').on('click', function (e) { $(this).toggleClass('descPictureClose'); });

  $('.clickable').on('click', function (e) { alert('Click works fine! IgnoreClass stopped onDragStart event.'); });

  /* Scrolling anchors */
  $('#toPictureAnch').on('mousedown', function (e) { scrollToAnch('pictureAnch'); return false; });
  $('#toBaseElementAnch').on('mousedown', function (e) { scrollToAnch('baseElementAnch'); return false; });
  $('#toBaseElementAnch2').on('mousedown', function (e) { scrollToAnch('baseElementAnch'); return false; });
  $('#toCssPatternAnch').on('mousedown', function (e) { scrollToAnch('cssPatternAnch'); return false; });

  function scrollToAnch(id) {
    return true;
    $('html, body').animate({
      scrollTop: '-=-' + $("#" + id).offset().top + 'px'
    }, 750);
    return false;
  }
}

function Submit_data() {
  // alert('hiiww');


  var periodical_type = $("#periodical_type").val();
  var que_year = $("#que_year").val();
  var que_period = $("#que_period").val();
  var que_numerical_list = $("#que_numerical_list").val();
  console.log('que_numerical_list===>', typeof (que_numerical_list))
  console.log('que_numerical_list===>', que_numerical_list.length)
  console.log('que_numerical_list key===>', typeof (Object.keys(que_numerical_list).length))

  if (periodical_type === null) {
    // alert('periodical_type empty')
    swal("Please select the  periodical data type from dropdown!");
    $('#periodical_type').css({ 'border': '1px solid red' });
    $('#periodical_type').focus();
    return false;
  } else if (que_year === null) {
    swal("Please select the year column!");
    $('#periodical_type').css({ 'border': '1px solid black' });
    $('#que_year').css({ 'border': '1px solid red' });
    $('#que_year').focus();
    return false;
  } else if (que_period === null) {
    swal("Please select the  period column!");
    $('#que_year').css({ 'border': '1px solid black' });
    $('#que_period').css({ 'border': '1px solid red' });
    $('#que_period').focus();
    return false;
  } else if (Object.keys(que_numerical_list).length === 0 || Object.keys(que_numerical_list).length == 0) {
    swal("Please select the numerical columns!");
    $('#que_year').css({ 'border': '1px solid black' });
    $('#que_period').css({ 'border': '1px solid black' });
    $('#que_numerical_list').css({ 'border': '1px solid red' });
    $('#que_numerical_list').focus();
    return false;
  } else {
    $.LoadingOverlay("show");
    setTimeout(function () {
      var filename = $('#filename_store').text();
      var checkData4 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken + "&periodical_type=" + periodical_type + "&que_year=" + que_year + "&que_period=" + que_period + "&que_numerical_list=" + JSON.stringify(que_numerical_list) + "&filename=" + filename;
      respdata4 = autoresponse("store_questionnaire_format", checkData4);
      if (respdata4) {
        $.LoadingOverlay("hide", true);
        swal({
          title: "Great!",
          text: "Your Data uploaded successfully!!",
          icon: "success",
          showCancelButton: true,
          confirmButtonColor: '#DD6B55',
        }).then(
          function () { location.reload(); },
          function () { return false; }
        );
      }

    }, 1000);

  }
  // console.log('periodical_type==>',periodical_type)
  // console.log('que_year==>',que_year)
  // console.log('que_period==>',que_period)
}

function close_model() {
  // alert('closed')
  $("#questionnaire").addClass("d-none");
  $("#Submit_data").addClass("d-none");
  $("#upload_data_btn").removeClass("d-none");


}

document.addEventListener('click', function (e) {
  if (e.target.className === 'modal') {
    // alert('clicked outside');
    $("#questionnaire").addClass("d-none");
    $("#Submit_data").addClass("d-none");
    $("#upload_data_btn").removeClass("d-none");
  }
}, false);

function show_uploaded_data_in_table() {
  // alert('hey');
  var checkData = "csrfmiddlewaretoken=" + csrfmiddlewaretoken;
  respdata = autoresponse("Show_dataupload_list_table", checkData);
  var html = "";

  console.log('respdata-->', respdata)
  $.each(respdata['data'], function (key, val) {

    var json_resp = JSON.parse(val['uploaded_country_list'])
    console.log('json_resp--->', json_resp)
    var file_upload_input_name = 'file_upload_input_name_' + val['id'];
    var file_upload_input_id = 'file_upload_input_id_' + val['id'];


    html += '<div class="card">';
    html += '<div class="card-header-1 p-2" id="headingOne_' + val['id'] + '">';
    html += '<h2 class="mb-0"><button class="btn btn-link btn-block text-left" type="button" data-toggle="collapse" data-target="#collapseOne_' + val['id'] + '" aria-expanded="true" aria-controls="collapseOne" style="font-size: 13px;text-decoration: none;">' + val['filename'] + '<i class="fa fa-chevron-circle-down fa fa-chevron-circle-down float-lg-right pt-1" aria-hidden="true"></i></button></h2></div>';
    html += '<div id="collapseOne_' + val['id'] + '" class="collapse" aria-labelledby="headingOne_' + val['id'] + '" data-parent="#accordionExample_upload_data_display">';
    html += '<div class="card-body-1 p-3">';
    html += '<div class="row">';
    html += '<div class="border-top col-md-12 mt-3 pt-3">';
    html += '<table class="table table-bordered">';
    html += '<thead>';
    html += '<tr>';
    html += '<th scope="col">List of Market</th>';
    html += '<th scope="col">Latest Quarter</th>';
    html += '<th scope="col">File uploaded on</th>';
    html += '</tr>';
    html += '</thead>';
    html += '<tbody>';
    $.each(json_resp, function (key1, val1) {

      html += '<tr>';
      html += '<td>' + val1['Market'] + '</td>';
      html += '<td>' + val1['Period'] + ' - ' + val1['Year'] + '</td>';
      html += '<td>' + val1['datetime_save'] + '</td>';
      html += '</tr>';

    });
    html += '</tbody>';
    html += '</table></div></div></div></div></div>';

  });

  $('#accordionExample_upload_data_display_list').html(html);

}



