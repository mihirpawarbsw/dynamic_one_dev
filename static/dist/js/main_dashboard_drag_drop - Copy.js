$(document).ready(function(){
// flag=window.localStorage.getItem('flag');
// if (flag==0) {
//    // window.location.replace("https://forecasting.azurewebsites.net/");
//    window.location.replace("http://127.0.0.1:8000/");
// }

// alert('aa');
var csrfmiddlewaretoken=csrftoken;


   setTimeout(function () { 
			var checkData2 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken;
			respdata2 = autoresponse("display_all_data", checkData2);		
			if (respdata2.status  == 200)
			{
			display_leftside_menu(respdata2);
			// alert('yes');
			}
			else
			{
			alert('no')
			// hidePreloader();//#function modification done by pranit on 25-05-2021
			} 
			
		}, 100);





 $("#docfile1").change(function(e){
            var fileName = e.target.files[0].name;
            $("#country_upload_file1").html(fileName);
          // alert("fileee")

   });



$("#insert_data").click(function(){
	
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

				  data={'csrfmiddlewaretoken':csrfmiddlewaretoken,'excel_data':text,'new_filename':new_filename,'brand_report_data': JSON.stringify(parsedObject_upload_item1)};
				  // data={'csrfmiddlewaretoken':csrfmiddlewaretoken,'excel_data':parsedObject_upload_item,'new_filename':new_filename,'brand_report_data': JSON.stringify(parsedObject_upload_item1)};

				respdata2 = autoresponse("upload_data", data);
				if (respdata2.status  == 200)
				{
					var checkData3 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken;
					respdata3 = autoresponse("display_all_data", checkData3);
					if (respdata3){
					 window.location.reload();
					}
					// var checkData3 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken;	
			  //       respdata3 = autoresponse("displaydata", checkData3);
			   
				}
				else
				{
				alert('Something Went Wrong');
				}

			}, 100);


});

$("#data-display-content").click(function(){
	alert('yesss')
});


function display_leftside_menu(resp){
	// alert('display_leftside_menu')
	console.log('resp',resp)
	// //console.log('lenght',Object.keys(resp['colname_data_dict_final']).length)
	var html= '';
	var i=0;
	var ii=0;
	var j=0;
	$.each(resp['colname_data_dict_final'], function (table_name, value1) {

		console.log('table_name',value1)
		
		var get_all_column_name=Object.keys(value1);
		var data_str = encodeURIComponent(JSON.stringify(value1));
		//console.log('table_name col name',get_all_column_name);
		
    	i++;
		html +='<ul class="subb-menu collapse" id="getting">';
		html +='<li class="child sub-main collapsed drag" data-toggle="collapse" data-target="#t'+i+'">';
		html +='<a class="child"  data-get_all_column_name="'+get_all_column_name+'" onclick="getall_columnname(this)" data-nestedarray='+data_str+'>'+table_name+'</a>';
		html +='</li>';
		$.each(value1, function (columns_name, value2) {
			// //console.log('columns_name',columns_name)
			// //console.log('value2',value2)
			c_data=exract_one_array_object_by_data(value2);
			// //console.log('c_data',c_data)
			ii++;
			j++;
			html +='<ul id="t'+i+'" class="child-sub collapse column'+j+'" >';
			html +='<ul class="subb-menu collapse show" id="getting2">';
			html +='<li class="child sub-main collapsed pl-4 drag" data-toggle="collapse" data-target="#c'+ii+'" >';
			html +='<a class="child" href="#" data-filename="'+table_name+'" data-columnname="'+columns_name+'" data-column_data="'+c_data+'" data-get_all_column_name="'+get_all_column_name+'">'+columns_name+'</a>';
			html +='</li>';
			$.each(value2, function (columns_data, value3) {
				// //console.log('value3',value3)
				html +='<ul id="c'+ii+'" class="child-sub collapse ">';
				html +='<li class="super-sub-menu drag"><a class="child" href="#">'+value3['Column_data']+'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span>'+value3['Count']+' </span>&nbsp;&nbsp;&nbsp;&nbsp;<span>'+value3['Percent']+' </span></a>';
				html +='</li>';
				html +='</ul>'; 
			});
			html +='</ul>';
			html +='</ul>';
		});
		html +='</ul>';
    	
    	
	    $('#display_leftside_menu').html(html);


	    $('.drag').draggable({ 
      appendTo: 'body',
      helper: 'clone'
    });
	//first section 
    $('#dropzone').droppable({
      activeClass: 'active',
      hoverClass: 'hover',
      accept: ":not(.ui-sortable-helper)", // Reject clones generated by sortable
      drop: function (e, ui) {
        var $el = $('<div class="drop-item">' + ui.draggable.text() + '</div>');
        $el.append($('<button type="button" class="btn btn-default btn-xs remove"><span class="glyphicon glyphicon-trash"></span></button>').click(function () { $(this).parent().detach(); }));
        $(this).append($el);
      }
    }).sortable({
      items: '.drop-item',
      sort: function() {
        // gets added unintentionally by droppable interacting with sortable
        // using connectWithSortable fixes this, but doesn't allow you to customize active/hoverClass options
        $( this ).removeClass( "active" );
      }
    });
    //second section
    // $('#dropzone_row').droppable({
    //   activeClass: 'active',
    //   hoverClass: 'hover',
    //   accept: ":not(.ui-sortable-helper)", // Reject clones generated by sortable
    //   drop: function (e, ui) {
    //     var $el = $('<div class="drop-item">' + ui.draggable.text() + '</div>');
    //     $el.append($('<button type="button" class="btn btn-default btn-xs remove"><span class="glyphicon glyphicon-trash"></span></button>').click(function () { $(this).parent().detach(); }));
    //     $(this).append($el);
    //   }
    // }).sortable({
    //   items: '.drop-item',
    //   sort: function() {
    //     // gets added unintentionally by droppable interacting with sortable
    //     // using connectWithSortable fixes this, but doesn't allow you to customize active/hoverClass options
    //     $( this ).removeClass( "active" );
    //   }
    // });
    // main_sorting_function2();
     $('#sTreePlus').droppable({
            activeClass: 'active',
            hoverClass: 'hover',
            accept: ":not(.ui-sortable-helper)", // Reject clones generated by sortable
            drop: function (e, ui) {
                var $el = $('<li id="item_R1" data-module="b" data-value="v1"><div>' + ui.draggable.text() + '</div></li>');
                // $el.append($('').click(function () { $(this).parent().detach(); }));
                $(this).append($el);
                // main_sorting_function1();
                main_sorting_function1();
            // alert('drag')
            }
        })

  



	});
}



