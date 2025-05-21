
import json
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

from django.contrib.auth.decorators import login_required

############################################################################################
############################################################################################
# testing function start here

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
        return render(request,'dashboard.html',{'title':'dashboard'})
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

        df.to_json(settings.PYTHONPATH + str(filename) +"_"+str(data_type_file)+".json", orient='records', lines=True)
        df.to_excel(settings.PYTHONPATH + str(filename) +"_"+str(data_type_file)+".xlsx",index=False)
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
        df = pd.read_json(settings.PYTHONPATH + filename+'.json', orient='records', lines=True)
        df.to_excel('display_all_data_df.xlsx')
        ################### added by mihir pawar on 03-08-2023 ########
        # Select numerical columns
        # colname_num = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        colname_num = ['Volume','Value','TDP','WD','ND','Avg Price','API']

        # Select categorical columns
        colname_obj = df.select_dtypes(include=['object']).columns.tolist()

        col_num = [col + "_NUM" for col in colname_num]
        col_obj = [col + "_STR" for col in colname_obj]

        common_list = col_obj + col_num
        print('-===common_list==',common_list)

        ################### added by mihir pawar on 03-08-2023 ########
        
        data_column_names = common_list
        # data_column_names = df.columns.tolist() #old code
        dict_col={'filename':data_column_names}

        responseValue = {
            "status": 200,
            "data_column_names":dict_col,
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
        for file_name in [file for file in os.listdir(settings.PYTHONPATH) if file.endswith('.json')]:
            file_name=file_name.replace('.json','')
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
        selected_weight_column_all = list(wt_measures_str.split(","))
        print('294====selected_weight_column_all',selected_weight_column_all)

        data_type_resp = 'sales'

        time_period_filter_val = ['MAT']
        measure_under_time_flag = 0
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

        dict_table[','.join([str(key) for key in dict_table.keys()])].extend(selected_weight_column_all)

        print('==dict_table after 342',dict_table)


        ################### GROUPINGS ON MEASURES - 28-08-2023 ################################
        dict_table,selected_weight_column_all,val_dict_final,dict_selected_measures_lst = add_groupings_measures(dict_table,measure_selected_key_val_resp,crosstab_function_name)
        print('====dict_table===',dict_table)
        print('====selected_weight_column_all===',selected_weight_column_all)
        print('====val_dict_final===',val_dict_final)
        # exit('======344')
        ################### GROUPINGS ON MEASURES - 28-08-2023 ################################


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
        df = pl.read_excel(settings.PYTHONPATH + filename)
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
        
        df = df[df['Time'].isin(time_period_filter_val)]
        ################ ADDED BY MIHIR PAWAR - 04-08-2023 - TIME FILTER ##################


        ############## ADDED BY MIHIR PAWAR - 30-08-2023 - DERIVED COUMNS ###
        time_derived_start = time.time()

        df = derived_measures_weights_cols(df)

        replace_values = {-np.inf: 0, np.inf: 0, 'null': 0, np.nan: 0}
        df.replace(replace_values, inplace=True)

        df.to_excel('df_SALES_FINAL.xlsx')
        print('====val_dict_final====249',val_dict_final)
        df = df[val_dict_final]
        time_derived_end = time.time()
        print("DERIVED FN TIME",time_derived_end - time_derived_start,"SECONDS!")
        ############## ADDED BY MIHIR PAWAR - 30-08-2023 - DERIVED COUMNS ###
        ######## Added By Mihir Pawar on 11-04-2023 ###############################################

        ###########################################################################################################
        # loop_vals_lst = loop_vals_lst + ['LinkID'] + base_filter_col_lst + [selected_weight_column_all]  # new code modified on 14-04-2023
        # loop_vals_lst = loop_vals_lst + ['LinkID'] + selected_weight_column_all  # new code modified on 14-04-2023

        # loop_vals_lst = list(set(loop_vals_lst))
        # loop_vals_lst = sorted(loop_vals_lst)

        # df = df[loop_vals_lst]

        df.to_excel('df_concat.xlsx')

        filter_dict_resp = base_filter_resp(df,dict_table,row_name,col_name,selected_weight_column_all) ################
        all_categories_vals = base_filter_resp_all(df,dict_table,row_name,col_name) ###########################

        ############### added by mihir pawar on 03-08-2023 #########
        # for keys_time in selected_weight_column_all:
        # df = df[df[].isin(values_temp)]
        ############### added by mihir pawar on 03-08-2023 #########

        # df.to_excel('df_final_cols.xlsx')

        
        crosstab_lst_final = []

        for selected_weight_column in selected_weight_column_all:
            cross_df_temp = crosstab_main_logics(dict_table, df, percent_calc, row_name, col_name,
                                 selected_weight_column,
                                 data_type_resp,
                                 seperated_flag_row, seperated_flag_col, totals_nested_flag)

            # cross_df_temp = cross_df_temp.droplevel(0, axis=1)

            lst_nd_wd_cols = ['WD', 'WD YA', 'WD PP', 'WD Bps Chg. vs YA', 'WD Bps Chg. vs PP',
                              'ND', 'ND YA', 'ND PP', 'ND Bps Chg. vs YA', 'ND Bps Chg. vs PP']
            print('===selected_weight_column 28699', selected_weight_column)

            if len(row_name) == 1:

                if selected_weight_column in lst_nd_wd_cols:
                    df_level1 = cross_df_temp.groupby(level=0).max()
                    df_level1.index = df_level1.index = pd.MultiIndex.from_arrays([df_level1.index.values,
                                                                                   len(df_level1.index) * ['AAAATotal']])
                else:
                    df_level1 = cross_df_temp.groupby(level=0).sum()
                    df_level1.index = df_level1.index = pd.MultiIndex.from_arrays([df_level1.index.values,
                                                                                   len(df_level1.index) * ['AAAATotal']])

            # Concatenate the totals row to the original DataFrame
            cross_df_temp = pd.concat([cross_df_temp, df_level1])

            elif len(row_name) > 1:
                # lst_nd_wd_cols = ['WD', 'WD YA', 'WD PP', 'ND', 'ND YA', 'ND PP']
                lst_nd_wd_cols = ['WD','WD YA','WD PP','WD Bps Chg. vs YA','WD Bps Chg. vs PP',
                      'ND','ND YA','ND PP','ND Bps Chg. vs YA','ND Bps Chg. vs PP']

                print('===selected_weight_column 28699', selected_weight_column)
                if selected_weight_column in lst_nd_wd_cols:
                    print('===selected_weight_column 286', "nd_wd")
                    agg_func = 'nd_wd'
                    cross_df_temp = subtotals_multi_actuals_new(cross_df_temp, row_name, agg_func)
                else:
                    print('===selected_weight_column 286', "others")
                    agg_func = 'others'
                    cross_df_temp = subtotals_multi_actuals_new(cross_df_temp, row_name, agg_func)


            cross_df_temp = pd.concat([cross_df_temp], keys=[selected_weight_column], axis=1)
            cross_df_temp.to_excel('cross_df_temp_donee.xlsx')

            crosstab_lst_final.append(cross_df_temp)

        cross_df = pd.concat(crosstab_lst_final,axis=1)
        cross_df = cross_df.droplevel(1, axis=1)
        cross_df.to_excel('cross_df_BEFORE_SWAPPING'+str(crosstab_function_name)+'.xlsx')

        if measure_under_time_flag == 1:

            cross_df = cross_df.swaplevel(0, 1, axis=1).sort_index(axis=1)
            # cross_df = cross_df.reindex(columns=selected_weight_column_all, level=0)
        else:
            pass
            # cross_df = cross_df.reindex(columns=cross_df.columns.levels[1][selected_weight_column_all], level=0)

        ############## CODE TO DROP 'TOTAL' FROM ALL LEVELS
        try:
            for level in cross_df.columns.levels:
                if 'Grand Total' in level:
                    cross_df = cross_df.drop('Grand Total', axis=1, level=level.name)
                else:
                    pass
        except:
            pass

        # try:
        #     for level in cross_df.index.levels:
        #         if 'Grand Total' in level:
        #             cross_df = cross_df.drop('Grand Total', axis=0, level=level.name)
        #         else:
        #             pass
        # except:
        #     pass

        ################################################################################################################
        if (seperated_flag_row == 0 and seperated_flag_col == 0):
        # if (len(row_name) == 1 and len(col_name) == 1):

            cross_df = cross_df.reindex(sorted(cross_df.index), axis=0)
            cross_df = cross_df.reindex(sorted(cross_df.columns), axis=1)
        ################################################################################################################

        cross_df.fillna(0,inplace=True)

         ########### ADDED BY MIHIR PAWAR - 02-05-2023 INDICES ON COLUMN PERCENT #####
        if percent_calc == 'column_percent' and indices_calc_flag == 1:
            cross_df = Indices_selected_base_column(cross_df,base_column)
            percent_calc = 'indices'

            cross_df.to_excel('cross_df_indices_cross_df.xlsx')

            level_1_names_cross_df = cross_df.columns.get_level_values(1).unique().tolist()

            base_column_names_indices_resp = {'base_column_names_indices_resp':level_1_names_cross_df}

        else:
            base_column_names_indices_resp = 0
            base_column_names_sig_resp = 0

        ########### ADDED BY MIHIR PAWAR - 02-05-2023 INDICES ON COLUMN PERCENT ########

        ############################ CROSSTAB MAIN FUNCTION - CREATED BY MIHIR PAWAR 21-12-2022 ########################

        ############## ADDED BY MIHIR PAWAR ON 30-06-2023- ALLIGN HEADERS ################
        # cross_df.to_excel("cross_df_allign_headers.xlsx")

        # cross_df = allign_headers_condn(cross_df, percent_calc,seperated_flag_row,seperated_flag_col,row_name,col_name)
        ############# ADDED BY MIHIR PAWAR ON 30-06-2023- ALLIGN HEADERS  ##############

            ################## ADDED BY MIHIR PAWAR ON 11-07-2023 ##################################
    ###################### SIGNIFICANCE LOGIC BEGINS ###########################################################
        if percent_calc == 'column_percent' and significance_flag == 1:

            print('SIGNIFICANCE FUNCTION TO SAVE FILE BEGINS...')

            cross_df_sig = cross_df.copy()

            ############## SIGNIFICANCE TEST - MANUAL CALCULATIONS - 12-06-2023 ##################################
            cross_df_actual_vals = crosstab_main_logics(dict_table, df, percent_calc, row_name, col_name,
                                 selected_weight_column,
                                 data_type_resp,
                                 seperated_flag_row, seperated_flag_col, totals_nested_flag)

            unique_groups_level1 = cross_df_actual_vals.columns.get_level_values(1).unique().tolist()
            unique_groups_level1_resp = {'unique_groups_level1': unique_groups_level1}

            cross_df_actual_vals.to_excel('cross_df_actual_vals.xlsx')

            significance_df = significance_fn(cross_df_sig, cross_df_actual_vals, base_column)
            significance_df = significance_df.replace([np.nan, np.inf, -np.inf], 0)

            level_0_names_cols_fnn = significance_df.columns.get_level_values(0).unique().tolist()
            level_0_names_cols_fnn = ' '.join(level_0_names_cols_fnn)
            # level_0_names_cols_fnn = level_0_names_cols_fnn.extend('Totals')

            # Add a new column "Totals" with the value 777
            new_column = pd.DataFrame(index=significance_df.index,
                                      columns=pd.MultiIndex.from_tuples([(level_0_names_cols_fnn, base_column)]),
                                      data=777)
            significance_df = pd.concat([significance_df, new_column], axis=1)

            level_1_names_cross_df = cross_df.columns.get_level_values(1).unique().tolist()
            significance_df = significance_df.reindex(columns=level_1_names_cross_df, level=1)
            significance_df.to_excel('FINAL_SIGNIFICANCE_DF.xlsx')

            significance_df_json1 = significance_df.to_json(orient='split')
            significance_df_json = json.loads(significance_df_json1)

            percent_calc = 'Significance'

            base_column_names_sig_resp = {'base_column_names_sig_resp':level_1_names_cross_df}

            print('452==unique_groups_level1_resp',unique_groups_level1_resp)

        else:

            unique_groups_level1_resp = 'unique_groups_level1_resp'
            base_column_names_indices_resp = 'base_column_names_indices_resp'
            base_column_names_sig_resp = 'base_column_names_sig_resp'
            significance_df_json = 'significance_df_json'

            print('455==unique_groups_level1_resp',unique_groups_level1_resp)
    ###################### SIGNIFICANCE LOGIC ENDS ###########################################################
    ################## ADDED BY MIHIR PAWAR ON 11-07-2023 ##################################

        ########## added by mihir pawar - rounding dataframe to user-defined limit ############################
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
            cross_df_graph = cross_df_graph.droplevel(0, axis=0)
            cross_df_graph = cross_df_graph.droplevel(0, axis=1)

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
            cross_df_graph.to_excel(settings.FINAL_CROSSTAB_OUTPUT+ 'FINAL_CROSSTAB_CHART.xlsx')
            cross_df_graph.to_csv(settings.FINAL_CROSSTAB_OUTPUT+ 'FINAL_CROSSTAB_CHART.csv')
            cross_df_graph.to_json(settings.FINAL_CROSSTAB_OUTPUT + 'crosstab_data' + ".json", orient = 'split')


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
        crosstab_summary.to_excel('crosstab_summary.xlsx')
        ############# SUMMARY OF CROSSTAB DATA ##############################

        ############# ADDED BY MIHIR PAWAR - SAVING CROSSTAB EXCEL FILE - 22-05-2023 ###########
        saving_crosstab_excel_file(cross_df,legends_df,percent_calc)
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

        ################ ADDED BY MIHIR PAWAR ON 20-05-2023 #####################
        if percent_calc == 'column_percent' or percent_calc == 'row_percent' or percent_calc == 'table_percent':
            cross_df = cross_df.mul(100)
        ################ ADDED BY MIHIR PAWAR ON 20-05-2023 #####################

        df_cross_json1 = cross_df.to_json(orient='split')  # records - pranit
        df_cross_json = json.loads(df_cross_json1)
        # ===============================Main Logic end here================================ #
        # ================================================================================================ #
        # ================================================================================================ #
        # testing code
        # df_cross_json2 = cross_df.to_json(orient='columns') #records - pranit
        # df_cross_json21 = json.loads(df_cross_json2)

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
                # "df_cross_json_test": df_cross_json21,
                "error": "Correct Data",
                # "merge_filename": filename_merged,

            }
    else:
        responseValue = {
            "status": 404,
            "error": "Incorrect Data",
        }


    return JsonResponse(responseValue, safe=False)


