// var API_URL='https://forecasting.azurewebsites.net/';
var API_URL='http://127.0.0.1:8000/';
// var API_URL='https://bsstrackertest.brand-scapes.com/';
// var API_URL='https://dynamicviewtest.brand-scapes.com/';
// var API_URL='https://dynamicviewtest.brand-scapes.com/';
// var API_URL='http://52.44.39.143:9000/';
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

function find_bps_string_in_array(facts_selected_value) {
    let result = [];

    // Iterate over each key in the object
    for (const fcats_key in facts_selected_value) {
        if (facts_selected_value.hasOwnProperty(fcats_key)) {
            // Apply the replacements in sequence and add to the result array
            const modifiedArray = facts_selected_value[fcats_key]
                .map(item => item.replace("QUARTER ", ""))
                .map(item => item.replace("HY ", ""))
                .map(item => item.replace(/\s/g, ''));
            
            result = result.concat(modifiedArray);
        }
    }
    return result
}

function match_facts_value_return_true_false(data,text,value) {
    // console.log('############################# start');
   
    // console.log('data', data);
    // console.log('value', value);
    // console.log('text', text);
    // Remove "HY" from each element
    const modifieddata = data.map(item => item.replace(/HY/g, ''));
     // console.log('data', modifieddata);
    let result;
    const match = modifieddata.find(item => item === text);
    // console.log('match', match);
    if (match) { // Output will be true, 'match found'
        switch(true) {
            case match.includes('GR'):
                result = GR_checkValue_logic(value);
                break;
            case match.includes('BPS'):
                result = BPS_checkValue_logic(value);
                break;
            default:
                // Handle the case where neither 'GR' nor 'Br' is found in match
                result = ['black'];
                break;
        }
    }else{
        result = ['black'];
    }
    // console.log('match_facts_value_return_true_false', result);
    // console.log('############################## end');
    return result;
}


function GR_checkValue_logic(value) {
    if (value > 0) {
        return ['green'];
    } else if (value < 0) {
        return ['red'];
    } else {
        return ['black'];
    }
}

