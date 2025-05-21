 $(document).ready(function() {
var csrfmiddlewaretoken=csrftoken;

var checkData = "csrfmiddlewaretoken=" + csrfmiddlewaretoken;
respdata = autoresponse("display_users_data", checkData);
if (respdata.status  == 200)
{
  // display_user_table(respdata);
}
else
{
alert('Something went wrong')
}

function display_user_table(resp){

  // console.log('display_users_data',resp['data'])

    // Get reference to the table body
    var tbody = $('#example tbody');
    var html='';
    var i=1;
    $.each(resp['data'], function (k, val) {

      
      // var id=val['Id'];
      console.log('val--->',val)
      html +='<tr>';
      html +='<td>'+i+'</td>';
      html +='<td>'+val['username']+'</td>';
      html +='<td>'+val['email']+'</td>';
      html +='<td>'+val['Role']+'</td>';
      if (val['is_superuser']==true) {
         var is_superuser='Yes';
      }else{
        var is_superuser='No';
      }
      html +='<td>'+is_superuser+'</td>';
      html +='<td><div><a class="mt-1" data-target="#update_user_model1" data-toggle="modal" data-Id='+val['Id']+' data-usertype='+val['is_superuser']+' data-role="'+val['Role']+'" data-username='+val['username']+' data-email='+val['email']+' data-country="'+val['country']+'"   data-category="'+val['category']+'"  onclick="edit_function_call(this);"><i class="fa fa-pencil" aria-hidden="true" style="cursor:pointer"></i></a><a class="mt-1 m-3 text-danger" onclick="deleteUser('+val['Id']+');"><i class="fa fa-trash" aria-hidden="true" style="cursor:pointer"></i></a></div></td>';
      
      html +='</tr>';

      i++;
    });

    tbody.append(html);

    
    new DataTable('#example', {
      responsive: true,
      paging: true, 
      lengthChange: false,
      pageLength : 5,
      dom: 'Bfrtip', // Include buttons in the DOM
      buttons: [
        'excel' // Add Excel download button
      ]
});
    



} //function closed 


});//document end here

function click_add_user(){

  // // alert('add user')
  //  $('#username').prop('readonly', false);
  // $('#email').prop('readonly', false);
  // $('#password').prop('readonly', false);
  // $('#pass_div').removeClass('d-none').addClass('d-block');
  // $('#countrylist_div').removeClass('d-block').addClass('d-none');
  // $('#categorylist_div').removeClass('d-block').addClass('d-none');
  // $("#exampleModalLabel").text('Add User');
  $('#username,#email,#password').val('');
  // $('#hidden_input').val('add_user');

}


function edit_function_call(e){

  
  // alert('id')
  var id=$(e).attr("data-Id")
  var role=$(e).attr("data-role")
  var username=$(e).attr("data-username")
  var email=$(e).attr("data-email")
  var country=$(e).attr("data-country")
  var category=$(e).attr("data-category")
  var usertype=$(e).attr("data-usertype")
 // console.log('role selected111',role)
  var country_selected_obj=category.split(" , ")
  var category_selected_obj=country.split(" , ")

  $('#role1 [value="'+role+'"]').attr('selected', 'true');
  $("#role1").multiselect('rebuild'); 

  var usertype=$(e).attr("data-usertype")
  $('#update_id').val(id);
  var update_id=$('#update_id').val(id);
  $('#username1').prop('readonly', true);
  $('#email1').prop('readonly', true);

  // alert(usertype)
  if (usertype==='true') {
  var ut=1;
  console.log('user_type is True 1')
} else {
  var ut=0;
  console.log('user_type is flase 0')
}
  // $('input[name="user_type1"]').removeAttr('checked');
  $('input:radio[name="user_type1"][value='+ut+']').attr('checked',true);
 
  $('#username1').val(username);
  $('#email1').val(email);
  

  var country1 = new Array();
  country1 = country.split(",");
  var category1 = new Array();
  category1 = category.split(",");



  var csrfmiddlewaretoken=csrftoken;
  var checkData={'csrfmiddlewaretoken':csrfmiddlewaretoken};
  respdata1 = autoresponse("ou_filter_user_module", checkData);
  respdata2 = autoresponse("categoryid_filter", checkData);
  country_filter1(respdata1,role,country1);
  category_filter_list1(respdata2,role,category1);
  // $('#password').html(username);


}


