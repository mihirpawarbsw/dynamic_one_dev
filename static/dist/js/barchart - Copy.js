var csrfmiddlewaretoken=csrftoken;
$("#chart_div").click(function (e) {
   // alert('Ooo bhai');

	var checkData = "csrfmiddlewaretoken=" + csrfmiddlewaretoken;
      // get_id_name=$(e).attr("data-get_id_name"); 
      respdata = autoresponse("bar_chart", checkData);
      // console.log('respdata',respdata.data)
      if (respdata.status  == 200)
      {
        // alert('success')
        barchart(respdata);
      }
      else
      {
      alert('Something went wrong')
      }

    $("#chart_Modal").modal("toggle")
});



function barchart(respdata){
	// alert('hii')
	// console.log('respdata',respdata);
	console.log('respdata row',respdata.res_data.index);
	console.log('respdata row',respdata.res_data.columns.length);
	column=[];dataset1=[];datarow=[];row=[];code_frame=[];code_frame1=[];


		for (var r =0; r<respdata.res_data.columns.length ; r++) {
			console.log('data row',r);
			ccol1=[];
			for (var c =0; c<respdata.res_data.index.length ; c++) {
				console.log('data col',c,'row data',r);
				ccol1.push(respdata.res_data.data[c][r]);
				
			}
			console.log('labels',respdata.res_data.columns[r],'col1',ccol1);
			dataset1.push({['label']:respdata.res_data.columns[r],['data']:ccol1});
		}

	for (var x = 0; x < respdata.res_data.index.length; x++) {
		code_frame.push('A'+x);
	}


	console.log('dataset1',dataset1);
	console.log('code_frame',code_frame);
	$('#BarChart').remove();
	$("#barchartdiv").append('<canvas id="BarChart"></canvas>');


	
	const ctx = document.getElementById('BarChart');
	new Chart(ctx, {
	type: 'bar',
	data: {
	  // labels: code_frame,
	  labels: respdata.res_data.index,
	   datasets:dataset1,
	
	},
	   options: {
	  scales: {
	    y: {
	      beginAtZero: true
	    }
	  },
	  tooltips: { mode: 'index', intersect: false }, hover: { mode: 'index', intersect: false }
	}
	});
  
}


// function barchart_bk(){
// // alert('hii')

// 	$('#BarChart').remove();
// 	$("#barchartdiv").append('<canvas id="BarChart"></canvas>');
// 	const ctx = document.getElementById('BarChart');

//   new Chart(ctx, {
//     type: 'bar',
//     data: {
//       labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
//       datasets: [{
//         label: '# of Votes',
//         data: [12, 19, 3, 5, 2, 3],
//         borderWidth: 1,
//                 backgroundColor: [
//           "rgba(10,20,30,0.3)",
//           "rgba(10,20,30,0.3)",
//           "rgba(10,20,30,0.3)",
//           "rgba(10,20,30,0.3)",
//           "rgba(10,20,30,0.3)"
//         ],
//         borderColor: [
//           "rgba(10,20,30,1)",
//           "rgba(10,20,30,1)",
//           "rgba(10,20,30,1)",
//           "rgba(10,20,30,1)",
//           "rgba(10,20,30,1)"
//         ],

//       },
//       {
//         label: '# of Votes',
//         data: [12, 19, 3, 5, 2, 3],
//         borderWidth: 1,
//         backgroundColor: [
//           "rgba(50,150,200,0.3)",
//           "rgba(50,150,200,0.3)",
//           "rgba(50,150,200,0.3)",
//           "rgba(50,150,200,0.3)",
//           "rgba(50,150,200,0.3)"
//         ],
//         borderColor: [
//           "rgba(50,150,200,1)",
//           "rgba(50,150,200,1)",
//           "rgba(50,150,200,1)",
//           "rgba(50,150,200,1)",
//           "rgba(50,150,200,1)"
//         ],
//       }
//      ]
//     },
//        options: {
//       scales: {
//         y: {
//           beginAtZero: true
//         }
//       }
//     }
//   });
  
// }