function BPS_checkValue_logic(value) {
    if (value <=(-30)) {
        return ['red'];
    } else if (value >= 30) {
        return ['green'];
    } else {
        return ['#FFBF00'];
    }
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
function crosstable_filterdata() {
    var filter_data = [];

    // Retrieve values for filters
    var filters = {
        filter1: $("#filter1").val(),
        filter2: $("#filter2").val(),
        filter3: $("#filter3").val(),
        filter4: $("#filter4").val(),
        filter5: $("#filter5").val(),
        filter6: $("#filter6").val(),
        filter7: $("#filter7").val(),
        filter8: $("#filter8").val(),
        filter9: $("#filter9").val(),
        filter10: $("#filter10").val(),
        filter1_brandindex: $("#filter1_brandindex").val()
    };

    // Retrieve filter names from data attributes
    var filter_names = {
        filter1: $("#filter1").attr("data-filtername"),
        filter2: $("#filter2").attr("data-filtername"),
        filter3: $("#filter3").attr("data-filtername"),
        filter4: $("#filter4").attr("data-filtername"),
        filter5: $("#filter5").attr("data-filtername"),
        filter6: $("#filter6").attr("data-filtername"),
        filter7: $("#filter7").attr("data-filtername"),
        filter8: $("#filter8").attr("data-filtername"),
        filter9: $("#filter9").attr("data-filtername"),
        filter10: $("#filter10").attr("data-filtername"),
        filter1_brandindex: $("#filter1_brandindex").attr("data-filtername")
    };

    // Loop through each filter and add to filter_data if it has a value
    $.each(filters, function (key, value) {
        if (value && value.length != 0) {
            filter_data.push({ [filter_names[key]]: value });
        }
    });

    // Remove any empty keys in the first filter_data object (if necessary)
    if (filter_data.length > 0 && filter_data[0]) {
        $.each(filter_data[0], function (key, value) {
            if (Object.keys(value).length == 0) {
                delete filter_data[0][key];
            }
        });
    }

    // Return the processed filter data
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
    var grand_total_index_array=[];
    var group_column_resp_keyname = Object.keys(group_column_resp)
    html2='';html3='';
    html +='<thead class="sticky-top thead-dark">';
    html +='<tr>';
    // cif condition added for row lenght missmatch case
    html +='<th scope="col" class="text-lg-center 1 align-baseline"  colspan='+single_row_length+' rowspan='+resp['df_cross_json']['columns'][0].length+' style="background-color: #595959 !important;color:white;position: sticky;left: -16px;z-index:1;" >'+row_str+'</th>';
    // console.log('resp lenght--->985',resp['df_cross_json']['columns'][0].length)
    // console.log('group_column_resp--->985',group_column_resp)
    // console.log('single_row_length--->985',single_row_length)
    // console.log('group_column_resp_keyname--->985',group_column_resp_keyname)
    // console.log('group_column_resp_keyname--->985',resp['df_cross_json']['columns'][0].length)
   
        const group_column_resp_result = createNestedStructure(columns_data);
        const numberOfLevels = getNestedLevels(group_column_resp_result);
        // console.log('group_column_resp_result 990',group_column_resp_result)
       
        // console.log('numberOfLevels',numberOfLevels)
        var header_i=0;
        var header_iL2=0;
        $.each(group_column_resp_result, function (k2, val2) {
             var grp_len=group_column_resp[k2].length;
            html +='<th scope="col"  class="text-lg-center 2 "  colspan='+grp_len+' style="background-color: #595959 !important;color:white;">'+k2+'</th>';
            
            $.each(val2, function (k3, val3) {
                var val3_count=Object.keys(val3).length;
                var sort_arrow_code='';
                
                if (column_length==1) {
                    grand_total_index_array.push({'L1': k2,'L2': k3});
                    // console.log('grand_total_index_array L1',grand_total_index_array)
                }
                if (column_length==2) {
                    var val3_count=0;

                    var get_facts_colorizer_object=$("#facts_coorizer_div_array").html();

                        if (get_facts_colorizer_object!="") {
                            var get_facts_colorizer_json=JSON.parse(get_facts_colorizer_object);
                             // console.log('get_facts_colorizer_json',get_facts_colorizer_json)
                            var matchingValues = getMatchingValues(header_i,get_facts_colorizer_json,k2,k3,val3,0,k2);
                            dropdown_match_index_key.push(matchingValues);
                            

                        }

                // facts color code end
                    if (resp['measure_type']=='measure_in_column') {
                        var sort_flag_array=[k2,k3];
                        // console.log('sort_flag_array 1 and 2',sort_flag_array)
                         if (k3.indexOf("Rank") !== -1) {
                            // console.log("The substring 'Rank' exists in the string.");
                            var sort_arrow_code='';
                        } else {
                            // console.log("The substring 'Rank' does not exist in the string.");
                            var sort_arrow_code='<span class="column_level_'+header_i+'" id="column_level_'+header_i+'" data-sortflag="desc_sort" data-column1="'+sort_flag_array+'" onclick="table_sorting_function(this)"><i class="fa fa-sort" aria-hidden="true" style="font-size:12px; cursor:pointer; position:relative; left:7px; color:white;"></i></span>';
                        }

                        grand_total_index_array.push({'L1': k3,'L2': k2});
                    }
                    if (resp['measure_type']=='measure_in_row') {
                        grand_total_index_array.push({'L1': k2,'L2': k3});
                    }
                    // grand_total_index_array.push({'L1': k3,'L2': k2});
                    // console.log('grand_total_index_array L2',grand_total_index_array)
                }
                // if (k3.includes('Door')==true || k3.includes('Unit')==true){
                //     var result3 = k3
                // }
                // else if (k3.includes('_')) {
                //   // Split the string by '_' and check if the second part exists
                //   let parts = k3.split('_');
                //   var result3 = parts[1] ? parts[1].trim() : '';
                //   //console.log(result3); // Output will be "GR% vs  Q1 2024" or "Q2 2024"
                // }else{
                //     var result3 = k3;
                // }
                // const [firstLine1, secondLine1] = k3.split('_');
                if (k3.includes('_')) {
                    var [firstLine1, secondLine1] = k3.split('_');
                    var dis_div='';
                    var div_underscore='_';

                } else {
                    var firstLine1 = k3;
                    var secondLine1='';
                    var dis_div='d-none';
                    var div_underscore='';
                    // Handle the case where there's no underscore
                }


                // console.log('result3===>',k3)
                // console.log('result3===>',k3.split('_')[1].trim())
                // html2 +='<th scope="col"  class="align-baseline text-lg-center 3"  colspan='+val3_count+' style="background-color: #3C6BE3 !important;;color:white">'+k3+'</th>';
                // html2 +='<th scope="col"  class="align-baseline text-lg-center 3"  colspan='+val3_count+' style="background-color: #595959 !important;;color:white">'+k3+' '+sort_arrow_code+'</th>';
                html2 +='<th scope="col"  class="align-baseline text-lg-center 3"  colspan='+val3_count+' style="background-color: #595959 !important;;color:white"><p class="w-100 text-center">'+ firstLine1+' '+div_underscore+'</p><div class="d-flex justify-content-between"><span class="text-center '+dis_div+'" style="width: 100%;"> '+secondLine1+' </span><span>'+sort_arrow_code+'</span></div></th>';

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

         
                         
                        grand_total_index_array.push({'L1': k2,'L2': k3,'L3': val4,index:header_i});
                        // console.log('grand_total_index_array L3',grand_total_index_array)
                         //     console.log("===========================================================");
                         //    console.log("266 matchingValues--->",matchingValues)
                         //     console.log("type get_facts_colorizer_object",typeof(get_facts_colorizer_object))
                         //    console.log("Index",header_i);
                         //    console.log("1st level",k2);
                         //    console.log("2nd level",k3);
                         //    console.log("3rd level",val4);
                         //    console.log("get_stored_object_json:1000",get_facts_colorizer_json);
                         //    console.log("k2",k2);
                         //    console.log("===========================================================");
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
                        var sort_flag_array=[k2,k3,val4];
                        // console.log('sort_flag_array 3 level',sort_flag_array)
                        if (val4.indexOf("Rank") !== -1) {
                            // console.log("The substring 'Rank' exists in the string.");
                            var sort_arrow_code='';
                        } else {
                            // console.log("The substring 'Rank' does not exist in the string.");
                            var sort_arrow_code='<span class="pr-2 column_level_'+header_i+'" id="column_level_'+header_i+'" data-sortflag="desc_sort" data-column1="'+sort_flag_array+'" onclick="table_sorting_function(this)"><i class="fa fa-sort" aria-hidden="true" style="font-size:12px; cursor:pointer; position:relative; left:7px; color:white;"></i></span>';
                        }

                        
                        // html3 +='<th scope="col"  class="align-baseline text-lg-center 4" style="background-color: #3C6BE3 !important;color:white">'+ val4+' </th>';
                        // Split the string by the underscore and get the part after the underscore
                        // let result = val4.split('_')[1].trim();
                        // console.log('=========501',val4.includes('Door'))
                        // if (val4.includes('Door')==true || val4.includes('Unit')==true){
                        //     var result4 = val4
                        // }
                        // else{
                        //     var result4 = val4.split('_')[1].trim();
                        // }

  
                        // const resulttest = "Sales (M Local Currency)_CAGR%  Q2 2024 vs  Q1 2024";
                        // const [firstLine, secondLine] = val4.split('_');
                         if (val4.includes('_')) {
                            var [firstLine, secondLine] = val4.split('_');
                            var dis_div='';
                            var div_underscore='_';

                        } else {
                            var firstLine = val4;
                            var secondLine='';
                            var dis_div='d-none';
                            var div_underscore='';
                            // Handle the case where there's no underscore
                        }


                        // html3 +='<th scope="col"  class="align-baseline text-lg-center 4"  style="background-color: #595959 !important;color:white" data-columnheadername="'+val4+'">'+ val4+' '+sort_arrow_code+'</th>';
                         // html3 +='<th scope="col"  class="align-baseline text-lg-center 4"  style="background-color: #595959 !important;color:white" data-columnheadername="'+val4+'">'+ result4+' '+sort_arrow_code+'</th>';

                         html3 +='<th scope="col"  class="align-baseline 455 header_left_align"  style="background-color: #595959 !important;color:white" data-columnheadername="'+val4+'"><p class="w-100 text-center">'+ firstLine+' '+div_underscore+'</p><div class="d-flex justify-content-between"><span class="text-center '+dis_div+'" style="width: 100%;"> '+secondLine+' </span><span>'+sort_arrow_code+'</span></div></th>';

          

                        // html3 +='<th scope="col"  class="align-baseline 455 header_left_align"  style="background-color: #595959 !important;color:white" data-columnheadername="'+val4+'"><p class=" text-center" style="width:90%">'+ firstLine+'_</p><div class="d-flex justify-content-between"><span class="text-center" style="width: 100%;"> '+secondLine+' </span><span>'+sort_arrow_code+'</span></div></th>';

                        header_i++;
                        k4i++;
                    });  
        console.log('=========501-==============end')
                }
                   header_iL2++;
            });

        });
    
    // console.log('grand_total_index_array-->',grand_total_index_array)
    $("#dropdown_range_filter").html(JSON.stringify(dropdown_match_index_key));
    $("#grand_total_index_array").html(JSON.stringify(grand_total_index_array));
    html +='</tr>';
    html +=html2+'</tr>';
    if (column_length==3) {
        html +=html3+'</tr>';
    }
    
    html +='</thead>';
    return html;
}

