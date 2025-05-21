
import json
import ast
import os
import time
import re
import polars as pl
import pandas as pd
import numpy as np
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
# Create your views here.
# from CCV_Tool.CCV_Tool.settings import pythonpath
from datetime import date
from datetime import datetime
from io import StringIO
from main_dashboard.bcst_sales_crosstab_calculation_seperated_functions import *
from main_dashboard.response_functions import *
from main_dashboard.bcst_sales_crosstab_calculation_functions import *
from main_dashboard.bcst_sales_derived_measures import *
from django.contrib.sessions.models import Session
from django.db import connection
from main_dashboard.bcst_sales_crosstab_table_resp import *
from matplotlib import pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import math
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse
from main_dashboard.PIVOT_DATA_CLEANING import *
############################################################################################
############################################################################################
# testing function start here

def store_questionnaire_format(request):
 
    periodical_type =request.POST.get('periodical_type')
    que_year =request.POST.get('que_year')
    que_period =request.POST.get('que_period')
    filename =request.POST.get('filename')
    que_numerical_list1 =request.POST.get('que_numerical_list')
    que_numerical_list = ast.literal_eval(que_numerical_list1)
    # print('que_numerical_list==>',list_data)
    # print('que_numerical_list type==>',type(list_data))
    # data tranformation code start here

    clean_create_data_V2(filename,periodical_type,que_year,que_period,que_numerical_list)
    # data tranformation code end here
    
    response={ 
            'code': 200,
            'message': 'Upload OK',
            }

    return JsonResponse(response, safe=False) 


# new upload data start here
def upload_chunk(request):
    if request.method == 'POST':
        try:
            uploaded_file =request.FILES.get('up')
            # print('uploaded_file==>',type(uploaded_file))
            if not uploaded_file:
                raise ValueError("No file uploaded")

            # Example: Save the uploaded file to a specific folder
            # destination = open('C:/python project/BCST_Sales_Tool/uploaded_data/' + uploaded_file.name, 'wb')
            destination = open(settings.TEMP_UPLOAD + uploaded_file.name, 'wb')

            for chunk in uploaded_file.chunks():
                destination.write(chunk)

            destination.close()

            # get all column name start
            columns,numerical_columns = get_column_names(settings.TEMP_UPLOAD + uploaded_file.name)
            print('columns==>',columns)
            print('numerical_columns==>',numerical_columns)

            # if columns:
            #     print("Column names:", columns)
            # else:
            #     print("Failed to retrieve column names.")
            # get all column name end

            return JsonResponse(
                { 
                    'ok': 1,
                    'info': 'Upload OK',
                    'filename': str(uploaded_file.name),
                    'column_list': ['A','B','C'],
                    'column_list':columns,
                    'numerical_columns':numerical_columns
                    
                }
                )
        except Exception as e:
            return JsonResponse({'ok': 0, 'info': str(e)})

    return JsonResponse({'ok': 0, 'info': 'Invalid request method'})

def get_column_names(file_path, sheet_name='Sheet1'):
    try:
        # Read the Excel file
        df = pd.read_excel(file_path, sheet_name)

        # Get column names and store them in a list
        column_names = df.columns.tolist()
        numerical_columns = df.select_dtypes(include='number').columns
        numerical_columns = numerical_columns.drop('Year', errors='ignore').tolist()
        return column_names,numerical_columns
    except Exception as e:
        print(f"Error: {e}")
        return None
# new upload data end here

def table_sample_data(request):
    file_path='C:/python project/CCV_Tool/CCV_Tool/sample_testing_data.xlsx'
    df = pd.read_excel(file_path)

    # convert into dictionary
    dict1 = df.to_dict(orient='records')
    # dict2={'dict1':dict1}
    # print(df)
    # print(dict1)

    # return render(request,'table_sample_data.html',dict2)
    return render(request,'table_sample_data.html',{'dict1':dict1})


def crosstab_ui_v1(request):
    return render(request,'crosstab_v1.html',{'title':'crosstab_v1'})

def test_page(request):
    return render(request,'test_working.html',{'title':'test_working'})


# def dashboard(request):
#     return render(request,'dashboard.html',{'title':'dashboard'})
def dashboard(request):
    # return render(request,'main_dashboard_lazyload1.html',{'title':'main_dashboard_lazyload1'})
    if request.session.has_key('is_logged'):
        username1 = request.user.username
        print('############################',username1)
        return render(request,'dashboard.html',{'username':username1})
    return redirect('/')


def main_dashboard_db_page(request):
    return render(request,'main_dashboard_db.html',{'title':'main_dashboard_db_page'})

def get_electrolux_india_column(request):
   
    query2 = "SELECT id,name FROM electrolux_india_column"
    cursor1 = connection.cursor()
    cursor1.execute(query2)
    rows1 = dictfetchall(cursor1)


    # rows_1 = list(rows1)
    responseValue = {
            "status": 200,
            "error": "correct Data",
            "data": rows1,
        }
    return JsonResponse(responseValue, safe=False) 


def dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]
# testing function end here
##############################################################################################
##############################################################################################

def main_dashboard(request):
    return render(request,'main_dashboard.html',{'title':'main_dashboard'})

def drag_and_drop(request):
    return render(request,'main_dashboard_drag_drop.html',{'title':'drag_and_drop'})

def crosstab_dash(request):


    return render(request,'crosstab.html',{'title':'crosstab'})

def upload_data(request):
    if request.method == "POST":
        excel_data = request.POST.get('excel_data')
        filename = request.POST.get('new_filename')
        data_type_file = request.POST.get('data_type_file')
        print("typee",type(excel_data))
        print("filename filename==",filename)
        list_resp = json.loads(excel_data)
        # df = pd.DataFrame(list_resp[0])
        if(len(list_resp)==1):
            df = pd.DataFrame(list_resp)
        elif(len(list_resp)==2):
            df = codeframe(list_resp)
            print('df type',type(df))
        # exit('EXIT CODE')

        
        print("list_resp typee json",type(list_resp))
        print("excel_data_excel_data== LENGTH",len(list_resp))
        # print("excel_data_excel_data==",list_resp[0])
        print('================================================')
        print('================================================')
        print('================================================')
        print('================================================')
        # print("excel_data_excel_data==",list_resp[1])
        # exit('exit code')
        # try:
        #     list_resp =  list(eval(excel_data))
        # except:


        
        # df = pd.DataFrame(data)
        # print(df)
        #################################################################
        # Textual month, day and year
        today = date.today()
        date_today = today.strftime("%d_%B_%Y")
        print("date_today =", date_today)
        time_now = datetime.now()
        current_time = time_now.strftime("%H_%M_%S")
        print("Current Time =", current_time)
        date_time = "_" + str(date_today) + "__" + str(current_time)
        print("date_time date_time", date_time)
        #################################################################

        # new_col_names_lst = []
        # for loop in df.columns:
        #     loop=loop.replace(" ","_")
        #     new_col_names_lst.append(loop)
        # df.columns = new_col_names_lst

        # df.to_json(settings.PYTHONPATH + str(filename) +"_"+str(data_type_file)+".json", orient='records', lines=True)
        # df.to_excel(settings.PYTHONPATH + str(filename) +"_"+str(data_type_file)+".xlsx",index=False) #og
        df.to_excel(settings.PYTHONPATH + str(filename) +".xlsx",index=False)
        # df.to_csv(settings.PYTHONPATH + str(filename) +"_"+str(data_type_file)+".csv",index=False)

        # df.to_json(settings.PYTHONPATH + "CCV_Uploaded_file_" + "_" + str(date_time) +".json", orient='records', lines=True)
        print('=============================================')
        # print(data)
        responseValue = {
            "status": 200,
            "error": "Correct Data",

        }
    else:
        responseValue = {
            "status": 404,
            "error": "Incorrect Data",
        }
    return JsonResponse(responseValue, safe=False)

def display_all_data(request):
    if request.method == "POST":

        filename = request.POST.get('filename')
        # df = pd.read_json(settings.PYTHONPATH + filename+'.json', orient='records', lines=True)
        df = pl.read_excel(settings.PYTHONPATH + filename+'.xlsx',sheet_name='Codeframe')
        df = df.to_pandas()
        # df.to_excel('testing.xlsx')
        ############################## OLD CODE ####################################
        # # Select numerical columns
        # # colname_num = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        # colname_num = ['Volume','Sales','TDP','WD','ND','Avg Price','API']
        # # colname_num = ['Sales']

        # # Select categorical columns
        # colname_obj = df.select_dtypes(include=['object']).columns.tolist()
        # colname_obj.remove('Time')
        ############################## OLD CODE ####################################

        colname_obj = df.loc[df['Count'] == 1, 'Variable'].tolist()
        colname_num = df.loc[df['Count'] != 1, 'Variable'].tolist()
        col_num = [col + "_NUM" for col in colname_num]
        col_obj = [col + "_STR" for col in colname_obj]

        common_list = col_obj + col_num
        print('-===common_list==',common_list)

        ################### added by mihir pawar on 03-08-2023 ########
        
        data_column_names = common_list
        # data_column_names = df.columns.tolist() #old code
        dict_col={'filename':data_column_names}

        ##################################### ADDED ON 25-09-2023 ##################
        dict_col_groups=[{'Dimensions':col_obj},{'Facts':col_num}]
        ##################################### ADDED ON 25-09-2023 ##################

        responseValue = {
            "status": 200,
            "data_column_names":dict_col,
            "data_column_names_groups":dict_col_groups,
            "error": "Correct Data",
    }
    else:
        responseValue = {
            "status": 404,
            "error": "Incorrect Data",
        }

    return JsonResponse(responseValue, safe=False)


def display_all_data1(request):
    if request.method == "POST":

        list_all_files = []
        # for file_name in [file for file in os.listdir(settings.PYTHONPATH) if file.endswith('.json')]:
        for file_name in [file for file in os.listdir(settings.PYTHONPATH) if file.endswith('.xlsx')]:
            # file_name=file_name.replace('.json','')
            file_name=file_name.replace('.xlsx','')
            list_all_files.append(file_name)

        responseValue = {
            "status": 200,
            "list_all_files":list_all_files,
            "error": "Correct Data",
    }
    else:
        responseValue = {
            "status": 404,
            "error": "Incorrect Data",
        }

    return JsonResponse(responseValue, safe=False)