function exract_one_array_object_by_data(resp){
	// //console.log('qqqqqqqqqqqqqq',resp)
   var array_nodes = [];
   $.each(resp, function (key, value) {
   	array_nodes.push(value['Column_data']);
   });
   return array_nodes;
}


});// document closed	
var column_name_list=[];
var row_name_list=[];
function get_columnname(resp){
	// alert('get_columnname');
	
	var html= '';
	var i=0;
	var filename = $(resp).attr('data-filename');
	var columnname = $(resp).attr('data-columnname');
	var column_data = $(resp).attr('data-column_data');
	
	column_data_array = column_data.split(',');
	var inner_tablename=$('#datasource_name').html();
	if (filename!=inner_tablename) {
		// alert('yes')
		$('#main_section_menu_list').empty()
		column_name_list=[];
	}
	
	var col_name_exit_check=$.inArray(columnname, column_name_list);
	// //console.log('columnname',columnname);
	// //console.log('column_name_list',column_name_list);
	// //console.log('data',data);
	// //console.log('columnname',columnname);

	if (col_name_exit_check==-1 ) {
			var num = Math.floor(Math.random() * 90000) + 10000;
			

			var ct_ul=$('#mainsection_column_name_store ul li').length;
			// alert(ct_ul)
			
			// alert(inner_tablename)
			
			// if (true) {}
			html +='<ul id="menu_content" class="menu-content out menu_content'+num+'" data-main_section_columnname="'+columnname+'">';
			html +='<ul class="sub-menu  show" id="products">';
			html +='<li class="main " data-toggle="collapse" data-target="#main_menu_sectiion'+num+'"><i class="fas fa-minus ml" onclick="delete_div(this.id)" id="menu_content'+num+'" style="color:red"></i><a href="#">'+columnname+'</a></li>';
			html +='<ul id="main_menu_sectiion'+num+'" class="child-sub collapse">';
			 $.each(column_data_array, function (key, value) {
		   	html +='<li class="sub-menu"><a class="child" href="#">'+value+'</a></li>';
		   });
			html +='</ul>'; 
			html +='</ul>';
			html +='</ul>';
			$('#main_section_menu_list').append(html);
			$('#datasource_name').html(filename);
			// mainsection_column_name_store
			column_name_list.push(columnname);
			row_name_list.push(columnname);
			// //console.log('column_name_list',column_name_list)
			$('#mainsection_column_name_store').html(column_name_list);
			// $('#mainsection_column_name_store ul').append("<li>"+columnname+"</li>");
		}
		//console.log('column_name_list',column_name_list);

		row_and_col_filter(column_name_list)


}