function header_stacked_logic_xls_download(html,group_column_resp,single_row_length,row_str,columns_data,resp){
    
    var r_text_val=$('#example2-left').sortableListsToArray()
    var rowfilter_sort_th=exract_one_array_object_by_labels(r_text_val);
    var row_str = rowfilter_sort_th.toString();
    row_str = row_str.replaceAll(",", " & ");
    if (rowfilter_sort_th.length>1 && resp['seperated_flag_row']==1) {
        
 
        var rowfilter_sort_th_copy=[];
        for (var iq = 0; iq<rowfilter_sort_th.length; iq++) {
            rowfilter_sort_th_copy.push(row_str);
        }
        rowfilter_sort_th=[];
        rowfilter_sort_th = [...rowfilter_sort_th_copy];
    }
    if (rowfilter_sort_th.length==1 && resp['seperated_flag_row']==1) {
        // rowfilter_sort_th.push('Metrics');
        var static_array=['###',rowfilter_sort_th[0],'Metrics'];
        rowfilter_sort_th=[];
        rowfilter_sort_th = [...static_array];
    }
    else if (rowfilter_sort_th.length>1) {
        rowfilter_sort_th.push('Metrics');
    }else{
        rowfilter_sort_th.unshift('###');
    }
    
    // console.log('rowfilter_sort_th-->',rowfilter_sort_th)
    var column_length=resp['df_cross_json']['columns'][0].length
    var dropdown_match_index_key=[];
    var grand_total_index_array=[];
    var group_column_resp_keyname = Object.keys(group_column_resp)
    html2='';html3='';
    html +='<thead class="sticky-top thead-dark">';
    html +='<tr>';
    // cif condition added for row lenght missmatch case
    // html +='<th scope="col" class="text-lg-center 1 align-baseline" rowspan='+resp['df_cross_json']['columns'][0].length+' style="background-color: #595959 !important;color:white;position: sticky;left: -16px;z-index:1;" >###</th>';
    for (var th = 0; th < single_row_length; th++) {
        html +='<th scope="col" class="text-lg-center 1 align-baseline" rowspan='+resp['df_cross_json']['columns'][0].length+' style="background-color: #595959 !important;color:white;position: sticky;left: -16px;z-index:1;" >'+rowfilter_sort_th[th]+'</th>';
    }
    // html +='<th scope="col" class="text-lg-center 1 align-baseline"  colspan='+single_row_length+' rowspan='+resp['df_cross_json']['columns'][0].length+' style="background-color: #595959 !important;color:white;position: sticky;left: -16px;z-index:1;" >'+row_str+'</th>';
    // console.log('resp lenght--->985',resp['df_cross_json']['columns'][0].length)
    // console.log('group_column_resp--->985',group_column_resp)
    // console.log('single_row_length--->985',single_row_length)
    // console.log('group_column_resp_keyname--->985',group_column_resp_keyname)
    // console.log('group_column_resp_keyname--->985',resp['df_cross_json']['columns'][0].length)
   
        const group_column_resp_result = createNestedStructure(columns_data);
        const numberOfLevels = getNestedLevels(group_column_resp_result);
        // console.log('group_column_resp_result 990',group_column_resp_result)
       
        // console.log('numberOfLevels',numberOfLevels)
        var header_i=0;
        var header_iL2=0;
        $.each(group_column_resp_result, function (k2, val2) {
             var grp_len=group_column_resp[k2].length;
            html +='<th scope="col"  class="text-lg-center 2 "  colspan='+grp_len+' style="background-color: #595959 !important;color:white;">'+k2+'</th>';
            
            $.each(val2, function (k3, val3) {
                var val3_count=Object.keys(val3).length;
                var sort_arrow_code='';
                
                if (column_length==1) {
                    grand_total_index_array.push({'L1': k2,'L2': k3});
                    // console.log('grand_total_index_array L1',grand_total_index_array)
                }
                if (column_length==2) {
                    var val3_count=0;

                    var get_facts_colorizer_object=$("#facts_coorizer_div_array").html();

                        if (get_facts_colorizer_object!="") {
                            var get_facts_colorizer_json=JSON.parse(get_facts_colorizer_object);
                             // console.log('get_facts_colorizer_json',get_facts_colorizer_json)
                            var matchingValues = getMatchingValues(header_i,get_facts_colorizer_json,k2,k3,val3,0,k2);
                            dropdown_match_index_key.push(matchingValues);
                            

                        }

                // facts color code end
                    if (resp['measure_type']=='measure_in_column') {
                        var sort_flag_array=[k2,k3];
                        // console.log('sort_flag_array 1 and 2',sort_flag_array)
                         if (k3.indexOf("Rank") !== -1) {
                            // console.log("The substring 'Rank' exists in the string.");
                            var sort_arrow_code='';
                        } else {
                            // console.log("The substring 'Rank' does not exist in the string.");
                            var sort_arrow_code='<span class="column_level_'+header_i+'" id="column_level_'+header_i+'" data-sortflag="desc_sort" data-column1="'+sort_flag_array+'" onclick="table_sorting_function(this)"><i class="fa fa-sort" aria-hidden="true" style="font-size:12px; cursor:pointer; position:relative; left:7px; color:white;"></i></span>';
                        }

                        grand_total_index_array.push({'L1': k3,'L2': k2});
                    }
                    if (resp['measure_type']=='measure_in_row') {
                        grand_total_index_array.push({'L1': k2,'L2': k3});
                    }
                    // grand_total_index_array.push({'L1': k3,'L2': k2});
                    // console.log('grand_total_index_array L2',grand_total_index_array)
                }
                // if (k3.includes('Door')==true || k3.includes('Unit')==true){
                //     var result3 = k3
                // }
                // else if (k3.includes('_')) {
                //   // Split the string by '_' and check if the second part exists
                //   let parts = k3.split('_');
                //   var result3 = parts[1] ? parts[1].trim() : '';
                //   //console.log(result3); // Output will be "GR% vs  Q1 2024" or "Q2 2024"
                // }else{
                //     var result3 = k3;
                // }
                // const [firstLine1, secondLine1] = k3.split('_');
                if (k3.includes('_')) {
                    var [firstLine1, secondLine1] = k3.split('_');
                    var dis_div='';
                    var div_underscore='_';

                } else {
                    var firstLine1 = k3;
                    var secondLine1='';
                    var dis_div='d-none';
                    var div_underscore='';
                    // Handle the case where there's no underscore
                }


                // console.log('result3===>',k3)
                // console.log('result3===>',k3.split('_')[1].trim())
                // html2 +='<th scope="col"  class="align-baseline text-lg-center 3"  colspan='+val3_count+' style="background-color: #3C6BE3 !important;;color:white">'+k3+'</th>';
                // html2 +='<th scope="col"  class="align-baseline text-lg-center 3"  colspan='+val3_count+' style="background-color: #595959 !important;;color:white">'+k3+' '+sort_arrow_code+'</th>';
                html2 +='<th scope="col"  class="align-baseline text-lg-center 3"  colspan='+val3_count+' style="background-color: #595959 !important;;color:white"><div><span>'+ firstLine1+' '+div_underscore+'</span><span class="text-center '+dis_div+'" > '+secondLine1+' </span></div></th>';

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

         
                         
                        grand_total_index_array.push({'L1': k2,'L2': k3,'L3': val4,index:header_i});
                        // console.log('grand_total_index_array L3',grand_total_index_array)
                         //     console.log("===========================================================");
                         //    console.log("266 matchingValues--->",matchingValues)
                         //     console.log("type get_facts_colorizer_object",typeof(get_facts_colorizer_object))
                         //    console.log("Index",header_i);
                         //    console.log("1st level",k2);
                         //    console.log("2nd level",k3);
                         //    console.log("3rd level",val4);
                         //    console.log("get_stored_object_json:1000",get_facts_colorizer_json);
                         //    console.log("k2",k2);
                         //    console.log("===========================================================");
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
                        var sort_flag_array=[k2,k3,val4];
                        // console.log('sort_flag_array 3 level',sort_flag_array)
                        if (val4.indexOf("Rank") !== -1) {
                            // console.log("The substring 'Rank' exists in the string.");
                            var sort_arrow_code='';
                        } else {
                            // console.log("The substring 'Rank' does not exist in the string.");
                            var sort_arrow_code='<span class="pr-2 column_level_'+header_i+'" id="column_level_'+header_i+'" data-sortflag="desc_sort" data-column1="'+sort_flag_array+'" onclick="table_sorting_function(this)"><i class="fa fa-sort" aria-hidden="true" style="font-size:12px; cursor:pointer; position:relative; left:7px; color:white;"></i></span>';
                        }

                        
                        // html3 +='<th scope="col"  class="align-baseline text-lg-center 4" style="background-color: #3C6BE3 !important;color:white">'+ val4+' </th>';
                        // Split the string by the underscore and get the part after the underscore
                        // let result = val4.split('_')[1].trim();
                        // console.log('=========501',val4.includes('Door'))
                        // if (val4.includes('Door')==true || val4.includes('Unit')==true){
                        //     var result4 = val4
                        // }
                        // else{
                        //     var result4 = val4.split('_')[1].trim();
                        // }

  
                        // const resulttest = "Sales (M Local Currency)_CAGR%  Q2 2024 vs  Q1 2024";
                        // const [firstLine, secondLine] = val4.split('_');
                         if (val4.includes('_')) {
                            var [firstLine, secondLine] = val4.split('_');
                            var dis_div='';
                            var div_underscore='_';

                        } else {
                            var firstLine = val4;
                            var secondLine='';
                            var dis_div='d-none';
                            var div_underscore='';
                            // Handle the case where there's no underscore
                        }


                        // html3 +='<th scope="col"  class="align-baseline text-lg-center 4"  style="background-color: #595959 !important;color:white" data-columnheadername="'+val4+'">'+ val4+' '+sort_arrow_code+'</th>';
                         // html3 +='<th scope="col"  class="align-baseline text-lg-center 4"  style="background-color: #595959 !important;color:white" data-columnheadername="'+val4+'">'+ result4+' '+sort_arrow_code+'</th>';

                         html3 +='<th scope="col"  class="align-baseline 455 header_left_align"  style="background-color: #595959 !important;color:white" data-columnheadername="'+val4+'"><div><span>'+ firstLine+' '+div_underscore+'</span><span class="text-center '+dis_div+'" > '+secondLine+' </span></div></th>';

                            // html3 +='<th scope="col"  class="align-baseline 455 header_left_align"  style="background-color: #595959 !important;color:white" data-columnheadername="'+val4+'"><span  class="w-100 text-center">'+ firstLine+' '+div_underscore+'<br>'+secondLine+' </span></th>';

          

                        // html3 +='<th scope="col"  class="align-baseline 455 header_left_align"  style="background-color: #595959 !important;color:white" data-columnheadername="'+val4+'"><p class=" text-center" style="width:90%">'+ firstLine+'_</p><div class="d-flex justify-content-between"><span class="text-center" style="width: 100%;"> '+secondLine+' </span><span>'+sort_arrow_code+'</span></div></th>';

                        header_i++;
                        k4i++;
                    });  
        // console.log('=========501-==============end')
                }
                   header_iL2++;
            });

        });
    
    // console.log('grand_total_index_array-->',grand_total_index_array)
    $("#dropdown_range_filter").html(JSON.stringify(dropdown_match_index_key));
    $("#grand_total_index_array").html(JSON.stringify(grand_total_index_array));
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
    console.log('data-->',data)
    console.log('searchText-->',searchText)
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

