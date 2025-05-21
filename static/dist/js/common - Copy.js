// var API_URL='https://forecasting.azurewebsites.net/';
// var API_URL='http://127.0.0.1:8000/';
var API_URL='http://52.44.39.143:9000/';
// var excel_download_url="static/";
// var API_URL='https://127.0.0.1:8000/';
// var API_URL='http://127.0.0.1:8000/';
// var API_URL='http://127.0.0.1:8000/';
// var API_URL='https://ietool.brand-scapes.com/';


function autoresponse(zurl,data) {
    var resultobj;
    var result;
    var zapiurl = API_URL + zurl;
    var formData = data;
    $.ajax({
        type: "POST",
        url: zapiurl,
        data: formData,
        dataType: 'json',
        async: !1,
         success: function (data) {
                resultobj = data;
            },
            error: function (textStatus, errorThrown) {
              // alert
               // swal({title: "Error!",
               //    text: "No Data Found Try Another filter!",
               //    type: "error",
               //    confirmButtonText: "OK"
               //  });
               hidePreloader();
            }
    });
   return resultobj;
}

function showPreloader() {
$("#preloader").show();
}

function hidePreloader() {
$("#preloader").hide();
}


// function crosstable_filterdata(){

//     var filter_data=[];
//     var filter1=$("#filter1").val();
//     var filter2=$("#filter2").val();
//     var filter3=$("#filter3").val();
//     var filter4=$("#filter4").val();
//     var filter5=$("#filter5").val();
//     var filter11=$("#filter1").attr("data-filtername");
//     var filter22=$("#filter2").attr("data-filtername");
//     var filter33=$("#filter3").attr("data-filtername");
//     var filter44=$("#filter4").attr("data-filtername");
//     var filter55=$("#filter5").attr("data-filtername");
//     filter_data.push({[filter11]:filter1,[filter22]:filter2,[filter33]:filter3,[filter44]:filter4,[filter55]:filter5});
//     $.each(filter_data[0], function (key1, value1) {
//          console.log('key1  data==>902',key1,'values1==>',value1)
//          let length = Object.keys(value1).length;
//           console.log('length',length)
//           if(length==0){
//                 delete filter_data[0][key1];
//            }
//         });
//     return filter_data;
// }


function crosstable_filterdata(){

    var filter_data=[];
    var filter1=$("#filter1").val();
    var filter2=$("#filter2").val();
    var filter3=$("#filter3").val();
    var filter4=$("#filter4").val();
    var filter5=$("#filter5").val();
    var filter11=$("#filter1").attr("data-filtername");
    var filter22=$("#filter2").attr("data-filtername");
    var filter33=$("#filter3").attr("data-filtername");
    var filter44=$("#filter4").attr("data-filtername");
    var filter55=$("#filter5").attr("data-filtername");
    // filter_data.push({[filter11]:filter1,[filter22]:filter2,[filter33]:filter3,[filter44]:filter4,[filter55]:filter5});
  //   filter_data.push({[filter11]:filter1});
  // console.log('1111 filter2 function',typeof(filter1.length))
    
    
    
    
    if((filter1.length)!=0 && (filter2.length)!=0 && (filter3.length)!=0 && (filter4.length)!=0 && (filter5.length!=0)) {
         filter_data.push({[filter11]:filter1,[filter22]:filter2,[filter33]:filter3,[filter44]:filter4,[filter55]:filter5});
    }
    else if((filter1.length)!=0 && (filter2.length)!=0 && (filter3.length)!=0 && (filter4.length!=0)) {
         filter_data.push({[filter11]:filter1,[filter22]:filter2,[filter33]:filter3,[filter44]:filter4});
    }
    else if((filter1.length)!=0 && (filter2.length)!=0 && (filter3.length!=0)) {
         filter_data.push({[filter11]:filter1,[filter22]:filter2,[filter33]:filter3});
    }
    else if((filter1.length!=0) && (filter2.length!=0)) {
         filter_data.push({[filter11]:filter1,[filter22]:filter2});
    }
    else if((filter1.length)!=0) {
         filter_data.push({[filter11]:filter1});
    }

    // console.log('1111 filter2 function',filter2.length)
    // console.log('1111 filter2 function',typeof(filter2))
    // console.log('1111 crosstable_filterdata function',filter_data)


    $.each(filter_data[0], function (key1, value1) {
         // console.log('key1  data==>902',key1,'values1==>',value1)
         let length = Object.keys(value1).length;
          // console.log('length',length)
          if(length==0){
                delete filter_data[0][key1];
           }
        });

    // console.log('crosstable_filterdata function',filter_data)
    return filter_data;
}
// #################################################################################################################
// #################################################################################################################
// table display logic start
function createNestedStructure(data) {
    const hierarchicalData = {};

    data.forEach(entry => {
        let currentLevel = hierarchicalData;

        for (let i = 0; i < entry.length - 1; i++) {
            const key = entry[i];

            if (!currentLevel[key]) {
                currentLevel[key] = {};
            }

            currentLevel = currentLevel[key];
        }

        // Set the last key to the last value in the entry
        const lastKey = entry[entry.length - 1];
        currentLevel[lastKey] = lastKey;
    });

    return hierarchicalData;
}
function getNestedLevels(obj, level = 0) {
    let maxLevel = level;

    for (const key in obj) {
        if (typeof obj[key] === 'object') {
            const childLevel = getNestedLevels(obj[key], level + 1);
            maxLevel = Math.max(maxLevel, childLevel);
        }
    }

    return maxLevel;
}