def crosstab_table(request):
    print("Function 1- crosstab_table STARED!")
    if request.method == "POST":
        measure_row_column_position = 'measure_in_column'
        agg_func = 'sum'
        time_start = time.time()
        rowfilter = request.POST.get('rowfilter_val')
        columnfilter = request.POST.get('columnfilter_val')
        percent_calc = request.POST.get('calculation_type_name')
        # weight_param = 'weighted'
        weight_param = request.POST.get('weight_type_name')
       
        final_row_col_array_grp = request.POST.get('final_row_col_array_grp')
        final_row_col_array_grp_json = json.loads(final_row_col_array_grp)
        # df = pd.DataFrame(final_row_col_array_grp_json)
        data_type_resp = request.POST.get('table_data_type_respone')
        data_type_resp = data_type_resp.replace('"', '')
        print('data_type_resp 152',data_type_resp)
        Measure = request.POST.get('weight_volume_type_name')
        seperated_flag_row = int(request.POST.get('seperated_flag_row_2'))
        seperated_flag_col = int(request.POST.get('seperated_flag_col_2'))
        # round_off_val = int(request.POST.get('decimal_point_filter'))
        # totals_nested_flag = int(request.POST.get('Total_column_filter'))
        totals_nested_flag = 1
        crosstab_function_name = 'crosstab1'
        measure_selected_key_val_resp = 0
        # selected_weight_column_all = ["YA_(Volume_Sales)","PP_(Volume_Sales)","Volume_Sales","Volume_%_Share"]
        # indices_calc_flag = 0
        # data_type_resp='response'
        # Measure = 'People'
        # Measure = 'Occasion'
        # Measure = 'Volume'
        # data_type_resp = 'respondent'
        # data_type_resp = 'response'#m
        print('data_type_resp==',data_type_resp)
        print('Measure==',Measure)
        print('Measure== type',type(Measure))
        print('data_type_resp== type',type(data_type_resp))
        # exit()

        rowfilter = rowfilter.replace('[', '')
        rowfilter = rowfilter.replace(']', '')
        rowfilter = rowfilter.replace('"', '')
        columnfilter = columnfilter.replace('[', '')
        columnfilter = columnfilter.replace(']', '')
        columnfilter = columnfilter.replace('"', '')


        row_name = list(rowfilter.split(","))
        col_name = list(columnfilter.split(","))

        print("row_name type",type(row_name))
        print("row_name row_name",row_name)
        print("col_name type",type(col_name))
        print("col_name col_name",col_name)

        # selected_weight_column = 'weighting'
        print("rowfilter",rowfilter)
        print("columnfilter",columnfilter)
        print("rowfilter type",type(rowfilter))
        print("columnfilter type",type(columnfilter))

        wt_measures_str = request.POST.get('wt_measures')
        wt_measures_str = wt_measures_str.replace('[', '')
        wt_measures_str = wt_measures_str.replace(']', '')
        wt_measures_str = wt_measures_str.replace('"', '')
        selected_weight_column22 = list(wt_measures_str.split(","))
        # print('294====selected_weight_column_all',selected_weight_column_all)

        data_type_resp = 'sales'

        # measure_under_time_flag = 1
        # measure_under_time_flag = request.POST.get('measure_time_toggle')
        # print('measure_under_time_flag',measure_under_time_flag)

        # print("weight_param",weight_param)
        # print("table_name",table_name)
        # print("seperated_flag_row",seperated_flag_row)
        # print("seperated_flag_col",seperated_flag_col)
        # print("final_row_col_array_grp",final_row_col_array_grp_json)
        # dict_table = final_row_col_array_grp_json[0] #commented 
        # print("dict_table",dict_table) 
        # print("dict_table type",type(dict_table))
        # exit('==================================');
        # round_off_val = decimal_point_filter
        # data_type_resp = 'concat'

        ################### ADDED ON 18-05-2023 - INDICES ################################
        if percent_calc == 'Indices':
            percent_calc = 'column_percent'
            significance_flag = 0
            indices_calc_flag = 1

        elif percent_calc == 'Significance':
            percent_calc = 'column_percent'
            significance_flag = 1
            indices_calc_flag = 0

        else:
            percent_calc = percent_calc
            significance_flag = 0
            indices_calc_flag = 0

        ################### ADDED ON 18-05-2023 - INDICES ################################

        dict_table = {}
        for loop_dict in final_row_col_array_grp_json:
            dict_table.update(loop_dict)
            print("loop_dict== loop_dict",loop_dict)

        print('dict_table====',dict_table)

        # dict_table[','.join([str(key) for key in dict_table.keys()])].extend(selected_weight_column_all)

        print('==dict_table after 342',dict_table)

        selected_weight_column_all = ['Volume','Volume YA', 'Volume PP','Sales (JPY)','Sales YA (JPY)','Sales PP (JPY)',
                                  'TDP TY','TDP YA', 'TDP PP','WD','WD YA','WD PP','ND','ND YA','ND PP',
                                  ]


        dict_base_filter_resp = {

        # 'Electrolux_India_respondent': [],
        'Electrolux_India_respondent': ['Age_:_Post_code','Gender']
        }
        
        
        # ================================================================================================ #
        # ================================================================================================ #
        # ===============================Main logic start here============================= #
        # ===============================Main logic start here============================= #
        
        ######################## CROSSTAB LOGIC #################################################

        selected_weight_column = create_selected_weight_column(Measure)

        ###################### ADDED ON 11-04-2023 #################################################
        loop_vals_lst = []
        for loop_vals in dict_table.values():
            loop_vals_lst.extend(loop_vals)

        base_filter_col_lst = []
        for loop_vals11 in dict_base_filter_resp.values():
            base_filter_col_lst.extend(loop_vals11)
        ###################### ADDED ON 11-04-2023 #################################################

    
        ##################################### POLARS ###################################
        start_time_read = time.time()
        # filename = list(dict_table.keys())[0] + ".json"
        # filename = list(dict_table.keys())[0] + ".csv"
        filename = list(dict_table.keys())[0] + ".xlsx"
        # df = pl.read_csv(settings.PYTHONPATH + filename)
        df = pl.read_excel(settings.PYTHONPATH + filename,sheet_name = 'Data')

        ################# NEW CODE - 11-03-2024 ###########################
        df_codeframe = pl.read_excel(settings.PYTHONPATH + filename,sheet_name = 'Codeframe')
        df_codeframe = df_codeframe.to_pandas()
        selected_weight_column_all = create_selected_weight_columns(selected_weight_column22,df_codeframe)
        ################# NEW CODE - 11-03-2024 ###########################
        print('line 151 else condition')
        end_time_read = time.time()
        print("Time taken to read file using POLARS was ", end_time_read - start_time_read, "seconds!")

        df = df.to_pandas()
        print('df colss before reading==',df.columns)
        df = df.rename(columns=rename_input_cols_dict)
        print('df colss after reading==',df.columns)
        ##################################### POLARS #####################################

        ################ ADDED BY MIHIR PAWAR - 04-08-2023 - TIME FILTER ##################
        time_period_vals = df['Time'].unique().tolist() #distinct/unique of time periods

        time_period_filter_val = [time_period_vals[0]]
        time_period_filter_val_resp = {'selected_time_period':time_period_filter_val}
        
        df = df[df['Time'].isin(time_period_filter_val)]
        ################ ADDED BY MIHIR PAWAR - 04-08-2023 - TIME FILTER ##################


        ############## ADDED BY MIHIR PAWAR - 30-08-2023 - DERIVED COUMNS ###
        time_derived_start = time.time()

        replace_values = {-np.inf: 0, np.inf: 0, 'null': 0, np.nan: 0}
        df.replace(replace_values, inplace=True)

        # df.to_excel('df_SALES_FINAL.xlsx')
        time_derived_end = time.time()
        print("DERIVED FN TIME",time_derived_end - time_derived_start,"SECONDS!")
        ############## ADDED BY MIHIR PAWAR - 30-08-2023 - DERIVED COUMNS ###
        ######## Added By Mihir Pawar on 11-04-2023 ###############################################

        ###########################################################################################################

        filter_dict_resp = base_filter_resp(df,dict_table,row_name,col_name,selected_weight_column_all) ################
        filter_dict_resp = remove_duplicate_keys_and_values(filter_dict_resp)
        all_categories_vals = base_filter_resp_all(df,dict_table,row_name,col_name) 

        ######################## NEW LOGIC PIVOT 11-03-2024 ############################
        if measure_row_column_position == "measure_in_row":

            cross_df = sales_crosstab_logic_MAIN(selected_weight_column_all, dict_table, df, percent_calc, col_name, row_name,
                                      data_type_resp,seperated_flag_col,
                                      seperated_flag_row, totals_nested_flag,agg_func)

            total_levels = cross_df.columns.nlevels
            print('total_levels',total_levels)

            if total_levels == 2:
                cross_df = cross_df.swaplevel(0, 1, axis=1).sort_index(axis=1)

            elif total_levels == 3:
                cross_df = cross_df.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, total_levels - 1, axis=1).sort_index(axis=1)

            elif total_levels == 4:
                cross_df = cross_df.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, 3, axis=1).swaplevel(3, total_levels - 1, axis=1).sort_index(axis=1)

            cross_df = cross_df.T

        elif measure_row_column_position == "measure_in_column":

            cross_df = sales_crosstab_logic_MAIN(selected_weight_column_all, dict_table, df, percent_calc, row_name, col_name,
                                      data_type_resp,
                                      seperated_flag_row, seperated_flag_col, totals_nested_flag,agg_func)

            total_levels = cross_df.columns.nlevels
            print('total_levels',total_levels)

            if total_levels == 2:
                cross_df = cross_df.swaplevel(0, 1, axis=1).sort_index(axis=1)

            elif total_levels == 3:
                cross_df = cross_df.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, total_levels - 1, axis=1).sort_index(axis=1)

            elif total_levels == 4:
                cross_df = cross_df.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, 3, axis=1).swaplevel(3, total_levels - 1, axis=1).sort_index(axis=1)

        # cross_df.to_excel('cross_df_MAIN.xlsx')

        #################### DERIVED COLUMNS - 11-03-2024 ###################################
        if measure_row_column_position == "measure_in_row":
            # cross_df.to_excel('cross_df_before_transpose.xlsx')
            cross_df = cross_df.T
            cross_df = derived_MAIN_fn(cross_df)
            cross_df = cross_df.T
            # cross_df.to_excel('CROSS_DF_CAUCULATIONS.xlsx')
            # exit('dfddgdgdvde')

        elif measure_row_column_position == "measure_in_column":
            cross_df = derived_MAIN_fn(cross_df)

        last_level_values_list = cross_df.columns.get_level_values(-1).unique().tolist()

        dict_selected_measures_lst = {}

        for key in selected_weight_column22:
            dict_selected_measures_lst[key] = [item for item in last_level_values_list if item.startswith(key)]
        print('last_level_values_list',last_level_values_list)
        print('dict_selected_measures_lst',dict_selected_measures_lst)

        #################### DERIVED COLUMNS - 11-03-2024 ###################################

        ################################################################################################################
        # if (seperated_flag_row == 0 and seperated_flag_col == 0):
        # # if (len(row_name) == 1 and len(col_name) == 1):

        #     cross_df = cross_df.reindex(sorted(cross_df.index), axis=0)
        #     cross_df = cross_df.reindex(sorted(cross_df.columns), axis=1)
        ################################################################################################################

        ######################################### GRAND TOTAL 2024 ############################
        # if measure_row_column_position == "measure_in_row":
        #     try:
        #         for level in cross_df.index.levels:
        #             if 'Grand Total' in level:
        #                 cross_df = cross_df.drop('Grand Total', axis=0, level=level.name)
        #     except:
        #         pass

        #     try:
        #         cross_df.drop(('Grand Total','Grand Total'), axis=1, inplace=True)
        #     except:
        #         pass

        #     try:
        #         cross_df.drop(('Grand Total',''), axis=1, inplace=True)
        #     except:
        #         pass

        # elif measure_row_column_position == "measure_in_column":
        #     try:
        #         for level in cross_df.columns.levels:
        #             if 'Grand Total' in level:
        #                 cross_df = cross_df.drop('Grand Total', axis=1, level=level.name)
        #     except:
        #         pass

        #     try:
        #         cross_df.drop(('Grand Total','Grand Total'), axis=0, inplace=True)
        #     except:
        #         pass

        #     try:
        #         cross_df.drop(('Grand Total',''), axis=0, inplace=True)
        #     except:
        #         pass

        ######################################### GRAND TOTAL 2024 ###########################

        ############# NEW CODE - ALLIGN HEADERS - 11-03-2024###################
        # cross_df.to_excel('BEFORE_allign_grand_total_headers_fN.xlsx')
        if measure_row_column_position == "measure_in_column":
            cross_df = allign_grand_total_headers_fn(cross_df)

            cross_df = cross_df.T
            cross_df = allign_grand_total_headers_fn(cross_df)
            cross_df = cross_df.T

        elif measure_row_column_position == "measure_in_row":
            cross_df = allign_grand_total_headers_fn(cross_df)

            cross_df = cross_df.T
            cross_df = allign_grand_total_headers_fn(cross_df)
            cross_df = cross_df.T

        # cross_df.to_excel('allign_grand_total_headers_fN.xlsx')
        ############# NEW CODE - ALLIGN HEADERS - 11-03-2024###################

        cross_df.fillna(0,inplace=True)
        cross_df = cross_df.replace([np.nan, np.inf, -np.inf], 0)

        ########## added by mihir pawar - rounding dataframe to user-defined limit 
        # cross_df = round(cross_df,round_off_val)

        ######################## CROSSTAB LOGIC #####################################################

        print('seperated_flag_row===',seperated_flag_row)
        print('seperated_flag_col===',seperated_flag_col)

        #################### ADDED BY MIHIR PAWAR ON 14-04-2023 ##########################
        # if ((seperated_flag_col == 1) and (len(row_name) == 1)) or ((seperated_flag_row == 1) and (len(col_name) == 1)) or ((seperated_flag_col == 1) and (seperated_flag_row == 1)):
        if (len(row_name) == 1) and (len(col_name) == 1):
            print("GRAPH LOGIC BEGINS...")

            ################# ADDED BY MIHIR PAWAR ON 25-04-2023 #############
            # REMOVING MULTIINDEX HEADER FROM COLUMN AND ROW
            cross_df_graph = cross_df.copy() 
            ######################### commented og 29092023 ###########################
            cross_df_graph = cross_df_graph.droplevel(0, axis=0)
            # cross_df_graph = cross_df_graph.droplevel(0, axis=1)
            ######################### commented og 29092023 ###########################
            # print('measure_under_time_flag==719',measure_under_time_flag)
            cross_df_graph.columns = cross_df_graph.columns.map(lambda x: '|'.join(x))
            # cross_df_graph.index = cross_df_graph.index.map(lambda x: '|'.join(x))

            # if measure_under_time_flag == 1:
            #     # separator = "|"

            #     # # Use regular expressions and str.replace to swap words for all columns
            #     # pattern = rf'(\w+){re.escape(separator)}(\w+)'
            #     # replacement = r'\2'+separator+r'\1'
            #     # cross_df_graph.columns = cross_df_graph.columns.str.replace(pattern, replacement, regex=True)
            #     ###################### method 2 of swapping ###################
            #     # Define the separator you want to use
            #     separator = '|'

            #     # Function to swap words in a column name
            #     def swap_words(column_name):
            #         words = column_name.split(separator)
            #         if len(words) == 2:
            #             return f"{words[1].strip()}{separator}{words[0].strip()}"
            #         else:
            #             return column_name

            #     # Apply the function to all column names
            #     cross_df_graph.columns = cross_df_graph.columns.map(swap_words)
                ############### method 2 of swapping #####################
            # # Define the old substring and the new substring
            # old_substring = "000AAAATotal"
            # new_substring = "Grand Total"

            # # Replace the old substring with the new substring in column names
            # new_columns = [col.replace(old_substring, new_substring) for col in cross_df_graph.columns]
            # cross_df_graph.columns = new_columns

            # if (seperated_flag_row == 1) and (seperated_flag_col == 1):
            #     cross_df_graph = cross_df.copy()
            #     print('1st chart fn condn======')
            #     cross_df_graph = cross_df_graph.droplevel(0, axis=0)
            #     cross_df_graph = cross_df_graph.droplevel(0, axis=1)

            # elif (seperated_flag_col == 1) and (len(row_name) == 1):
            #     print('2nd chart fn condn======')
            #     cross_df_graph = cross_df.copy()
            #     cross_df_graph = cross_df_graph.droplevel(0, axis=1)

            # elif (seperated_flag_row == 1) and (len(col_name) == 1):
            #     print('3rd chart fn condn======')
            #     cross_df_graph = cross_df.copy()
            #     cross_df_graph = cross_df_graph.droplevel(0, axis=0)

            ################# ADDED BY MIHIR PAWAR ON 25-04-2023 #############
            # cross_df_graph.to_excel(settings.FINAL_CROSSTAB_OUTPUT+ 'FINAL_CROSSTAB_CHART.xlsx')
            # cross_df_graph.to_csv(settings.FINAL_CROSSTAB_OUTPUT+ 'FINAL_CROSSTAB_CHART.csv')
            # cross_df_graph.to_json(settings.FINAL_CROSSTAB_OUTPUT + 'crosstab_data' + ".json", orient = 'split')


        if ('time_period' in row_name) or ('time_period' in col_name) or (('time_period' in row_name) and ('time_period' in col_name)):
            time_period_flag = 1
        else:
            time_period_flag = 0
        print("GRAPH LOGIC ENDS...")
        ################### ADDED BY MIHIR PAWAR ON 14-04-2023 ##########################

        # cross_df.style.highlight_max(color='lightgreen', axis=0)

        time_end = time.time()
        print("TIME TAKEN TO RUN CROSSTAB FUNCTION WAS ", time_end - time_start, "SECONDS!!!")
        # cross_df.to_excel(output_settings.PYTHONPATH + "FINAL_CROSSTAB.xlsx",engine='openpyxl')

        def highlight_max(s, props=''):
            return np.where(s == np.nanmax(s.values), props, '')

        def highlight_min(s, props=''):
            return np.where(s == np.nanmin(s.values), props, '')
    ######################################## STYLING COLUMNS AND INDEX ###################################################

        ######################################## STYLING COLUMNS AND INDEX ###################################################

                # exit("end!")
        row_nameStr = ','.join([str(elem) for elem in row_name])
        col_nameStr = ','.join([str(elem) for elem in col_name])
        selected_weight_column_str = ','.join([str(elem) for elem in selected_weight_column_all])

        legends_dict = {'Parameters':['Row Variable','Column Variable','Facts Variables','Calculation Type'],
                        'Values':[row_nameStr,col_nameStr,selected_weight_column_str,percent_calc.capitalize()]}

        legends_df = pd.DataFrame(legends_dict)
        legends_df.set_index('Parameters',inplace=True)

        ########## ADDED BY MIHIR PAWAR ON 17-05-2023 ###############################################
        legends_df['Values'] = legends_df['Values'].replace(r"_", " ", regex=True)

        ########## ADDED BY MIHIR PAWAR ON 17-05-2023 ###############################################
        print("========")
        print(legends_df)
        print("========")

        # cross_df = cross_df.replace(to_replace=0,value=np.nan)

        ############# SUMMARY OF CROSSTAB DATA ##############################
        crosstab_summary = cross_df.describe()
        # crosstab_summary.to_excel('crosstab_summary.xlsx')
        ############# SUMMARY OF CROSSTAB DATA ##############################

        ############# ADDED BY MIHIR PAWAR - SAVING CROSSTAB EXCEL FILE - 22-05-2023 ###########
        # saving_crosstab_excel_file(cross_df,legends_df,percent_calc)
        ############# ADDED BY MIHIR PAWAR - SAVING CROSSTAB EXCEL FILE -

        # cross_df_highlighter = cross_df.copy()

        # dfs = [cross_df_highlighter,legends_df]
        # # dfs = [legends_df,cross_df_highlighter]
        # startrow = 0
        # with pd.ExcelWriter(settings.FINAL_CROSSTAB_OUTPUT+'cross_df.xlsx') as writer:
        #     counter = 0
        #     for df in dfs:

        #         df.to_excel(writer, engine="openpyxl", startrow=startrow)
        #         startrow += (df.shape[0] + 7)

        df_cross_json1 = cross_df.to_json(orient='split')  # records - pranit
        df_cross_json = json.loads(df_cross_json1)

        time_end = time.time()
        print("Time of execution - ", time_end - time_start)

        ############################# base filter response function ##########################
        # filter_dict_resp = base_filter_resp()
        ############################# base filter response function ##########################
        base_column_names_resp = {'type':'other','base_column_names_resp':'No Indices/Significance Selected'}
        responseValue = {
                "status": 200,
                "row_length": 'row_length',
                "column_length": 'column_length',
                "rowcount_dict":'rowcount_dict',
                "columncount_dict":'columncount_dict',
                "df_cross_json": df_cross_json,
                "significance_df_json": 'No Significance Data',
                "base_column_names_resp": base_column_names_resp,
                "dict_selected_measures_lst": dict_selected_measures_lst,
                # "base_column_names_indices_resp": base_column_names_indices_resp,
                "filter_dict_resp":filter_dict_resp,
                "all_categories_vals":all_categories_vals,
                "time_period_flag": time_period_flag,
                "time_period_vals": time_period_vals,
                "time_period_filter_val_resp": time_period_filter_val_resp,
                # "df_cross_json_test": df_cross_json21,
                "error": "Correct Data",
                "seperated_flag_col":seperated_flag_col,
                # "merge_filename": filename_merged,

            }
    else:
        responseValue = {
            "status": 404,
            "error": "Incorrect Data",
        }

    # response = StreamingHttpResponse(responseValue)

    return JsonResponse(responseValue, safe=False)
    # return StreamingHttpResponse(responseValue)


