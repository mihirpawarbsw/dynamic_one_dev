
import json
import os
import time
import re

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
from main_dashboard.crosstab_calculation_seperated_functions import *
from main_dashboard.response_functions import *
from main_dashboard.crosstab_calculation_functions import *
from django.contrib.sessions.models import Session
from django.db import connection
from main_dashboard.crosstab_table_resp import *

import warnings
warnings.filterwarnings('ignore')

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

def test_page(request):
    return render(request,'test_working.html',{'title':'test_working'})


def main_dashboard_lazyload1(request):
    return render(request,'main_dashboard_lazyload1.html',{'title':'main_dashboard_lazyload1'})


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
        data_column_names =df.columns.values.tolist()
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
        round_off_val = int(request.POST.get('decimal_point_filter'))
        totals_nested_flag = int(request.POST.get('Total_column_filter'))

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

        dict_table = {}
        for loop_dict in final_row_col_array_grp_json:
            dict_table.update(loop_dict)
            print("loop_dict== loop_dict",loop_dict)

        print('dict_table====',dict_table)
        
        
        # ================================================================================================ #
        # ================================================================================================ #
        # ===============================Main logic start here============================= #
        ######## Added By Mihir Pawar on 25-10-2022 ###############################################
        if len(list(dict_table.keys())) > 1:
            if data_type_resp == 'merged':
                print("MERGE FUNCTION STARTED!")
                df = merge_data(dict_table)
                print("MERGE FUNCTION ENDS!")

            # elif data_type_resp == 'concat':
            #     print("CONCAT FUNCTION STARTED!")
            #     df = concat_data(dict_table)
            #     print("CONCAT FUNCTION ENDS!")

        else:
            filename = list(dict_table.keys())[0] + ".json"
            df = pd.read_json(settings.PYTHONPATH + filename, orient='records', lines=True)
            print('line 151 else condition')

        # print("df shape dimensionss",df.shape)
        ############################ CROSSTAB MAIN FUNCTION - CREATED BY MIHIR PAWAR 21-12-2022 ########################
        # if (data_type_resp == 'concat') and (('Country' in row_name) or ('Country' in col_name)):
        # print("CONCAT FUNCTION STARTED!")

        # if Measure == 'Volume':
        #     df_default_cols = df.columns
        #     df_edited = df_default_cols + ['Volume']
        #     print("df_edited===VOLUME",df_edited)
        #     df = df[df_edited]

        # if Measure == 'weighting':
        #     df_default_cols = df.columns
        #     df_edited = df_default_cols + ['weighting']
        #     print("df_edited===weighting",df_edited)
        #     df = df[df_edited]
        # df = vol_weight_check(df)

        if (data_type_resp == 'concat'):
            crosstab_list = []

            loop_vals_lst = []
            for loop_vals in dict_table.values():
                loop_vals_lst.extend(loop_vals)

            # loop_vals_lst = loop_vals_lst + ['LinkID','weighting']            #old code
            loop_vals_lst = loop_vals_lst + ['LinkID', 'weighting']  # new code modified on 05-12-2022

            loop_vals_lst = list(set(loop_vals_lst))

            if ('Country' in row_name) or ('Country' in col_name) or (('Country' in row_name) and ('Country' in col_name)):
                for data_concat_loop in dict_table.keys():

                    print("dict_table.keys===", data_concat_loop)

                    table_name = data_concat_loop + ".json"
                    print("table_name", table_name)

                    df_table = pd.read_json(settings.PYTHONPATH + table_name, orient='records', lines=True)

                    country_name = df_table['Country'].unique().tolist()
                    country_name_str = ''.join(country_name)
                    print("country_name",country_name)

                    df = df_table[loop_vals_lst]

                    cross_df = crosstab_main(df, dict_table, Measure, weight_param, row_name, col_name, data_type_resp,
                              percent_calc, seperated_flag_row, seperated_flag_col, totals_nested_flag)

                    cross_df.to_excel("CROSSX_" + country_name_str + ".xlsx")

                ##########################################################################################################################
                    if (('Country' in row_name) and ('Country' in col_name)):
                        print("CONDITION 1- ('Country' in row_name) and ('Country' in col_name)")

                        cross_df = pd.concat([cross_df], keys=[country_name_str], axis=0)
                        cross_df = pd.concat([cross_df], keys=[country_name_str], axis=1)

                    elif (('Country' in row_name) and ('Country' not in col_name)):
                        print("CONDITION 2- ('Country' in row_name) and ('Country' not in col_name)")
                        if percent_calc == 'row_percent':

                            cross_df = pd.concat([cross_df], keys=[country_name_str], axis=0)

                    elif (('Country' not in row_name) and ('Country' in col_name)):
                        print("CONDITION 3- ('Country' not in row_name) and ('Country' in col_name)")
                        if percent_calc == 'column_percent' or percent_calc == 'actual_count':
                            cross_df = pd.concat([cross_df], keys=[country_name_str], axis=1)

                ##########################################################################################################################
                    crosstab_list.append(cross_df)

                if (('Country' in row_name) and ('Country' in col_name)):

                    cross_df = pd.concat(crosstab_list, axis=0)
                    cross_df = pd.concat(crosstab_list, axis=1)


                elif (('Country' in row_name) and ('Country'  not in col_name)):

                    cross_df = pd.concat(crosstab_list)

                elif (('Country' not in row_name) and ('Country' in col_name)):

                    cross_df = pd.concat(crosstab_list,axis=1)

            else:
                df = concat_data(dict_table)
                cross_df = crosstab_main(df, dict_table, Measure, weight_param, row_name, col_name, data_type_resp,
                                         percent_calc, seperated_flag_row, seperated_flag_col, totals_nested_flag)

            # try:
            #     cross_df = cross_df.reindex(sorted(cross_df.columns), axis=1)
            #     cross_df = cross_df.reindex(sorted(cross_df.index), axis=0)
            # except:
            #     pass

        else:
            cross_df = crosstab_main(df, dict_table, Measure, weight_param, row_name, col_name, data_type_resp,
                                     percent_calc, seperated_flag_row, seperated_flag_col, totals_nested_flag)


        cross_df.fillna(0,inplace=True)

        if percent_calc == 'actual_count':
            cross_df = cross_df.drop('Total')
            # cross_df.to_excel("CROSSX.xlsx")

        ############################ CROSSTAB MAIN FUNCTION - CREATED BY MIHIR PAWAR 21-12-2022 ########################

        ########################## REMOVING DUPLICATE COLUMNS #######################################################
        # if data_type_resp != 'concat':
        #     cross_df = cross_df[~cross_df.index.duplicated(keep='last')]
        #
        #     cross_df = cross_df.loc[:, ~cross_df.columns.duplicated(keep='last')].copy()
        #
        ########################## REMOVING DUPLICATE COLUMNS #######################################################

        ########## added by mihir pawar - rounding dataframe to user-defined limit ############################
        cross_df = round(cross_df,round_off_val)
        cross_df.to_excel('cross_dfxxcc.xlsx')
        ########## added by mihir pawar - rounding dataframe to user-defined limit ############################

        ################## Working on removing the prefix from crostab ###################################

        cross_df.rename(columns=lambda x: re.sub('.*}','', x), inplace=True)
        cross_df.rename(index=lambda x: re.sub('.*}','', x), inplace=True)

        cross_df.rename(columns=lambda x: re.sub('_',' ', x), inplace=True)
        cross_df.rename(index=lambda x: re.sub('_',' ', x), inplace=True)

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

        legends_dict = {'Parameters':['Row Filter','Column Filter','Calculation Type','Weight Parameter','Measure'],
                        'Values':[row_nameStr,col_nameStr,percent_calc,weight_param,Measure]}

        legends_df = pd.DataFrame(legends_dict)
        legends_df.set_index('Parameters',inplace=True)
        print("========")
        print(legends_df)
        print("========")

        # cross_df = cross_df.replace(to_replace=0,value=np.nan)

        cross_df_highlighter = cross_df.copy()

        dfs = [cross_df_highlighter,legends_df]
        # dfs = [legends_df,cross_df_highlighter]
        startrow = 0
        with pd.ExcelWriter(settings.FINAL_CROSSTAB_OUTPUT+'cross_df.xlsx') as writer:
            counter = 0
            for df in dfs:
                # if counter == 0:
                    # df.style.apply(highlight_max, props='color:white;background-color:darkblue;', axis=0)\
                    #     .apply(highlight_min, props='color:black;background-color:pink;', axis=0).to_excel(writer, engine="openpyxl", startrow=startrow)
                    # df.style.background_gradient(cmap='PuBu').to_excel(writer, engine="openpyxl", startrow=startrow) #original working

                #     df.style.background_gradient(cmap='PuBu').to_excel(writer, engine="openpyxl", startrow=startrow) #original working
                #
                # else:
                #     df.to_excel(writer, engine="openpyxl", startrow=startrow)
                #
                # counter = counter + 1

                df.to_excel(writer, engine="openpyxl", startrow=startrow)
                startrow += (df.shape[0] + 7)

        ########################### VISUALIZATIONS ############################################################
        # barplot = cross_df.plot.bar(rot=35)
        # pl = cross_df.plot(kind="bar", stacked=True, rot=90)
        # plt.show()
        #
        # plt.savefig(output_pythonpath + 'crosstab.jpg')  # save the figure to file

        # import plotly.express as px
        #
        # fig = px.bar(cross_df.unstack())
        # fig.show()


        ########################### VISUALIZATIONS ############################################################
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

        responseValue = {
                "status": 200,
                "row_length": 'row_length',
                "column_length": 'column_length',
                "rowcount_dict":'rowcount_dict',
                "columncount_dict":'columncount_dict',
                "df_cross_json": df_cross_json,
                # "df_cross_json_test": df_cross_json21,
                "error": "Correct Data",
                # "merge_filename": filename_merged,
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
       
        final_row_col_array_grp = request.POST.get('final_row_col_array_grp')
        final_row_col_array_grp_json = json.loads(final_row_col_array_grp)
        # df = pd.DataFrame(final_row_col_array_grp_json)
        data_type_resp = request.POST.get('table_data_type_respone')
        data_type_resp = data_type_resp.replace('"', '')
        print('data_type_resp 152',data_type_resp)
        Measure = request.POST.get('weight_volume_type_name')
        seperated_flag_row = int(request.POST.get('seperated_flag_row_2'))
        seperated_flag_col = int(request.POST.get('seperated_flag_col_2'))
        round_off_val = int(request.POST.get('decimal_point_filter'))
        totals_nested_flag = int(request.POST.get('Total_column_filter'))
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

        dict_table = {}
        for loop_dict in final_row_col_array_grp_json:
            dict_table.update(loop_dict)
            print("loop_dict== loop_dict",loop_dict)

        print('dict_table====',dict_table)
        
        
        # ================================================================================================ #
        # ================================================================================================ #
        # ===============================Main logic start here============================= #
        ######## Added By Mihir Pawar on 25-10-2022 ###############################################

        if data_type_resp == 'merged':
            filename_merged = list(dict_table.keys())
            filename_merged = '_'.join([str(elem) for i, elem in enumerate(filename_merged)]) + ".json"
            print("filename_merged", filename_merged)
            df = pd.read_json(settings.MERGED_PYTHONPATH + filename_merged, orient='records', lines=True)
        else:
            filename = list(dict_table.keys())[0] + ".json"
            df = pd.read_json(settings.PYTHONPATH + filename, orient='records', lines=True)
            print('line 151 else condition')

        # if len(list(dict_table.keys())) > 1:
        #     if data_type_resp == 'merged':
        #         print("MERGE FUNCTION STARTED!")
        #         df = merge_data(dict_table)
        #         print("MERGE FUNCTION ENDS!")

        #     # elif data_type_resp == 'concat':
        #     #     print("CONCAT FUNCTION STARTED!")
        #     #     df = concat_data(dict_table)
        #     #     print("CONCAT FUNCTION ENDS!")

        # else:
        #     filename = list(dict_table.keys())[0] + ".json"
        #     df = pd.read_json(settings.PYTHONPATH + filename, orient='records', lines=True)
        #     print('line 151 else condition')

        # print("df shape dimensionss",df.shape)
        ############################ CROSSTAB MAIN FUNCTION - CREATED BY MIHIR PAWAR 21-12-2022 ########################
        
        # if (data_type_resp == 'concat') and (('Country' in row_name) or ('Country' in col_name)):
        # print("CONCAT FUNCTION STARTED!")
        # crosstab_list = []

        # loop_vals_lst = []
        # for loop_vals in dict_table.values():
        #     loop_vals_lst.extend(loop_vals)

        # # loop_vals_lst = loop_vals_lst + ['LinkID','weighting']            #old code
        # loop_vals_lst = loop_vals_lst + ['LinkID', 'weighting']  # new code modified on 05-12-2022

        # loop_vals_lst = list(set(loop_vals_lst))

        if (data_type_resp == 'concat'):
            crosstab_list = []

            loop_vals_lst = []
            for loop_vals in dict_table.values():
                loop_vals_lst.extend(loop_vals)

            # loop_vals_lst = loop_vals_lst + ['LinkID','weighting']            #old code
            loop_vals_lst = loop_vals_lst + ['LinkID', 'weighting']  # new code modified on 05-12-2022

            loop_vals_lst = list(set(loop_vals_lst))

            if ('Country' in row_name) or ('Country' in col_name) or (('Country' in row_name) and ('Country' in col_name)):
                for data_concat_loop in dict_table.keys():

                    print("dict_table.keys===", data_concat_loop)

                    table_name = data_concat_loop + ".json"
                    print("table_name", table_name)

                    df_table = pd.read_json(settings.PYTHONPATH + table_name, orient='records', lines=True)

                    country_name = df_table['Country'].unique().tolist()
                    country_name_str = ''.join(country_name)
                    print("country_name",country_name)

                    df = df_table[loop_vals_lst]

                    cross_df = crosstab_main(df, dict_table, Measure, weight_param, row_name, col_name, data_type_resp,
                              percent_calc, seperated_flag_row, seperated_flag_col, totals_nested_flag)

                    

                    cross_df.to_excel("CROSSX_" + country_name_str + ".xlsx")

                ##########################################################################################################################
                    if (('Country' in row_name) and ('Country' in col_name)):
                        print("CONDITION 1- ('Country' in row_name) and ('Country' in col_name)")

                        cross_df = pd.concat([cross_df], keys=[country_name_str], axis=0)
                        cross_df = pd.concat([cross_df], keys=[country_name_str], axis=1)

                    elif (('Country' in row_name) and ('Country' not in col_name)):
                        print("CONDITION 2- ('Country' in row_name) and ('Country' not in col_name)")
                        if percent_calc == 'row_percent':

                            cross_df = pd.concat([cross_df], keys=[country_name_str], axis=0)

                    elif (('Country' not in row_name) and ('Country' in col_name)):
                        print("CONDITION 3- ('Country' not in row_name) and ('Country' in col_name)")
                        if percent_calc == 'column_percent' or percent_calc == 'actual_count':
                            cross_df = pd.concat([cross_df], keys=[country_name_str], axis=1)

                ##########################################################################################################################
                    crosstab_list.append(cross_df)

                if (('Country' in row_name) and ('Country' in col_name)):

                    cross_df = pd.concat(crosstab_list, axis=0)
                    cross_df = pd.concat(crosstab_list, axis=1)


                elif (('Country' in row_name) and ('Country'  not in col_name)):

                    cross_df = pd.concat(crosstab_list)

                elif (('Country' not in row_name) and ('Country' in col_name)):

                    cross_df = pd.concat(crosstab_list,axis=1)

            else:
                df = concat_data(dict_table)
                cross_df = crosstab_main(df, dict_table, Measure, weight_param, row_name, col_name, data_type_resp,
                                         percent_calc, seperated_flag_row, seperated_flag_col, totals_nested_flag)

            # try:
            #     cross_df = cross_df.reindex(sorted(cross_df.columns), axis=1)
            #     cross_df = cross_df.reindex(sorted(cross_df.index), axis=0)
            # except:
            #     pass

        else:
            cross_df = crosstab_main(df, dict_table, Measure, weight_param, row_name, col_name, data_type_resp,
                                     percent_calc, seperated_flag_row, seperated_flag_col, totals_nested_flag)


        cross_df.fillna(0,inplace=True)

        if percent_calc == 'actual_count':
            cross_df = cross_df.drop('Total')
            # cross_df.to_excel("CROSSX.xlsx")

        ############################ CROSSTAB MAIN FUNCTION - CREATED BY MIHIR PAWAR 21-12-2022 ########################

        ########################## REMOVING DUPLICATE COLUMNS #######################################################
        # if data_type_resp != 'concat':
        #     cross_df = cross_df[~cross_df.index.duplicated(keep='last')]
        #
        #     cross_df = cross_df.loc[:, ~cross_df.columns.duplicated(keep='last')].copy()
        #
        ########################## REMOVING DUPLICATE COLUMNS #######################################################

        ########## added by mihir pawar - rounding dataframe to user-defined limit ############################
        cross_df = round(cross_df,round_off_val)
        # cross_df.to_excel('cross_dfxxcc.xlsx')
        ########## added by mihir pawar - rounding dataframe to user-defined limit ############################

        ################## Working on removing the prefix from crostab ###################################

        cross_df.rename(columns=lambda x: re.sub('.*}','', x), inplace=True)
        cross_df.rename(index=lambda x: re.sub('.*}','', x), inplace=True)

        cross_df.rename(columns=lambda x: re.sub('_',' ', x), inplace=True)
        cross_df.rename(index=lambda x: re.sub('_',' ', x), inplace=True)

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

        legends_dict = {'Parameters':['Row Filter','Column Filter','Calculation Type','Weight Parameter','Measure'],
                        'Values':[row_nameStr,col_nameStr,percent_calc,weight_param,Measure]}

        legends_df = pd.DataFrame(legends_dict)
        legends_df.set_index('Parameters',inplace=True)
        print("========")
        print(legends_df)
        print("========")

        # cross_df = cross_df.replace(to_replace=0,value=np.nan)

        cross_df_highlighter = cross_df.copy()

        dfs = [cross_df_highlighter,legends_df]
        # dfs = [legends_df,cross_df_highlighter]
        startrow = 0
        with pd.ExcelWriter(settings.FINAL_CROSSTAB_OUTPUT+'cross_df.xlsx') as writer:
            counter = 0
            for df in dfs:
                # if counter == 0:
                    # df.style.apply(highlight_max, props='color:white;background-color:darkblue;', axis=0)\
                    #     .apply(highlight_min, props='color:black;background-color:pink;', axis=0).to_excel(writer, engine="openpyxl", startrow=startrow)
                    # df.style.background_gradient(cmap='PuBu').to_excel(writer, engine="openpyxl", startrow=startrow) #original working

                #     df.style.background_gradient(cmap='PuBu').to_excel(writer, engine="openpyxl", startrow=startrow) #original working
                #
                # else:
                #     df.to_excel(writer, engine="openpyxl", startrow=startrow)
                #
                # counter = counter + 1

                df.to_excel(writer, engine="openpyxl", startrow=startrow)
                startrow += (df.shape[0] + 7)

        ########################### VISUALIZATIONS ############################################################
        # barplot = cross_df.plot.bar(rot=35)
        # pl = cross_df.plot(kind="bar", stacked=True, rot=90)
        # plt.show()
        #
        # plt.savefig(output_pythonpath + 'crosstab.jpg')  # save the figure to file

        # import plotly.express as px
        #
        # fig = px.bar(cross_df.unstack())
        # fig.show()


        ########################### VISUALIZATIONS ############################################################
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

        responseValue = {
                "status": 200,
                "row_length": 'row_length',
                "column_length": 'column_length',
                "rowcount_dict":'rowcount_dict',
                "columncount_dict":'columncount_dict',
                "df_cross_json": df_cross_json,
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

def base_filter(request):
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
