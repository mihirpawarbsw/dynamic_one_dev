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
			var data_type_file=$('#calculation_type').val();
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

				  data={'csrfmiddlewaretoken':csrfmiddlewaretoken,'excel_data':text,'new_filename':new_filename,'data_type_file':data_type_file,'brand_report_data': JSON.stringify(parsedObject_upload_item1)};
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

var table_column_array=[];
var selected_table_column_array=[];
function display_leftside_menu(resp){
	// alert('display_leftside_menu')
	console.log('resp',resp)
	// //console.log('lenght',Object.keys(resp['colname_data_dict_final']).length)
	var html= '';
	var i=0;
	var ii=0;
	var j=0;
	var resp_len=Object.keys(resp['colname_dict_final']).length;
	console.log('resp_len',resp_len)
	// $.each(resp['colname_dict_final'], function (table_name, value1) {
		var get_all_column_name=Object.keys(resp['colname_dict_final']);
	 for (var w = 0; w<resp_len; w++) {
	 	console.log('loop',w)

		console.log('table_name==>',get_all_column_name[w],'values==>',resp['colname_dict_final'][get_all_column_name[w]])
		const keys = Object.keys(resp['colname_dict_final'])
		// var aa=table_name
		
		// table_column_array.push({
    //         [table_name]: keys
    //     });

		
		// // var data_str = encodeURIComponent(JSON.stringify(value1));
		// console.log('table_name col name',get_all_column_name);
		// console.log('value1',resp['colname_dict_final']);

		i++;
		html +='<ul class="subb-menu collapse" id="getting">';
		html +='<li class="child sub-main collapsed " data-toggle="collapse" data-target="#t'+i+'">';
		html +='<a class="child text-truncate w-75"  data-get_all_column_name="'+get_all_column_name+'"  >'+get_all_column_name[w]+'</a>';
		html +='</li>';
		// $.each(value1['colname_obj'], function (columns_name, value2) {
		var get_all_column_value=Object.values(resp['colname_dict_final'][get_all_column_name[w]]['colname_obj']);
			console.log('get_all_column_value',get_all_column_value)
		for (var ww = 0; ww<get_all_column_value.length; ww++) {
		// 	console.log('value2',value2)
		// 	//console.log('value2',value2)
		// 	// c_data=exract_one_array_object_by_data(value2);
		
			ii++;
			j++;
			html +='<ul id="t'+i+'" class="child-sub collapse column'+j+'" >';
			html +='<ul class="subb-menu collapse show" id="getting2">';
			html +='<li class="child sub-main collapsed pl-4 drag" data-toggle="collapse" data-target="#c'+ii+'"  data-filename="'+get_all_column_name[w]+'">';
			html +='<a class="child text-truncate w-75" data-toggle="tooltip" data-placement="right" title="'+get_all_column_value[ww]+'" href="#" data-filename="'+get_all_column_name[w]+'" data-columnname="'+get_all_column_value[ww]+'" data-get_all_column_name="'+get_all_column_name+'">'+get_all_column_value[ww]+'</a>';
			html +='</li>';
			
			html +='</ul>';
			html +='</ul>';

		// // });
		}
		html +='</ul>';
		   $('#display_leftside_menu').html(html);
		
	// });
		 }

	// console.log('final table array',table_column_array)

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


function display_leftside_menu_for_each_06_12_2022(resp){
	// alert('display_leftside_menu')
	console.log('resp',resp)
	// //console.log('lenght',Object.keys(resp['colname_data_dict_final']).length)
	var html= '';
	var i=0;
	var ii=0;
	var j=0;
	
	$.each(resp['colname_dict_final'], function (table_name, value1) {

		console.log('table_name==>',table_name,'values==>',value1)
		const keys = Object.keys(value1)
		var aa=table_name
		
		table_column_array.push({
            [table_name]: keys
        });

		var get_all_column_name=Object.keys(value1);
		// var data_str = encodeURIComponent(JSON.stringify(value1));
		console.log('table_name col name',get_all_column_name);
		console.log('value1',value1);

		i++;
		html +='<ul class="subb-menu collapse" id="getting">';
		html +='<li class="child sub-main collapsed " data-toggle="collapse" data-target="#t'+i+'">';
		html +='<a class="child text-truncate w-75"  data-get_all_column_name="'+get_all_column_name+'"  >'+table_name+'</a>';
		html +='</li>';
		$.each(value1['colname_obj'], function (columns_name, value2) {
			console.log('value2',value2)
			//console.log('value2',value2)
			// c_data=exract_one_array_object_by_data(value2);
		
			ii++;
			j++;
			html +='<ul id="t'+i+'" class="child-sub collapse column'+j+'" >';
			html +='<ul class="subb-menu collapse show" id="getting2">';
			html +='<li class="child sub-main collapsed pl-4 drag" data-toggle="collapse" data-target="#c'+ii+'"  data-filename="'+table_name+'">';
			html +='<a class="child text-truncate w-75" data-toggle="tooltip" data-placement="right" title="'+value2+'" href="#" data-filename="'+table_name+'" data-columnname="'+value2+'" data-get_all_column_name="'+get_all_column_name+'">'+value2+'</a>';
			html +='</li>';
			
			html +='</ul>';
			html +='</ul>';

		});
		html +='</ul>';
		   $('#display_leftside_menu').html(html);
		
	});

	console.log('final table array',table_column_array)

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
function display_leftside_menu_old_sub_group(resp){
	// alert('display_leftside_menu')
	console.log('resp',resp)
	// //console.log('lenght',Object.keys(resp['colname_data_dict_final']).length)
	var html= '';
	var i=0;
	var ii=0;
	var j=0;
	
	$.each(resp['colname_data_dict_final'], function (table_name, value1) {

		console.log('table_name==>',table_name,'values==>',value1)
		const keys = Object.keys(value1)
		var aa=table_name
		
		table_column_array.push({
            [table_name]: keys
        });

		var get_all_column_name=Object.keys(value1);
		var data_str = encodeURIComponent(JSON.stringify(value1));
		//console.log('table_name col name',get_all_column_name);
		
    	i++;
		html +='<ul class="subb-menu collapse" id="getting">';
		html +='<li class="child sub-main collapsed " data-toggle="collapse" data-target="#t'+i+'">';
		html +='<a class="child text-truncate w-75"  data-get_all_column_name="'+get_all_column_name+'" onclick="getall_columnname(this)" data-nestedarray='+data_str+'>'+table_name+'</a>';
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
			html +='<li class="child sub-main collapsed pl-4 drag" data-toggle="collapse" data-target="#c'+ii+'"  data-filename="'+table_name+'">';
			html +='<a class="child text-truncate w-75" data-toggle="tooltip" data-placement="right" title="'+columns_name+'" href="#" data-filename="'+table_name+'" data-columnname="'+columns_name+'" data-column_data="'+c_data+'" data-get_all_column_name="'+get_all_column_name+'">'+columns_name+'</a>';
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


	});

	console.log('final table array',table_column_array)

	$('.drag').draggable({ 
      appendTo: 'body',
      helper: 'clone'
    });
	// first section 
    // $('#dropzone').droppable({
    //   activeClass: 'active',
    //   hoverClass: 'hover',
    //   accept: ":not(.ui-sortable-helper)", // Reject clones generated by sortable
    //   drop: function (e, ui) {
    //     // var $el = $('<div class="drop-item" >' + ui.draggable.text() + '</div>');
    //     // $el.append($('<button type="button" class="btn btn-default btn-xs remove"><span class="glyphicon glyphicon-trash"></span></button>').click(function () { $(this).parent().detach(); }));
    //     // $(this).append($el);
    //      var $el = $('<li class="drop-item" id="item_b1" data-module="b" data-value="' + ui.draggable.text() + '"><div>' + ui.draggable.text() + '</div></li>');
		//     $el.append($('<button type="button" class="btn btn-default btn-xs remove"><i class="fa fa-minus-square" aria-hidden="true"></i></button>').click(function () { $(this).parent().detach(); }));
		//     $(this).append($el);
		    
		//     // selected_table_column_array.push(ui.draggable.text());
		//      // comparing_two_array(table_column_array,selected_table_column_array);
    //   }
    // }).sortable({
    //   items: '.drop-item',
    //   sort: function() {
    //     $( this ).removeClass( "active" );
    //   }
    // });

   



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

function myFunction(e) {
  alert('yes')
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


$('#clear_all_row').click(function(){
 // alert('yes11')
 $('#sTreePlus').empty();
});


$('#clear_all_column').click(function(){
 // alert('yes11')
 $('#sTree2').empty();
});

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
		// row_and_col_filter(get_all_column_name_array)
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



// function main_sorting_function() {
//         lert('main_sorting_function1')
//         var options = {
//             placeholderCss: {'background-color': '#ff8'},
//             hintCss: {'background-color':'#bbf'},
//             onChange: function( cEl )
//             {
//                 console.log( 'onChange' );
//             },
//             complete: function( cEl )
//             {
//                 console.log( 'complete' );
//             },
//             isAllowed: function( cEl, hint, target )
//             {
//                 // Be carefull if you test some ul/ol elements here.
//                 // Sometimes ul/ols are dynamically generated and so they have not some attributes as natural ul/ols.
//                 // Be careful also if the hint is not visible. It has only display none so it is at the previous place where it was before(excluding first moves before showing).
//                 if( target.data('module') === 'c' && cEl.data('module') !== 'c' )
//                 {
//                     hint.css('background-color', '#ff9999');
//                     return false;
//                 }
//                 else
//                 {
//                     hint.css('background-color', '#99ff99');
//                     return true;
//                 }
//             },
//             opener: {
//                 active: true,
//                 as: 'html',  // if as is not set plugin uses background image
//                 close: '<i class="fa fa-minus c3"></i>',  // or 'fa-minus c3'
//                 open: '<i class="fa fa-plus"></i>',  // or 'fa-plus'
//                 openerCss: {
//                     'display': 'inline-block',
//                     //'width': '18px', 'height': '18px',
//                     'float': 'left',
//                     'margin-left': '-35px',
//                     'margin-right': '5px',
//                     //'background-position': 'center center', 'background-repeat': 'no-repeat',
//                     'font-size': '1.1em'
//                 }
//             },
//             ignoreClass: 'clickable'
//         };

//         var optionsPlus = {
//             insertZonePlus: true,
//             placeholderCss: {'background-color': '#ff8'},
//             hintCss: {'background-color':'#bbf'},
//             opener: {
//                 active: true,
//                 as: 'html',  // if as is not set plugin uses background image
//                 close: '<i class="fa fa-minus c3"></i>',
//                 open: '<i class="fa fa-plus"></i>',
//                 openerCss: {
//                     'display': 'inline-block',
//                     'float': 'left',
//                     'margin-left': '-35px',
//                     'margin-right': '5px',
//                     'font-size': '1.1em'
//                 }
//             }
//         };

//         $('#sTree2').sortableLists( options );
//         $('#sTreePlus').sortableLists( optionsPlus );

   
//     }       


function main_sorting_function1() {
        // alert('main_sorting_function1')
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




// function main_sorting_function2() {
//         lert('main_sorting_function2')
//         var options = {
//             placeholderCss: {'background-color': '#ff8'},
//             hintCss: {'background-color':'#bbf'},
//             onChange: function( cEl )
//             {
//                 console.log( 'onChange' );
//             },
//             complete: function( cEl )
//             {
//                 console.log( 'complete' );
//             },
//             isAllowed: function( cEl, hint, target )
//             {
//                 // Be carefull if you test some ul/ol elements here.
//                 // Sometimes ul/ols are dynamically generated and so they have not some attributes as natural ul/ols.
//                 // Be careful also if the hint is not visible. It has only display none so it is at the previous place where it was before(excluding first moves before showing).
//                 if( target.data('module') === 'c' && cEl.data('module') !== 'c' )
//                 {
//                     hint.css('background-color', '#ff9999');
//                     return false;
//                 }
//                 else
//                 {
//                     hint.css('background-color', '#99ff99');
//                     return true;
//                 }
//             },
//             opener: {
//                 active: true,
//                 as: 'html',  // if as is not set plugin uses background image
//                 close: '<i class="fa fa-minus c3"></i>',  // or 'fa-minus c3'
//                 open: '<i class="fa fa-plus"></i>',  // or 'fa-plus'
//                 openerCss: {
//                     'display': 'inline-block',
//                     //'width': '18px', 'height': '18px',
//                     'float': 'left',
//                     'margin-left': '-35px',
//                     'margin-right': '5px',
//                     //'background-position': 'center center', 'background-repeat': 'no-repeat',
//                     'font-size': '1.1em'
//                 }
//             },
//             ignoreClass: 'clickable'
//         };

//         var optionsPlus = {
//             insertZonePlus: true,
//             placeholderCss: {'background-color': '#ff8'},
//             hintCss: {'background-color':'#bbf'},
//             opener: {
//                 active: true,
//                 as: 'html',  // if as is not set plugin uses background image
//                 close: '<i class="fa fa-minus c3"></i>',
//                 open: '<i class="fa fa-plus"></i>',
//                 openerCss: {
//                     'display': 'inline-block',
//                     'float': 'left',
//                     'margin-left': '-35px',
//                     'margin-right': '5px',
//                     'font-size': '1.1em'
//                 }
//             }
//         };

//         $('#sTree2').sortableLists( options );
        
//     }       

    
//     // $('#toArrBtn').on( 'click', function(){ 
//     // 	console.log( 'row array',$('#sTreePlus').sortableListsToArray() ); 
//     // } );
//     // $('#toArrBtn').on( 'click', function(){ 
//     // 	console.log( 'column array',$('#sTree2').sortableListsToArray() ); 
//     // } );

    $('#toArrBtn').on( 'click', function(){ 
    	// alert('hmm')
    	
    	// seperated_flag_row=0;//nested
    	// seperated_flag_col=1;//separate
    	
    	var Row_array_data=$('#sTreePlus').sortableListsToArray();
    	var Column_array_data=$('#sTree2').sortableListsToArray();
    	// console.log('Row_array_data',Row_array_data)
    	// console.log('Column_array_data',Column_array_data)

    	var final_combine_array=[];
    	var final_combine_array2=[];

	    	$.each(Row_array_data, function (key1, value1) {
	    		// console.log('final_col_array_grp====',key1,value1)
							final_combine_array.push({[key1]:value1});
							// z++;
				});
					$.each(Column_array_data, function (key1, value1) {
	    		// console.log('final_col_array_grp====',key1,value1)
							final_combine_array.push({[key1]:value1});
							// z++;
				});

	    console.log('final_combine_array ==== 808',final_combine_array)
	  	for (var i = 0 ;i < final_combine_array.length; i++) {
				$.each(final_combine_array[i], function (key1, value1) {
					// console.log('final_row_array_grp====',key1,value1)
							final_combine_array2.push(value1);
				});
			}
			console.log('final_combine_array2 ==== 820',final_combine_array2)


    	// var Row_array_data=$('#dropzone_section').sortableListsToArray();
    	// var Column_array_data=$('#sTree2').sortableListsToArray();

    	console.log( 'Row array',Row_array_data); 
    	console.log( 'Column array',Column_array_data); 
    	final_row_col_array_grp1=comparing_array_object(final_combine_array2);
    	final_row_col_array_grp=sorting_comparing_object(final_row_col_array_grp1)
    	console.log('final_row_col_array_grp 8451 ',final_row_col_array_grp1);
    	console.log('final_row_col_array_grp 845',final_row_col_array_grp);
    

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
		console.log('table_name1 949' ,table_name1);
		get_table_resp(Row_array_new,Col_array_new,seperated_flag_row,seperated_flag_col,final_row_col_array_grp,table_name1)
		




    } );


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
			// 		$.each(final_row_array_grp[i], function (k111, val222) {
			// 			// console.log('line 903==>',val222);
			// 		});
			// }

    	// console.log( 'final_row_array_grp line 943',final_row_array_grp); 
    	// group by table name end
    	return final_row_array_grp;

}
function get_table_resp(Row_array_new,Col_array_new,seperated_flag_row,seperated_flag_col,final_row_col_array_grp,table_name1) {
	console.log('table_name22 ==' ,table_name1);
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