#=============================================================================================
def crosstab_table_page2(request):
    print("Function 2- crosstab_table_page2 STARTED!")

    if request.method == "POST":
        # measure_row_column_position = 'measure_in_column'
        measure_row_column_position = request.POST.get('measure_type')
        agg_func = 'sum'
        time_start = time.time()
        rowfilter = request.POST.get('rowfilter_val')
        columnfilter = request.POST.get('columnfilter_val')
        percent_calc = request.POST.get('calculation_type_name')
        # weight_param = 'weighted'
        weight_param = request.POST.get('weight_type_name')
        base_column = request.POST.get('base_column')
       
        final_row_col_array_grp = request.POST.get('final_row_col_array_grp')
        print('final_row_col_array_grp typee==',type(final_row_col_array_grp))
        print('final_row_col_array_grp dataa',final_row_col_array_grp)
        final_row_col_array_grp_json = json.loads(final_row_col_array_grp)
        print('909==final_row_col_array_grp_json',final_row_col_array_grp_json)
        dict_base_filter_data_resp = request.POST.get('filter_data')
        print('dict_base_filter_data_resp typee==',type(dict_base_filter_data_resp))
        print('dict_base_filter_data_resp dataa==',dict_base_filter_data_resp)

        dict_base_filter_data_resp_json11 = ast.literal_eval(dict_base_filter_data_resp)
        dict_base_filter_data_resp_json = json.loads(dict_base_filter_data_resp_json11)
        print('929==dict_base_filter_data_resp_json',dict_base_filter_data_resp_json)
        print('929==dict_base_filter_data_resp_json930',type(dict_base_filter_data_resp_json))
        # dict_base_filter_data_resp_json = dict_base_filter_data_resp[0]
        # df = pd.DataFrame(final_row_col_array_grp_json)
        data_type_resp = request.POST.get('table_data_type_respone')
        data_type_resp = data_type_resp.replace('"', '')
        print('data_type_resp 152',data_type_resp)
        Measure = request.POST.get('weight_volume_type_name')
        seperated_flag_row = int(request.POST.get('seperated_flag_row_2'))
        seperated_flag_col = int(request.POST.get('seperated_flag_col_2'))
        # round_off_val = int(request.POST.get('decimal_point_filter'))
        # totals_nested_flag = int(request.POST.get('Total_column_filter'))
        totals_nested_flag = 1
        crosstab_function_name = 'crosstab2'
        # selected_weight_column_all = ["YA_(Volume_Sales)","PP_(Volume_Sales)","Volume_Sales","Volume_%_Share"]
        # indices_calc_flag = 0
        # filename = 'cbl_respondent_cbl_response.json'

        # data_type_resp='response'
        # Measure = 'People'
        # Measure = 'Occasion'
        # Measure = 'Volume'
        # data_type_resp = 'respondent'
        # data_type_resp = 'response'#m
        print('data_type_resp==',data_type_resp)
        print('Measure==',Measure)
        print('Measure== type',type(Measure))
        print('data_type_resp== type',type(data_type_resp))
        # exit()

        rowfilter = rowfilter.replace('[', '')
        rowfilter = rowfilter.replace(']', '')
        rowfilter = rowfilter.replace('"', '')
        columnfilter = columnfilter.replace('[', '')
        columnfilter = columnfilter.replace(']', '')
        columnfilter = columnfilter.replace('"', '')


        row_name = list(rowfilter.split(","))
        col_name = list(columnfilter.split(","))

        print("row_name type",type(row_name))
        print("row_name row_name",row_name)
        print("col_name type",type(col_name))
        print("col_name col_name",col_name)

        # selected_weight_column = 'weighting'
        print("rowfilter",rowfilter)
        print("columnfilter",columnfilter)
        print("rowfilter type",type(rowfilter))
        print("columnfilter type",type(columnfilter))

        wt_measures_str = request.POST.get('wt_measures')
        wt_measures_str = wt_measures_str.replace('[', '')
        wt_measures_str = wt_measures_str.replace(']', '')
        wt_measures_str = wt_measures_str.replace('"', '')
        selected_weight_column22 = list(wt_measures_str.split(","))
        print('selected_weight_column22===927',selected_weight_column22)

        Time_val = request.POST.get('Time_val')
        Time_val = Time_val.replace('[', '')
        Time_val = Time_val.replace(']', '')
        Time_val = Time_val.replace('"', '')
        time_period_filter_val = list(Time_val.split(","))
        time_period_filter_val_resp = {'selected_time_period':time_period_filter_val}

        # time_period_filter_val = ['MAT','QTR']
        # measure_under_time_flag = int(request.POST.get('measure_time_toggle'))
        # print('measure_under_time_flag crosstab func 2',measure_under_time_flag)

        data_type_resp = 'sales'
        # measure_selected_key_val_resp = {'Volume':['Volume','Volume YA', 'Volume PP'],
        # 'API':['API','API YA','API PP']}
        measure_selected_key_val_resp11 = request.POST.get('facts_object')
        measure_selected_key_val_resp = json.loads(measure_selected_key_val_resp11)
        print('=====measure_selected_key_val_resp==',measure_selected_key_val_resp)

        selected_weight_column22 = list(measure_selected_key_val_resp.keys())
        # print("weight_param",weight_param)
        # print("table_name",table_name)
        # print("seperated_flag_row",seperated_flag_row)
        # print("seperated_flag_col",seperated_flag_col)
        # print("final_row_col_array_grp",final_row_col_array_grp_json)
        # dict_table = final_row_col_array_grp_json[0] #commented 
        # print("dict_table",dict_table) 
        # print("dict_table type",type(dict_table))
        # exit('==================================');
        # round_off_val = decimal_point_filter
        # data_type_resp = 'concat'
        # base_column = 'Total'
        ################### ADDED ON 18-05-2023 - INDICES ################################
        if percent_calc == 'Indices':
            percent_calc = 'column_percent'
            significance_flag = 0
            indices_calc_flag = 1

        elif percent_calc == 'Significance':
            percent_calc = 'column_percent'
            significance_flag = 1
            indices_calc_flag = 0

        else:
            percent_calc = percent_calc
            significance_flag = 0
            indices_calc_flag = 0
        ################### ADDED ON 18-05-2023 - INDICES ################################
        # dict_table = final_row_col_array_grp_json[0]
        dict_table = {}
        for loop_dict in final_row_col_array_grp_json:
            dict_table.update(loop_dict)
            print("loop_dict== loop_dict",loop_dict)

        print('dict_table====',dict_table)

        ################ ADDED BY MIHIR PAWAR ON 24-05-2023 ###############################
        print('dict_base_filter_data_resp_json==1050',dict_base_filter_data_resp_json)
        print('dict_base_filter_data_resp_json==1051',type(dict_base_filter_data_resp_json))
        # dict_base_filter_data = dict_base_filter_data_resp_json[0]
        dict_base_filter_data = {}
        for loop_dict in dict_base_filter_data_resp_json:
            print('loop_dict====2nd crosstab fn==',loop_dict)
            
            dict_base_filter_data.update(loop_dict)
            print("loop_dict== loop_dict",loop_dict)

        print('dict_base_filter_data====',dict_base_filter_data)
        ################ ADDED BY MIHIR PAWAR ON 24-05-2023 ###############################
        # ================================================================================================ #
        # ================================================================================================ #
        # ===============================Main logic start here============================= #
        ######################## CROSSTAB LOGIC #################################################

        selected_weight_column = create_selected_weight_column(Measure)

        ###################### ADDED ON 11-04-2023 #################################################
        loop_vals_lst = []
        for loop_vals in dict_table.values():
            loop_vals_lst.extend(loop_vals)

        base_filter_col_lst = list(dict_base_filter_data.keys())
        # base_filter_col_lst = []
        # for loop_vals11 in dict_base_filter_data.keys():  #for CROSSTAB PAGE 2 ONLY
        #     # base_filter_col_lst.extend(loop_vals11)
        #     print("loop_vals11=== page2 ",loop_vals11)
        
        ##################################### POLARS ###################################
        start_time_read = time.time()
        # filename = list(dict_table.keys())[0] + ".json"
        # filename = list(dict_table.keys())[0] + ".csv"
        filename = list(dict_table.keys())[0] + ".xlsx"
        # df = pl.read_csv(settings.PYTHONPATH + filename)
        df = pl.read_excel(settings.PYTHONPATH + filename,sheet_name = 'Data')

        ################# NEW CODE - 11-03-2024 ###########################
        df_codeframe = pl.read_excel(settings.PYTHONPATH + filename,sheet_name = 'Codeframe')
        df_codeframe = df_codeframe.to_pandas()
        selected_weight_column_all = create_selected_weight_columns(selected_weight_column22,df_codeframe)
        print('selected_weight_column_all 1027',selected_weight_column_all)
        # exit('selected_weight_column_all===1028')
        ################# NEW CODE - 11-03-2024 ###########################
        print('line 151 else condition')
        end_time_read = time.time()
        print("Time taken to read file using POLARS was ", end_time_read - start_time_read, "seconds!")

        df = df.to_pandas()
        print('df colss before reading==',df.columns)
        df = df.rename(columns=rename_input_cols_dict)
        print('df colss after reading==',df.columns)
        ##################################### POLARS #####################################

        ################ ADDED BY MIHIR PAWAR - 04-08-2023 - TIME FILTER #################
        time_period_vals = df['Time'].unique().tolist() #distinct/unique of time periods
        df = df[df['Time'].isin(time_period_filter_val)]
        ################ ADDED BY MIHIR PAWAR - 04-08-2023 - TIME FILTER #################

        ######## Added By Mihir Pawar 24-04-2023 - READ FILE LOGIC FOR CROSSTAB FUNCTION 2 ONLY ###############################################

         ############## ADDED BY MIHIR PAWAR - 30-08-2023 - DERIVED COUMNS ###
        time_derived_start = time.time()

        replace_values = {-np.inf: 0, np.inf: 0, 'null': 0, np.nan: 0}
        df.replace(replace_values, inplace=True)

        # df.to_excel('df_SALES_FINAL.xlsx')

        time_derived_end = time.time()
        print("DERIVED FN TIME",time_derived_end - time_derived_start,"SECONDS!")
        ############## ADDED BY MIHIR PAWAR - 30-08-2023 - DERIVED COUMNS ###

        ########################################################################################################
        filter_dict_resp = base_filter_resp(df,dict_table,row_name,col_name,selected_weight_column_all) ###########################
        filter_dict_resp = remove_duplicate_keys_and_values(filter_dict_resp)
        all_categories_vals = base_filter_resp_all(df,dict_table,row_name,col_name)

        df = base_filter_data(df,dict_base_filter_data) ###########################

        ######################## NEW LOGIC PIVOT 11-03-2024 ############################
        if measure_row_column_position == "measure_in_row":

            cross_df = sales_crosstab_logic_MAIN(selected_weight_column_all, dict_table, df, percent_calc, col_name, row_name,
                                      data_type_resp,seperated_flag_col,
                                      seperated_flag_row, totals_nested_flag,agg_func)
            # cross_df.to_excel('cross_df_MAIN_measure_row_column_position.xlsx')
            total_levels = cross_df.columns.nlevels
            print('total_levels',total_levels)

            if total_levels == 2:
                cross_df = cross_df.swaplevel(0, 1, axis=1)

            elif total_levels == 3:
                cross_df = cross_df.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, total_levels - 1, axis=1)

            elif total_levels == 4:
                cross_df = cross_df.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, 3, axis=1).swaplevel(3, total_levels - 1, axis=1)

            ################## old code - added .sort_index() ###############
            # if total_levels == 2:
            #     cross_df = cross_df.swaplevel(0, 1, axis=1).sort_index(axis=1)

            # elif total_levels == 3:
            #     cross_df = cross_df.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, total_levels - 1, axis=1).sort_index(axis=1)

            # elif total_levels == 4:
            #     cross_df = cross_df.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, 3, axis=1).swaplevel(3, total_levels - 1, axis=1).sort_index(axis=1)
            ################## old code - added .sort_index() ###############

            cross_df = cross_df.T

        elif measure_row_column_position == "measure_in_column":
            print('===================================================1085')
            print('selected_weight_column_all',selected_weight_column_all)
            print('dict_table',dict_table)
            print('df',df.shape)
            print('percent_calc',percent_calc)
            print('row_name',row_name)
            print('col_name',col_name)
            print('===================================================1085')

            cross_df = sales_crosstab_logic_MAIN(selected_weight_column_all, dict_table, df, percent_calc, row_name, col_name,
                                      data_type_resp,
                                      seperated_flag_row, seperated_flag_col, totals_nested_flag,agg_func)
            # cross_df.to_excel('cross_df_MAIN_measure_row_column_position.xlsx')
            total_levels = cross_df.columns.nlevels
            print('total_levels',total_levels)

            if total_levels == 2:
                cross_df = cross_df.swaplevel(0, 1, axis=1)

            elif total_levels == 3:
                cross_df = cross_df.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, total_levels - 1, axis=1)

            elif total_levels == 4:
                cross_df = cross_df.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, 3, axis=1).swaplevel(3, total_levels - 1, axis=1)

            ################## old code - added .sort_index() ###############
            # if total_levels == 2:
            #     cross_df = cross_df.swaplevel(0, 1, axis=1).sort_index(axis=1)

            # elif total_levels == 3:
            #     cross_df = cross_df.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, total_levels - 1, axis=1).sort_index(axis=1)

            # elif total_levels == 4:
            #     cross_df = cross_df.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, 3, axis=1).swaplevel(3, total_levels - 1, axis=1).sort_index(axis=1)
            ################## old code - added .sort_index() ###############

        # cross_df.to_excel('cross_df_MAIN.xlsx')

        #################### DERIVED COLUMNS - 11-03-2024 ###################################
        if measure_row_column_position == "measure_in_row":
            cross_df = cross_df.T
            cross_df = derived_MAIN_fn(cross_df)
            cross_df = cross_df.T

        elif measure_row_column_position == "measure_in_column":
            cross_df = derived_MAIN_fn(cross_df)

        lst_measures = list(measure_selected_key_val_resp.values())
        lst_measures_vals = [item for sublist in lst_measures for item in (sublist if isinstance(sublist, list) else [sublist])]
        print('lst_measures 11577',lst_measures)

        if measure_row_column_position == "measure_in_row":
            cross_df = cross_df.loc[cross_df.index.get_level_values(-1).isin(list(lst_measures_vals)),:]
        elif measure_row_column_position == 'measure_in_column':
            cross_df = cross_df.loc[:,cross_df.columns.get_level_values(-1).isin(list(lst_measures_vals))]

        #################### DERIVED COLUMNS - 11-03-2024 ###################################

                ######################################### GRAND TOTAL 2024 ############################
        if measure_row_column_position == "measure_in_row":
        #     try:
        #         for level in cross_df.index.levels:
        #             if 'Grand Total' in level:
        #                 cross_df = cross_df.drop('Grand Total', axis=0, level=level.name)
        #     except:
        #         pass

            try:
                cross_df.drop(('Grand Total','Grand Total'), axis=1, inplace=True)
            except:
                pass

            try:
                cross_df.drop(('Grand Total',''), axis=1, inplace=True)
            except:
                pass

        elif measure_row_column_position == "measure_in_column":
        #     try:
        #         for level in cross_df.columns.levels:
        #             if 'Grand Total' in level:
        #                 cross_df = cross_df.drop('Grand Total', axis=1, level=level.name)
        #     except:
        #         pass

            try:
                cross_df.drop(('Grand Total','Grand Total'), axis=0, inplace=True)
            except:
                pass

            try:
                cross_df.drop(('Grand Total',''), axis=0, inplace=True)
            except:
                pass

            ######################################### GRAND TOTAL 2024 ###########################

        cross_df.fillna(0,inplace=True)
        cross_df = cross_df.replace([np.nan, np.inf, -np.inf], 0)
        # cross_df.to_excel('NULL_CROSSDF.xlsx')

        ############################### NEW LOGIC DERIVED COLUMNS - 29-09-2023 ############################
        # cross_df.to_excel('BEFORE_allign_grand_total_headers_fN.xlsx')
        if measure_row_column_position == "measure_in_column":
            cross_df = allign_grand_total_headers_fn(cross_df)

            cross_df = cross_df.T
            cross_df = allign_grand_total_headers_fn(cross_df)
            cross_df = cross_df.T

        elif measure_row_column_position == "measure_in_row":
            cross_df = allign_grand_total_headers_fn(cross_df)

            cross_df = cross_df.T
            cross_df = allign_grand_total_headers_fn(cross_df)
            cross_df = cross_df.T

        # cross_df.to_excel('allign_grand_total_headers_fN.xlsx')
        ########### ORDERING THE TIME PERIODS ACCORDING TO THE DESIRED ORDER - 01-08-2023 ##########################

        ################# CROSSTAB MAIN FUNCTION - CREATED BY MIHIR PAWAR 21-12-2022 ########

        ############## ADDED BY MIHIR PAWAR ON 30-06-2023- ALLIGN HEADERS ################
        # cross_df.to_excel("cross_df_allign_headers.xlsx")
        # if percent_calc !='actual_count':
        #     cross_df = allign_headers_condn(cross_df, percent_calc,seperated_flag_row,seperated_flag_col,row_name,col_name)
        ############# ADDED BY MIHIR PAWAR ON 30-06-2023- ALLIGN HEADERS  ##############

        ########## added by mihir pawar - rounding dataframe to user-defined limit ############################
        # cross_df = round(cross_df,round_off_val)

        ######################## CROSSTAB LOGIC #####################################################
              
        # if ((seperated_flag_col == 1) and (len(row_name) == 1)) or ((seperated_flag_row == 1) and (len(col_name) == 1)) or ((seperated_flag_col == 1) and (seperated_flag_row == 1)):
        if (len(row_name) == 1) and (len(col_name) == 1):
            print("GRAPH LOGIC BEGINS...")

            ################# ADDED BY MIHIR PAWAR ON 25-04-2023 #############
            # REMOVING MULTIINDEX HEADER FROM COLUMN AND ROW 
            cross_df_graph = cross_df.copy()
            cross_df_graph = cross_df_graph.droplevel(0, axis=0)
            # cross_df_graph = cross_df_graph.droplevel(0, axis=1)
            # print('measure_under_time_flag==1372',measure_under_time_flag)
            cross_df_graph.columns = cross_df_graph.columns.map(lambda x: '|'.join(x))
            # cross_df_graph.index = cross_df_graph.index.map(lambda x: '|'.join(x))

            # if measure_under_time_flag == 1:
            #     # separator = "|"
            #     # # Use regular expressions and str.replace to swap words for all columns
            #     # pattern = rf'(\w+){re.escape(separator)}(\w+)'
            #     # replacement = r'\2'+separator+r'\1'
            #     # cross_df_graph.columns = cross_df_graph.columns.str.replace(pattern, replacement, regex=True)

            #     ####################### METHOD 2 OF SWAPPING #############
            #     separator = '|'

            #     # Function to swap words in a column name
            #     def swap_words(column_name):
            #         words = column_name.split(separator)
            #         if len(words) == 2:
            #             return f"{words[1].strip()}{separator}{words[0].strip()}"
            #         else:
            #             return column_name

            #     # Apply the function to all column names
            #     cross_df_graph.columns = cross_df_graph.columns.map(swap_words)
            #     ####################### METHOD 2 OF SWAPPING #############

            # ################ ADDED BY MIHIR PAWAR ON 25-04-2023 #############
            # cross_df_graph.to_excel(settings.FINAL_CROSSTAB_OUTPUT+ 'FINAL_CROSSTAB_CHART.xlsx')
            # cross_df_graph.to_csv(settings.FINAL_CROSSTAB_OUTPUT+ 'FINAL_CROSSTAB_CHART.csv')

            # cross_df_graph.to_json(settings.FINAL_CROSSTAB_OUTPUT + 'crosstab_data' + ".json", orient='split')
        
        if ('time_period' in row_name) or ('time_period' in col_name) or (('time_period' in row_name) and ('time_period' in col_name)):
            time_period_flag = 1
        else:
            time_period_flag = 0
        ################### ADDED BY MIHIR PAWAR ON 14-04-2023 ##########################

        # cross_df.rename(columns=lambda x: re.sub('total','_total', x), inplace=True)
        # cross_df.rename(index=lambda x: re.sub('total','_total', x), inplace=True)
        ################## Working on removing the prefix from crostab ###################################

        # cross_df.style.highlight_max(color='lightgreen', axis=0)

        time_end = time.time()
        print("TIME TAKEN TO RUN CROSSTAB FUNCTION WAS ", time_end - time_start, "SECONDS!!!")
        # cross_df.to_excel(output_settings.PYTHONPATH + "FINAL_CROSSTAB.xlsx",engine='openpyxl')

        def highlight_max(s, props=''):
            return np.where(s == np.nanmax(s.values), props, '')

        def highlight_min(s, props=''):
            return np.where(s == np.nanmin(s.values), props, '')
        ######################################## STYLING COLUMNS AND INDEX ###################################################

        ######################################## STYLING COLUMNS AND INDEX ###################################################

        # exit("end!")
        row_nameStr = ','.join([str(elem) for elem in row_name])
        col_nameStr = ','.join([str(elem) for elem in col_name])
        selected_weight_column_str = ','.join([str(elem) for elem in lst_measures_vals])

        legends_dict = {'Parameters':['Row Variable','Column Variable','Facts Variables','Calculation Type'],
                        'Values':[row_nameStr,col_nameStr,selected_weight_column_str,percent_calc.capitalize()]}

        legends_df = pd.DataFrame(legends_dict)
        legends_df.set_index('Parameters',inplace=True)

        ########## ADDED BY MIHIR PAWAR ON 17-05-2023 ###############################################
        legends_df['Values'] = legends_df['Values'].replace(r"_", " ", regex=True)

        ########## ADDED BY MIHIR PAWAR ON 17-05-2023 ###############################################
        print("========")
        print(legends_df)
        print("========")

        # cross_df = cross_df.replace(to_replace=0,value=np.nan)

        ############# SUMMARY OF CROSSTAB DATA ##############################
        crosstab_summary = cross_df.describe()
        # crosstab_summary.to_excel('crosstab_summary.xlsx')
        ############# SUMMARY OF CROSSTAB DATA ##############################
        ############# ADDED BY MIHIR PAWAR - SAVING CROSSTAB EXCEL FILE - 22-05-2023 ###########
        # saving_crosstab_excel_file(cross_df,legends_df,percent_calc)
        # saving_crosstab_excel_file(cross_df,legends_df,percent_calc)
        ############# ADDED BY MIHIR PAWAR - SAVING CROSSTAB EXCEL FILE - 22-05-2023 ###########

        # cross_df_highlighter = cross_df.copy()

        # dfs = [cross_df_highlighter,legends_df]
        # # dfs = [legends_df,cross_df_highlighter]
        # startrow = 0
        # with pd.ExcelWriter(settings.FINAL_CROSSTAB_OUTPUT+'cross_df.xlsx') as writer:
        #     counter = 0
        #             for df in dfs:
        #     if counter == 0:
        #     #     # df.style.apply(highlight_max, props='color:white;background-color:darkblue;', axis=0)\
        #     #     #     .apply(highlight_min, props='color:black;background-color:pink;', axis=0).to_excel(writer, engine="openpyxl", startrow=startrow)
        #     #     df.style.background_gradient(cmap='PuBu').to_excel(writer, engine="openpyxl", startrow=startrow) #original working
        #     #
        #         if percent_calc == 'column_percent' or 'Indices':
        #             df.style.background_gradient(cmap='PuBu',axis = 1).to_excel(writer, engine="openpyxl", startrow=startrow) #original working
        #         elif percent_calc == 'row_percent':
        #             df.style.background_gradient(cmap='PuBu',axis = 0).to_excel(writer, engine="openpyxl", startrow=startrow) #original working
        #         elif percent_calc == 'table_percent' or 'actual_count':
        #             df.style.background_gradient(cmap='PuBu',axis = None).to_excel(writer, engine="openpyxl", startrow=startrow) #original working

        #     #
        #     else:
        #         df.to_excel(writer, engine="openpyxl", startrow=startrow)
        #     #
        #     # counter = counter + 1

        #     # df.to_excel(writer, engine="openpyxl", startrow=startrow,index = cross_df.columns[0])
        #     startrow += (df.shape[0] + 7)


        ############### ADDED BY MIHIR PAWAR ON 20-05-2023 #####################
        if percent_calc == 'column_percent' or percent_calc == 'row_percent' or percent_calc == 'table_percent' or percent_calc == 'Significance':
            cross_df = cross_df.mul(100)
        ############### ADDED BY MIHIR PAWAR ON 20-05-2023 #####################

        df_cross_json1 = cross_df.to_json(orient='split')  # records - pranit
        df_cross_json = json.loads(df_cross_json1)
        # ===============================Main Logic end here================================ #
        # ================================================================================================ #
        # ================================================================================================ #
        # testing code
        # df_cross_json2 = cross_df.to_json(orient='columns') #records - pranit
        # df_cross_json21 = json.loads(df_cross_json2)

        if (percent_calc == 'Indices'):
            significance_df_json = 'No Significance Data'

        elif (percent_calc == 'Significance'):
            base_column_names_resp = base_column_names_resp
            significance_df_json = significance_df_json

        elif percent_calc == 'column_percent' or percent_calc == 'row_percent' or percent_calc == 'table_percent' or percent_calc == 'actual_count':
            base_column_names_resp =  {'type':'other','base_column_names_resp':'No Indices/Significance Selected'}
            # base_column_names_resp = 'No Indices/Significance Selected'
            significance_df_json = 'No Significance Data'

        time_end = time.time()
        print("Time of execution - ", time_end - time_start)

        responseValue = {
                "status": 200,
                "row_length": 'row_length',
                "column_length": 'column_length',
                "rowcount_dict":'rowcount_dict',
                "columncount_dict":'columncount_dict',
                "df_cross_json": df_cross_json,
                "significance_df_json": significance_df_json,
                "base_column_names_resp": base_column_names_resp,
                "dict_selected_measures_lst": measure_selected_key_val_resp,
                # "base_column_names_indices_resp": base_column_names_indices_resp,
                "filter_dict_resp":filter_dict_resp,
                "all_categories_vals":all_categories_vals,
                "time_period_flag": time_period_flag,
                "time_period_vals": time_period_vals,
                "time_period_filter_val_resp": time_period_filter_val_resp,
                # "df_cross_json_test": df_cross_json21,
                "error": "Correct Data",
                "seperated_flag_col":seperated_flag_col,
                # "merge_filename": filename_merged,

            }
    else:
        responseValue = {
            "status": 404,
            "error": "Incorrect Data",
        }


    return JsonResponse(responseValue, safe=False)