function getall_columnname(resp){
	// alert('dddddd');
		var table_name = $(resp).text();
		$('#source_name').html(table_name)
		var get_all_column_name = $(resp).attr('data-get_all_column_name');
		var get_all_column_name_array = get_all_column_name.split(",");
		var nestedarray = $(resp).attr('data-nestedarray');
		var my_object = JSON.parse(decodeURIComponent(nestedarray));
		// console.log('my_object',my_object)
		
		// section_sorting_row_data(get_all_column_name_array);
		// section_sorting_column_data(get_all_column_name_array);
		row_and_col_filter(get_all_column_name_array)
		base_filter(my_object)
		// main_sorting_function();

	}

function base_filter(resp2) {
	delete resp2['weighting'];
	// console.log('resp2',resp2)
    var optgroups_main=[];
    var new_array=[];
    var i=0
    $.each(resp2, function (col_k, col_val) {
	    var children1=[];
	    select=false;
	    // console.log('col_k',col_k)
    	// if (i==0) {
    	// 	var select=true;
    	// 	// alert('ss')
    	// }
	    
	    	 $.each(col_val, function (col_k1, col_val1) {
	    		 children={label: col_val1['Column_data'], value: col_val1['Column_data'],selected: select}
				 children1.push(children);
			});
		 new_array={label: col_k,id:col_k,children: children1}
	     optgroups_main.push(new_array);   

		i++;
	});
   	console.log('optgroups_main',optgroups_main)
    $('#basefilter').multiselect('dataprovider', optgroups_main); 
    $('#basefilter').multiselect('rebuild');
}

// $("#basefilter").on("change", function() {
//   	var option=[];
//   	var colname=[];
//   	var final1=[];

//     $("option", this).map(function() {
//       if (this.selected) {
//       	option.push(this.value);
//       	colname.push(this.closest("optgroup").label);
//       	var final={'option':option,
//       		'colname':colname
//       	}
//       	final1.push(final)
      		
      	
//       	return final;
//       }
      	
//     }).get()
//  console.log('final',final1)
// })


$("#basefilter").on("change", function() {
  var data=
    $("option", this).map(function() {
      if (this.selected){
      	 return children={optgroup: this.closest("optgroup").label, value: this.value}
      }
    }).get()
  console.log('data',data)
})



// $("#basefilter").on("change", function() {
// 	alert('ss')
//   console.log(
//     $("option", this).map(function() {
//       if (this.selected) return this.value + " " + this.closest("optgroup").label
//     }).get()
//   )
// })



function section_sorting_row_data(resp){

		//####################################row dynamic ui start################################
		var html= '';
		html +='<section id="main_content">';
		html +='<ul id="sTreePlus" class="sTreePlus mV10">';
		$.each(resp, function (k1, val1) {
			html +='<li id="item_R'+k1+'" data-module="b" data-value='+val1+'><div>'+val1+'</div></li>';
		});
		html +='</ul>';
		html +='</section>';
		$("#row_section").empty();
		$('#row_section').html(html);

		//####################################row dynamic ui end################################

}

function section_sorting_column_data(resp){

		//####################################row dynamic ui start################################
		var html1= '';
		html1 +='<section id="main_content">';
		html1 +='<ul class="sTree2 listsClass" id="sTree2">';
		$.each(resp, function (k11, val11) {
			html1 +='<li id="item_C'+k11+'" data-module="b" data-value='+val11+'><div>'+val11+'</div></li>';
		});
		html1 +='</ul>';
		html1 +='</section>';
		$("#column_section").empty();
		$('#column_section').html(html1);

		//####################################row dynamic ui end################################

}



// $('#rowfilter').change(function (){

//     var rowfilter_data =$('#rowfilter').val();
//     //console.log('row filter',rowfilter_data);

//     var size = Object.keys(rowfilter_data).length;
//     if (size>0) {
//     	$("#row_section").empty();



//     	section_sorting_row_data(rowfilter_data);
//     	main_sorting_function1();
//     	// row_main_sorting_function();
//     }else{
//     	alert('Please Select atleast one value...');
//     	$("#row_section").empty();
//     }

// 	});  


// $('#columnfilter').change(function (){

//     var columnfilter_data =$('#columnfilter').val();
//     //console.log('row filter',columnfilter_data);

//     var size = Object.keys(columnfilter_data).length;
//     if (size>0) {
//     	$("#column_section").empty();
//     	section_sorting_column_data(columnfilter_data);
//     	// row_main_sorting_function();
//     	main_sorting_function2();
//     }else{
//     	alert('Please Select atleast one value...');
//     	$("#column_section").empty();
//     }

// 	}); 



// function row_main_sorting_function() {
			   
//         $('#sTree2').sortableLists();
//         $('#sTreePlus').sortableLists();
     
// 		}		