function update_user_data(){

  // alert('hii')
   var csrfmiddlewaretoken=csrftoken;
  var username=$("#username1").val();
  var email=$("#email1").val();
  var user_type=$('input[name="user_type1"]:checked').val();
  var role=$("#role1").val();
  var countrylist=$("#countrylist1").val();
  var categorylist=$("#categorylist1").val();
  var update_id=$('#update_id').val();

  // console.log('categorylist',categorylist)
  // console.log('countrylist',countrylist)
  if (role=='Global Head') {
    var page_access_view='All 4 views';
  }else if(role=='OU Head'){
    var page_access_view='All 4 views';
  }else if(role=='Category Head'){
      var page_access_view='3 views except Sub-Cannel view';
  }else if(role=='Country Head'){
    var page_access_view='All 4 views';
  }



   if (countrylist==null || countrylist=='') {
     swal({
              text: 'Please Select country',
              icon: "error",
              button: "Ok!",
            });
     return false;

  }else if(categorylist==null || categorylist==''){
     swal({
              text: 'Please Select category',
              icon: "error",
              button: "Ok!",
            });
     return false;
  }
     // else if(role==null || role==''){
  //    swal({
  //             text: 'Please Select role',
  //             icon: "error",
  //             button: "Ok!",
  //           });
  //    return false;
  // }


  var checkData={'csrfmiddlewaretoken':csrfmiddlewaretoken,'username':username,'email':email,'user_type':user_type,'role':role,'countrylist':JSON.stringify(countrylist),'categorylist':JSON.stringify(categorylist),'page_access_view':page_access_view,'update_id':update_id};

// var checkData={'csrfmiddlewaretoken':csrfmiddlewaretoken};
        respdata = autoresponse("update_user", checkData);
        if (respdata.code  == 200)
        {
          // $('#example').DataTable().ajax.reload();
         
          swal({
                text: respdata.Message,
                icon: "success",
                button: "Ok!",
              }).then(function(){
                   $('#update_user_model1').modal('hide');
                 location.reload();
              })
        
          
        }
        else
        {
         swal({

                text: respdata.Message,
                icon: "error",
                button: "Ok!",
              });
        }

  
}


function add_user(){

  // alert('add_user')

  var csrfmiddlewaretoken=csrftoken;
  var username=$("#username").val();
  var email=$("#email").val();
  // var password=$("#password").val();
  var user_type=$('input[name="user_type"]:checked').val();
  var role=$("#role").val();
  var countrylist=$("#countrylist").val();
  var categorylist=$("#categorylist").val();


  if (role=='Global Head') {
    var page_access_view='All 4 views';
  }else if(role=='Category Head'){
    var page_access_view='All 4 views';
  }else if(role=='OU Head'){
      var page_access_view='3 views except Sub-Cannel view';
  }else if(role=='Country Head'){
    var page_access_view='All 4 views';
  }

  //

  if (username==null || username=='') {
     swal({
              text: 'Please Select User name',
              icon: "error",
              button: "Ok!",
            });
     return false;

  }else if(email==null || email==''){
     swal({
              text: 'Please Select Email Id',
              icon: "error",
              button: "Ok!",
            });
     return false;
  }
  // else if(password==null || password==''){
  //    swal({
  //             text: 'Please Select Password',
  //             icon: "error",
  //             button: "Ok!",
  //           });
  //    return false;
  // }
  else if(role==null || role==''){
     swal({
              text: 'Please Select Role',
              icon: "error",
              button: "Ok!",
            });
     return false;
  }
  else if(countrylist==null){
     swal({
              text: 'Please Select Country',
              icon: "error",
              button: "Ok!",
            });
     return false;
  }else if(categorylist==null){
     swal({
              text: 'Please Select Category',
              icon: "error",
              button: "Ok!",
            });
     return false;
  }else {

    var checkData={'csrfmiddlewaretoken':csrfmiddlewaretoken,'username':username,'email':email,'user_type':user_type,'role':role,'countrylist':JSON.stringify(countrylist),'categorylist':JSON.stringify(categorylist),'page_access_view':page_access_view };
        respdata = autoresponse("add_user", checkData);
        if (respdata.code  == 200)
        {
          // $('#example').DataTable().ajax.reload();
          // location.reload();
          swal({
                text: respdata.Message,
                icon: "success",
                button: "Ok!",
              }).then(function(){
                   $('#add_user_model').modal('hide');
                 location.reload();
              })
          $( '#userForm' ).each(function(){
              this.reset();
          });
          $('#countrylist_div').removeClass('d-block').addClass('d-none');
          $('#categorylist_div').removeClass('d-block').addClass('d-none');
          $('#add_user_model').modal('hide');
        }
        else
        {
         swal({

                text: respdata.Message,
                icon: "error",
                button: "Ok!",
              });
        }
     
  }
     
} 