// ########################################################################################
 // old code
function getSelectedValues_facts_filter_1() {
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

    return selectedValues;
}


// ###########################################################################################3
// new codee
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
    console.log('before selectedValues 511', selectedValues);


    // const updatedData = updateSalesData(selectedValues);
    // console.log('after selectedValues 511', updatedData);

    return selectedValues;
}

function getSelectedIndex_facts_filter_all() {
    var select = document.getElementById("facts_group_filter");
        var optgroups = select.getElementsByTagName("optgroup");
        var data = {};

        for (var i = 0; i < optgroups.length; i++) {
            var optgroup = optgroups[i];
            var label = optgroup.label;
            var options = optgroup.getElementsByTagName("option");
            var selectedIndexes = [];

            for (var j = 0; j < options.length; j++) {
                if (options[j].selected) {
                    selectedIndexes.push(j);
                }
            }

            data[label] = selectedIndexes;
        }
         console.log('getSelectedIndex_facts_filter_all 565', data);
        return data;
}

 // Function to update entries containing "Growth" in any key of the data object
function updateSalesData(data) {
    // Get the value from the input field with the ID "comparison_time_period"
    var comparative_tp = $("#comparison_time_period").val()+'(%)' ;

    // Iterate over each property in the data object
    Object.keys(data).forEach(key => {
        if (Array.isArray(data[key])) {
            data[key] = data[key].map(entry => {
                if (entry.includes("Growth")) {
                    const index = entry.indexOf("vs");
                    if (index !== -1) {
                        // Replace everything after "vs" with the comparative_tp value dynamically
                        return `${entry.substring(0, index + 3)}${comparative_tp}`;
                    }
                }
                return entry; // Return the entry unchanged if no "Growth" or "vs" is found
            });
        }
    });
    return data; // Return the modified data
}


