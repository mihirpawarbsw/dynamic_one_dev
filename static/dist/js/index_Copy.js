$(document).ready(function(){



$("#Login_btn").click(function(){
  // alert("The paragraph was clicked.");
var email = $("#email").val();
var password = $("#password").val();
console.log(email,password);
var user="admin";
var pass="F0reca$ting#2!&o2!"
if (email==user && password==pass) {

	// alert('yes');
	window.localStorage.setItem('flag', '1');
	// window.location.replace("http://127.0.0.1:8000/upload");
	window.location.replace("https://forecasting.azurewebsites.net/upload");


}
else{
	// alert('User And Password Is Incorrect');
	swal({title: "Error!",
              text: "Email And Password Is Incorrect!",
              type: "error",
              confirmButtonText: "OK"
            });
}


});

});