function deleteUser(id,e){

  swal({
    title: "Are you sure?",
    text: "Are you sure you want to delete this user!",
    icon: "warning",
    buttons: true,
    dangerMode: true,
  })
  .then((willDelete) => {
    if (willDelete) {

      setTimeout(function () {
        var csrfmiddlewaretoken=csrftoken;
        var checkData={'csrfmiddlewaretoken':csrfmiddlewaretoken,'id':id };
        respdata = autoresponse("deleteUser", checkData);
        if (respdata.status  == 200)
          {
            swal("Username has been deleted successfully!", { icon: "success",});
            location.reload();
          }
      }, 600);

    } else {
      swal("Username is not deleted!");
    }
  });

 
  // if (respdata.status  == 200)
  // {

  //   // location.reload();
  // }
  // else
  // {
  // alert('Something went wrong')
  // }

} 



function country_filter(resp,role){
    console.log('countrylist 216',resp)
    $("#countrylist").empty();
    var i=0;
        $.each(resp['data'], function (key1, value) {
                $("#countrylist").append('<optgroup label="'+key1+'"  class="dropmenu">');
            $.each(value, function (key2, value1) {

                  if (role=='Global Head' || role=='Category Head') {

                    $("#countrylist").append('<option selected value="'+value1[1]+'">'+value1[0]+'</option>');

                  }else if (role=='OU Head' || role=='Country Head') {
                    $("#countrylist").append('<option   value="'+value1[1]+'">'+value1[0]+'</option>');
                  }  
                    
                        
                 
                i++;
            });
            $("#countrylist").append('</optgroup>');
           
        });

     
    if (role=='Global Head' || role=='Category Head') {

      $("#countrylist").multiselect('rebuild'); 
      $("#countrylist").multiselect({
          //  enableClickableOptGroups: true,
         enableFiltering: true,
              maxHeight:400,
              enableCaseInsensitiveFiltering:true,
              enableClickableOptGroups: true,
                 numberDisplayed: 1,
                includeSelectAllOption: true,
                // selectAll: true,
                search   : true,
          });
      $("#countrylist").multiselect('disable'); 

    }else if (role=='OU Head' || role=='Country Head') {
       $("#countrylist").multiselect('enable');
       $("#countrylist").multiselect('rebuild'); 
        $("#countrylist").multiselect({
            //  enableClickableOptGroups: true,
           enableFiltering: true,
                maxHeight:400,
                enableCaseInsensitiveFiltering:true,
                enableClickableOptGroups: true,
                   numberDisplayed: 1,
                  includeSelectAllOption: true,
                  // selectAll: true,
                  search   : true,
            });

    } 

   

}


function category_filter_list(resp,role){
  console.log('category_filter_list-->162',resp)
  $("#categorylist").empty();
    $.each(resp['data'], function (k, val) {
      // console.log('category_filter_list-->val',val)
        if (role=='Global Head' || role=='Country Head' || role=='OU Head') {

           $("#categorylist").append('<option selected value="'+val[0]+'" >'+val[1]+'</option>');

        }else if (role=='Category Head') {
           $("#categorylist").append('<option  value="'+val[0]+'" >'+val[1]+'</option>');
        }  

        // $("#categorylist").append('<option selected value="'+val[0]+'" >'+val[1]+'</option>');
  });


    if (role=='Global Head' || role=='Country Head' || role=='OU Head') {

     $("#categorylist").multiselect('rebuild'); 
      $("#categorylist").multiselect({
        //  enableClickableOptGroups: true,
       enableFiltering: true,
            maxHeight:400,
            enableCaseInsensitiveFiltering:true,
            enableClickableOptGroups: true,
               numberDisplayed: 1,
              includeSelectAllOption: true,
              // selectAll: true,
              search   : true,
        });
      $("#categorylist").multiselect('disable'); 

    }else if (role=='Category Head') {
       $("#categorylist").multiselect('enable');
       $("#categorylist").multiselect('rebuild'); 
        $("#categorylist").multiselect({
        //  enableClickableOptGroups: true,
       enableFiltering: true,
            maxHeight:400,
            enableCaseInsensitiveFiltering:true,
            enableClickableOptGroups: true,
               numberDisplayed: 1,
              includeSelectAllOption: true,
              // selectAll: true,
              search   : true,
        });

    } 


    
}

function searchStringInArray(array, searchString) {
  return array.includes(searchString) ? 1 : 0;
}