#=============================================================================================



def crosstab_table_v1(request):

    if request.method == "POST":
        rowfilter = request.POST.get('rowfilter_val')
        columnfilter = request.POST.get('columnfilter_val')
        percent_calc = request.POST.get('calculation_type_name')
        weight_param = request.POST.get('weight_type_name')
        table_name = request.POST.get('tbl_name')
        seperated_flag_row = int(request.POST.get('seperated_flag_row_2'))
        seperated_flag_col = int(request.POST.get('seperated_flag_col_2'))
        row_name = list(rowfilter.split(","))
        col_name = list(columnfilter.split(","))
        print("rowfilter",rowfilter)
        print("columnfilter",columnfilter)
        print("weight_param",weight_param)
        print("table_name",table_name)
        print("seperated_flag_row",seperated_flag_row)
        print("seperated_flag_col",seperated_flag_col)
        


        time_start=time.time()
        filename = table_name+".json"
        # filename = "Kitkat(BLS1564)_all_questions.xlsx"
        # pythonpath = r"C:/Users/MihirPawar/Desktop/Python Project BSW/Python Files1/ccv_tool//")
        # df = pd.read_json(pythonpath + filename, orient='records', lines=True)
        # df = pd.read_excel(pythonpath + filename)
        df = pd.read_json(settings.PYTHONPATH + filename, orient='records', lines=True)
        print("df", df.head(2))
        print("df colsss", df.columns)

        ####### added by MIHIR PAWAR 19-08-2022 ##########################################################
        df = prefix_values(df)
        ####### added by MIHIR PAWAR 19-08-2022 ##########################################################
        # exit("codeeee==")

        #'Gender', 'age_group', 'Zones', 'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6','Q7', 'weighting'
        # row_name=['Q1', 'Q2', 'Q3']
        # row_name=['Q1']
        # col_name=['Gender']
        # col_name=['Gender','age_group', 'Zones']

        print("row_name", row_name)
        print("col_name", col_name)

        # percent_calc = 'column_percent'
        # percent_calc = 'row_percent'
        # percent_calc = 'actual_count'
        # percent_calc = 'grand_total_count'

        selected_weight_column = 'weighting'
        # weight_param = 'weighted'

        ####### FOR STACKED ROWS 0NE BELOW ANOTHER######################################################
        # seperated_flag_row = 0
        ####### FOR STACKED ROWS 0NE BELOW ANOTHER######################################################

        ####### FOR STACKED COLUMNS 0NE BESIDE ANOTHER######################################################
        # seperated_flag_col = 1
        ####### FOR STACKED COLUMNS 0NE BESIDE ANOTHER ######################################################

        ################# CALCULATION PARAMETER #################################################
        if percent_calc == 'column_percent':
            parameter_calc='columns'
        elif percent_calc == 'row_percent':
            parameter_calc = 'index'
        elif percent_calc == 'actual_count':
            parameter_calc = False
        elif percent_calc == 'grand_total_count':
            parameter_calc = 'all'
        ################# CALCULATION PARAMETER #################################################

        row_list_vals = []
        df_row=df[row_name]
        if len(row_name) > 1:
            for loop_row in range(len(row_name)):
                str_row = numpy.array(df_row.iloc[:,loop_row])
                row_list_vals.append(str_row)

        col_list_vals = []
        df_col=df[col_name]
        if len(col_name) > 1:
            for loop_row2 in range(len(col_name)):
                str_col = numpy.array(df_col.iloc[:,loop_row2])
                col_list_vals.append(str_col)

        ################# CROSSTAB BOTH NESTED ##################################################
        if seperated_flag_row == 0 and seperated_flag_col == 0:
            if weight_param == 'unweighted':
                cross_df=unweighted_calc(df,row_name,col_name,row_list_vals,col_list_vals,percent_calc,parameter_calc,selected_weight_column)

            if weight_param == 'weighted':
                cross_df = weighted_calc(df,row_name,col_name,row_list_vals,col_list_vals,parameter_calc,percent_calc,selected_weight_column)
        ################# CROSSTAB BOTH NESTED ##################################################

        if seperated_flag_row==1 and seperated_flag_col==0:
            cross_df=seperated_rows(df,weight_param,row_name,col_name,parameter_calc,selected_weight_column,col_list_vals,percent_calc)

            # cross_df.to_excel("Cross_df_seperated_rows.xlsx")

        if seperated_flag_col==1 and seperated_flag_row==0:
            cross_df = seperated_cols(df,weight_param,row_name,col_name,parameter_calc,selected_weight_column,row_list_vals,percent_calc)

            # cross_df.to_excel("Cross_df_seperated_cols.xlsx")

        # cross_df.to_excel("Cross_df_final.xlsx")
        cross_df.to_excel('static/download_cross_table_excel/cross_df.xlsx')
        print("cross_df",cross_df)
        print("CODE EXECUTED SUCCESSFULLY!")

        df_cross_json1 = cross_df.to_json(orient='split') #records - pranit
        df_cross_json = json.loads(df_cross_json1)
        # testing code
        df_cross_json2 = cross_df.to_json(orient='columns') #records - pranit
        df_cross_json21 = json.loads(df_cross_json2)

        time_end = time.time()
        print("Time of execution - ", time_end - time_start)

        responseValue = {
                "status": 200,
                "row_length": 'row_length',
                "column_length": 'column_length',
                "rowcount_dict":'rowcount_dict',
                "columncount_dict":'columncount_dict',
                "df_cross_json": df_cross_json,
                "df_cross_json_test": df_cross_json21,
                "error": "Correct Data",

            }
    else:
        responseValue = {
            "status": 404,
            "error": "Incorrect Data",
        }


    return JsonResponse(responseValue, safe=False)