// ###########################################################################################


//reordering category 
function reorderArray(arr) {
    // Define the order for the first few elements
    const sortOrder = ['Skincare', 'Make-up', 'Fragrance'];

    // Separate the items that are in sortOrder from those that are not
    const orderedPart = arr.filter(item => sortOrder.includes(item));
    const remainingPart = arr.filter(item => !sortOrder.includes(item));

    // Sort the orderedPart based on the sortOrder array
    orderedPart.sort((a, b) => sortOrder.indexOf(a) - sortOrder.indexOf(b));

    // Concatenate the sorted orderedPart with the remainingPart
    return orderedPart.concat(remainingPart);
}

function time_period_filters_bk(resp){
            console.log('orginal resp time_period',resp)


            // Sorting the array using a custom comparator function
            

            resp.sort(customSort);
            // console.log('sort resp time_period',resp)
            if (resp.length>0) {

                 $.each(resp, function (key2, value2) {
                    var value2_original=value2;
                    if (value2.includes("QUARTER")) {
                        value2 = value2.replace("QUARTER", "");
                        if (value2=='Q3_2023') {
                            $("#time_period").append('<option style="width: 100px" selected  value="'+value2_original+'" >'+value2+'</option>');
                        }else{
                            $("#time_period").append('<option  style="width: 100px" value="'+value2_original+'" >'+value2+'</option>');
                        }

                    }else{

                        if (value2=='Q3_2023') {
                            $("#time_period").append('<option style="width: 100px" selected  value="'+value2+'" >'+value2+'</option>');
                        }else{
                            $("#time_period").append('<option  style="width: 100px" value="'+value2+'" >'+value2+'</option>');
                        }

                    }

                    
            

              });

             $("#time_period").multiselect('rebuild');  
              $("#time_period").multiselect({
                    //  enableClickableOptGroups: true,
              // enableCollapsibleOptGroups: true,
              includeSelectAllOption: true,
              selectAll: true,
              search   : true,
              enableCaseInsensitiveFiltering: true,
              // maxHeight: 200,
              // buttonWidth: '100px'
                });
           
             
            }

            comparative_time_period_resp();
      
}

