$(document).ready(function(){
// flag=window.localStorage.getItem('flag');
// if (flag==0) {
//    // window.location.replace("https://forecasting.azurewebsites.net/");
//    window.location.replace("http://127.0.0.1:8000/");
// }

var csrfmiddlewaretoken=csrftoken;

   setTimeout(function () {
   		var retrievedObject = localStorage.getItem('column_name_list_object');
   		var tbl_name1 = localStorage.getItem('tbl_name');
   		var column_name_list_object1_str = JSON.stringify(retrievedObject);
   		var column_name_list_object2_parse = JSON.parse(retrievedObject);
   		// console.log('column_name_list_object',retrievedObject)
   		// console.log('column_name_list_object1',column_name_list_object1)

			var checkData1 = "csrfmiddlewaretoken=" + csrfmiddlewaretoken+"&tbl_name1=" + tbl_name1+"&column_name_list_object1_str=" + column_name_list_object1_str;
			respdata1 = autoresponse("crosstab_table", checkData1);		
			if (respdata1.status  == 200)
			{
			// display_leftside_menu(respdata2);
			alert('yes');
			}
			else
			{
			alert('no')
			// hidePreloader();
			} 
			
		}, 100);


});// document closed