def crosstab_table_old(request):
    if request.method == "POST":
        rowfilter = request.POST.get('rowfilter_val')
        columnfilter = request.POST.get('columnfilter_val')
        percent_calc = request.POST.get('calculation_type_name')
        weight_param = request.POST.get('weight_type_name')
        table_name = request.POST.get('tbl_name')
        print('columnfilter_val',rowfilter)
        print('columnfilter',list(columnfilter.split(",")))
        print('columnfilter',type(columnfilter))
        print('percent_calc',percent_calc)
        print('weight_param',weight_param)
        print('percent_calc typee',type(percent_calc))
        print('weight_param typee',type(weight_param))
        time_start=time.time()
        # filename = "BLS200_Test_Brand_3_colss.json"
        filename = table_name+".json"
        print('filename',table_name)
        # print('table_name11',table_name11)
        # filename = "Kitkat(BLS1564)-Control_weighting.json"
        # row_name = ['Gender','Region']
        # col_name = ['Gender','Age_group']
        row_name = list(rowfilter.split(","))
        col_name = list(columnfilter.split(","))

    
        df = pd.read_json(settings.PYTHONPATH + filename, orient='records', lines=True)
        # df['Gender']=='Male' &&  df['Zone']=='Cental India'
        # print("df", df.head(2))
        # print("df colsss", df.columns)
        # exit("codeeee==")

        row_list_vals = []
        df_row = df[row_name]
        if len(row_name) > 1:
            for loop_row in range(len(row_name)):
                str_row = np.array(df_row.iloc[:, loop_row])
                row_list_vals.append(str_row)

        col_list_vals = []
        df_col = df[col_name]
        if len(col_name) > 1:
            for loop_row2 in range(len(col_name)):
                str_col = np.array(df_col.iloc[:, loop_row2])
                col_list_vals.append(str_col)
        ############ crosstab new logic 4 types - 29-07-2022 #######################
        # percent_calc = 'column_percent'
        # percent_calc = 'row_percent'
        # percent_calc = 'actual_count'
        # percent_calc = 'grand_total_count'

        # weight_param='weighted'
        selected_weight_column = 'weighting'

        ## BOTH ROWS AND COLUMNS HAVE LENGTH EQUAL TO 1
        if weight_param=='unweighted':

            if percent_calc != 'grand_total_count':
                if len(row_name) == 1 and len(col_name) == 1:

                    print(" FIRST CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH EQUAL TO 1!")
                    row_name = ''.join([str(elem) for elem in row_name])
                    col_name=''.join([str(elem) for elem in col_name])

                    cross_df = pd.crosstab(index=[df[row_name]], columns=[df[col_name]], rownames=[row_name], colnames=[col_name]).fillna(0)

                ## BOTH ROWS AND COLUMNS HAVE LENGTH GREATER THAN 1
                elif len(row_name) != 1 and len(col_name) != 1:

                    print(" SECOND CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH GREATER THAN 1!")
                    cross_df=pd.crosstab(index=row_list_vals,columns=col_list_vals, rownames=row_name, colnames=col_name).fillna(0)

                ## IF ROW = 1 AND COLUMNS GREATER THAN 1
                elif len(row_name) == 1 and len(col_name) != 1:

                    print("THIRD CONDTION SATISFIED :- IF ROW = 1 AND COLUMNS GREATER THAN 1!")
                    row_name = ''.join([str(elem) for elem in row_name])

                    cross_df = pd.crosstab(index=[df[row_name]], columns=col_list_vals, rownames=[row_name], colnames=col_name).fillna(0)
                ## IF ROWS GREATER THAN 1 AND COLUMN = 1
                elif len(row_name) != 1 and len(col_name) == 1:

                    print("FOURTH CONDTION SATISFIED :- IF ROWS GREATER THAN 1 AND COLUMN = 1!")
                    col_name=''.join([str(elem) for elem in col_name])

                    cross_df = pd.crosstab(index=row_list_vals, columns=[df[col_name]], rownames=row_name, colnames=[col_name]).fillna(0)

                # cross_df.to_excel('cross_df.xlsx')

            #################### Crosstab Logic ########################################################

            ############## Percentage of Total - Columns,rows and actual Logic ##############################################################

            if percent_calc=='grand_total_count':
                if len(row_name) == 1 and len(col_name) == 1:

                    print(" FIRST CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH EQUAL TO 1!")
                    row_name_str = ''.join([str(elem) for elem in row_name])
                    col_name_str = ''.join([str(elem) for elem in col_name])

                    cross_df = pd.crosstab(index=[df[row_name_str]], columns=[df[col_name_str]], rownames=[row_name_str],
                                           colnames=[col_name_str],
                                           normalize=True, margins=True,
                                           margins_name='Female_Total').fillna(0).round(4) * 100

                    ## BOTH ROWS AND COLUMNS HAVE LENGTH GREATER THAN 1
                elif len(row_name) != 1 and len(col_name) != 1:

                    print(" SECOND CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH GREATER THAN 1!")
                    cross_df = pd.crosstab(index=row_list_vals, columns=col_list_vals, rownames=row_name, colnames=col_name,
                                           normalize=True, margins=True,
                                           margins_name='Female_Total').fillna(0).round(4) * 100

                    ## IF ROW = 1 AND COLUMNS GREATER THAN 1
                elif len(row_name) == 1 and len(col_name) != 1:
                    print("THIRD CONDTION SATISFIED :- IF ROW = 1 AND COLUMNS GREATER THAN 1!")
                    row_name_str = ''.join([str(elem) for elem in row_name])

                    cross_df = pd.crosstab(index=[df[row_name_str]], columns=col_list_vals, rownames=[row_name_str],
                                           colnames=col_name,
                                           normalize=True, margins=True,
                                           margins_name='Female_Total').fillna(0).round(4) * 100
                    ## IF ROWS GREATER THAN 1 AND COLUMN = 1
                elif len(row_name) != 1 and len(col_name) == 1:
                    print("FOURTH CONDTION SATISFIED :- IF ROWS GREATER THAN 1 AND COLUMN = 1!")
                    col_name_str = ''.join([str(elem) for elem in col_name])

                    cross_df = pd.crosstab(index=row_list_vals, columns=[df[col_name_str]], rownames=row_name,
                                           colnames=[col_name_str],
                                           normalize=True, margins=True,
                                           margins_name='Female_Total').fillna(0).round(4) * 100

                # cross_df.to_excel("grand_total_percent_crosstab.xlsx")
                cross_df.to_excel("static/download_cross_table_excel/cross_df.xlsx")

            if percent_calc=='actual_count':
                total_row_list=[]
                for loop_col in cross_df.columns:
                    total_row = cross_df[loop_col].sum()
                    total_row_list.append(total_row)
                # print('total_row_list',total_row_list)

                # index_len=len(df.index)
                # cross_df.loc[index_len] = total_row_list
                # cross_df = cross_df.rename(index={index_len: 'Female_Total'})

                cross_df.loc['Female_Total', :] = total_row_list
                # cross_df.to_excel('cross_df_actual_count.xlsx')
                cross_df.to_excel('static/download_cross_table_excel/cross_df.xlsx')

            elif percent_calc=='column_percent':
                total_row_list=[]
                for loop_col in cross_df.columns:
                    cross_df[loop_col] = (cross_df[loop_col] / cross_df[loop_col].sum()) * 100

                    total_row = cross_df[loop_col].sum()
                    total_row_list.append(total_row)
                # print('total_row_list',total_row_list)

                cross_df.loc['Female_Total', :] = total_row_list

                # cross_df.to_excel('cross_df_col_percent.xlsx')
                cross_df.to_excel('static/download_cross_table_excel/cross_df.xlsx')

            elif percent_calc == 'row_percent':
                print("row_percent===")
                cross_df=cross_df.T
                for loop_col in cross_df.columns:
                    cross_df[loop_col] = (cross_df[loop_col] / cross_df[loop_col].sum()) * 100

                cross_df = cross_df.T

                cross_df['Female_Total'] = cross_df.sum(axis=1)
                # cross_df.to_excel('cross_df_row_percent.xlsx')
                cross_df.to_excel('static/download_cross_table_excel/cross_df.xlsx')
            ############## Percentage of Total - Columns,rows and actual Logic ##############################################################

        elif weight_param=='weighted':

            if percent_calc != 'grand_total_count':
                if len(row_name) == 1 and len(col_name) == 1:

                    print(" FIRST CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH EQUAL TO 1!")
                    row_name = ''.join([str(elem) for elem in row_name])
                    col_name=''.join([str(elem) for elem in col_name])

                    cross_df = pd.crosstab(index=[df[row_name]], columns=[df[col_name]], rownames=[row_name],
                                           colnames=[col_name],values=df[selected_weight_column],aggfunc=sum).fillna(0)

                ## BOTH ROWS AND COLUMNS HAVE LENGTH GREATER THAN 1
                elif len(row_name) != 1 and len(col_name) != 1:

                    print(" SECOND CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH GREATER THAN 1!")
                    cross_df=pd.crosstab(index=row_list_vals,columns=col_list_vals, rownames=row_name, colnames=col_name,
                                         values=df[selected_weight_column],aggfunc=sum).fillna(0)

                ## IF ROW = 1 AND COLUMNS GREATER THAN 1
                elif len(row_name) == 1 and len(col_name) != 1:

                    print("THIRD CONDTION SATISFIED :- IF ROW = 1 AND COLUMNS GREATER THAN 1!")
                    row_name = ''.join([str(elem) for elem in row_name])

                    cross_df = pd.crosstab(index=[df[row_name]], columns=col_list_vals, rownames=[row_name],
                                           colnames=col_name,values=df[selected_weight_column],aggfunc=sum).fillna(0)
                ## IF ROWS GREATER THAN 1 AND COLUMN = 1
                elif len(row_name) != 1 and len(col_name) == 1:

                    print("FOURTH CONDTION SATISFIED :- IF ROWS GREATER THAN 1 AND COLUMN = 1!")
                    col_name=''.join([str(elem) for elem in col_name])

                    cross_df = pd.crosstab(index=row_list_vals, columns=[df[col_name]], rownames=row_name,
                                           colnames=[col_name],values=df[selected_weight_column],aggfunc=sum).fillna(0)

                # cross_df.to_excel('cross_df_weighted.xlsx')

            if percent_calc=='grand_total_count':
                if len(row_name) == 1 and len(col_name) == 1:

                    print(" FIRST CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH EQUAL TO 1!")
                    row_name_str = ''.join([str(elem) for elem in row_name])
                    col_name_str = ''.join([str(elem) for elem in col_name])

                    cross_df = pd.crosstab(index=[df[row_name_str]], columns=[df[col_name_str]], rownames=[row_name_str],
                                           colnames=[col_name_str],values=df[selected_weight_column],aggfunc=sum,
                                           normalize=True, margins=True,
                                           margins_name='Female_Total').fillna(0).round(4) * 100

                    ## BOTH ROWS AND COLUMNS HAVE LENGTH GREATER THAN 1
                elif len(row_name) != 1 and len(col_name) != 1:

                    print(" SECOND CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH GREATER THAN 1!")
                    cross_df = pd.crosstab(index=row_list_vals, columns=col_list_vals, rownames=row_name, colnames=col_name,
                                           values = df[selected_weight_column], aggfunc = sum,
                                           normalize=True, margins=True,
                                           margins_name='Female_Total').fillna(0).round(4) * 100

                    ## IF ROW = 1 AND COLUMNS GREATER THAN 1
                elif len(row_name) == 1 and len(col_name) != 1:
                    print("THIRD CONDTION SATISFIED :- IF ROW = 1 AND COLUMNS GREATER THAN 1!")
                    row_name_str = ''.join([str(elem) for elem in row_name])

                    cross_df = pd.crosstab(index=[df[row_name_str]], columns=col_list_vals, rownames=[row_name_str],
                                           colnames=col_name,values=df[selected_weight_column],aggfunc=sum,
                                           normalize=True, margins=True,
                                           margins_name='Female_Total').fillna(0).round(4) * 100
                    ## IF ROWS GREATER THAN 1 AND COLUMN = 1
                elif len(row_name) != 1 and len(col_name) == 1:
                    print("FOURTH CONDTION SATISFIED :- IF ROWS GREATER THAN 1 AND COLUMN = 1!")
                    col_name_str = ''.join([str(elem) for elem in col_name])

                    cross_df = pd.crosstab(index=row_list_vals, columns=[df[col_name_str]], rownames=row_name,
                                           colnames=[col_name_str],values=df[selected_weight_column],aggfunc=sum,
                                           normalize=True, margins=True,
                                           margins_name='Female_Total').fillna(0).round(4) * 100

                # cross_df.to_excel('cross_df_weighted_grand_total.xlsx')
                cross_df.to_excel('static/download_cross_table_excel/cross_df.xlsx')

            if percent_calc=='actual_count':
                total_row_list=[]
                for loop_col in cross_df.columns:
                    total_row = cross_df[loop_col].sum()
                    total_row_list.append(total_row)
                # print('total_row_list',total_row_list)

                # index_len=len(df.index)
                # cross_df.loc[index_len] = total_row_list
                # cross_df = cross_df.rename(index={index_len: 'Female_Total'})

                cross_df.loc['Female_Total', :] = total_row_list
                # cross_df.to_excel('cross_df_actual_count_weighted.xlsx')
                cross_df.to_excel('static/download_cross_table_excel/cross_df.xlsx')

            elif percent_calc=='column_percent':
                total_row_list=[]
                for loop_col in cross_df.columns:
                    cross_df[loop_col] = (cross_df[loop_col] / cross_df[loop_col].sum()) * 100

                    total_row = cross_df[loop_col].sum()
                    total_row_list.append(total_row)
                print('total_row_list',total_row_list)

                cross_df.loc['Female_Total', :] = total_row_list

                # cross_df.to_excel('cross_df_col_percent_weighted.xlsx')
                cross_df.to_excel('static/download_cross_table_excel/cross_df.xlsx')

            elif percent_calc == 'row_percent':
                print("row_percent===")
                cross_df=cross_df.T
                for loop_col in cross_df.columns:
                    cross_df[loop_col] = (cross_df[loop_col] / cross_df[loop_col].sum()) * 100

                cross_df = cross_df.T

                cross_df['Female_Total'] = cross_df.sum(axis=1)
                # cross_df.to_excel('cross_df_row_percent_weighted.xlsx')
                cross_df.to_excel('static/download_cross_table_excel/cross_df.xlsx')


                
        ############ crosstab new logic 4 types - 29-07-2022 #######################

        df_cross_json1 = cross_df.to_json(orient='split') #records - pranit
        df_cross_json = json.loads(df_cross_json1)
        df_cross_json111 = df_cross_json['index']
        # print('===============================',df_cross_json111)

        #################### Crosstab Logic ########################################################

        ##################### logic for table logic responses ########################################################
        # print("row_name row_name ",row_name)
        # print("row_name row_name typeee==",type(row_name))
        # row_name1=row_name.copy()
        # col_name1=col_name.copy()

        # row_name1.append("All")
        # col_name1.append("All")

        # row_length=len(row_name1)
        # column_length=len(col_name1)

        # rowcount_dict,columncount_dict=value_count_freq(df,filename,row_name,col_name)

        ##################### logic for table logic responses ########################################################

        time_end = time.time()
        print("Time of execution - ", time_end - time_start)

        responseValue = {
                "status": 200,
                "row_length": 'row_length',
                "column_length": 'column_length',
                "rowcount_dict":'rowcount_dict',
                "columncount_dict":'columncount_dict',
                "df_cross_json": df_cross_json,
                "error": "Correct Data",

            }
    else:
        responseValue = {
            "status": 404,
            "error": "Incorrect Data",
        }


    return JsonResponse(responseValue, safe=False)