function comparative_time_period_resp_bk() {
    var final_row_col_array_grp1 = localStorage.getItem('final_row_col_array_grp');
    var final_row_col_array_grp2 = JSON.parse(final_row_col_array_grp1);
    var filename = Object.keys(final_row_col_array_grp2[0]);
    var current_timeperiod = $("#time_period").val();
    var checkData5 = {
        'csrfmiddlewaretoken': csrfmiddlewaretoken,
        'current_timeperiod': current_timeperiod,
        'filename': filename[0]
    };
    var resp_filter = autoresponse("comparative_time_period_resp", checkData5);
 
    // Assuming `autoresponse` is synchronous and `resp_filter` is immediately available
    let newData = [];
 
    if (resp_filter['status'] == 200) {
        const data = resp_filter['comparative_time_period_resp'];
 
        // Sort the years in descending order and then reverse the quarters, store in array for guaranteed order
        Object.keys(data).sort((a, b) => b - a).forEach(year => {
            newData.push({
                year: year,
                quarters: data[year].slice().reverse()
            });
        });
        console.log('Reversed and re-ordered data', newData);
 
        var tp_active = $("#time_period").val();
        var lastDigits = tp_active.match(/\d{4}$/);
        var newYear = parseInt(lastDigits[0]) - 1;
        var newString = tp_active.replace(/\d{4}$/, newYear);
        console.log('newString------->', newString);
 
        newData.forEach(item => {
            $("#comparison_time_period").append('<optgroup label="' + item.year + '" id="' + item.year.replace(/[^a-zA-Z0-9]/g, '') + '" class="dropmenu">');
            item.quarters.forEach(quarter => {
                var quarterDisplay = quarter.replace("QUARTER ", "");
                var selected = quarterDisplay === newString.replace("QUARTER ", "") ? ' selected' : '';
                $("#comparison_time_period").append('<option style="width: 100px"' + selected + ' value="' + quarter + '">' + quarterDisplay + '</option>');
            });
            $("#comparison_time_period").append('</optgroup>');
        });
 
        $("#comparison_time_period").multiselect('rebuild');
        $("#comparison_time_period").multiselect({
            includeSelectAllOption: true,
            selectAll: true,
            search: true,
            enableCaseInsensitiveFiltering: true
        });
    }
 
    var get_val_ctp = $("#comparison_time_period").val();
    $("#store_selected_comparison_time_period_value").html(get_val_ctp);
}