function hasMatchingSubstring(string) {


    const matchingArray = ['Growth', 'Share bps', 'Sales Share','Sales Share YA'];


    for (let i = 0; i < matchingArray.length; i++) {
        if (string.includes(matchingArray[i]) ) {
            return string + '(%)'; // If any element matches, return true
        }
    }
    return string; // If no match found, return false
}

// function hasMatchingSubstring(string) {
//     const matchingArray = ['Growth', 'Sales Share', 'Sales Share YA'];
//     const notMatchingArray = ['bps Chg', 'Share bps', 'Exclude3'];

//     for (let i = 0; i < matchingArray.length; i++) {
//         if (string.includes(matchingArray[i])) {
//             return string + '(%)'; // If any element matches, return true
//         }
//     }

//     for (let i = 0; i < notMatchingArray.length; i++) {
//         if (string.includes(notMatchingArray[i])) {
//             return string; // If any element matches, return false
//         }
//     }

//     return string; // If no match found, return false
// }




// This function is currently not using in tool
function header_nested_logic(html,group_column_resp,single_row_length,row_str,columns_data,resp){
    
    html2='';html3='';
    html +='<thead class="thead-dark">';
    html +='<tr>';
    // cif condition added for row lenght missmatch case
    html +='<th scope="col" class="align-baseline text-lg-center 1 align-middle" colspan='+single_row_length+' rowspan="3">'+row_str+'</th>';
    console.log('main group_column_resp--->985',group_column_resp)

        const group_column_resp_result = createNestedStructure(columns_data);
        const numberOfLevels = getNestedLevels(group_column_resp_result);
        console.log('group_column_resp_result 990',group_column_resp_result)
        // var grp_len=val1.length; 
        console.log('numberOfLevels',numberOfLevels)
        $.each(group_column_resp_result, function (k2, val2) {
            console.log('1st each loop start===========================================');
            console.log('group_column_resp_result type k2',k2);
            console.log('group_column_resp_result type val2',val2);
            var val2_count=Object.keys(group_column_resp[k2]).length;
            html +='<th scope="col"  class="align-baseline text-lg-center 1"  colspan='+val2_count+'>'+k2+'</th>';
            $.each(val2, function (k3, val3) {
            
                console.log('key3------------>',k3);
                console.log('val3------------>',val3);
                var val3_count=Object.keys(val3).length;
                html2 +='<th scope="col"  class="align-baseline text-lg-center 1"  colspan='+val3_count+'>'+k3+'</th>';

                $.each(val3, function (k4, val4) {
                    html3 +='<th scope="col"  class="align-baseline text-lg-center 1" >'+k4+'</th>';
                });
            });
            console.log('1st each loop end===========================================');
        });
    // html +='</tr>';
    html +='</tr>';
    html +=html2+'</tr>';
    html +=html3+'</tr>';
    html +='</thead>';
    return html;
}



