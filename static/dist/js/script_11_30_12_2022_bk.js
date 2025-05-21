// $(document).ready(function(){










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

// var data = ["A1","A2","A3","A3","A4","A5","A6","A7","A8","A9","A10","A11","A12", "A13","A14", "A14","A15", "A16","A17", "A18","A19", "A20","A21", "A22","A23", "A24","A25", "A26","A27", "A28","A29", "A30","A31", "A32","A33", "A34"]

var data=['LinkID', 'Country', 'Are_you_comfortable_in_taking_following_survey_in_English_or_any_other_language', 'Do_you_work_in_any_of_these_industries', 'Gender', 'Age', 'Age_:_Post_code', 'Please_select_Items_you_have_at_home_in_working_condition_::_Electricity_connection', 'Please_select_Items_you_have_at_home_in_working_condition_::_Ceiling_fan', 'Please_select_Items_you_have_at_home_in_working_condition_::_LPG_stove','LinkID', 'Country', 'Are_you_comfortable_in_taking_following_survey_in_English_or_any_other_language', 'Do_you_work_in_any_of_these_industries', 'Gender', 'Age', 'Age_:_Post_code', 'Please_select_Items_you_have_at_home_in_working_condition_::_Electricity_connection', 'Please_select_Items_you_have_at_home_in_working_condition_::_Ceiling_fan', 'Please_select_Items_you_have_at_home_in_working_condition_::_LPG_stove','Please_select_Items_you_have_at_home_in_working_condition_::_LPG_stove', 'Please_select_Items_you_have_at_home_in_working_condition_::_Two-wheeler', 'Please_select_Items_you_have_at_home_in_working_condition_::_Colour_TV', 'Please_select_Items_you_have_at_home_in_working_condition_::_Refrigerator', 'weighting'];


let limit = Math.min(data.length, 7);
var selectControl = $('#delaerDetails');
var selectionContainer = $('.select-container');
var ul = $('#dealerDropdown .search-results-list');
var searchText = $("#dealerDropdown .search-box");


var deleteSelectedText = $(".dealerDetails .delete-selected-text");
var selectedText = $(".dealerDetails .selected-text");






var displayArray = data.slice(0, limit);
let debouncedCreateElements = debounce(createAndAppend, 300);
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
// callback_drag_and_drop_function();

$('.dealerDetails').on('click', function() {
  $("#dealerDropdown").show();
});

function createAndAppend(dataToAppend) {
  console.log("called, " , dataToAppend);
  createElement('li', dataToAppend);
}

function createElement(tagName, dataToCreate) {
  ul.html('');
  addElementsToUL(dataToCreate);
};

function addElementsToUL(dataToCreate) {
  var listHTML = '';
  console.log('===================================================== start');
  console.log(dataToCreate, limit);
  dataToCreate.forEach(function(item, index) {
    // listHTML += `<li class="drag"  id=${index}><a class="btn btn-default">${dataToCreate[index]}</a></li>`;
    listHTML += `<li class="text-left drag child  collapsed text-break border-bottom" data-toggle="collapse" data-target="#intro2"  id=${index}><a href="#" class="text-wrap">${dataToCreate[index]}</a></li>`;
  });
  ul.append(listHTML);
}
function filterValues() {
  let searchedResults = filterArray(data, getSearchBoxValue(), 0);
  debouncedCreateElements(searchedResults);
}

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
  // callback_drag_and_drop_function();
  deleteSelectedText.addClass("hide");
  // alert('1')

})

searchText.on('keyup', function() {
  console.log('keyup=== called')
  
  filterValues();

 
});

function getSearchBoxValue() {
   // alert('setSearchBoxValue')
  return searchText.val();
}

function setSearchBoxValue(value) {

  return searchText.val(value);


}

$('#dealerDropdown .search-result').on('scroll', function() {
  if($(this).scrollTop() + $(this).innerHeight() >= $(this)[0].scrollHeight) {
    let filteredData = filterArray(data, getSearchBoxValue(), 1)
    addElementsToUL(filteredData);
    callback_drag_and_drop_function();
  }
})

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
         // alert('sTreePlus')
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
         // alert('sTree2')
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


// });

 

   

    
}//end function


function callback_drag_and_drop_function2() {
    
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
         // alert('sTreePlus')
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
         // alert('sTree2')
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


// });

 

   

    
}//end function


function section_callbackk() {
  alert('helloo')
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
         alert('sTreePlus')
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
         alert('sTree2')
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



function find_table_name_dy(Row_array_data,Column_array_data){
      console.log('=================find_table_name_dy start===============')
      console.log('Row_array_data row 250',Row_array_data)
      console.log('Column_array_data col 250' ,Column_array_data)

      var final_combine_array=[];
      var final_combine_array2=[];
      console.log('length Row',Row_array_data.length)
      console.log('length col',Column_array_data.length)

        if (Row_array_data.length>0) {
          $.each(Row_array_data, function (key1, value1) {
            // console.log('final_col_array_grp====',key1,value1)
                final_combine_array.push({[key1]:value1});
                // z++;
          });
        }
        if (Column_array_data.length>0) {
          $.each(Column_array_data, function (key1, value1) {
            // console.log('final_col_array_grp====',key1,value1)
                final_combine_array.push({[key1]:value1});
                // z++;
          });
        }
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

$("#table_name").click(function(){
 // alert('hhh')
  callback_drag_and_drop_function();
});
// =====================================================================

// =====================================================================