function time_period_filters_09_05_2024_bk(resp){

            $("#time_period").empty();
            // console.log('facts_assign_fun==328',selected_resp1)
        var i=
        $.each(resp, function (key1, value) {
                $("#time_period").append('<optgroup label="'+key1+'" id="'+key1.replace(/[^a-zA-Z0-9]/g, '')+'" class="dropmenu">');
            $.each(value, function (key2, value1) {

                    
                    $("#time_period").append('<option class="dropmenu" value="'+value1+'" >'+value1.replace("QUARTER", "")+'</option>');
                    
            });
            $("#time_period").append('</optgroup>');
        });


          $("#time_period").multiselect('rebuild'); 
           $("#time_period").multiselect({
                    //  enableClickableOptGroups: true,
              // enableCollapsibleOptGroups: true,
              includeSelectAllOption: true,
              selectAll: true,
              search   : true,
              enableCaseInsensitiveFiltering: true,
              // maxHeight: 200,
              // buttonWidth: '100px'
                });

            

            // comparative_time_period_resp();
      
}

// Function to get URL parameters
function getUrlParameter(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    const regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    const results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}

// Function to decode HTML entities
function decodeHTMLEntities(text) {
    let txt = document.createElement("textarea");
    txt.innerHTML = text;
    return txt.value;
}


const apply_codition_footnote_check_bps_and_gr_exit = (arrays, chars) => {
    const result = {};
    chars.forEach(char => {
        const found = Object.values(arrays).flat().some(item => item.includes(char));
        if (found) {
            result[char] = true;
        } else {
            result[char] = false;
        }
    });
    return result;
};

function moveKeyToEnd(obj, key) {
    if (obj.hasOwnProperty(key)) {
        // Extract the value associated with the key
        const value = obj[key];
        
        // Remove the key from the original object
        const { [key]: _, ...rest } = obj;
        
        // Add the key back to the end
        return { ...rest, [key]: value };
    }
    // Return the original object if the key is not present
    return obj;
}


// Function to delete a key if it exists and return the updated object
function deleteKeyIfExists(obj, key) {
    if (key in obj) {
        delete obj[key];
        console.log(`"${key}" has been deleted.`);
    } else {
        console.log(`"${key}" does not exist in the object.`);
    }
    return obj; // Return the updated object
}

function transformInput(input) {
  // Initialize the result object
  let result = {};

  // Iterate over the input array dynamically
  input.forEach(item => {
    let key = Object.keys(item)[0];  // Dynamically get the key
    let value = item[key];           // Get the corresponding value
    
    // If the value is an array, apply transformations
    if (Array.isArray(value)) {
      // Replace "&" with "&amp;" in the array values
      result[key] = value.map(element => element.replace("&", "&amp;"));

      // Add "EC" dynamically to all arrays
      // result[key].push("EC");
    } else {
      // If the value is not an array, assign it as-is
      result[key] = value;
    }
  });

  return result;  // Return the transformed result
}

function searchKeyAndReturnArray_old(obj, keyToSearch) {
  // Check if the key exists in the object
  if (obj.hasOwnProperty(keyToSearch)) {
    // Return the key and its value in the required array format
    return [{
      [keyToSearch]: obj[keyToSearch]
    }];
  }
  // If the key doesn't exist, return null or an empty array, as required
  return [];
}