function header_stacked_logic(html,group_column_resp,single_row_length,row_str,columns_data,resp){
    var column_length=resp['df_cross_json']['columns'][0].length
    var dropdown_match_index_key=[];
    html2='';html3='';
    html +='<thead class="thead-dark">';
    html +='<tr>';
    // cif condition added for row lenght missmatch case
    html +='<th scope="col" class="text-lg-center 1 align-baseline" colspan='+single_row_length+' rowspan="3">'+row_str+'</th>';
    // console.log('resp lenght--->985',resp['df_cross_json']['columns'][0].length)
    // console.log('main response group_column_resp--->985',group_column_resp)
   
        const group_column_resp_result = createNestedStructure(columns_data);
        const numberOfLevels = getNestedLevels(group_column_resp_result);
        // console.log('group_column_resp_result 990',group_column_resp_result)
       
        // console.log('numberOfLevels',numberOfLevels)
        var header_i=0;
        var header_iL2=0;
        $.each(group_column_resp_result, function (k2, val2) {
             var grp_len=group_column_resp[k2].length;
            html +='<th scope="col"  class="text-lg-center 2"  colspan='+grp_len+'>'+k2+'</th>';
            
            $.each(val2, function (k3, val3) {
                var val3_count=Object.keys(val3).length;
                if (column_length==2) {
                    var val3_count=0;

                     // facts color code start
                    // var get_facts_colorizer_object=$("#facts_coorizer_div_array").html();
                    // if (get_facts_colorizer_object!="") {
                    //     var get_facts_colorizer_json=JSON.parse(get_facts_colorizer_object);
                    //      // console.log('get_facts_colorizer_json',get_facts_colorizer_json)
                    //     var matchingValues = getMatchingValues_facts_in_row_level(header_iL2,get_facts_colorizer_json,k2,k3,0);
                    //     dropdown_match_index_key.push(matchingValues);
                    //     console.log("===========================================================");
                    //     console.log("266 matchingValues--->",matchingValues)

                    //     console.log("Index",header_iL2);
                    //     console.log("1st level",k2);
                    //     console.log("2nd level",k3);
                    //     console.log("get_stored_object_json:1000",get_facts_colorizer_json);
                    //     console.log("===========================================================");

                    // }

                // facts color code end

                }

                html2 +='<th scope="col"  class="align-baseline text-lg-center 3"  colspan='+val3_count+'>'+k3+'</th>';

                if (column_length==3) {
                    var k4i=0
                    $.each(val3, function (k4, val4) {

                        if (k4i===0) {
                            header_i=header_i;
                        }if (header_i===0) {
                            header_i=k4i;
                        }

                        var get_facts_colorizer_object=$("#facts_coorizer_div_array").html();

                        if (get_facts_colorizer_object!="") {
                            var get_facts_colorizer_json=JSON.parse(get_facts_colorizer_object);
                             // console.log('get_facts_colorizer_json',get_facts_colorizer_json)
                            var matchingValues = getMatchingValues(header_i,get_facts_colorizer_json,k2,k3,val4,0,k2);
                            dropdown_match_index_key.push(matchingValues);
                            // console.log("===========================================================");
                            // console.log("266 matchingValues--->",matchingValues)
                            //  console.log("type get_facts_colorizer_object",typeof(get_facts_colorizer_object))
                            // console.log("Index",header_i);
                            // console.log("1st level",k2);
                            // console.log("2nd level",k3);
                            // console.log("3rd level",val4);
                            // console.log("get_stored_object_json:1000",get_facts_colorizer_json);
                            // console.log("k2",k2);
                            // console.log("===========================================================");

                        }
                           
                                // if (matchingValues) {
                                //     matchingValues['index']=header_i;
                                //     // console.log("if condition Matching Values:1000",key1+'===='+ matchingValues);
                                //     // var item = {
                                //     //     value: text,
                                //     //     min: minValueInput.val(),
                                //     //     max: maxValueInput.val(),
                                //     //     index:key2,
                                //     // };

                                //     dropdown_match_index_key.push(matchingValues);
                                // }
                        
                        // }

                        // html3 +='<th scope="col"  class="align-baseline text-lg-center 4" >'+header_i + ' -->'+ hasMatchingSubstring(val4)+'</th>';
                        html3 +='<th scope="col"  class="align-baseline text-lg-center 4" >'+ val4+'</th>';
                        header_i++;
                        k4i++;
                    });  
                }
                   header_iL2++;
            });

        });
                
    $("#dropdown_range_filter").html(JSON.stringify(dropdown_match_index_key));
    html +='</tr>';
    html +=html2+'</tr>';
    if (column_length==3) {
        html +=html3+'</tr>';
    }
    
    html +='</thead>';
    return html;
}