function delete_div(argument) {
	//console.log('argument',argument)
	var deleted_col=$('.'+argument).attr('data-main_section_columnname');
	// column value deleted
	for( var i = 0; i < column_name_list.length; i++){ 
    
        if ( column_name_list[i] === deleted_col) { 
    
            column_name_list.splice(i, 1); 
        }
    
    }

	// row value deleted
	for( var i = 0; i < row_name_list.length; i++){ 
    
        if ( row_name_list[i] === deleted_col) { 
    
            row_name_list.splice(i, 1); 
        }
    
    }

	$('.'+argument).remove();
	//console.log('delete_div',column_name_list)
	//console.log('deleted_col',deleted_col)
	row_and_col_filter(column_name_list);
}


function row_and_col_filter(resp) {
	$("#rowfilter").empty();
	$("#columnfilter").empty();
	$.each(resp, function (k1, val2) {
			$("#rowfilter").append('<option value='+val2+' selected="">'+val2+'</option>');
		});
	$.each(resp, function (k1, val2) {
			$("#columnfilter").append('<option value='+val2+' selected="">'+val2+'</option>');
		});
	 $('#rowfilter').multiselect('rebuild');
	 $('#columnfilter').multiselect('rebuild');
	
}






// ########################################################################################
// ########################################################################################
//sorting code start here



function main_sorting_function() {
        lert('main_sorting_function1')
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

   
    }       


function main_sorting_function1() {
        alert('main_sorting_function1')
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

        // $('#sTree2').sortableLists( options );
        $('#sTreePlus').sortableLists( options );
        // $('#sTreePlus').sortableLists( optionsPlus );

   
    }       




function main_sorting_function2() {
        lert('main_sorting_function2')
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
        
    }       

    
    // $('#toArrBtn').on( 'click', function(){ 
    // 	console.log( 'row array',$('#sTreePlus').sortableListsToArray() ); 
    // } );
    // $('#toArrBtn').on( 'click', function(){ 
    // 	console.log( 'column array',$('#sTree2').sortableListsToArray() ); 
    // } );

    $('#toArrBtn').on( 'click', function(){ 
    	
    	// seperated_flag_row=0;//nested
    	// seperated_flag_col=1;//separate
    	var Row_array_data=$('#sTreePlus').sortableListsToArray();
    	var Column_array_data=$('#sTree2').sortableListsToArray();
    	console.log( 'Row array',Row_array_data); 
    	console.log( 'Column array',Column_array_data); 


    	var row_objecr_grp=groupArrayOfObjects(Row_array_data,"order");
		var Row_array_data_len = Object.keys(Row_array_data).length;
		var row_object_grp_len = Object.keys(row_objecr_grp).length;


		var Column_objecr_grp=groupArrayOfObjects(Column_array_data,"order");
		var Column_array_data_len = Object.keys(Column_array_data).length;
		var Column_object_grp_len = Object.keys(Column_objecr_grp).length;


		console.log('row_objecr_grp row',row_objecr_grp);
		console.log('Value1_size row lenght' ,row_object_grp_len);
		console.log('Row_array_data_len lenght11' ,Row_array_data_len);

		//row condition list
		if (row_object_grp_len===1) {
			var seperated_flag_row=0;
			// alert('seperated_flag_row 0')
		}
		else if(row_object_grp_len>1 && Row_array_data_len==row_object_grp_len){
			var seperated_flag_row=1;
			// alert('seperated_flag_row 1')
		}

		//Column condition list
		if (Column_object_grp_len===1) {
			var seperated_flag_col=0;
			// alert('seperated_flag_row 0')
		}
		else if(Column_object_grp_len>1 && Column_array_data_len==Column_object_grp_len){
			var seperated_flag_col=1;
			// alert('seperated_flag_row 1')
		}

		var Row_array_new= exract_one_array_object_by_data(Row_array_data);
		var Col_array_new= exract_one_array_object_by_data(Column_array_data);
		get_table_resp(Row_array_new,Col_array_new,seperated_flag_row,seperated_flag_col)
		console.log('Row_array_new' ,Row_array_new);
		console.log('Col_array_new' ,Col_array_new);




    } );




function get_table_resp(Row_array_new,Col_array_new,seperated_flag_row,seperated_flag_col) {
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


		localStorage.removeItem("seperated_flag_row");
		localStorage.setItem('seperated_flag_row', seperated_flag_row);

		localStorage.removeItem("seperated_flag_col");
		localStorage.setItem('seperated_flag_col', seperated_flag_col);


		localStorage.removeItem("tbl_name");
		localStorage.setItem('tbl_name', tbl_name);
		// window.location.href = API_URL+'crosstab_dash/';
		window.open(API_URL+'crosstab_dash/', '_blank'); 
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
//sorting code end here    
// ############################################################################################
// ############################################################################################
