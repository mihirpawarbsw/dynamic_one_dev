$(document).ready(function(){
  callback_drag_and_drop_function();
 });
var csrfmiddlewaretoken=csrftoken;
// var data = [
//   "11111","22","33","444","555","666","777","8888","9999","100","blah","blah2","892/13a","blah","blah2","892/13a","blah","blah2","892/13a","blah","blah2","892/13a","blah","blah2","892/13a","blah","blah2","892/13a","blah","blah2","892/13a","blah","blah2","892/13a","blah","blah2","892/13a","blah","end loop"

// ]

    let limit;
    var selectControl; 
    var selectionContainer;
    var ul;
    var searchText;
    var deleteSelectedText;
    var selectedText;



  setTimeout(function () { 
      var checkData2 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken;  
      respdata2 = autoresponse("display_all_data", checkData2);   
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
  var resp_len=Object.keys(resp['colname_dict_final']).length;

    var get_all_column_name=Object.keys(resp['colname_dict_final']);
   for (var w = 0; w<resp_len; w++) {
    console.log('loop',w)

    console.log('table_name==>',get_all_column_name[w],'values==>',resp['colname_dict_final'][get_all_column_name[w]])
    const keys = Object.keys(resp['colname_dict_final'])
    i++;
    html +='<ul class="subb-menu collapse" id="getting">';
    html +='<li class="child sub-main collapsed " data-toggle="collapse" data-target="#intro'+i+'">';
    html +='<a class="child text-truncate w-75 dealerDetails"  id="'+get_all_column_name[w]+'"   data-get_table_name="'+get_all_column_name[w]+'"  onclick="get_all_column_data(this);" data-get_id_name="dealerDropdown'+w+'">'+get_all_column_name[w]+'</a>';
    html +='</li>';

    html +='<ul id="intro'+i+'" class="child-sub collapse">';
    // html +='<ul class="subb-menu collapse show " id="getting1">';
    html +='<li class="pl-4 " data-target="#intro'+i+'">';
    // html +='<li class="child sub-main collapsed pl-4 " data-target="#intro'+i+'">';
    html +='<div id="dealerDropdown'+w+'" class="dropdown-container child  hide">';
    html +='<div class="search" style="display: none;">';
    html +='<input type="text" class="search-box"/>';
    html +='</div>';
    html +='<div class="search-result">';
    html +='<ul class="search-results-list">';
    html +='</ul>';
    html +='</div></div></li></ul>';


    html +='</ul>';
       $('#display_leftside_menu').html(html);
    
     }


  }

var data=[];
var get_id_name;
function get_all_column_data(e) {

      var checkData2 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken;
      var table_name=$(e).attr("id"); 
      get_id_name=$(e).attr("data-get_id_name"); 

      respdata = autoresponse("display_all_data", checkData2);   
      if (respdata.status  == 200)
      {
        console.log('table_name',table_name)
        console.log('get_id_name',get_id_name)
        console.log('respdata',respdata)
        console.log('respdata finale',respdata['colname_dict_final'][table_name]['colname_obj'])
        data=[];
        data=respdata['colname_dict_final'][table_name]['colname_obj'];
        display_all_column_name()

      }
      else
      {
      alert('Something went wrong')
      }

}


function display_all_column_name() {
  // alert('display_all_column_name')

   limit = Math.min(data.length, 10);
   selectControl = $('#delaerDetails');
   selectionContainer = $('.select-container');
   ul = $('#'+get_id_name+' .search-results-list');
   searchText = $('#'+get_id_name+' .search-box');
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
        console.log("called, " , dataToAppend);
        // createElement('li', dataToAppend);
        var dataToCreate=dataToAppend

        ul.html('');

        var listHTML = '';
        console.log(dataToCreate, limit);
        dataToCreate.forEach(function(item, index) {
          listHTML += `<li class="drag" id=${index}>${dataToCreate[index]}</li>`;
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


    $('#'+get_id_name+' .search-result').on('scroll', function() {
      if($(this).scrollTop() + $(this).innerHeight() >= $(this)[0].scrollHeight) {
        let filteredData = filterArray(data, getSearchBoxValue(), 1)
        // addElementsToUL(filteredData);
        var dataToCreate=filteredData
        var listHTML = '';
        console.log(dataToCreate, limit);
        dataToCreate.forEach(function(item, index) {
          listHTML += `<li class="drag" id=${index}>${dataToCreate[index]}</li>`;
        });
        ul.append(listHTML);
      }
    })
   $('#'+get_id_name).show();





  }//display_all_column_name end





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
  return searchText.val();
}

function setSearchBoxValue(value) {
  return searchText.val(value);
}





// ==========================================================
// ==========================================================

function callback_drag_and_drop_function() {
    

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
        console.log('==============ss',table_name);
        var $el = $('<li class="drop-item " id="item_b1" data-module="b" data-filename="'+table_name+'" data-value="' + ui.draggable.text() + '"><div><span id="clickable">' + ui.draggable.text() + '</span></div></li>');
        // $el.append($('<button type="button" onclick="myFunction()" class="btn btn-default btn-xs remove "><i class="fa fa-minus-square" aria-hidden="true"></i></button>').click(function () { $(this).parent().detach(); }));
        $(this).append($el);
        // console.log('Table section',e);
        var Row_array_data=$('#sTreePlus').sortableListsToArray();
        var Column_array_data=$('#sTree2').sortableListsToArray();
        find_table_name_dy(Row_array_data,Column_array_data)
      console.log('line 201 Row_array_data',Row_array_data)
      console.log('lline 201 Column_array_data',Column_array_data)


      }
    }).sortable({
      items: '.drop-item',
      sort: function() {
        // gets added unintentionally by droppable interacting with sortable
        // using connectWithSortable fixes this, but doesn't allow you to customize active/hoverClass options
        $( this ).removeClass( "active" );
      }
    });

   //SECTION 2
    $('#sTree2').droppable({
      activeClass: 'active',
      hoverClass: 'hover',
      accept: ":not(.ui-sortable-helper)", // Reject clones generated by sortable
      drop: function (e, ui) {
        var table_name=ui.draggable[0].getAttribute("data-filename");
        var $el = $('<li class="drop-item" id="item_b1" data-module="b"  data-filename="'+table_name+'" data-value="' + ui.draggable.text() + '"><div>' + ui.draggable.text() + '</div></li>');
        // $el.append($('<button type="button" class="btn btn-default btn-xs remove"><i class="fa fa-minus-square" aria-hidden="true"></i></button>').click(function () { $(this).parent().detach(); }));
        $(this).append($el);
         var Row_array_data1=$('#sTreePlus').sortableListsToArray();
        var Column_array_data1=$('#sTree2').sortableListsToArray();
          console.log('Row_array_data Row 111',Row_array_data1)
      console.log('length col 111',Column_array_data1)

        // alert('ss')
        find_table_name_dy(Row_array_data1,Column_array_data1)
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