def base_filter_old(request):
    if request.method == "POST":

        filename = "BLS141_Test_Brand.json"
        selected_column = 'Age_Group'

        df = pd.read_json(settings.PYTHONPATH + filename, orient='records', lines=True)

        filter_df = df['video_definition'].value_counts()
        filter_df_dict = filter_df.to_dict()
        # print("response", data_dict)
        responseValue = {
            "status": 405,
            "error": "Incorrect Data",
            "postdata": request.POST,
            # "request data" : youtube_video_df,
        }
        return JsonResponse(responseValue, safe=True)


################################## DATE - 28-06-2023 #################################
def significance_fn_resp(request):
    if request.method == "POST":
        ############ GET parameters ####################################
        rowfilter = request.POST.get('rowfilter_val')
        columnfilter = request.POST.get('columnfilter_val')
        base_column = request.POST.get('base_column')
        print('base_column===',base_column)

        rowfilter = rowfilter.replace('[', '')
        rowfilter = rowfilter.replace(']', '')
        rowfilter = rowfilter.replace('"', '')
        columnfilter = columnfilter.replace('[', '')
        columnfilter = columnfilter.replace(']', '')
        columnfilter = columnfilter.replace('"', '')

        row_name = list(rowfilter.split(","))
        col_name = list(columnfilter.split(","))

        percent_calc = request.POST.get('calculation_type_name')
        seperated_flag_row = int(request.POST.get('seperated_flag_row_2'))
        seperated_flag_col = int(request.POST.get('seperated_flag_col_2'))
        ############ GET parameters ####################################

        cross_df = pd.read_json(settings.FINAL_CROSSTAB_OUTPUT + 'crosstab_data' + ".json", orient='split')

        cross_df = cross_df.mul(100)

        cross_df_actual_vals = pd.read_json(settings.FINAL_CROSSTAB_OUTPUT + 'cross_df_actual_vals_significance.json',orient='split')

        cross_df_sig = pd.read_json(settings.FINAL_CROSSTAB_OUTPUT + 'cross_df_sig_significance.json',orient='split')

        print('cross_df_actual_vals columns',cross_df_actual_vals.columns)
        print('cross_df_actual_vals index',cross_df_actual_vals.index)
        print('cross_df_sig columns',cross_df_sig.columns)
        print('cross_df_sig index',cross_df_sig.index)

        cross_df = pd.concat([cross_df], keys=row_name, axis=0)
        cross_df = pd.concat([cross_df], keys=col_name, axis=1)

        cross_df_sig = pd.concat([cross_df_sig], keys=row_name, axis=0)
        cross_df_sig = pd.concat([cross_df_sig], keys=col_name, axis=1)

        cross_df_actual_vals = pd.concat([cross_df_actual_vals], keys=row_name, axis=0)
        cross_df_actual_vals = pd.concat([cross_df_actual_vals], keys=col_name, axis=1)

        significance_df = significance_fn(cross_df_sig, cross_df_actual_vals,base_column)
        significance_df = significance_df.replace([np.nan, np.inf, -np.inf], 0)

        level_0_names_cols_fnn = significance_df.columns.get_level_values(0).unique().tolist()
        level_0_names_cols_fnn = ' '.join(level_0_names_cols_fnn)
        # level_0_names_cols_fnn = level_0_names_cols_fnn.extend('Totals')

        # Add a new column "Totals" with the value 777
        new_column = pd.DataFrame(index=significance_df.index,
                                  columns=pd.MultiIndex.from_tuples([(level_0_names_cols_fnn,base_column)]), data=777)
        significance_df = pd.concat([significance_df,new_column], axis=1)

        ############ Re-arranging the columns of Significance dataframe as per order of Crosstab dataframe #############################        
        level_1_names_cross_df = cross_df.columns.get_level_values(1).unique().tolist()

        # significance_df = significance_df.loc[:,
        #                   significance_df.columns.get_level_values(1).isin(list(level_1_names_cross_df))]

        significance_df = significance_df.reindex(columns=level_1_names_cross_df, level=1)
        ############ Re-arranging the columns of Significance dataframe as per order of Crosstab dataframe #############################

        # significance_df = allign_headers_condn(significance_df, percent_calc,seperated_flag_row,seperated_flag_col,row_name,col_name)

        significance_df.to_excel('SIGNIFICANCE_FN_significance_df_final.xlsx')

        ################ creating response #######################################
        df_cross_json1 = cross_df.to_json(orient='split')
        df_cross_json = json.loads(df_cross_json1)

        significance_df_json1 = significance_df.to_json(orient='split')
        significance_df_json = json.loads(significance_df_json1)

        responseValue = {
                "status": 200,
                "df_cross_json": df_cross_json,
                "significance_df_json": significance_df_json,
                "error": "Correct Data",
                # "merge_filename": filename_merged,

            }
    else:
        responseValue = {
            "status": 404,
            "error": "Incorrect Data",
        }


    return JsonResponse(responseValue, safe=False)