// Function to check if a given string matches any value in the array
function getMatchingValues(index,facts_colorizer_array,L1,L2,L3,flag,tpname) {
    
    // console.log('index-->',index,'<--facts_colorizer_array-->',facts_colorizer_array,'<--L1-->',L1,'<--L2-->',L2,'<--L3-->',L3,'<--tpname-->',tpname)
   
    // return false;
    if (flag===0) {
      
        for (var i = 0; i < facts_colorizer_array.length; i++) {
        if (L3 === facts_colorizer_array[i].factsvalue) {
            return {
                tp_name: facts_colorizer_array[i].tp_name,
                factsheader: facts_colorizer_array[i].factsheader,
                factsvalue: facts_colorizer_array[i].factsvalue,
                input1: facts_colorizer_array[i].input1,
                input2: facts_colorizer_array[i].input2,
                index:index,
                };
            }
        }
        return {};
    }
    if(flag===1){


    //       console.log("start ===========================================================");
    // console.log('index--->',index)
    // console.log('facts_colorizer_array--->',facts_colorizer_array)
    // console.log('facts_colorizer_array length--->',facts_colorizer_array[index]['index'])
     
     if ((Object.keys(facts_colorizer_array[index]).length !== 0)) {

        if(index ==  facts_colorizer_array[index]['index']) {
            return {
                tp_name: facts_colorizer_array[index]['tp_name'],
                factsheader: facts_colorizer_array[index]['factsheader'],
                factsvalue: facts_colorizer_array[index]['factsvalue'],
                input1: facts_colorizer_array[index]['input1'],
                input2: facts_colorizer_array[index]['input2'],
                index: index
                };
            }else{

                return null;

            }
        }

        // console.log("end ===========================================================");

     }
        
        

   

}

function getMatchingValues_facts_in_row_level(facts_colorizer_array,RL2,measure) {
    
    // console.log('index-->',index,'<--facts_colorizer_array-->',facts_colorizer_array,'<--L1-->',L1,'<--L2-->',L2,'<--L3-->',L3)
   // console.log("start ===========================================================");
   //  console.log('index--->',index)
   //  console.log('facts_colorizer_array--->',facts_colorizer_array)
   //  console.log('L2--->',L2)
   //  console.log('L3--->',L3)
    // return false;
    if (facts_colorizer_array.length>0) {
      
        for (var i = 0; i < facts_colorizer_array.length; i++) {
        if (measure === facts_colorizer_array[i].factsvalue) {
            return {
                tp_name: facts_colorizer_array[i].tp_name,
                factsheader: facts_colorizer_array[i].factsheader,
                factsvalue: facts_colorizer_array[i].factsvalue,
                input1: facts_colorizer_array[i].input1,
                input2: facts_colorizer_array[i].input2,
                rl2: RL2,
                measure: measure,
                };
            }
        }
        return {};
    }else{
         return {};
    }



}