function searchKeyAndReturnArray(obj, keyToSearch) {
  // Check if the key exists in the object
  if (obj.hasOwnProperty(keyToSearch)) {
    // Return only the values associated with the key
    return obj[keyToSearch];
  }
  // If the key doesn't exist, return null or an empty array
  return [];
}




function filter_validation_checkdata_old(rowfilter_sort, columnfilter_sort) {
    var datafilter_check = [
        {
            'filter': $("#filter1").attr("data-filtername") || 0,
            'value': $("#filter1").val(),
        },
        {
            'filter': $("#filter2").attr("data-filtername") || 0,
            'value': $("#filter2").val(),
        },
        {
            'filter': $("#filter3").attr("data-filtername") || 0,
            'value': $("#filter3").val(),
        },
        {
            'filter': $("#filter4").attr("data-filtername") || 0,
            'value': $("#filter4").val(),
        },
        {
            'filter': $("#filter5").attr("data-filtername") || 0,
            'value': $("#filter5").val(),
        },
        {
            'filter': $("#filter6").attr("data-filtername") || 0,
            'value': $("#filter6").val(),
        },
        {
            'filter': $("#filter7").attr("data-filtername") || 0,
            'value': $("#filter7").val(),
        },
        {
            'filter': $("#filter8").attr("data-filtername") || 0,
            'value': $("#filter8").val(),
        },
        {
            'filter': $("#filter9").attr("data-filtername") || 0,
            'value': $("#filter9").val(),
        },
        {
            'filter': $("#filter10").attr("data-filtername") || 0,
            'value': $("#filter10").val(),
        }
    ];

    // Remove entries where the filter is 0
    datafilter_check = datafilter_check.filter(item => item.filter !== 0);

    let combined_row_column = rowfilter_sort.concat(columnfilter_sort);

    try {
        for (let item of datafilter_check) {
            // Check if the filter key exists in the combined_row_column array
            if (combined_row_column.includes(item.filter)) {
                // Check if the value is empty or null
                if (!item.value || item.value.length === 0) {
                    console.log(`${item.filter} has an empty value.`);
                    $.LoadingOverlay("hide", true);
                    // Return false if any value is empty
                    return false;
                }
            }
        }
        // Return true if all values are non-empty
        return true;
    } catch (error) {
        alert(error.message, `has an empty value array.`);
    }
}

function filter_validation_checkdata(rowfilter_sort, columnfilter_sort) {
        // console.log('rowfilter_sort',rowfilter_sort)
    // console.log('columnfilter_sort',columnfilter_sort)
    var metrics_filter=$("#facts_group_filter").val();
    // console.log('---metrics_filter---',metrics_filter)
    var datafilter_check = [
        {
            'filter': $("#filter1").attr("data-filtername") || 0,
            'value': $("#filter1").val(),
        },
        {
            'filter': $("#filter2").attr("data-filtername") || 0,
            'value': $("#filter2").val(),
        },
        {
            'filter': $("#filter3").attr("data-filtername") || 0,
            'value': $("#filter3").val(),
        },
        {
            'filter': $("#filter4").attr("data-filtername") || 0,
            'value': $("#filter4").val(),
        },
        {
            'filter': $("#filter5").attr("data-filtername") || 0,
            'value': $("#filter5").val(),
        },
        {
            'filter': $("#filter6").attr("data-filtername") || 0,
            'value': $("#filter6").val(),
        },
        {
            'filter': $("#filter7").attr("data-filtername") || 0,
            'value': $("#filter7").val(),
        },
        {
            'filter': $("#filter8").attr("data-filtername") || 0,
            'value': $("#filter8").val(),
        },
        {
            'filter': $("#filter9").attr("data-filtername") || 0,
            'value': $("#filter9").val(),
        },
        {
            'filter': $("#filter10").attr("data-filtername") || 0,
            'value': $("#filter10").val(),
        },
        {
            'filter': 'Metrics',
            'value': metrics_filter
        }
    ];

    // Remove entries where the filter is 0
    datafilter_check = datafilter_check.filter(item => item.filter !== 0);
    // console.log('datafilter_check',datafilter_check)

    // let combined_row_column = rowfilter_sort.concat(columnfilter_sort);
    let combined_row_column = rowfilter_sort.concat(columnfilter_sort).concat('Metrics');
     // console.log('combined_row_column',combined_row_column)
    try {
        for (let item of datafilter_check) {
            // Check if the filter key exists in the combined_row_column array
            if (combined_row_column.includes(item.filter)) {
                // Check if the value is empty or null
                if (!item.value || item.value.length === 0) {
                    console.log(`${item.filter} has an empty value.`);
                    $.LoadingOverlay("hide", true);
                    // Return false and the name of the filter with an empty value
                    return { result: false, emptyFilter: item.filter,code:404,message:item.filter + ' filter is empty, please select atleast one value' };
                }
            }
        }
        // Return true if all values are non-empty
        return { result: true, emptyFilter: null,code:200,message:'Return true if all values are non-empty' };
    } catch (error) {
        // alert(error.message, `has an empty value array.`);
        return { result: false, emptyFilter: item.filter,code:404,message:'filter is empty, please select atleast one value' };
    }
}