############# ADDED BY MIHIE PAWAR ON 14-04-2023 ####################################
def bar_chart(request):
    # PYTHONPATH = r"C:\Users\MihirPawar\Desktop\Python Project BSW\Python Files1\ccv_tool\output_crosstab\\"
    # IMG_OUTPUT_PYTHONPATH = r"C:\Users\MihirPawar\Desktop\Python Project BSW\Python Files1\ccv_tool\output_crosstab\charts\\"

    ####################################################################################################
    filter_timeperiod = [request.POST.get('Timeperiod_chart')] 
    filter_fact =request.POST.get('Facts_chart')
    facts_groups_filter =request.POST.get('Other_chart')  
    dict_selected_measures_lst =json.loads(request.POST.get('dict_selected_measures_lst')) 
    # print(dict_selected_measures_lst111)
    # print(type(dict_selected_measures_lst111))
    # exit('exit') 
    dict_selected_measures_lst111 = {'Volume': ['Volume', 'Volume YA', 'Volume PP', 'Volume Share', 'Volume Share YA',
                                         'Volume Share PP', 'Volume Growth vs YA', 'Volume Growth vs PP',
                                         'Volume Share bps Chg. vs YA', 'Volume Share bps Chg. vs PP']}
    ####################################################################################################
    facts_groups_dict = {
        'Absolutes': [
            'Volume', 'Volume YA', 'Volume PP',
            'Value (JPY)', 'Value YA (JPY)', 'Value PP (JPY)',
            'TDP TY', 'TDP YA', 'TDP PP',
            'WD', 'WD YA', 'WD PP',
            'ND', 'ND YA', 'ND PP',
            'API', 'API YA', 'API PP',
            'Avg Price', 'Avg Price YA', 'Avg Price PP'
        ],
        'Share': [
            'Volume Share', 'Volume Share YA', 'Volume Share PP',
            'Value Share', 'Value Share YA', 'Value Share PP',
            'TDP Share', 'TDP Share YA', 'TDP Share PP'
        ],
        'Growth': [
            'Volume Growth vs YA', 'Volume Growth vs PP',
            'Avg Price Growth vs YA', 'Avg Price Growth vs PP',
            'Value Growth vs YA', 'Value Growth vs PP',
            'TDP Growth vs YA', 'TDP Growth vs PP'
        ],
        'bps change': [
            'Volume Share bps Chg. vs YA', 'Volume Share bps Chg. vs PP',
            'Value Share bps Chg. vs YA', 'Value Share bps Chg. vs PP',
            'TDP Share bps Chg. vs YA', 'TDP Share bps Chg. vs PP',
            'WD bps Chg. vs YA', 'WD bps Chg. vs PP',
            'ND bps Chg. vs YA', 'ND bps Chg. vs PP',
            'API Chg. Vs YA', 'API Chg. Vs PP'
        ]
    }
    ####################################################################################################
    vals_filter_fact_lst = []
    if filter_fact in dict_selected_measures_lst.keys():
        vals_filter_fact = dict_selected_measures_lst[filter_fact]

        vals_filter_fact_lst.append(vals_filter_fact)

    vals_filter_fact_lst = [item for sublist in vals_filter_fact_lst for item in sublist]

    facts_groups_filter_values = facts_groups_dict[facts_groups_filter]

    common_values_facts_lst = list(set(vals_filter_fact_lst).intersection(facts_groups_filter_values))
    print('===common_values_facts_lst===',common_values_facts_lst)

    ####################################################################################################
    # cross_df = pd.read_excel(settings.FINAL_CROSSTAB_OUTPUT + "FINAL_CROSSTAB_CHART.xlsx")
    cross_df_graph = pd.read_json(settings.FINAL_CROSSTAB_OUTPUT + "crosstab_data.json",orient='split')
    # cross_df_graph.to_excel(settings.FINAL_CROSSTAB_OUTPUT + "crosstab_dataHHH.xlsx")
    print("cross_df_graph index 883",cross_df_graph.index)
    print("cross_df_graph cols",cross_df_graph.columns)

    selected_columns_time = [col for col in cross_df_graph.columns if any(sub in col for sub in filter_timeperiod)]
    print('selected_columns_time==',selected_columns_time)
    # Select and keep only the desired columns in the DataFrame
    cross_df_graph = cross_df_graph[selected_columns_time]

    cross_df_graph.columns = cross_df_graph.columns.str.replace(r'\|.*$', '', regex=True)

    print('COLSS',cross_df_graph.columns)
    cross_df_graph = cross_df_graph[common_values_facts_lst]
    # cross_df_graph.to_excel(settings.FINAL_CROSSTAB_OUTPUT + 'FILTERED_DATAFRRAME.xlsx')
    ####################################################################################################
      # Find the minimum and maximum values in the entire DataFrame
    min_value = cross_df_graph.values.min()
    max_value = cross_df_graph.values.max()

    # Create a dictionary to store the min and max values
    min_max_dict = {
        'min_value': math.floor(min_value),
        'max_value': math.ceil(max_value)
    }
    # cross_df_df1=cross_df.copy()
    # cross_df_df1.index = cross_df_df1.iloc[:,0]
    # cross_df.index = cross_df.iloc[:,0]
    # exit("end!")
    ########################### VISUALIZATIONS ############################################################
    # barplot = cross_df.plot.bar(rot=35)
    # img = cross_df_df1.plot(kind="bar", stacked=False, rot=90)
    # plt.show()
    # plt.savefig(settings.IMG_OUTPUT_PYTHONPATH + 'crosstab.png',bbox_inches='tight')  
    # save the figure to file
    if len(cross_df_graph) == 0:
        responseValue = {
            "status": 400,
            "error": "Incorrect Data",       
        }
    else:
        df_cross_json1 = cross_df_graph.to_json(orient='split') # records - pranit
        df_cross_json = json.loads(df_cross_json1)
        responseValue = {
                "status": 200,
                "error": "correct Data",
                "res_data": df_cross_json,        
                "min_max_dict": min_max_dict,        
                }
    
    return JsonResponse(responseValue, safe=True)


############# ADDED BY MIHIE PAWAR ON 14-04-2023 ####################################