function find_match_facts_colorizer_value(data,searchText) {
    
    for (let i = 0; i < data.length; i++) {
      if (data[i].factsvalue === searchText) {
        // console.log("Value is true");
        // Do something if value is true
        return data[i];
      } else {
        // console.log("Value is false");
        // Do something if value is false
        return 0;
      }
    }
}

// Sorting function of current time period filter
function customSort(a, b) {
    if (a.includes('QUARTER')) return -1; // 'QUARTER' should come first
    if (b.includes('QUARTER')) return 1;  // 'QUARTER' should come first
    if (a.includes('YTD')) return -1;     // 'YTD' should come second
    if (b.includes('YTD')) return 1;      // 'YTD' should come second
    if (a.includes('MAT')) return -1;     // 'MAT' should come third
    if (b.includes('MAT')) return 1;      // 'MAT' should come third
    return 0;  // If none of the above conditions match, keep them in the same order
}


function replace_CY_YA_string(original_string,current_time_period_resp,comparative_time_period_resp) {
    if (original_string.includes("CY")) {
         var replace_string = original_string.replace("CY",current_time_period_resp.replace("QUARTER", ""));
    }
    else if (original_string.includes("YA")) {
         var replace_string = original_string.replace("YA",comparative_time_period_resp.replace("QUARTER", ""));
    }
    else {
         var replace_string = original_string;
    }
    return {replace_string,original_string};
 }


function getSelectedValues_facts_filter() {
    var selectedValues = {};
    var selectElement = document.getElementById("facts_group_filter");
    var optgroups = selectElement.getElementsByTagName("optgroup");
    
    for (var i = 0; i < optgroups.length; i++) {
        var options = optgroups[i].getElementsByTagName("option");
        var selectedOptions = [];
        
        for (var j = 0; j < options.length; j++) {
            if (options[j].selected) {
                selectedOptions.push(options[j].value);
            }
        }
        
        selectedValues[optgroups[i].label] = selectedOptions;
    }
    console.log('before selectedValues 511',selectedValues)
    // Update the data object
    // var final_data=updateSalesData(selectedValues);
    const data = {
    "Sales (M JPY)": [
        "Sales (M JPY)_QUARTER Q4 2023",
        "Sales (M JPY)_Sales Share QUARTER Q4 2023(%)",
        "Sales (M JPY)_Sales Growth vs QUARTER Q1 2019(%)"
    ],
    "Other Data": [
        "Other Data Growth vs Some Date"
    ],
    "Not an Array": "This should not be changed"
};

    console.log('after selectedValues 511',updateSalesData(data))
    return selectedValues;
}



function updateSalesData(data) {
    // Iterate over each property in the data object
    Object.keys(data).forEach(key => {
        if (Array.isArray(data[key])) {
            data[key] = data[key].map(entry => {
                if (entry.includes("Growth")) {
                    const index = entry.indexOf("vs");
                    if (index !== -1) {
                        // Replace everything after "vs" with "QUARTER Q4 2030(%)"
                        return `${entry.substring(0, index + 3)}QUARTER Q4 2030(%)`;
                    }
                }
                return entry; // Return the entry unchanged if no "Growth" or "vs" is found
            });
        }
    });
}

 // Function to update entries containing "Growth" in any key of the data object
function updateSalesData_old(data) {
    // console.log('data--->',data1)
    // data={
    //     "Sales (M JPY)": [
    //         "Sales (M JPY)_QUARTER Q4 2023",
    //         "Sales (M JPY)_Sales Share QUARTER Q4 2023(%)",
    //         "Sales (M JPY)_Sales Growth vs QUARTER Q1 2019(%)"
    //     ]
    // }
    // Iterate over each property in the data object
    for (const key in data) {
        if (Array.isArray(data[key])) {
            data[key] = data[key].map(entry => {
                if (entry.includes("Growth")) {
                    const index = entry.indexOf("vs");
                    if (index !== -1) {
                        // Replace everything after "vs" with "QUARTER Q4 2030(%)"
                        return `${entry.substring(0, index + 3)}QUARTER Q4 2030(%)`;
                    }
                }
                return entry; // Return the entry unchanged if no "Growth" or "vs" is found
            });
        }
    }
}