function country_filter1(resp,role,selectvalue_country){

     console.log('countrylist 216',resp)
    $("#countrylist1").empty();
    var i=0;
        $.each(resp['data'], function (key1, value) {
                $("#countrylist1").append('<optgroup label="'+key1+'"  class="dropmenu">');
            $.each(value, function (key2, value1) {
                  const searchResult = searchStringInArray(selectvalue_country,value1[0]);

                  if (role=='Global Head' || role=='Category Head') {

                    if (searchResult==1) {
                       $("#countrylist1").append('<option selected value="'+value1[1]+'">'+value1[0]+'</option>');
                    }else{
                       $("#countrylist1").append('<option selected value="'+value1[1]+'">'+value1[0]+'</option>');
                    }

                   

                  }else if (role=='OU Head' || role=='Country Head') {
                    if (searchResult==1) {
                       $("#countrylist1").append('<option selected value="'+value1[1]+'">'+value1[0]+'</option>');
                    }else{
                       $("#countrylist1").append('<option value="'+value1[1]+'">'+value1[0]+'</option>');
                    }
                    // $("#countrylist1").append('<option   value="'+value1[1]+'">'+value1[0]+'</option>');
                  }  
                    
                        
                 
                i++;
            });
            $("#countrylist1").append('</optgroup>');
           
        });

     
    if (role=='Global Head' || role=='Category Head') {

      $("#countrylist1").multiselect('rebuild'); 
      $("#countrylist1").multiselect({
          //  enableClickableOptGroups: true,
         enableFiltering: true,
              maxHeight:400,
              enableCaseInsensitiveFiltering:true,
              enableClickableOptGroups: true,
                 numberDisplayed: 1,
                includeSelectAllOption: true,
                // selectAll: true,
                search   : true,
          });
      $("#countrylist1").multiselect('disable'); 

    }else if (role=='OU Head' || role=='Country Head') {
       $("#countrylist1").multiselect('enable');
       $("#countrylist1").multiselect('rebuild'); 
        $("#countrylist1").multiselect({
            //  enableClickableOptGroups: true,
           enableFiltering: true,
                maxHeight:400,
                enableCaseInsensitiveFiltering:true,
                enableClickableOptGroups: true,
                   numberDisplayed: 1,
                  includeSelectAllOption: true,
                  // selectAll: true,
                  search   : true,
            });

    } 

   

}


function category_filter_list1(resp,role,selectvalue_category){
   console.log('category_filter_list-->162',resp)
  $("#categorylist1").empty();
    $.each(resp['data'], function (k, val) {
      // console.log('category_filter_list-->val',val)
      const searchResult1 = searchStringInArray(selectvalue_category,val[1]);

        if (role=='Global Head' || role=='Country Head' || role=='OU Head') {

           if (searchResult1==1) {
               $("#categorylist1").append('<option selected value="'+val[0]+'">'+val[1]+'</option>');
            }else{
               $("#categorylist1").append('<option selected value="'+val[0]+'">'+val[1]+'</option>');
            }

           // $("#categorylist1").append('<option selected value="'+val[0]+'" >'+val[1]+'</option>');

        }else if (role=='Category Head') {
           if (searchResult1==1) {
               $("#categorylist1").append('<option selected value="'+val[0]+'">'+val[1]+'</option>');
            }else{
               $("#categorylist1").append('<option value="'+val[0]+'">'+val[1]+'</option>');
            }
           // $("#categorylist1").append('<option  value="'+val[0]+'" >'+val[1]+'</option>');
        }  

        // $("#categorylist").append('<option selected value="'+val[0]+'" >'+val[1]+'</option>');
  });


    if (role=='Global Head' || role=='Country Head' || role=='OU Head') {

     $("#categorylist1").multiselect('rebuild'); 
      $("#categorylist1").multiselect({
        //  enableClickableOptGroups: true,
       enableFiltering: true,
            maxHeight:400,
            enableCaseInsensitiveFiltering:true,
            enableClickableOptGroups: true,
               numberDisplayed: 1,
              includeSelectAllOption: true,
              // selectAll: true,
              search   : true,
        });
      $("#categorylist1").multiselect('disable'); 

    }else if (role=='Category Head') {
       $("#categorylist1").multiselect('enable');
       $("#categorylist1").multiselect('rebuild'); 
        $("#categorylist1").multiselect({
        //  enableClickableOptGroups: true,
       enableFiltering: true,
            maxHeight:400,
            enableCaseInsensitiveFiltering:true,
            enableClickableOptGroups: true,
               numberDisplayed: 1,
              includeSelectAllOption: true,
              // selectAll: true,
              search   : true,
        });

    } 


    
}