#=============================================================================================
def crosstab_table_page2(request):
    print("Function 2- crosstab_table_page2 STARTED!")

    if request.method == "POST":
        time_start = time.time()
        rowfilter = request.POST.get('rowfilter_val')
        columnfilter = request.POST.get('columnfilter_val')
        percent_calc = request.POST.get('calculation_type_name')
        # weight_param = 'weighted'
        weight_param = request.POST.get('weight_type_name')
        base_column = request.POST.get('base_column')
       
        final_row_col_array_grp = request.POST.get('final_row_col_array_grp')
        print('final_row_col_array_grp typee==',type(final_row_col_array_grp))
        dict_base_filter_data_resp = request.POST.get('filter_data')
        print('dict_base_filter_data_resp typee==',dict_base_filter_data_resp)
        print('dict_base_filter_data_resp dataa==',dict_base_filter_data_resp)
        final_row_col_array_grp_json = json.loads(final_row_col_array_grp)
        dict_base_filter_data_resp_json = json.loads(dict_base_filter_data_resp)
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
        selected_weight_column_all = list(wt_measures_str.split(","))

        Time_val = request.POST.get('Time_val')
        Time_val = Time_val.replace('[', '')
        Time_val = Time_val.replace(']', '')
        Time_val = Time_val.replace('"', '')
        time_period_filter_val = list(Time_val.split(","))

        # time_period_filter_val = ['MAT','QTR']
        measure_under_time_flag = int(request.POST.get('measure_time_toggle'))
        print('measure_under_time_flag crosstab func 2',measure_under_time_flag)

        data_type_resp = 'sales'
        # measure_selected_key_val_resp = {'Volume':['Volume','Volume YA', 'Volume PP'],
        # 'API':['API','API YA','API PP']}
        measure_selected_key_val_resp11 = request.POST.get('facts_object')
        measure_selected_key_val_resp = json.loads(measure_selected_key_val_resp11)
        print('=====measure_selected_key_val_resp==',measure_selected_key_val_resp)

        selected_weight_column_all = list(measure_selected_key_val_resp.keys())
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

        dict_table = {}
        for loop_dict in final_row_col_array_grp_json:
            dict_table.update(loop_dict)
            print("loop_dict== loop_dict",loop_dict)

        print('dict_table====',dict_table)

        dict_table[','.join([str(key) for key in dict_table.keys()])].extend(selected_weight_column_all)

        print('==dict_table after 342',dict_table)


        ################### GROUPINGS ON MEASURES - 28-08-2023 ################################
        dict_table,selected_weight_column_all,val_dict_final,dict_selected_measures_lst = add_groupings_measures(dict_table,measure_selected_key_val_resp,crosstab_function_name)
        print('====dict_table===',dict_table)
        print('====selected_weight_column_all===',selected_weight_column_all)
        print('====val_dict_final===',val_dict_final)
        # exit('======344')
        ################### GROUPINGS ON MEASURES - 28-08-2023 ################################

        ################ ADDED BY MIHIR PAWAR ON 24-05-2023 ###############################

        dict_base_filter_data = {}
        for loop_dict in dict_base_filter_data_resp_json:
            print('loop_dict====2nd crosstab fn==',loop_dict)
            
            dict_base_filter_data.update(loop_dict)
            print("loop_dict== loop_dict",loop_dict)

        print('dict_base_filter_data====',dict_base_filter_data)
        ################ ADDED BY MIHIR PAWAR ON 24-05-2023 ###############################
        # dict_base_filter_data = {
            # 'Gender': ['Female'],
            # 'Country': ['China'],
            # 'SEC_Classification':['SEC A3',0],
            # 'Do_you_work_in_any_of_these_industries':['Food industry','Healthcare industry'],
            # 'Age_:_Post_code': ['21 – 30 years', '36 – 45 years']
        # }
        
        
        # ================================================================================================ #
        # ================================================================================================ #
        # ===============================Main logic start here============================= #
        ######## Added By Mihir Pawar on 25-10-2022 ###############################################

        # if data_type_resp == 'merged':
        #     filename_merged = list(dict_table.keys())
        #     filename_merged = '_'.join([str(elem) for i, elem in enumerate(filename_merged)]) + ".json"
        #     print("filename_merged", filename_merged)
        #     df = pd.read_json(settings.MERGED_PYTHONPATH + filename_merged, orient='records', lines=True)
        # else:
        #     filename = list(dict_table.keys())[0] + ".json"
        #     df = pd.read_json(settings.PYTHONPATH + filename, orient='records', lines=True)
        #     print('line 151 else condition')

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
        ###################### ADDED ON 11-04-2023 #################################################

        ######## Added By Mihir Pawar 24-04-2023 - READ FILE LOGIC FOR CROSSTAB FUNCTION 2 ONLY ###############################################

        
        ##################################### POLARS #####################################
        start_time_read = time.time()
        # filename = list(dict_table.keys())[0] + ".json"
        # filename = list(dict_table.keys())[0] + ".csv"
        filename = list(dict_table.keys())[0] + ".xlsx"
        # df = pl.read_csv(settings.PYTHONPATH + filename)
        df = pl.read_excel(settings.PYTHONPATH + filename)
        print('line 151 else condition')
        end_time_read = time.time()
        print("Time taken to read file using POLARS was ", end_time_read - start_time_read, "seconds!")

        df = df.to_pandas()
        df = df.rename(columns=rename_input_cols_dict)
    ##################################### POLARS #########################################

        ################ ADDED BY MIHIR PAWAR - 04-08-2023 - TIME FILTER #################
        time_period_vals = df['Time'].unique().tolist() #distinct/unique of time periods
        df = df[df['Time'].isin(time_period_filter_val)]
        ################ ADDED BY MIHIR PAWAR - 04-08-2023 - TIME FILTER #################


        ######## Added By Mihir Pawar 24-04-2023 - READ FILE LOGIC FOR CROSSTAB FUNCTION 2 ONLY ###############################################

         ############## ADDED BY MIHIR PAWAR - 30-08-2023 - DERIVED COUMNS ###
        time_derived_start = time.time()

        df = derived_measures_weights_cols(df)

        replace_values = {-np.inf: 0, np.inf: 0, 'null': 0, np.nan: 0}
        df.replace(replace_values, inplace=True)

        df.to_excel('df_SALES_FINAL.xlsx')
        print('====val_dict_final====249',val_dict_final)
        df = df[val_dict_final]
        time_derived_end = time.time()
        print("DERIVED FN TIME",time_derived_end - time_derived_start,"SECONDS!")
        ############## ADDED BY MIHIR PAWAR - 30-08-2023 - DERIVED COUMNS ###

        #########################################################################################################


        # if (data_type_resp == 'respondent') or (data_type_resp == 'response'):
        #     loop_vals_lst = loop_vals_lst + ['LinkID'] + base_filter_col_lst + selected_weight_column_all  # new code modified on 14-04-2023
        #     # loop_vals_lst = loop_vals_lst + ['LinkID'] + [selected_weight_column_all]  # new code modified on 14-04-2023

        #     loop_vals_lst = list(set(loop_vals_lst))
        #     loop_vals_lst = sorted(loop_vals_lst)

        #     df = df[loop_vals_lst]

        df.to_excel('df_concat.xlsx')

        filter_dict_resp = base_filter_resp(df,dict_table,row_name,col_name,selected_weight_column_all) ###########################
        all_categories_vals = base_filter_resp_all(df,dict_table,row_name,col_name)

        df = base_filter_data(df,dict_base_filter_data) ###########################

        ############# added by mihir pawar on 03-08-2023 ############

        ############# added by mihir pawar on 03-08-2023 ############

        df.to_excel('df_final_cols.xlsx')

        
        crosstab_lst_final = []

        for selected_weight_column in selected_weight_column_all:
            cross_df_temp = crosstab_main_logics(dict_table, df, percent_calc, row_name, col_name,
                                 selected_weight_column,
                                 data_type_resp,
                                 seperated_flag_row, seperated_flag_col, totals_nested_flag)

            # cross_df_temp = cross_df_temp.droplevel(0, axis=1)


            lst_nd_wd_cols = ['WD', 'WD YA', 'WD PP', 'WD Bps Chg. vs YA', 'WD Bps Chg. vs PP',
                              'ND', 'ND YA', 'ND PP', 'ND Bps Chg. vs YA', 'ND Bps Chg. vs PP']
            print('===selected_weight_column 28699', selected_weight_column)

            if len(row_name) == 1:

                if selected_weight_column in lst_nd_wd_cols:
                    df_level1 = cross_df_temp.groupby(level=0).max()
                    df_level1.index = df_level1.index = pd.MultiIndex.from_arrays([df_level1.index.values,
                                                                                   len(df_level1.index) * ['AAAATotal']])
                else:
                    df_level1 = cross_df_temp.groupby(level=0).sum()
                    df_level1.index = df_level1.index = pd.MultiIndex.from_arrays([df_level1.index.values,
                                                                                   len(df_level1.index) * ['AAAATotal']])

            # Concatenate the totals row to the original DataFrame
            cross_df_temp = pd.concat([cross_df_temp, df_level1])


            elif len(row_name) > 1:
                # lst_nd_wd_cols = ['WD', 'WD YA', 'WD PP', 'ND', 'ND YA', 'ND PP']
                lst_nd_wd_cols = ['WD','WD YA','WD PP','WD Bps Chg. vs YA','WD Bps Chg. vs PP',
                      'ND','ND YA','ND PP','ND Bps Chg. vs YA','ND Bps Chg. vs PP']

                print('===selected_weight_column 28699', selected_weight_column)
                if selected_weight_column in lst_nd_wd_cols:
                    print('===selected_weight_column 286', "nd_wd")
                    agg_func = 'nd_wd'
                    cross_df_temp = subtotals_multi_actuals_new(cross_df_temp, row_name, agg_func)
                else:
                    print('===selected_weight_column 286', "others")
                    agg_func = 'others'
                    cross_df_temp = subtotals_multi_actuals_new(cross_df_temp, row_name, agg_func)


            cross_df_temp = pd.concat([cross_df_temp], keys=[selected_weight_column], axis=1)
            cross_df_temp.to_excel('cross_df_temp_donee.xlsx')

            crosstab_lst_final.append(cross_df_temp)

        cross_df = pd.concat(crosstab_lst_final,axis=1)
        cross_df = cross_df.droplevel(1, axis=1)
        cross_df.to_excel('cross_df_BEFORE_SWAPPING'+str(crosstab_function_name)+'.xlsx')

        print('selected_weight_column_all===1004',selected_weight_column_all)
        
        if measure_under_time_flag == 1:

            cross_df = cross_df.swaplevel(0, 1, axis=1).sort_index(axis=1)
            print('measure_under_time_flag condn 1009==',measure_under_time_flag)
            cross_df.to_excel('cross_df_AFTER_SWAPPING.xlsx')
            cross_df = cross_df.reindex(columns=selected_weight_column_all, level=1)
            # cross_df = cross_df.reindex(columns=cross_df.columns.levels[1][selected_weight_column_all], level=1)
        else:
            pass
            # cross_df = cross_df.reindex(columns=cross_df.columns.levels[1][selected_weight_column_all], level=0)
            # cross_df = cross_df.reindex(columns=cross_df.columns.levels[1][selected_weight_column_all], level=0)

        ############## CODE TO DROP 'TOTAL' FROM ALL LEVELS
        try:
            for level in cross_df.columns.levels:
                if 'Grand Total' in level:
                    cross_df = cross_df.drop('Grand Total', axis=1, level=level.name)
                else:
                    pass
        except:
            pass

        try:
            for level in cross_df.index.levels:
                if 'Grand Total' in level:
                    cross_df = cross_df.drop('Grand Total', axis=0, level=level.name)
                else:
                    pass
        except:
            pass


        cross_df.to_excel('cross_df_AFTER_SWAPPING11.xlsx')

        # ################################################################################################################
        # if (seperated_flag_row == 0 and seperated_flag_col == 0):

        #     cross_df = cross_df.reindex(sorted(cross_df.index), axis=0)
        #     cross_df = cross_df.reindex(sorted(cross_df.columns), axis=1)
        # ################################################################################################################

        cross_df.fillna(0,inplace=True)

        ########### ADDED BY MIHIR PAWAR - 02-05-2023 INDICES ON COLUMN PERCENT #####
        if percent_calc == 'column_percent' and indices_calc_flag == 1:
            cross_df = Indices_selected_base_column(cross_df,base_column)
            percent_calc = 'Indices'

            cross_df.to_excel('cross_df_indices_cross_df.xlsx')

            level_1_names_cross_df = cross_df.columns.get_level_values(1).unique().tolist()

            # Find the index of 'Total' in the list
            index_of_total = level_1_names_cross_df.index('Total')
            # Remove 'Total' from its current position
            level_1_names_cross_df.pop(index_of_total)
            # Insert 'Total' at the beginning of the list
            level_1_names_cross_df.insert(0, 'Total')          

            base_column_names_resp = {'type':'Indices','base_column_names_resp':level_1_names_cross_df}
            # base_column_names_resp = {'base_column_names_resp':level_1_names_cross_df}

        ########### ADDED BY MIHIR PAWAR - 02-05-2023 INDICES ON COLUMN PERCENT ########

        ############################ CROSSTAB MAIN FUNCTION - CREATED BY MIHIR PAWAR 21-12-2022 ########################

        ############## ADDED BY MIHIR PAWAR ON 30-06-2023- ALLIGN HEADERS ################
        # cross_df.to_excel("cross_df_allign_headers.xlsx")
        # if percent_calc !='actual_count':
        #     cross_df = allign_headers_condn(cross_df, percent_calc,seperated_flag_row,seperated_flag_col,row_name,col_name)
        ############# ADDED BY MIHIR PAWAR ON 30-06-2023- ALLIGN HEADERS  ##############

            ################## ADDED BY MIHIR PAWAR ON 11-07-2023 ##################################
    ###################### SIGNIFICANCE LOGIC BEGINS ###########################################################
        if percent_calc == 'column_percent' and significance_flag == 1:

            print('SIGNIFICANCE FUNCTION TO SAVE FILE BEGINS...')

            cross_df_sig = cross_df.copy()

            ############## SIGNIFICANCE TEST - MANUAL CALCULATIONS - 12-06-2023 ##################################
            cross_df_actual_vals = crosstab_main_logics(dict_table, df, percent_calc, row_name, col_name,
                                 selected_weight_column,
                                 data_type_resp,
                                 seperated_flag_row, seperated_flag_col, totals_nested_flag)

            unique_groups_level1 = cross_df_actual_vals.columns.get_level_values(1).unique().tolist()
            unique_groups_level1_resp = {'unique_groups_level1': unique_groups_level1}

            cross_df_actual_vals.to_excel('cross_df_actual_vals.xlsx')

            significance_df = significance_fn(cross_df_sig, cross_df_actual_vals, base_column)
            significance_df = significance_df.replace([np.nan, np.inf, -np.inf], 0)

            level_0_names_cols_fnn = significance_df.columns.get_level_values(0).unique().tolist()
            level_0_names_cols_fnn = ' '.join(level_0_names_cols_fnn)
            # level_0_names_cols_fnn = level_0_names_cols_fnn.extend('Totals')

            # Add a new column "Totals" with the value 777
            new_column = pd.DataFrame(index=significance_df.index,
                                      columns=pd.MultiIndex.from_tuples([(level_0_names_cols_fnn, base_column)]),
                                      data=777)
            significance_df = pd.concat([significance_df, new_column], axis=1)

            level_1_names_cross_df = cross_df.columns.get_level_values(1).unique().tolist()
            significance_df = significance_df.reindex(columns=level_1_names_cross_df, level=1)
            significance_df.to_excel('FINAL_SIGNIFICANCE_DF.xlsx')

            significance_df_json1 = significance_df.to_json(orient='split')
            significance_df_json = json.loads(significance_df_json1)

            percent_calc = 'Significance'

            base_column_names_resp = {'type':'Significance','base_column_names_resp':level_1_names_cross_df}
            # base_column_names_resp = [level_1_names_cross_df]


    #     elif percent_calc != 'Indices':
    #         print('879===else unique_groups_level1_resp')
    #         # base_column_names_indices_resp = 'base_column_names_indices_resp'
    #         base_column_names_sig_resp = 'base_column_names_sig_resp'
    #         significance_df_json = 'significance_df_json'
    # ###################### SIGNIFICANCE LOGIC ENDS ###########################################################
    ################## ADDED BY MIHIR PAWAR ON 11-07-2023 ##################################

        ########## added by mihir pawar - rounding dataframe to user-defined limit ############################
        # cross_df = round(cross_df,round_off_val)

        ######################## CROSSTAB LOGIC #####################################################

        ################## Working on removing the prefix from crostab ###################################

        cross_df.rename(columns=lambda x: re.sub('.*}','', x), inplace=True)
        cross_df.rename(index=lambda x: re.sub('.*}','', x), inplace=True)

        cross_df.rename(columns=lambda x: re.sub('_',' ', x), inplace=True)
        cross_df.rename(index=lambda x: re.sub('_',' ', x), inplace=True)

         #################### ADDED BY MIHIR PAWAR ON 14-04-2023 ##########################
      
        # if ((seperated_flag_col == 1) and (len(row_name) == 1)) or ((seperated_flag_row == 1) and (len(col_name) == 1)) or ((seperated_flag_col == 1) and (seperated_flag_row == 1)):
        if (len(row_name) == 1) and (len(col_name) == 1):
            print("GRAPH LOGIC BEGINS...")

            ################# ADDED BY MIHIR PAWAR ON 25-04-2023 #############
            # REMOVING MULTIINDEX HEADER FROM COLUMN AND ROW 
            cross_df_graph = cross_df.copy()
            cross_df_graph = cross_df_graph.droplevel(0, axis=0)
            cross_df_graph = cross_df_graph.droplevel(0, axis=1)

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
            # REMOVING MULTIINDEX HEADER FROM COLUMN AND ROW 

            ################ ADDED BY MIHIR PAWAR ON 25-04-2023 #############
            cross_df_graph.to_excel(settings.FINAL_CROSSTAB_OUTPUT+ 'FINAL_CROSSTAB_CHART.xlsx')
            cross_df_graph.to_csv(settings.FINAL_CROSSTAB_OUTPUT+ 'FINAL_CROSSTAB_CHART.csv')

            cross_df_graph.to_json(settings.FINAL_CROSSTAB_OUTPUT + 'crosstab_data' + ".json", orient='split')
        

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
        crosstab_summary.to_excel('crosstab_summary.xlsx')
        ############# SUMMARY OF CROSSTAB DATA ##############################
        ############# ADDED BY MIHIR PAWAR - SAVING CROSSTAB EXCEL FILE - 22-05-2023 ###########
        saving_crosstab_excel_file(cross_df,legends_df,percent_calc)
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
                # "base_column_names_indices_resp": base_column_names_indices_resp,
                "filter_dict_resp":filter_dict_resp,
                "all_categories_vals":all_categories_vals,
                "time_period_flag": time_period_flag,
                "time_period_vals": time_period_vals,
                # "df_cross_json_test": df_cross_json21,
                "error": "Correct Data",
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

    # cross_df = pd.read_excel(settings.FINAL_CROSSTAB_OUTPUT + "FINAL_CROSSTAB_CHART.xlsx")
    cross_df = pd.read_json(settings.FINAL_CROSSTAB_OUTPUT + "crosstab_data.json",orient='split')

    print("cross_df index 883",cross_df.index)
    print("cross_df cols",cross_df.columns)

    cross_df_df1=cross_df.copy()
    # cross_df_df1.index = cross_df_df1.iloc[:,0]
    # cross_df.index = cross_df.iloc[:,0]
    # exit("end!")
    ########################### VISUALIZATIONS ############################################################
    # barplot = cross_df.plot.bar(rot=35)
    # img = cross_df_df1.plot(kind="bar", stacked=False, rot=90)
    # plt.show()
    # plt.savefig(settings.IMG_OUTPUT_PYTHONPATH + 'crosstab.png',bbox_inches='tight')  
    # save the figure to file
    if len(cross_df) == 0:
        responseValue = {
            "status": 400,
            "error": "Incorrect Data",       
        }
    else:
        df_cross_json1 = cross_df.to_json(orient='split') # records - pranit
        df_cross_json = json.loads(df_cross_json1)
        responseValue = {
                "status": 200,
                "error": "correct Data",
                "res_data": df_cross_json        
                }
    
    return JsonResponse(responseValue, safe=True)


############# ADDED BY MIHIE PAWAR ON 14-04-2023 ####################################

