import chardet
import json
from itertools import chain
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
from main_dashboard.pivot_data_transformation_and_comparative_time_period_logics import *
from main_dashboard.bcst_sales_data_constants import *
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


def Add_to_favourite(request):
    user = request.user
    username = user.username
    user_id = user.id
    row_variable = request.POST.get('row_variable')
    column_variable = request.POST.get('column_variable')
    other_variable = request.POST.get('other_variable')
    add_to_favourite_name = request.POST.get('add_to_favourite_name')
    selected_DB_name = request.POST.get('selected_DB_name')
    selected_filename = request.POST.get('selected_filename')
    time_range = request.POST.get('time_range')
    comparative_time_period = request.POST.get('comparative_time_period')
    selected_time_period = request.POST.get('selected_time_period')
    currency = request.POST.get('currency')
    row_variable_html = request.POST.get('row_variable_html')
    column_variable_html = request.POST.get('column_variable_html')
    other_variable_html = request.POST.get('other_variable_html')
    stored_json_response_data = request.POST.get('stored_json_response_data')

    
    

    # Convert the JSON strings to Python objects
    filters_data_object = request.POST.get('filters_data')
    dict_base_filter_data_resp_json = json.loads(filters_data_object)
    filters_data_object_json = json.dumps(dict_base_filter_data_resp_json)

    get_facts_selected_values = request.POST.get('get_facts_selected_values')
    get_facts_selected_values_json = json.loads(get_facts_selected_values)
    get_facts_selected_dumps = json.dumps(get_facts_selected_values_json)

    datetime_save = datetime.now()

    # print('filters_data_object-->', dict_base_filter_data_resp_json)
    # print('filters_data_object-->', type(dict_base_filter_data_resp_json))
    # print('===================================================================')
    # print('get_facts_selected_values-->', get_facts_selected_values)
    # print('get_facts_selected_values-->', type(get_facts_selected_values))

    # Parameterized query to avoid SQL injection
    query = """
    INSERT INTO user_table_view_history (
        user_id, username, add_to_favourite_name, row_variable, column_variable, other_variable,
        filename, database_name, timestamp, filters_data,facts_selected_values,time_range,comparative_time_period,selected_time_period,currency,row_variable_html,column_variable_html,other_variable_html,json_data
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor = connection.cursor()
    cursor.execute(query, (
        user_id, username, add_to_favourite_name, row_variable, column_variable, other_variable,
        selected_filename, selected_DB_name, datetime_save, filters_data_object_json, get_facts_selected_dumps,time_range,comparative_time_period,selected_time_period,currency,row_variable_html,column_variable_html,other_variable_html,stored_json_response_data
    ))
    rowcount = cursor.rowcount
    cursor.close()

    # print('rowcount', rowcount)

    if rowcount > 0:
        response = {
            'code': 200,
            'message': 'Data Save Successfully',
        }
    else:
        response = {
            'code': 400,
            'message': 'No Data Inserted',
        }

    return JsonResponse(response, safe=False)



def display_user_history_view(request):

    history_id = request.POST.get('history_id')
    user = request.user
    username = user.username
    user_id = user.id
    

    query = "SELECT id, username, add_to_favourite_name, row_variable, column_variable, other_variable, filename, database_name, timestamp, time_range, comparative_time_period, selected_time_period, currency,json_data,row_variable_html,column_variable_html,other_variable_html,facts_selected_values,filters_data  FROM user_table_view_history where id='"+str(history_id)+"'"
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = dictfetchall(cursor)
        rowcount = cursor.rowcount

    if rowcount > 0:
        response = {
            'code': 200,
            'message': 'Data Save Successfully',
            'data': rows,
        }
    else:
        response = {
            'code': 400,
            'message': 'No Data Found',
        }

    return JsonResponse(response, safe=False)

def verify_user_history_exit(request):

    history_id = request.POST['history_id']
    userid = request.POST['userid']
    username = request.POST['username']
    

    query = "SELECT *  FROM user_table_view_history where id='"+str(history_id)+"' and user_id='"+str(userid)+"' and username='"+str(username)+"' order by id desc"
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = dictfetchall(cursor)
        rowcount = cursor.rowcount

    if rowcount > 0:
        response = {
            'code': 200,
            'message': 'data exit',
            'data': rows,
        }
    else:
        response = {
            'code': 400,
            'message': 'No Data Found',
        }

    return JsonResponse(response, safe=False)




def Show_Add_to_favourite_list(request):

    user = request.user
    username = user.username
    user_id = user.id
    
    query = "SELECT id, username,user_id, add_to_favourite_name, row_variable, column_variable, other_variable, filename, database_name, timestamp, time_range, comparative_time_period, selected_time_period, currency  FROM user_table_view_history where user_id='"+str(user_id)+"' order by id desc"

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = dictfetchall(cursor)
        rowcount = cursor.rowcount

    if rowcount > 0:
        response = {
            'code': 200,
            'message': 'Data Save Successfully',
            'data': rows,
        }
    else:
        response = {
            'code': 400,
            'message': 'No Data Found',
        }

    return JsonResponse(response, safe=False)




def Delete_recently_added_view(request):

        if (request.method == 'POST'):
            delete_id = request.POST['delete_id']
            user = request.user
            user_id = user.id
            print('user_id-->',user_id)
            print('user_id-->',type(user_id))
            if delete_id=='delete_all':
                query = "Delete from user_table_view_history where user_id ="+str(user_id)+" "
                print('if query',query)
                
            else:
                query = "Delete from user_table_view_history where id = "+delete_id+" "
                print('else query',query)
              
            cursor = connection.cursor()
            cursor.execute(query)
            rowcount = cursor.rowcount
            if (rowcount > 0):
                responseValue = {'code': '200', 'message': 'Your save data has been Deleted Successfully'}
            else:
                responseValue = {'code': '500', 'message': 'Something Went Wrong1'}
        else:
            responseValue = {'code': '500', 'message': 'Something Went Wrong2'}        
        return JsonResponse(responseValue, safe=False)

# new upload data start here
def upload_chunk(request):
    if request.method == 'POST':
        try:
            uploaded_file =request.FILES.get('up')
            extension = os.path.splitext(uploaded_file.name)[1]
            base_name = os.path.splitext(uploaded_file.name)[0]
            print('extension==>',extension)
            if not uploaded_file:
                raise ValueError("No file uploaded")

            # Example: Save the uploaded file to a specific folder
            # destination = open('C:/python project/BCST_Sales_Tool/uploaded_data/' + uploaded_file.name, 'wb')
            destination = open(settings.ORIGINAL_DATA + uploaded_file.name, 'wb')

            for chunk in uploaded_file.chunks():
                destination.write(chunk)

            destination.close()

            # Generate CSV file
            if(extension == '.xlsx'):
                
                df = pd.read_excel(settings.ORIGINAL_DATA + uploaded_file.name)
                df.to_csv(settings.TEMP_UPLOAD + base_name+'.csv', index=False)
            return JsonResponse(
                { 
                    'ok': 1,
                    'info': 'Upload OK',
                    'filename': str(uploaded_file.name),
                    # 'column_list': ['A','B','C'],
                    # 'column_list':columns,
                    # 'numerical_columns':numerical_columns
                    
                }
                )
        except Exception as e:
            return JsonResponse({'ok': 0, 'info': str(e)})

    return JsonResponse({'ok': 0, 'info': 'Invalid request method'})

    return JsonResponse({'ok': 0, 'info': 'Invalid request method'})


# new upload data start here
def upload_chunk_2(request):
    if request.method == 'POST':
        
        user = request.user
        username = user.username
        user_id = user.id
        uploaded_file =request.FILES.get('file_upload_input_name')
        data_type = request.POST.get('data_type')
        datetime_save = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        extension = os.path.splitext(uploaded_file.name)[1]
        base_name = os.path.splitext(uploaded_file.name)[0]
        print('extension==>',extension)
        print('extensionuploaded_file',uploaded_file.name)
        if not uploaded_file:
            raise ValueError("No file uploaded")

        # Example: Save the uploaded file to a specific folder
        # destination = open('C:/python project/BCST_Sales_Tool/uploaded_data/' + uploaded_file.name, 'wb')
        destination = open(settings.ORIGINAL_DATA + uploaded_file.name, 'wb')

        for chunk in uploaded_file.chunks():
            destination.write(chunk)

        destination.close()

        df = pd.read_excel(settings.ORIGINAL_DATA + uploaded_file.name)
        # print('df list',df['Market'].unique().tolist())


        # #####################################################
        # ############ start #################################
        # Define a period order for comparison
        period_order = {'Q1': 1, 'Q2': 2, 'Q3': 3, 'Q4': 4}
        # Add a numerical representation of the periods
        df['period_num'] = df['Period'].map(period_order)
        # Step 1: Find the maximum year for each country
        max_year_df = df.groupby('Market')['Year'].max().reset_index()
        # Merge this information back into the original DataFrame
        merged_df = pd.merge(df, max_year_df, on=['Market', 'Year'])
        # Step 2: Within the maximum year, find the maximum period for each country
        max_period_df = merged_df.loc[merged_df.groupby('Market')['period_num'].idxmax()]
        # Select the specific columns
        result_df = max_period_df[['Market', 'Period', 'Year']]
        # Convert to list of dictionaries
        list_of_dicts = result_df.to_dict(orient='records')
        for entry in list_of_dicts:
            entry['datetime_save'] = datetime_save
        print('list_of_dicts',list_of_dicts)
        # ############ end ########################
        # #####################################################

        # #########################################################
        # ########## SQL CODE START########################


        query = "INSERT INTO upload_data_master(user_id,user_name,filename,data_type,uploaded_country_list,timestamp) VALUES ('" + str(user_id) + "','" + str(username) + "','" + str(uploaded_file) + "','" + str(data_type) + "','" + str(json.dumps(list_of_dicts)) + "','" + datetime_save+ "')"
        cursor = connection.cursor()
        cursor.execute(query)
        rowcount = cursor.rowcount
        # Get the inserted ID
        inserted_id = cursor.lastrowid

        cursor.close()

        # ########## SQL CODE END #########################
        # #########################################################

        # Generate CSV file
        # if(extension == '.xlsx'):
        #     df = pd.read_excel(settings.ORIGINAL_DATA + uploaded_file.name)
        #     # df.to_csv(settings.TEMP_UPLOAD + base_name+'.csv', index=False)
        #     print('df list',df['Market'].unique().tolist())
        return JsonResponse({ 
                'code': 200,
                'info': 'Upload OK',
                'filename': str(uploaded_file.name),
                'inserted_id':inserted_id,
                # 'column_list': ['A','B','C'],
                # 'column_list':columns,
                # 'numerical_columns':numerical_columns
                
            })
    else:
        return JsonResponse({'code':404, 'info': 'Invalid request method'})


def Show_dataupload_list_table(request):

    user = request.user
    username = user.username
    user_id = user.id
    # last_id = request.POST.get('last_id')
    
    query = "SELECT id,user_id,user_name,filename,data_type,uploaded_country_list,timestamp  FROM upload_data_master where user_id='"+str(user_id)+"' order by id desc"

    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = dictfetchall(cursor)
        rowcount = cursor.rowcount

    if rowcount > 0:
        response = {
            'code': 200,
            'message': 'success',
            'data': rows,
        }
    else:
        response = {
            'code': 400,
            'message': 'No Data Found',
        }

    return JsonResponse(response, safe=False)


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

def bring_key_to_first(data, key):
    # Create a new dictionary with the specified key first
    new_data = {key: data[key]}
    
    # Add the remaining keys in their original order
    new_data.update({k: v for k, v in data.items() if k != key})
    
    return new_data


def crosstab_ui_v1(request):
    return render(request,'crosstab_v1.html',{'title':'crosstab_v1'})

def test_page(request):
    return render(request,'test_working.html',{'title':'test_working'})


# def dashboard(request):
#     return render(request,'dashboard.html',{'title':'dashboard'})


def display_all_data1(request):
    if request.method == "POST":
        # db_type = 'Sales'
        db_type = request.POST.get('type')
        print('db_type',db_type)

        list_all_files = []
        # for file_name in [file for file in os.listdir(settings.PYTHONPATH) if file.endswith('.json')]:
        # for file_name in [file for file in os.listdir(settings.PYTHONPATH) if file.endswith('.csv')]:
        for file_name in [file for file in os.listdir(settings.TEMP_UPLOAD) if file.endswith('.csv')]:
            # file_name=file_name.replace('.json','')
            file_name=file_name.replace('.csv','')
            list_all_files.append(file_name)

        list_filtered_files = [item for item in list_all_files if db_type in item]
        # Remove strings that contain '_Q1_'
        list_filtered_files = [s for s in list_filtered_files if '_Q1_' not in s]
        responseValue = {
            "status": 200,
            "list_all_files":list_filtered_files,
            "error": "Correct Data",
    }
    else:
        responseValue = {
            "status": 404,
            "error": "Incorrect Data",
        }

    return JsonResponse(responseValue, safe=False)
@login_required(login_url='/')
def dashboard(request):
    # return render(request,'main_dashboard_lazyload1.html',{'title':'main_dashboard_lazyload1'})
    if request.session.has_key('is_logged'):
        username1 = request.user.username
        print('############################',username1)
        return render(request,'dashboard.html',{'username':username1})
    return redirect(settings.LOGOUT_REDIRECT_URL)


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
    # return render(request,'main_dashboard.html',{'title':'main_dashboard'})
    if request.session.has_key('is_logged'):
        username1 = request.user.username
        print('############################',username1)
        return render(request,'main_dashboard.html',{'title':'main_dashboard'})
    return redirect(settings.LOGOUT_REDIRECT_URL)

def drag_and_drop(request):
    return render(request,'main_dashboard_drag_drop.html',{'title':'drag_and_drop'})

def crosstab_dash(request):
    if request.session.has_key('is_logged'):
        username1 = request.user.username
        print('############################',username1)
        return render(request,'crosstab.html',{'username':username1})
    return redirect(settings.LOGOUT_REDIRECT_URL)


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

def ensure_list(dictionary):
    # Iterate over dictionary items
    for key, value in dictionary.items():
        # Check if the value is not a list
        if not isinstance(value, list):
            # Convert the value into a list
            dictionary[key] = [value]
    return dictionary

def display_all_data(request):
    if request.method == "POST":

        filename = request.POST.get('filename')
        print('filename 614',filename)

        db_type = filename.split('_')[0]
        print('617 db_type',db_type)

        if db_type == 'Multichannel':
            final_dict = renaming_and_reordering(db_type)

        # df = pd.read_json(settings.PYTHONPATH + filename+'.json', orient='records', lines=True)
        # df = pl.read_excel(settings.TEMP_UPLOAD + filename+'.xlsx',sheet_name='Codeframe')
        # df = pd.read_csv(settings.TEMP_UPLOAD + filename+'.csv') #####
        # df = df.to_pandas()
        # df.to_excel('testing.xlsx')
        ##############################################################################
        # Open the file in binary mode and detect the encoding
        # with open(settings.TEMP_UPLOAD + filename+'.csv', 'rb') as f:
        #     result = chardet.detect(f.read(100000))  # Read the first 100000 bytes
        #     detected_encoding = result['encoding']

        # print(f"Detected encoding: {detected_encoding}")

        # Read the CSV file using the detected encoding
        df = pd.read_csv(settings.TEMP_UPLOAD + filename+'.csv',low_memory=False,engine='c')

        if db_type == 'Multichannel':
            df = df.rename(columns = final_dict)
        print('df cols',df.columns)
        ##############################################################################
        ############################## OLD CODE ####################################
        # # Select numerical columns
        # # colname_num = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
        # colname_num = ['Volume','Sales','TDP','WD','ND','Avg Price','API']
        # # colname_num = ['Sales']

        # # Select categorical columns
        # colname_obj = df.select_dtypes(include=['object']).columns.tolist()
        # colname_obj.remove('Time')
        ############################## OLD CODE ####################################

        # colname_obj = df.loc[df['Count'] == 1, 'Variable'].tolist()
        # colname_num = df.loc[df['Count'] != 1, 'Variable'].tolist()
        colname_obj = sorted(df.select_dtypes(include=['object']).columns.tolist())
        colname_num = sorted(df.select_dtypes(include=['number']).columns.tolist())

        colname_obj = [element.split('}', 1)[1] if '}' in element else element for element in colname_obj]
        colname_num = [element.split('}', 1)[1] if '}' in element else element for element in colname_num]
        try:
            colname_num.remove("Year")
        except:
            pass

        try:
            colname_obj.remove("Period")
        except:
            pass

        try:
            colname_obj.remove("Data source")
        except:
            pass
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
        seperator_param = 'millions'
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

        ######################## 04-06-2024 - BLANK COLNAME ####################
        if col_name == ['']:
            col_name = []
        else:
            col_name = col_name 
        ######################## 04-06-2024 - BLANK COLNAME ####################
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
        selected_weight_column22 = list(wt_measures_str.split(","))
        # selected_weight_column22 = ['Sales (M JPY)','Unit']
        # selected_weight_column22 = ['Sales (M USD)','Sales (M LC)']
        # print('294====selected_weight_column_all',selected_weight_column_all)

        data_type_resp = 'sales'

        base_sales_index_colname = 'Shiseido'
        # base_sales_index_colname = '1996 EDP'

        # selected_full_period = ['MAT Q4 2020']
        # comparative_full_period = ['MAT Q4 2019']

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
        filename = list(dict_table.keys())[0] + ".csv"
        # df = pd.read_csv(settings.TEMP_UPLOAD + filename)

        ##############################################################################
        db_flag = list(dict_table.keys())[0].split('_', 1)[0]
        print('dfff 12222 db_flag',db_flag)
        filename = list(dict_table.keys())[0] + ".csv"
        # Open the file in binary mode and detect the encoding
        # with open(settings.TEMP_UPLOAD + filename, 'rb') as f:
        #     result = chardet.detect(f.read(100000))  # Read the first 100000 bytes
        #     detected_encoding = result['encoding']

        # print(f"Detected encoding: {detected_encoding}")
        #######################################################################################

        #######################################################################################
        df = pd.read_csv(settings.TEMP_UPLOAD + filename,low_memory=False,engine='c')
        df[df.select_dtypes(include=['object']).columns] = df.select_dtypes(include=['object']).apply(lambda x: x.str.strip())

        ############################ FILL VALUES #########################################################
        categorical_cols = df.select_dtypes(include=['object']).columns
        numerical_cols = df.select_dtypes(include=['number']).columns

        # Fill categorical columns with "Not Available"
        df[categorical_cols] = df[categorical_cols].fillna("Not Available")

        # Fill numerical columns with 0
        df[numerical_cols] = df[numerical_cols].fillna(0)
        ############################ FILL VALUES #########################################################

        ##############################################################################
        # df = pl.read_excel(settings.TEMP_UPLOAD + filename)
        # df = df.to_pandas()
        df = df.rename(columns=rename_input_cols_dict)

        end_time_read = time.time()
        print("Time taken to read file using Pandas was ", end_time_read - start_time_read, "seconds!")
        ##################################### POLARS #####################################

        ############################ FILL VALUES #########################################################
        categorical_cols = df.select_dtypes(include=['object']).columns
        numerical_cols = df.select_dtypes(include=['number']).columns

        # Fill categorical columns with "Not Available"
        df[categorical_cols] = df[categorical_cols].fillna("Not Available")

        # Fill numerical columns with 0
        df[numerical_cols] = df[numerical_cols].fillna(0)
        ############################ FILL VALUES #########################################################

        ############### CODE TO ORDER CATEGORIES - 22-04-2024 #########################################
        if (category_var_name in row_name) or (category_var_name in col_name):
            mapping_category_dict = {'Skincare':'01}Skincare','Make-up':'02}Make-up','Fragrance':'03}Fragrance'}
            df[category_var_name] = df[category_var_name].replace(mapping_category_dict)
        ############### CODE TO ORDER CATEGORIES - 22-04-2024 #########################################

        ############### CODE TO ORDER CHANNEL - 26-04-2024 ##############################
        if (channel_var_name in row_name) or (channel_var_name in col_name):
            mapping_channel_dict = {'Department Stores':'01}Department Stores','E-Commerce':'02}E-Commerce','Specialty Stores':'03}Specialty Stores','Standalone Boutiques':'04}Standalone Boutiques'}
            df[channel_var_name] = df[channel_var_name].replace(mapping_channel_dict)
        ############### CODE TO ORDER CHANNEL - 26-04-2024 #########################################

        # ############### CODE TO ORDER Brand - 26-04-2024 ###########################
        if (brand_var_name in row_name) or (brand_var_name in col_name):
            mapping_brand_dict = {'(Other panel)':'~}(Other panel)'}
            df[brand_var_name] = df[brand_var_name].replace(mapping_brand_dict)
        # ############### CODE TO ORDER Brand - 26-04-2024 ###########################

        ################ ADDED BY MIHIR PAWAR - 04-08-2023 - TIME FILTER ##################
        # time_period_vals = df['Time'].unique().tolist() #distinct/unique of time periods

        # time_period_filter_val = [time_period_vals[0]]
        # time_period_filter_val = ['Q3_2023']
        # time_period_filter_val_resp = {'selected_time_period':time_period_filter_val}
        
        # df = df[df['Time'].isin(time_period_filter_val)]
        ################ ADDED BY MIHIR PAWAR - 04-08-2023 - TIME FILTER ##################


        ############## ADDED BY MIHIR PAWAR - 30-08-2023 - DERIVED COUMNS ###
        time_derived_start = time.time()

        # replace_values = {-np.inf: 0, np.inf: 0, 'null': 0, np.nan: 0}
        # df.replace(replace_values, inplace=True)

        # df.to_excel('df_SALES_FINAL.xlsx')
        time_derived_end = time.time()
        print("DERIVED FN TIME",time_derived_end - time_derived_start,"SECONDS!")
        ############## ADDED BY MIHIR PAWAR - 30-08-2023 - DERIVED COUMNS ###

        ################ code to generate selected and comparative periods - 15-0402024 ##########
        Current_yr = df['Year'].max()
        Previous_yr = Current_yr - 1
        max_year_df = df[df['Year'] == Current_yr]
        current_period = max_year_df['Period'].max()

        selected_full_period = ['QUARTER ' + str(current_period) + ' ' + str(Current_yr)]
        comparative_full_period = ['QUARTER ' + str(current_period) + ' ' + str(Previous_yr)]

        print('selected_full_period 540',selected_full_period)
        print('comparative_full_period 541',comparative_full_period)
        ################ code to generate selected and comparative periods - 15-0402024 ##########

        ####################################################################################
        filter_dict_resp = base_filter_resp(df,dict_table,row_name,col_name)

        # # Function to replace NaN with "Not Available"
        # def replace_nan(d):
        #     for key, value in d.items():
        #         if isinstance(value, dict):
        #             replace_nan(value)  # Recur for nested dictionaries
        #         elif isinstance(value, list):
        #             d[key] = [v if not pd.isna(v) else "Not Available" for v in value]
        #         elif pd.isna(value):
        #             d[key] = "Not Available"
        #     return d

        def replace_nan(d):
            # Predefine the "Not Available" value once to avoid redundant creation
            na_value = "Not Available"

            for key, value in d.items():
                if isinstance(value, dict):
                    # Use recursion for nested dictionaries
                    d[key] = replace_nan(value)
                elif isinstance(value, list):
                    # List comprehension avoids multiple function calls to pd.isna()
                    d[key] = [v if not pd.isna(v) else na_value for v in value]
                elif pd.isna(value):
                    d[key] = na_value

            return d

        # Replace NaN values in the dictionary
        filter_dict_resp = replace_nan(filter_dict_resp)
        #####################################################################################

        ####################### added on 24-06-2024 #################################################
        if ("Brand" in row_name) and (len(row_name)==1) and (measure_row_column_position == 'measure_in_column'):
            df['Brand sales index'] = 'Shiseido'
            brand_sales_index_value_flag = 'Yes'
        else:
            brand_sales_index_value_flag = 'No'
        ####################### added on 24-06-2024 #################################################

        ############ logic for CAGR - 29-08-2024 #################
        selected_time_range = selected_full_period[0].split()[0]
        if selected_time_range == 'FY':
            cagr_power_val = Current_yr - Previous_yr
            
        else:
            cagr_power_val = 989898
        ############ logic for CAGR - 29-08-2024 #################

        ######################## CODE TO TRANSFORM THE DATA 08-04-2024 ##################
        if (db_flag != 'Doors') or ((db_flag == 'Doors') and ('Door' not in selected_weight_column22)):
            df,selected_full_period_str,comparative_full_period_str = data_transformation(df,selected_weight_column22,selected_full_period,comparative_full_period)
        elif ((db_flag == 'Doors') and ('Door' in selected_weight_column22)):
            df,selected_full_period_str,comparative_full_period_str = data_transformation_doors(filename,selected_weight_column22,selected_full_period,comparative_full_period,seperator_param)

        column_list = list(df.columns)

        selected_weight_column_all = [column_name for column_name in column_list if any(substring in column_name for substring in selected_weight_column22)]

        # filter_dict_resp = base_filter_resp(df,dict_table,row_name,col_name)

        ################### ADDED ON 20-06-2024 ####################################################
        if ("Brand" in row_name) and (len(row_name)==1) and (measure_row_column_position == 'measure_in_column'):
            unique_base_index_brand_product_lst = df[brand_var_name].unique().tolist()
            unique_base_index_brand_product_resp = {brand_var_name:unique_base_index_brand_product_lst}
        elif ("Product Name" in row_name) and (len(row_name)==1) and (measure_row_column_position == 'measure_in_column'):
            unique_base_index_brand_product_lst = df['Product Name'].unique().tolist()
            unique_base_index_brand_product_resp = {'Product Name':unique_base_index_brand_product_lst}
        else:
            unique_base_index_brand_product_resp = {'Brand_Product':'No Brand/Product in the selection'}
        ################### ADDED ON 20-06-2024 ####################################################

        ################# CODE TO REPLACE "}" WITH "" -- 25-04-2024 ###

        # Check if category_var_name key is present in the dictionary
        if category_var_name in filter_dict_resp:
            filter_dict_resp[category_var_name] = [re.sub(r'.*}', '', value) for value in filter_dict_resp[category_var_name]]

        if channel_var_name in filter_dict_resp:
            filter_dict_resp[channel_var_name] = [re.sub(r'.*}', '', value) for value in filter_dict_resp[channel_var_name]]

        if brand_var_name in filter_dict_resp:
            filter_dict_resp[brand_var_name] = [re.sub(r'.*}', '', value) for value in filter_dict_resp[brand_var_name]]
        ################# CODE TO REPLACE "}" WITH "" -- 25-04-2024 ###

        print('55---99 filter_dict_resp',filter_dict_resp)
        filter_dict_resp = remove_duplicate_keys_and_values(filter_dict_resp)
        all_categories_vals = base_filter_resp_all(df,dict_table,row_name,col_name) 

        ######## CODE TO BRING BRAND AT FIRST POSITION IF PRESENT IN FILTER RESPONSE ####
        if 'Brand' in filter_dict_resp:
            filter_dict_resp = bring_key_to_first(filter_dict_resp, 'Brand')
        ######## CODE TO BRING BRAND AT FIRST POSITION IF PRESENT IN FILTER RESPONSE ####

        ################ ADDED BY MIHIR PAWAR - 04-08-2023 - TIME FILTER ##################
        time_period_vals = df['Time'].unique().tolist() #distinct/unique of time periods

        time_period_filter_val = [time_period_vals[0]]
        time_period_filter_val_resp = {'selected_time_period':time_period_filter_val}
        
        ################ ADDED BY MIHIR PAWAR - 04-08-2023 - TIME FILTER ##################

        ######################## CODE TO TRANSFORM THE DATA 08-04-2024 ################
        ######################## NEW LOGIC PIVOT 11-03-2024 ############################
        if (len(row_name) > 0) and (len(col_name) > 0):
            no_row_col_flag = 'row_col_present'
        else:
            no_row_col_flag = 'no_row_col_present'

        if no_row_col_flag == 'row_col_present':
            if measure_row_column_position == "measure_in_row":

                cross_df = sales_crosstab_logic_MAIN(selected_weight_column_all, dict_table, df, percent_calc, col_name, row_name,
                                          data_type_resp,seperated_flag_col,
                                          seperated_flag_row, totals_nested_flag,agg_func,measure_row_column_position)

                total_levels = cross_df.columns.nlevels
                print('total_levels',total_levels)

                if total_levels == 2:
                    cross_df = cross_df.swaplevel(0, 1, axis=1).sort_index(axis=1)

                elif total_levels == 3:
                    cross_df = cross_df.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, total_levels - 1, axis=1).sort_index(axis=1)

                elif total_levels == 4:
                    cross_df = cross_df.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, 3, axis=1).swaplevel(3, total_levels - 1, axis=1).sort_index(axis=1)

                # cross_df = cross_df.T

            elif measure_row_column_position == "measure_in_column":

                cross_df = sales_crosstab_logic_MAIN(selected_weight_column_all, dict_table, df, percent_calc, row_name, col_name,
                                          data_type_resp,
                                          seperated_flag_row, seperated_flag_col, totals_nested_flag,agg_func,measure_row_column_position)

                total_levels = cross_df.columns.nlevels
                print('total_levels',total_levels)

                if total_levels == 2:
                    cross_df = cross_df.swaplevel(0, 1, axis=1).sort_index(axis=1)

                elif total_levels == 3:
                    cross_df = cross_df.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, total_levels - 1, axis=1).sort_index(axis=1)

                elif total_levels == 4:
                    cross_df = cross_df.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, 3, axis=1).swaplevel(3, total_levels - 1, axis=1).sort_index(axis=1)

        ###########################################################################
        elif no_row_col_flag == 'no_row_col_present':

            if (len(row_name) >= 1) and len(col_name) == 0:

                if seperated_flag_row == 0:
                    cross_df = pd.DataFrame(df.groupby(row_name)[selected_weight_column_all].sum())
                    row_name_str = ''.join([str(elem) for elem in row_name])
                    cross_df = pd.concat([cross_df], keys=[row_name_str], axis=0)
                    # cross_df.to_excel('cross_df_MAIN_444.xlsx')

                elif seperated_flag_row == 1:
                    cross_df_stacked_lst = []
                    for row_name_loop in row_name:
                        cross_df = pd.DataFrame(df.groupby(row_name_loop)[selected_weight_column_all].sum())

                        row_name_str = ''.join([str(elem) for elem in row_name_loop])

                        cross_df = pd.concat([cross_df], keys=[row_name_str], axis=0)
                        cross_df_stacked_lst.append(cross_df)

                    cross_df = pd.concat(cross_df_stacked_lst)

                # if measure_row_column_position == "measure_in_row":
                #     cross_df = cross_df.T
                # elif measure_row_column_position == "measure_in_column":
                #     pass

                if len(row_name) == 1:

                    df_level1 = cross_df.groupby(level=0).agg(agg_func)
                    df_level1.index = df_level1.index = pd.MultiIndex.from_arrays([df_level1.index.values,
                                                                                   len(df_level1.index) * ['Grand Total']])
                    # Concatenate the totals row to the original DataFrame
                    cross_df = pd.concat([cross_df, df_level1])

                elif len(row_name) > 1:

                    cross_df = subtotals_multi_actuals_new(cross_df, row_name, agg_func)

            cross_df = pd.concat([cross_df], keys=['Facts'], axis=1)
            # Create a copy of the original DataFrame
            df_gt = cross_df.copy()

            df_gt = df_gt.droplevel(0, axis=1)
            # Rename the level 0 column to "Grand Total"
            df_gt = pd.concat([df_gt], keys=['Grand Total'], axis=1)

            # Concatenate the original and copied DataFrames side by side
            cross_df = pd.concat([cross_df, df_gt], axis=1)

        if measure_row_column_position == "measure_in_row":
            cross_df = cross_df.T
        elif measure_row_column_position == "measure_in_column":
            pass
        ###########################################################################
                
        try:
           cross_df = cross_df[~cross_df.columns.duplicated(keep='first')]
        except:
            pass

        try:
            cross_df = cross_df[~cross_df.index.duplicated(keep='first')]
        except:
            pass
        # cross_df.to_excel('cross_df_MAIN.xlsx')

        ################### ADDED ON 30-09-2024 - GRAND TOTAL ALL PIVOT #############
        ################### ADDED ON 30-09-2024 - GRAND TOTAL ALL PIVOT #############
        # if (len(row_name) > 0) and (len(col_name) > 0):
        #     no_row_col_flag = 'row_col_present'
        # else:
        #     no_row_col_flag = 'no_row_col_present'

        # if no_row_col_flag == 'row_col_present':
        #     if measure_row_column_position == "measure_in_row":

        #         cross_df_UNFILTERED_UNFILTERED = sales_crosstab_logic_MAIN(selected_weight_column_all, dict_table, df_UNFILTERED, percent_calc, col_name, row_name,
        #                                   data_type_resp,seperated_flag_col,
        #                                   seperated_flag_row, totals_nested_flag,agg_func,measure_row_column_position)

        #         total_levels = cross_df_UNFILTERED_UNFILTERED.columns.nlevels
        #         print('total_levels',total_levels)

        #         if total_levels == 2:
        #             cross_df_UNFILTERED_UNFILTERED = cross_df_UNFILTERED_UNFILTERED.swaplevel(0, 1, axis=1).sort_index(axis=1)

        #         elif total_levels == 3:
        #             cross_df_UNFILTERED_UNFILTERED = cross_df_UNFILTERED_UNFILTERED.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, total_levels - 1, axis=1).sort_index(axis=1)

        #         elif total_levels == 4:
        #             cross_df_UNFILTERED_UNFILTERED = cross_df_UNFILTERED.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, 3, axis=1).swaplevel(3, total_levels - 1, axis=1).sort_index(axis=1)

        #         # cross_df_UNFILTERED = cross_df_UNFILTERED.T

        #     elif measure_row_column_position == "measure_in_column":

        #         cross_df_UNFILTERED = sales_crosstab_logic_MAIN(selected_weight_column_all, dict_table, df_UNFILTERED, percent_calc, row_name, col_name,
        #                                   data_type_resp,
        #                                   seperated_flag_row, seperated_flag_col, totals_nested_flag,agg_func,measure_row_column_position)

        #         total_levels = cross_df_UNFILTERED.columns.nlevels
        #         print('total_levels',total_levels)

        #         if total_levels == 2:
        #             cross_df_UNFILTERED = cross_df_UNFILTERED.swaplevel(0, 1, axis=1).sort_index(axis=1)

        #         elif total_levels == 3:
        #             cross_df_UNFILTERED = cross_df_UNFILTERED.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, total_levels - 1, axis=1).sort_index(axis=1)

        #         elif total_levels == 4:
        #             cross_df_UNFILTERED = cross_df_UNFILTERED.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, 3, axis=1).swaplevel(3, total_levels - 1, axis=1).sort_index(axis=1)

        # ###########################################################################
        # elif no_row_col_flag == 'no_row_col_present':

        #     if (len(row_name) >= 1) and len(col_name) == 0:

        #         if seperated_flag_row == 0:
        #             cross_df_UNFILTERED = pd.DataFrame(df.groupby(row_name)[selected_weight_column_all].sum())
        #             row_name_str = ''.join([str(elem) for elem in row_name])
        #             cross_df_UNFILTERED = pd.concat([cross_df_UNFILTERED], keys=[row_name_str], axis=0)
        #             # cross_df_UNFILTERED.to_excel('cross_df_UNFILTERED_MAIN_444.xlsx')

        #         elif seperated_flag_row == 1:
        #             cross_df_UNFILTERED_stacked_lst = []
        #             for row_name_loop in row_name:
        #                 cross_df_UNFILTERED = pd.DataFrame(df.groupby(row_name_loop)[selected_weight_column_all].sum())

        #                 row_name_str = ''.join([str(elem) for elem in row_name_loop])

        #                 cross_df_UNFILTERED = pd.concat([cross_df_UNFILTERED], keys=[row_name_str], axis=0)
        #                 cross_df_UNFILTERED_stacked_lst.append(cross_df_UNFILTERED)

        #             cross_df_UNFILTERED = pd.concat(cross_df_UNFILTERED_stacked_lst)

        #         # if measure_row_column_position == "measure_in_row":
        #         #     cross_df_UNFILTERED = cross_df_UNFILTERED.T
        #         # elif measure_row_column_position == "measure_in_column":
        #         #     pass

        #         if len(row_name) == 1:

        #             df_level1 = cross_df_UNFILTERED.groupby(level=0).agg(agg_func)
        #             df_level1.index = df_level1.index = pd.MultiIndex.from_arrays([df_level1.index.values,
        #                                                                            len(df_level1.index) * ['Grand Total']])
        #             # Concatenate the totals row to the original DataFrame
        #             cross_df_UNFILTERED = pd.concat([cross_df_UNFILTERED, df_level1])

        #         elif len(row_name) > 1:

        #             cross_df_UNFILTERED = subtotals_multi_actuals_new(cross_df_UNFILTERED, row_name, agg_func)

        #     cross_df_UNFILTERED = pd.concat([cross_df_UNFILTERED], keys=['Facts'], axis=1)
        #     # Create a copy of the original DataFrame
        #     df_gt = cross_df_UNFILTERED.copy()

        #     df_gt = df_gt.droplevel(0, axis=1)
        #     # Rename the level 0 column to "Grand Total"
        #     df_gt = pd.concat([df_gt], keys=['Grand Total'], axis=1)

        #     # Concatenate the original and copied DataFrames side by side
        #     cross_df_UNFILTERED = pd.concat([cross_df_UNFILTERED, df_gt], axis=1)

        # if measure_row_column_position == "measure_in_row":
        #     cross_df_UNFILTERED = cross_df_UNFILTERED.T
        # elif measure_row_column_position == "measure_in_column":
        #     pass
        # ###########################################################################
                
        # try:
        #    cross_df_UNFILTERED = cross_df_UNFILTERED[~cross_df_UNFILTERED.columns.duplicated(keep='first')]
        # except:
        #     pass

        # try:
        #     cross_df_UNFILTERED = cross_df_UNFILTERED[~cross_df_UNFILTERED.index.duplicated(keep='first')]
        # except:
        #     pass
        # cross_df_UNFILTERED.to_excel('cross_df_UNFILTERED_MAIN.xlsx')

        ################### ADDED ON 30-09-2024 - GRAND TOTAL ALL PIVOT #############
        ################### ADDED ON 30-09-2024 - GRAND TOTAL ALL PIVOT #############

        #################### DERIVED COLUMNS - 11-03-2024 ###################################
        cross_df.fillna(0,inplace=True)
        if measure_row_column_position == "measure_in_row":
            # cross_df.to_excel('cross_df_before_transpose.xlsx')
            cross_df = cross_df.T           
            cross_df = derived_MAIN_fn(cross_df,base_sales_index_colname,row_name,col_name,measure_row_column_position,cagr_power_val,brand_sales_index_value_flag='No')
            cross_df = cross_df.T
            # cross_df.to_excel('CROSS_DF_CAUCULATIONS.xlsx')
            # exit('dfddgdgdvde')

        elif measure_row_column_position == "measure_in_column":
            cross_df = derived_MAIN_fn(cross_df,base_sales_index_colname,row_name,col_name,measure_row_column_position,cagr_power_val,brand_sales_index_value_flag)

        # cross_df.to_excel('before_replace_cy_ya_with_actual_period.xlsx')
        ################## CODE TO REPLACE CY AND YA WITH ACTUAL PERIOD - 19-04-2024 ####
        cross_df = replace_cy_ya_with_actual_period(cross_df,measure_row_column_position,selected_full_period_str,comparative_full_period_str)
        # cross_df.to_excel('after_replace_cy_ya_with_actual_period.xlsx')
        # cross_df.to_excel('cross_df_derived_MAIN_fn.xlsx')
        ################## CODE TO REPLACE CY AND YA WITH ACTUAL PERIOD - 19-04-2024 ####
        last_level_values_list = cross_df.columns.get_level_values(-1).unique().tolist()

        dict_selected_measures_lst = {}

        print('selected_weight_column22 598',selected_weight_column22)
        for key in selected_weight_column22:
            dict_selected_measures_lst[key] = [item for item in last_level_values_list if item.startswith(key)]
        print('last_level_values_list',last_level_values_list)
        print('dict_selected_measures_lst',dict_selected_measures_lst)

        ##################### new code filter data 02-04-2024 #########################################
        # current_time_period_actual = selected_weight_column22[0] + '_ ' + selected_full_period_str
        # print('current_time_period_actual 645',current_time_period_actual)

        # if db_flag == 'Sellout':
        #     if (len(selected_weight_column22)==1):
        #         index_lst_cols = [0,1,3]
        #     elif (len(selected_weight_column22)==2):
        #         index_lst_cols = [0,1,3,7,8,10]

        # elif ((db_flag == 'Sale') or (db_flag == 'Door')):
        #     if (len(selected_weight_column22)==1):
        #         index_lst_cols = [0,1,3]
        #     elif (len(selected_weight_column22)>1):
        #         index_lst_cols = [0,1,3,8,10]

        ############### OLD CODE DEFAULT SELECTIONS - 23-04-2024 ########################################
        # if (measure_row_column_position == 'measure_in_column') and (len(row_name) == 1) and (("Brand" in row_name) or ("Product Name" in row_name)):
        #     print('brand condition!')
        #     if len(selected_weight_column22) == 1:
        #         index_lst_cols = [0, 1, 3]
        #     elif len(selected_weight_column22) == 2:
        #         index_lst_cols = [0, 1, 3, 9, 10, 12]
        #     elif len(selected_weight_column22) == 3:
        #         index_lst_cols = [0, 1, 3, 9, 10, 12, 18, 19, 21]
        #     elif len(selected_weight_column22) == 4:
        #         index_lst_cols = [0, 1, 3, 9, 10, 12, 18, 19, 21, 27, 28, 30]
        #     elif len(selected_weight_column22) == 5:
        #         index_lst_cols = [0, 1, 3, 9, 10, 12, 18, 19, 21, 27, 28, 30, 36, 37, 39]
        # else:
        #     ##############################################################
        #     print('not condtiontion')
        #     if len(selected_weight_column22) == 1:
        #         index_lst_cols = [0, 1, 3]
        #     elif len(selected_weight_column22) == 2:
        #         index_lst_cols = [0, 1, 3, 8, 9, 11]
        #     elif len(selected_weight_column22) == 3:
        #         index_lst_cols = [0, 1, 3, 8, 9, 11, 16, 17, 19]
        #     elif len(selected_weight_column22) == 4:
        #         index_lst_cols = [0, 1, 3, 8, 9, 11, 16, 17, 19,24,25,27]
        #     elif len(selected_weight_column22) == 5:
        #         index_lst_cols = [0, 1, 3, 8, 9, 11, 16, 17, 19,24,25,27,32,33,35]
        ############### OLD CODE DEFAULT SELECTIONS - 23-04-2024 ########################################

        ############# REMOVED RANK - 23-09-2024 ############################################################
        # if (measure_row_column_position == 'measure_in_column') and (len(row_name) == 1) and (("Brand" in row_name) or ("Product Name" in row_name)):
        #     print('brand condition!')
        #     if len(selected_weight_column22) == 1:
        #         index_lst_cols = [1, 3]
        #     elif len(selected_weight_column22) == 2:
        #         index_lst_cols = [1, 3, 10, 12]
        #     elif len(selected_weight_column22) == 3:
        #         index_lst_cols = [1, 3, 10, 12, 19, 21]
        #     elif len(selected_weight_column22) == 4:
        #         index_lst_cols = [1, 3, 10, 12, 19, 21, 28, 30]
        #     elif len(selected_weight_column22) == 5:
        #         index_lst_cols = [1, 3, 10, 12, 19, 21, 28, 30, 37, 39]
        # else:
        #     ##############################################################
        #     print('not condtiontion')
        #     if len(selected_weight_column22) == 1:
        #         index_lst_cols = [1, 3]
        #     elif len(selected_weight_column22) == 2:
        #         index_lst_cols = [1, 3, 9, 11]
        #     elif len(selected_weight_column22) == 3:
        #         index_lst_cols = [1, 3, 9, 11, 17, 19]
        #     elif len(selected_weight_column22) == 4:
        #         index_lst_cols = [1, 3, 9, 11, 17, 19, 25, 27]
        #     elif len(selected_weight_column22) == 5:
        #         index_lst_cols = [1, 3, 9, 11, 17, 19, 25, 27, 33, 35]
        # ############# REMOVED RANK - 23-09-2024 ############################################################

        ##################### NEW LOGIC DYNAMIC SUBSET #######################################
        def generate_index_list(base_start, base_step, length):
            # Generate the index list dynamically
            index_list = []
            for i in range(length):
                index_list.append(base_start + i * base_step)  # First index in the pair
                index_list.append(base_start + i * base_step + 2)  # Second index in the pair
            return index_list

        if (measure_row_column_position == 'measure_in_column') and (len(row_name) == 1) and ({"Brand", "Product Name"} & set(row_name)):
            print('brand condition!')
            base_start = 1
            base_step = 10  # distance between each additional set for 'brand condition'
            index_lst_cols = generate_index_list(base_start, base_step, len(selected_weight_column22))
        else:
            print('not condition')
            base_start = 1
            base_step = 9  # distance between each additional set for 'not condition'
            index_lst_cols = generate_index_list(base_start, base_step, len(selected_weight_column22))

        ##################### NEW LOGIC DYNAMIC SUBSET #######################################


        sublist = [last_level_values_list[i] for i in index_lst_cols]

        cross_df = cross_df.loc[:, cross_df.columns.get_level_values(-1).isin(list(sublist))]

        dict_selected_measures_filtered_lst = {}
        for key in selected_weight_column22:
            dict_selected_measures_filtered_lst[key] = [item for item in sublist if item.startswith(key)]
        print('dict_selected_measures_filtered_lst===',dict_selected_measures_filtered_lst)

        if (any('Sales (LC)' in item for item in selected_weight_column_all)):
            dict_selected_measures_lst = dict_selected_measures_filtered_lst
        #################### DERIVED COLUMNS - 11-03-2024 ###################################

        period_to_be_replaced_str = [selected_full_period_str][0].split()[0]
        ##### CODE TO REPLACE QUARTER - 19-04-2024 ###########################
        if period_to_be_replaced_str =='QUARTER':

            if measure_row_column_position == "measure_in_column":
                try:
                    cross_df.rename(columns=lambda x: re.sub('QUARTER','', x), inplace=True)
                except:
                    pass
            if measure_row_column_position == "measure_in_row":
                try:
                    cross_df.rename(index=lambda x: re.sub('QUARTER','', x), inplace=True)
                except:
                    pass

        #################### REPLACE SALES - 09-05-2024 ####################
        # selected_weight_column22_STR = selected_weight_column22[0]
        # dict_selected_measures_filtered_lst

        # old_string = selected_weight_column22_STR
        # new_string = 'Sales'

        # # Replace old string with new string in the entire dictionary
        # dict_selected_measures_filtered_lst = replace_string_in_dict(dict_selected_measures_filtered_lst, old_string, new_string)

        # print('dict_selected_measures_filtered_lst 716',dict_selected_measures_filtered_lst)

        # dict_selected_measures_lst = replace_string_in_dict(dict_selected_measures_lst, old_string, new_string)

        # print('dict_selected_measures_lst 555',dict_selected_measures_lst)
        #################### REPLACE SALES - 09-05-2024 ####################




        ##### CODE TO REPLACE QUARTER - 19-04-2024 ###########################

        ################################################################################################################
        # if (seperated_flag_row == 0 and seperated_flag_col == 0):
        # # if (len(row_name) == 1 and len(col_name) == 1):

        #     cross_df = cross_df.reindex(sorted(cross_df.index), axis=0)
        #     cross_df = cross_df.reindex(sorted(cross_df.columns), axis=1)
        ################################################################################################################

        #### CODE TO DROP GRAND TOTAL WHEN SALES LC  IS SELECTED - 18-04-2024 ####
        # if (any('Sales (LC)' in item for item in selected_weight_column_all)):
        #     if measure_row_column_position == "measure_in_column":
        #         if ('Country' in row_name):
        #             print('seeeeerrr')

        #             try:
        #                 # Identify columns that contain "Grand Total" in any level
        #                 grand_total_index = [col for col in cross_df.index if any('Grand Total' in level for level in col)]

        #                 # Drop the identified columns
        #                 cross_df = cross_df.drop(index=grand_total_index)
        #             except Exception as e:
        #                 print("An error occurred:", e)
                    
        #             # try:
        #             #     for level in cross_df.index.levels:
        #             #         if 'Grand Total' in level:
        #             #             print('grand total in rows found!')
        #             #             print('level rows ',level)
        #             #             cross_df = cross_df.drop('Grand Total', axis=0, level=level.name)
        #             # except:
        #             #     pass

        #         elif ('Country' in col_name):
        #             try:
        #                 # Identify columns that contain "Grand Total" in any level
        #                 grand_total_columns = [col for col in cross_df.columns if any('Grand Total' in level for level in col)]

        #                 # Drop the identified columns
        #                 cross_df = cross_df.drop(columns=grand_total_columns)
        #             except Exception as e:
        #                 print("An error occurred:", e)

                    # try:
                    #     for level in cross_df.columns.levels:
                    #         if 'Grand Total' in level:
                    #             print('grand total found in columns!')
                    #             print('level columns ',level)
                    #             cross_df = cross_df.drop('Grand Total', axis=1, level=level.name)
                    # except:
                    #     pass

        #     elif measure_row_column_position == "measure_in_row":
        #         try:
        #             for level in cross_df.columns.levels:
        #                 if 'Grand Total' in level:
        #                     cross_df = cross_df.drop('Grand Total', axis=1, level=level.name)
        #         except:
        #             pass

        #### CODE TO DROP GRAND TOTAL WHEN SALES LC  IS SELECTED - 18-04-2024 ####

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

        ###################### code to remove prefix } - 22-04-2024 ###############################
        if ((category_var_name in row_name) or (category_var_name in col_name)) or ((channel_var_name in row_name) or (channel_var_name in col_name)) or ((brand_var_name in row_name) or (brand_var_name in col_name)):
            try:
                cross_df = remove_prefix(cross_df)
            except:
                pass
        ###################### code to remove prefix } - 22-04-2024 ###############################

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
        # cross_df.to_excel('NULL_CROSSDF.xlsx')
        ############# SUMMARY OF CROSSTAB DATA ##############################
        # crosstab_summary = cross_df.describe()
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
        # cross_df.to_excel('FINAL_CROSSTABB.xlsx')
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
                "dict_selected_measures_filtered_lst": dict_selected_measures_filtered_lst,
                # "base_column_names_indices_resp": base_column_names_indices_resp,
                "filter_dict_resp":filter_dict_resp,
                "all_categories_vals":all_categories_vals,
                "time_period_flag": time_period_flag,
                "time_period_vals": time_period_vals,
                "time_period_filter_val_resp": time_period_filter_val_resp,
                # "df_cross_json_test": df_cross_json21,
                "error": "Correct Data",
                "seperated_flag_col":seperated_flag_col,
                "current_time_period_resp":selected_full_period_str,
                "comparative_time_period_resp":comparative_full_period_str,
                "measure_type":measure_row_column_position,
                "display_table":'No',
                # "unique_base_index_brand_product_resp":unique_base_index_brand_product_resp,
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


def crosstab_table_NEWLOGIC_WITHOUT_DF(request):
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
        seperator_param = 'millions'
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

        ######################## 04-06-2024 - BLANK COLNAME ####################
        if col_name == ['']:
            col_name = []
        else:
            col_name = col_name 
        ######################## 04-06-2024 - BLANK COLNAME ####################
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
        selected_weight_column22 = list(wt_measures_str.split(","))
        # selected_weight_column22 = ['Sales (M JPY)','Unit']
        # selected_weight_column22 = ['Sales (M USD)','Sales (M LC)']
        # print('294====selected_weight_column_all',selected_weight_column_all)

        data_type_resp = 'sales'

        base_sales_index_colname = 'Shiseido'
        # base_sales_index_colname = '1996 EDP'

        # selected_full_period = ['MAT Q4 2020']
        # comparative_full_period = ['MAT Q4 2019']

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
        filename = list(dict_table.keys())[0] + ".csv"
        # df = pd.read_csv(settings.TEMP_UPLOAD + filename)

        ##############################################################################
        db_flag = list(dict_table.keys())[0].split('_', 1)[0]
        print('dfff 12222 db_flag',db_flag)
        filename = list(dict_table.keys())[0] + ".csv"
        # Open the file in binary mode and detect the encoding
        # with open(settings.TEMP_UPLOAD + filename, 'rb') as f:
        #     result = chardet.detect(f.read(100000))  # Read the first 100000 bytes
        #     detected_encoding = result['encoding']

        # print(f"Detected encoding: {detected_encoding}")
        #######################################################################################

        #######################################################################################
        df = pd.read_csv(settings.TEMP_UPLOAD + filename,low_memory=False,engine='c')
        df[df.select_dtypes(include=['object']).columns] = df.select_dtypes(include=['object']).apply(lambda x: x.str.strip())

        ############################ FILL VALUES #########################################################
        categorical_cols = df.select_dtypes(include=['object']).columns
        numerical_cols = df.select_dtypes(include=['number']).columns

        # Fill categorical columns with "Not Available"
        df[categorical_cols] = df[categorical_cols].fillna("Not Available")

        # Fill numerical columns with 0
        df[numerical_cols] = df[numerical_cols].fillna(0)
        ############################ FILL VALUES #########################################################

        ##############################################################################
        # df = pl.read_excel(settings.TEMP_UPLOAD + filename)
        # df = df.to_pandas()
        df = df.rename(columns=rename_input_cols_dict)

        end_time_read = time.time()
        print("Time taken to read file using Pandas was ", end_time_read - start_time_read, "seconds!")
        ##################################### POLARS #####################################

        ############### CODE TO ORDER CATEGORIES - 22-04-2024 #########################################
        if (category_var_name in row_name) or (category_var_name in col_name):
            mapping_category_dict = {'Skincare':'01}Skincare','Make-up':'02}Make-up','Fragrance':'03}Fragrance'}
            df[category_var_name] = df[category_var_name].replace(mapping_category_dict)
        ############### CODE TO ORDER CATEGORIES - 22-04-2024 #########################################

        ############### CODE TO ORDER CHANNEL - 26-04-2024 ##############################
        if (channel_var_name in row_name) or (channel_var_name in col_name):
            mapping_channel_dict = {'Department Stores':'01}Department Stores','E-Commerce':'02}E-Commerce','Specialty Stores':'03}Specialty Stores','Standalone Boutiques':'04}Standalone Boutiques'}
            df[channel_var_name] = df[channel_var_name].replace(mapping_channel_dict)
        ############### CODE TO ORDER CHANNEL - 26-04-2024 #########################################

        # ############### CODE TO ORDER Brand - 26-04-2024 ###########################
        if (brand_var_name in row_name) or (brand_var_name in col_name):
            mapping_brand_dict = {'(Other panel)':'~}(Other panel)'}
            df[brand_var_name] = df[brand_var_name].replace(mapping_brand_dict)
        # ############### CODE TO ORDER Brand - 26-04-2024 ###########################

        ################ ADDED BY MIHIR PAWAR - 04-08-2023 - TIME FILTER ##################
        # time_period_vals = df['Time'].unique().tolist() #distinct/unique of time periods

        # time_period_filter_val = [time_period_vals[0]]
        # time_period_filter_val = ['Q3_2023']
        # time_period_filter_val_resp = {'selected_time_period':time_period_filter_val}
        
        # df = df[df['Time'].isin(time_period_filter_val)]
        ################ ADDED BY MIHIR PAWAR - 04-08-2023 - TIME FILTER ##################


        ############## ADDED BY MIHIR PAWAR - 30-08-2023 - DERIVED COUMNS ###
        time_derived_start = time.time()

        # replace_values = {-np.inf: 0, np.inf: 0, 'null': 0, np.nan: 0}
        # df.replace(replace_values, inplace=True)

        # df.to_excel('df_SALES_FINAL.xlsx')
        time_derived_end = time.time()
        print("DERIVED FN TIME",time_derived_end - time_derived_start,"SECONDS!")
        ############## ADDED BY MIHIR PAWAR - 30-08-2023 - DERIVED COUMNS ###

        ################ code to generate selected and comparative periods - 15-0402024 ##########
        Current_yr = df['Year'].max()
        Previous_yr = Current_yr - 1
        max_year_df = df[df['Year'] == Current_yr]
        current_period = max_year_df['Period'].max()

        selected_full_period = ['QUARTER ' + str(current_period) + ' ' + str(Current_yr)]
        comparative_full_period = ['QUARTER ' + str(current_period) + ' ' + str(Previous_yr)]

        print('selected_full_period 540',selected_full_period)
        print('comparative_full_period 541',comparative_full_period)
        ################ code to generate selected and comparative periods - 15-0402024 ##########

        ####################################################################################
        filter_dict_resp = base_filter_resp(df,dict_table,row_name,col_name)

        # # Function to replace NaN with "Not Available"
        # def replace_nan(d):
        #     for key, value in d.items():
        #         if isinstance(value, dict):
        #             replace_nan(value)  # Recur for nested dictionaries
        #         elif isinstance(value, list):
        #             d[key] = [v if not pd.isna(v) else "Not Available" for v in value]
        #         elif pd.isna(value):
        #             d[key] = "Not Available"
        #     return d

        def replace_nan(d):
            # Predefine the "Not Available" value once to avoid redundant creation
            na_value = "Not Available"

            for key, value in d.items():
                if isinstance(value, dict):
                    # Use recursion for nested dictionaries
                    d[key] = replace_nan(value)
                elif isinstance(value, list):
                    # List comprehension avoids multiple function calls to pd.isna()
                    d[key] = [v if not pd.isna(v) else na_value for v in value]
                elif pd.isna(value):
                    d[key] = na_value

            return d

        # Replace NaN values in the dictionary
        filter_dict_resp = replace_nan(filter_dict_resp)
        #####################################################################################

        ####################### added on 24-06-2024 #################################################
        if ("Brand" in row_name) and (len(row_name)==1) and (measure_row_column_position == 'measure_in_column'):
            df['Brand sales index'] = 'Shiseido'
            brand_sales_index_value_flag = 'Yes'
        else:
            brand_sales_index_value_flag = 'No'
        ####################### added on 24-06-2024 #################################################

        ############ logic for CAGR - 29-08-2024 #################
        selected_time_range = selected_full_period[0].split()[0]
        if selected_time_range == 'FY':
            cagr_power_val = Current_yr - Previous_yr
            
        else:
            cagr_power_val = 989898

        if (db_flag != 'Doors') or ((db_flag == 'Doors') and ('Door' not in selected_weight_column22)):
            df,selected_full_period_str,comparative_full_period_str = data_transformation(df,selected_weight_column22,selected_full_period,comparative_full_period)
        elif ((db_flag == 'Doors') and ('Door' in selected_weight_column22)):
            df,selected_full_period_str,comparative_full_period_str = data_transformation_doors(filename,selected_weight_column22,selected_full_period,comparative_full_period,seperator_param)
        ############ logic for CAGR - 29-08-2024 #################
        print('1036==',df.columns)
        print('1037==',selected_weight_column22)

        suffixes = ['_CY', '_YA']

        new_columns_df = [col + suffix for col in selected_weight_column22 for suffix in suffixes] + ['Time']
        print('1042==',new_columns_df)

        column_list11 = list(df.columns)
        column_list = [item for item in column_list11 if item not in selected_weight_column22] + new_columns_df
        ######################## CODE TO TRANSFORM THE DATA 08-04-2024 #################

        print('column_list 1045',column_list)

        selected_weight_column_all = [column_name for column_name in column_list if any(substring in column_name for substring in selected_weight_column22)]
        print('selected_weight_column_all 1048',selected_weight_column_all)

        ################### ADDED ON 20-06-2024 ####################################################
        if ("Brand" in row_name) and (len(row_name)==1) and (measure_row_column_position == 'measure_in_column'):
            unique_base_index_brand_product_lst = df[brand_var_name].unique().tolist()
            unique_base_index_brand_product_resp = {brand_var_name:unique_base_index_brand_product_lst}
        elif ("Product Name" in row_name) and (len(row_name)==1) and (measure_row_column_position == 'measure_in_column'):
            unique_base_index_brand_product_lst = df['Product Name'].unique().tolist()
            unique_base_index_brand_product_resp = {'Product Name':unique_base_index_brand_product_lst}
        else:
            unique_base_index_brand_product_resp = {'Brand_Product':'No Brand/Product in the selection'}
        ################### ADDED ON 20-06-2024 ####################################################

        ################# CODE TO REPLACE "}" WITH "" -- 25-04-2024 ###

        # Check if category_var_name key is present in the dictionary
        if category_var_name in filter_dict_resp:
            filter_dict_resp[category_var_name] = [re.sub(r'.*}', '', value) for value in filter_dict_resp[category_var_name]]

        if channel_var_name in filter_dict_resp:
            filter_dict_resp[channel_var_name] = [re.sub(r'.*}', '', value) for value in filter_dict_resp[channel_var_name]]

        if brand_var_name in filter_dict_resp:
            filter_dict_resp[brand_var_name] = [re.sub(r'.*}', '', value) for value in filter_dict_resp[brand_var_name]]
        ################# CODE TO REPLACE "}" WITH "" -- 25-04-2024 ###

        print('55---99 filter_dict_resp',filter_dict_resp)
        filter_dict_resp = remove_duplicate_keys_and_values(filter_dict_resp)
        all_categories_vals = base_filter_resp_all(df,dict_table,row_name,col_name) 

        ######## CODE TO BRING BRAND AT FIRST POSITION IF PRESENT IN FILTER RESPONSE ####
        if 'Brand' in filter_dict_resp:
            filter_dict_resp = bring_key_to_first(filter_dict_resp, 'Brand')
        ######## CODE TO BRING BRAND AT FIRST POSITION IF PRESENT IN FILTER RESPONSE ####

        ################ ADDED BY MIHIR PAWAR - 04-08-2023 - TIME FILTER ##################
        # time_period_vals = df['Time'].unique().tolist() #distinct/unique of time periods

        # time_period_filter_val = [time_period_vals[0]]
        # time_period_filter_val_resp = {'selected_time_period':time_period_filter_val}
        ################ ADDED BY MIHIR PAWAR - 04-08-2023 - TIME FILTER ##################

        ######################## CODE TO TRANSFORM THE DATA 08-04-2024 ################
        ######################## NEW LOGIC PIVOT 11-03-2024 ############################
        if (len(row_name) > 0) and (len(col_name) > 0):
            no_row_col_flag = 'row_col_present'
        else:
            no_row_col_flag = 'no_row_col_present'

        if no_row_col_flag == 'row_col_present':
            if measure_row_column_position == "measure_in_row":

                cross_df = sales_crosstab_logic_MAIN(selected_weight_column_all, dict_table, df, percent_calc, col_name, row_name,
                                          data_type_resp,seperated_flag_col,
                                          seperated_flag_row, totals_nested_flag,agg_func,measure_row_column_position)

                total_levels = cross_df.columns.nlevels
                print('total_levels',total_levels)

                if total_levels == 2:
                    cross_df = cross_df.swaplevel(0, 1, axis=1).sort_index(axis=1)

                elif total_levels == 3:
                    cross_df = cross_df.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, total_levels - 1, axis=1).sort_index(axis=1)

                elif total_levels == 4:
                    cross_df = cross_df.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, 3, axis=1).swaplevel(3, total_levels - 1, axis=1).sort_index(axis=1)

                # cross_df = cross_df.T

            elif measure_row_column_position == "measure_in_column":

                cross_df = sales_crosstab_logic_MAIN(selected_weight_column_all, dict_table, df, percent_calc, row_name, col_name,
                                          data_type_resp,
                                          seperated_flag_row, seperated_flag_col, totals_nested_flag,agg_func,measure_row_column_position)

                total_levels = cross_df.columns.nlevels
                print('total_levels',total_levels)

                if total_levels == 2:
                    cross_df = cross_df.swaplevel(0, 1, axis=1).sort_index(axis=1)

                elif total_levels == 3:
                    cross_df = cross_df.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, total_levels - 1, axis=1).sort_index(axis=1)

                elif total_levels == 4:
                    cross_df = cross_df.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, 3, axis=1).swaplevel(3, total_levels - 1, axis=1).sort_index(axis=1)

        ###########################################################################
        elif no_row_col_flag == 'no_row_col_present':

            if (len(row_name) >= 1) and len(col_name) == 0:

                if seperated_flag_row == 0:
                    cross_df = pd.DataFrame(df.groupby(row_name)[selected_weight_column_all].sum())
                    row_name_str = ''.join([str(elem) for elem in row_name])
                    cross_df = pd.concat([cross_df], keys=[row_name_str], axis=0)
                    # cross_df.to_excel('cross_df_MAIN_444.xlsx')

                elif seperated_flag_row == 1:
                    cross_df_stacked_lst = []
                    for row_name_loop in row_name:
                        cross_df = pd.DataFrame(df.groupby(row_name_loop)[selected_weight_column_all].sum())

                        row_name_str = ''.join([str(elem) for elem in row_name_loop])

                        cross_df = pd.concat([cross_df], keys=[row_name_str], axis=0)
                        cross_df_stacked_lst.append(cross_df)

                    cross_df = pd.concat(cross_df_stacked_lst)

                # if measure_row_column_position == "measure_in_row":
                #     cross_df = cross_df.T
                # elif measure_row_column_position == "measure_in_column":
                #     pass

                if len(row_name) == 1:

                    df_level1 = cross_df.groupby(level=0).agg(agg_func)
                    df_level1.index = df_level1.index = pd.MultiIndex.from_arrays([df_level1.index.values,
                                                                                   len(df_level1.index) * ['Grand Total']])
                    # Concatenate the totals row to the original DataFrame
                    cross_df = pd.concat([cross_df, df_level1])

                elif len(row_name) > 1:

                    cross_df = subtotals_multi_actuals_new(cross_df, row_name, agg_func)

            cross_df = pd.concat([cross_df], keys=['Facts'], axis=1)
            # Create a copy of the original DataFrame
            df_gt = cross_df.copy()

            df_gt = df_gt.droplevel(0, axis=1)
            # Rename the level 0 column to "Grand Total"
            df_gt = pd.concat([df_gt], keys=['Grand Total'], axis=1)

            # Concatenate the original and copied DataFrames side by side
            cross_df = pd.concat([cross_df, df_gt], axis=1)

        if measure_row_column_position == "measure_in_row":
            cross_df = cross_df.T
        elif measure_row_column_position == "measure_in_column":
            pass
        ###########################################################################
                
        try:
           cross_df = cross_df[~cross_df.columns.duplicated(keep='first')]
        except:
            pass

        try:
            cross_df = cross_df[~cross_df.index.duplicated(keep='first')]
        except:
            pass
        # cross_df.to_excel('cross_df_MAIN.xlsx')

        ################### ADDED ON 30-09-2024 - GRAND TOTAL ALL PIVOT #############
        ################### ADDED ON 30-09-2024 - GRAND TOTAL ALL PIVOT #############
        # if (len(row_name) > 0) and (len(col_name) > 0):
        #     no_row_col_flag = 'row_col_present'
        # else:
        #     no_row_col_flag = 'no_row_col_present'

        # if no_row_col_flag == 'row_col_present':
        #     if measure_row_column_position == "measure_in_row":

        #         cross_df_UNFILTERED_UNFILTERED = sales_crosstab_logic_MAIN(selected_weight_column_all, dict_table, df_UNFILTERED, percent_calc, col_name, row_name,
        #                                   data_type_resp,seperated_flag_col,
        #                                   seperated_flag_row, totals_nested_flag,agg_func,measure_row_column_position)

        #         total_levels = cross_df_UNFILTERED_UNFILTERED.columns.nlevels
        #         print('total_levels',total_levels)

        #         if total_levels == 2:
        #             cross_df_UNFILTERED_UNFILTERED = cross_df_UNFILTERED_UNFILTERED.swaplevel(0, 1, axis=1).sort_index(axis=1)

        #         elif total_levels == 3:
        #             cross_df_UNFILTERED_UNFILTERED = cross_df_UNFILTERED_UNFILTERED.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, total_levels - 1, axis=1).sort_index(axis=1)

        #         elif total_levels == 4:
        #             cross_df_UNFILTERED_UNFILTERED = cross_df_UNFILTERED.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, 3, axis=1).swaplevel(3, total_levels - 1, axis=1).sort_index(axis=1)

        #         # cross_df_UNFILTERED = cross_df_UNFILTERED.T

        #     elif measure_row_column_position == "measure_in_column":

        #         cross_df_UNFILTERED = sales_crosstab_logic_MAIN(selected_weight_column_all, dict_table, df_UNFILTERED, percent_calc, row_name, col_name,
        #                                   data_type_resp,
        #                                   seperated_flag_row, seperated_flag_col, totals_nested_flag,agg_func,measure_row_column_position)

        #         total_levels = cross_df_UNFILTERED.columns.nlevels
        #         print('total_levels',total_levels)

        #         if total_levels == 2:
        #             cross_df_UNFILTERED = cross_df_UNFILTERED.swaplevel(0, 1, axis=1).sort_index(axis=1)

        #         elif total_levels == 3:
        #             cross_df_UNFILTERED = cross_df_UNFILTERED.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, total_levels - 1, axis=1).sort_index(axis=1)

        #         elif total_levels == 4:
        #             cross_df_UNFILTERED = cross_df_UNFILTERED.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, 3, axis=1).swaplevel(3, total_levels - 1, axis=1).sort_index(axis=1)

        # ###########################################################################
        # elif no_row_col_flag == 'no_row_col_present':

        #     if (len(row_name) >= 1) and len(col_name) == 0:

        #         if seperated_flag_row == 0:
        #             cross_df_UNFILTERED = pd.DataFrame(df.groupby(row_name)[selected_weight_column_all].sum())
        #             row_name_str = ''.join([str(elem) for elem in row_name])
        #             cross_df_UNFILTERED = pd.concat([cross_df_UNFILTERED], keys=[row_name_str], axis=0)
        #             # cross_df_UNFILTERED.to_excel('cross_df_UNFILTERED_MAIN_444.xlsx')

        #         elif seperated_flag_row == 1:
        #             cross_df_UNFILTERED_stacked_lst = []
        #             for row_name_loop in row_name:
        #                 cross_df_UNFILTERED = pd.DataFrame(df.groupby(row_name_loop)[selected_weight_column_all].sum())

        #                 row_name_str = ''.join([str(elem) for elem in row_name_loop])

        #                 cross_df_UNFILTERED = pd.concat([cross_df_UNFILTERED], keys=[row_name_str], axis=0)
        #                 cross_df_UNFILTERED_stacked_lst.append(cross_df_UNFILTERED)

        #             cross_df_UNFILTERED = pd.concat(cross_df_UNFILTERED_stacked_lst)

        #         # if measure_row_column_position == "measure_in_row":
        #         #     cross_df_UNFILTERED = cross_df_UNFILTERED.T
        #         # elif measure_row_column_position == "measure_in_column":
        #         #     pass

        #         if len(row_name) == 1:

        #             df_level1 = cross_df_UNFILTERED.groupby(level=0).agg(agg_func)
        #             df_level1.index = df_level1.index = pd.MultiIndex.from_arrays([df_level1.index.values,
        #                                                                            len(df_level1.index) * ['Grand Total']])
        #             # Concatenate the totals row to the original DataFrame
        #             cross_df_UNFILTERED = pd.concat([cross_df_UNFILTERED, df_level1])

        #         elif len(row_name) > 1:

        #             cross_df_UNFILTERED = subtotals_multi_actuals_new(cross_df_UNFILTERED, row_name, agg_func)

        #     cross_df_UNFILTERED = pd.concat([cross_df_UNFILTERED], keys=['Facts'], axis=1)
        #     # Create a copy of the original DataFrame
        #     df_gt = cross_df_UNFILTERED.copy()

        #     df_gt = df_gt.droplevel(0, axis=1)
        #     # Rename the level 0 column to "Grand Total"
        #     df_gt = pd.concat([df_gt], keys=['Grand Total'], axis=1)

        #     # Concatenate the original and copied DataFrames side by side
        #     cross_df_UNFILTERED = pd.concat([cross_df_UNFILTERED, df_gt], axis=1)

        # if measure_row_column_position == "measure_in_row":
        #     cross_df_UNFILTERED = cross_df_UNFILTERED.T
        # elif measure_row_column_position == "measure_in_column":
        #     pass
        # ###########################################################################
                
        # try:
        #    cross_df_UNFILTERED = cross_df_UNFILTERED[~cross_df_UNFILTERED.columns.duplicated(keep='first')]
        # except:
        #     pass

        # try:
        #     cross_df_UNFILTERED = cross_df_UNFILTERED[~cross_df_UNFILTERED.index.duplicated(keep='first')]
        # except:
        #     pass
        # cross_df_UNFILTERED.to_excel('cross_df_UNFILTERED_MAIN.xlsx')

        ################### ADDED ON 30-09-2024 - GRAND TOTAL ALL PIVOT #############
        ################### ADDED ON 30-09-2024 - GRAND TOTAL ALL PIVOT #############

        #################### DERIVED COLUMNS - 11-03-2024 ###################################
        cross_df.fillna(0,inplace=True)
        if measure_row_column_position == "measure_in_row":
            # cross_df.to_excel('cross_df_before_transpose.xlsx')
            cross_df = cross_df.T           
            cross_df = derived_MAIN_fn(cross_df,base_sales_index_colname,row_name,col_name,measure_row_column_position,cagr_power_val,brand_sales_index_value_flag='No')
            cross_df = cross_df.T
            # cross_df.to_excel('CROSS_DF_CAUCULATIONS.xlsx')
            # exit('dfddgdgdvde')

        elif measure_row_column_position == "measure_in_column":
            cross_df = derived_MAIN_fn(cross_df,base_sales_index_colname,row_name,col_name,measure_row_column_position,cagr_power_val,brand_sales_index_value_flag)

        # cross_df.to_excel('before_replace_cy_ya_with_actual_period.xlsx')
        ################## CODE TO REPLACE CY AND YA WITH ACTUAL PERIOD - 19-04-2024 ####
        cross_df = replace_cy_ya_with_actual_period(cross_df,measure_row_column_position,selected_full_period_str,comparative_full_period_str)
        # cross_df.to_excel('after_replace_cy_ya_with_actual_period.xlsx')
        # cross_df.to_excel('cross_df_derived_MAIN_fn.xlsx')
        ################## CODE TO REPLACE CY AND YA WITH ACTUAL PERIOD - 19-04-2024 ####
        last_level_values_list = cross_df.columns.get_level_values(-1).unique().tolist()

        dict_selected_measures_lst = {}

        print('selected_weight_column22 598',selected_weight_column22)
        for key in selected_weight_column22:
            dict_selected_measures_lst[key] = [item for item in last_level_values_list if item.startswith(key)]
        print('last_level_values_list',last_level_values_list)
        print('dict_selected_measures_lst',dict_selected_measures_lst)

        ##################### new code filter data 02-04-2024 #########################################
        # current_time_period_actual = selected_weight_column22[0] + '_ ' + selected_full_period_str
        # print('current_time_period_actual 645',current_time_period_actual)

        # if db_flag == 'Sellout':
        #     if (len(selected_weight_column22)==1):
        #         index_lst_cols = [0,1,3]
        #     elif (len(selected_weight_column22)==2):
        #         index_lst_cols = [0,1,3,7,8,10]

        # elif ((db_flag == 'Sale') or (db_flag == 'Door')):
        #     if (len(selected_weight_column22)==1):
        #         index_lst_cols = [0,1,3]
        #     elif (len(selected_weight_column22)>1):
        #         index_lst_cols = [0,1,3,8,10]

        ############### OLD CODE DEFAULT SELECTIONS - 23-04-2024 ########################################
        # if (measure_row_column_position == 'measure_in_column') and (len(row_name) == 1) and (("Brand" in row_name) or ("Product Name" in row_name)):
        #     print('brand condition!')
        #     if len(selected_weight_column22) == 1:
        #         index_lst_cols = [0, 1, 3]
        #     elif len(selected_weight_column22) == 2:
        #         index_lst_cols = [0, 1, 3, 9, 10, 12]
        #     elif len(selected_weight_column22) == 3:
        #         index_lst_cols = [0, 1, 3, 9, 10, 12, 18, 19, 21]
        #     elif len(selected_weight_column22) == 4:
        #         index_lst_cols = [0, 1, 3, 9, 10, 12, 18, 19, 21, 27, 28, 30]
        #     elif len(selected_weight_column22) == 5:
        #         index_lst_cols = [0, 1, 3, 9, 10, 12, 18, 19, 21, 27, 28, 30, 36, 37, 39]
        # else:
        #     ##############################################################
        #     print('not condtiontion')
        #     if len(selected_weight_column22) == 1:
        #         index_lst_cols = [0, 1, 3]
        #     elif len(selected_weight_column22) == 2:
        #         index_lst_cols = [0, 1, 3, 8, 9, 11]
        #     elif len(selected_weight_column22) == 3:
        #         index_lst_cols = [0, 1, 3, 8, 9, 11, 16, 17, 19]
        #     elif len(selected_weight_column22) == 4:
        #         index_lst_cols = [0, 1, 3, 8, 9, 11, 16, 17, 19,24,25,27]
        #     elif len(selected_weight_column22) == 5:
        #         index_lst_cols = [0, 1, 3, 8, 9, 11, 16, 17, 19,24,25,27,32,33,35]
        ############### OLD CODE DEFAULT SELECTIONS - 23-04-2024 ########################################

        ############# REMOVED RANK - 23-09-2024 ############################################################
        if (measure_row_column_position == 'measure_in_column') and (len(row_name) == 1) and (("Brand" in row_name) or ("Product Name" in row_name)):
            print('brand condition!')
            if len(selected_weight_column22) == 1:
                index_lst_cols = [1, 3]
            elif len(selected_weight_column22) == 2:
                index_lst_cols = [1, 3, 10, 12]
            elif len(selected_weight_column22) == 3:
                index_lst_cols = [1, 3, 10, 12, 19, 21]
            elif len(selected_weight_column22) == 4:
                index_lst_cols = [1, 3, 10, 12, 19, 21, 28, 30]
            elif len(selected_weight_column22) == 5:
                index_lst_cols = [1, 3, 10, 12, 19, 21, 28, 30, 37, 39]
        else:
    ##############################################################
            print('not condtiontion')
            if len(selected_weight_column22) == 1:
                index_lst_cols = [1, 3]
            elif len(selected_weight_column22) == 2:
                index_lst_cols = [1, 3, 9, 11]
            elif len(selected_weight_column22) == 3:
                index_lst_cols = [1, 3, 9, 11, 17, 19]
            elif len(selected_weight_column22) == 4:
                index_lst_cols = [1, 3, 9, 11, 17, 19, 25, 27]
            elif len(selected_weight_column22) == 5:
                index_lst_cols = [1, 3, 9, 11, 17, 19, 25, 27, 33, 35]
        ############# REMOVED RANK - 23-09-2024 ############################################################

        sublist = [last_level_values_list[i] for i in index_lst_cols]

        cross_df = cross_df.loc[:, cross_df.columns.get_level_values(-1).isin(list(sublist))]

        dict_selected_measures_filtered_lst = {}
        for key in selected_weight_column22:
            dict_selected_measures_filtered_lst[key] = [item for item in sublist if item.startswith(key)]
        print('dict_selected_measures_filtered_lst===',dict_selected_measures_filtered_lst)

        if (any('Sales (LC)' in item for item in selected_weight_column_all)):
            dict_selected_measures_lst = dict_selected_measures_filtered_lst
        #################### DERIVED COLUMNS - 11-03-2024 ###################################

        period_to_be_replaced_str = [selected_full_period_str][0].split()[0]
        ##### CODE TO REPLACE QUARTER - 19-04-2024 ###########################
        if period_to_be_replaced_str =='QUARTER':

            if measure_row_column_position == "measure_in_column":
                try:
                    cross_df.rename(columns=lambda x: re.sub('QUARTER','', x), inplace=True)
                except:
                    pass
            if measure_row_column_position == "measure_in_row":
                try:
                    cross_df.rename(index=lambda x: re.sub('QUARTER','', x), inplace=True)
                except:
                    pass

        #################### REPLACE SALES - 09-05-2024 ####################
        # selected_weight_column22_STR = selected_weight_column22[0]
        # dict_selected_measures_filtered_lst

        # old_string = selected_weight_column22_STR
        # new_string = 'Sales'

        # # Replace old string with new string in the entire dictionary
        # dict_selected_measures_filtered_lst = replace_string_in_dict(dict_selected_measures_filtered_lst, old_string, new_string)

        # print('dict_selected_measures_filtered_lst 716',dict_selected_measures_filtered_lst)

        # dict_selected_measures_lst = replace_string_in_dict(dict_selected_measures_lst, old_string, new_string)

        # print('dict_selected_measures_lst 555',dict_selected_measures_lst)
        #################### REPLACE SALES - 09-05-2024 ####################




        ##### CODE TO REPLACE QUARTER - 19-04-2024 ###########################

        ################################################################################################################
        # if (seperated_flag_row == 0 and seperated_flag_col == 0):
        # # if (len(row_name) == 1 and len(col_name) == 1):

        #     cross_df = cross_df.reindex(sorted(cross_df.index), axis=0)
        #     cross_df = cross_df.reindex(sorted(cross_df.columns), axis=1)
        ################################################################################################################

        #### CODE TO DROP GRAND TOTAL WHEN SALES LC  IS SELECTED - 18-04-2024 ####
        # if (any('Sales (LC)' in item for item in selected_weight_column_all)):
        #     if measure_row_column_position == "measure_in_column":
        #         if ('Country' in row_name):
        #             print('seeeeerrr')

        #             try:
        #                 # Identify columns that contain "Grand Total" in any level
        #                 grand_total_index = [col for col in cross_df.index if any('Grand Total' in level for level in col)]

        #                 # Drop the identified columns
        #                 cross_df = cross_df.drop(index=grand_total_index)
        #             except Exception as e:
        #                 print("An error occurred:", e)
                    
        #             # try:
        #             #     for level in cross_df.index.levels:
        #             #         if 'Grand Total' in level:
        #             #             print('grand total in rows found!')
        #             #             print('level rows ',level)
        #             #             cross_df = cross_df.drop('Grand Total', axis=0, level=level.name)
        #             # except:
        #             #     pass

        #         elif ('Country' in col_name):
        #             try:
        #                 # Identify columns that contain "Grand Total" in any level
        #                 grand_total_columns = [col for col in cross_df.columns if any('Grand Total' in level for level in col)]

        #                 # Drop the identified columns
        #                 cross_df = cross_df.drop(columns=grand_total_columns)
        #             except Exception as e:
        #                 print("An error occurred:", e)

                    # try:
                    #     for level in cross_df.columns.levels:
                    #         if 'Grand Total' in level:
                    #             print('grand total found in columns!')
                    #             print('level columns ',level)
                    #             cross_df = cross_df.drop('Grand Total', axis=1, level=level.name)
                    # except:
                    #     pass

        #     elif measure_row_column_position == "measure_in_row":
        #         try:
        #             for level in cross_df.columns.levels:
        #                 if 'Grand Total' in level:
        #                     cross_df = cross_df.drop('Grand Total', axis=1, level=level.name)
        #         except:
        #             pass

        #### CODE TO DROP GRAND TOTAL WHEN SALES LC  IS SELECTED - 18-04-2024 ####

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

        ###################### code to remove prefix } - 22-04-2024 ###############################
        if ((category_var_name in row_name) or (category_var_name in col_name)) or ((channel_var_name in row_name) or (channel_var_name in col_name)) or ((brand_var_name in row_name) or (brand_var_name in col_name)):
            try:
                cross_df = remove_prefix(cross_df)
            except:
                pass
        ###################### code to remove prefix } - 22-04-2024 ###############################

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
        # cross_df.to_excel('NULL_CROSSDF.xlsx')
        ############# SUMMARY OF CROSSTAB DATA ##############################
        # crosstab_summary = cross_df.describe()
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
        # cross_df.to_excel('FINAL_CROSSTABB.xlsx')
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
                "dict_selected_measures_filtered_lst": dict_selected_measures_filtered_lst,
                # "base_column_names_indices_resp": base_column_names_indices_resp,
                "filter_dict_resp":filter_dict_resp,
                "all_categories_vals":all_categories_vals,
                "time_period_flag": time_period_flag,
                "time_period_vals": time_period_vals,
                "time_period_filter_val_resp": 'time_period_filter_val_resp',
                # "df_cross_json_test": df_cross_json21,
                "error": "Correct Data",
                "seperated_flag_col":seperated_flag_col,
                "current_time_period_resp":selected_full_period_str,
                "comparative_time_period_resp":comparative_full_period_str,
                "measure_type":measure_row_column_position,
                "display_table":'No',
                # "unique_base_index_brand_product_resp":unique_base_index_brand_product_resp,
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

        table_sort_flag = request.POST.get('table_sort_flag')
        column_name_sort_table = request.POST.get('column_name_sort_table')
        column_name_sort_table_lst = ast.literal_eval(column_name_sort_table)
        print('column_name_sort_table_lst',column_name_sort_table_lst)

        final_row_col_array_grp = request.POST.get('final_row_col_array_grp')
        print('final_row_col_array_grp typee==',type(final_row_col_array_grp))
        print('final_row_col_array_grp dataa',final_row_col_array_grp)
        final_row_col_array_grp_json = json.loads(final_row_col_array_grp)
        print('909==final_row_col_array_grp_json',final_row_col_array_grp_json)
        dict_base_filter_data_resp = request.POST.get('filter_data')
        print('dict_base_filter_data_resp typee==',type(dict_base_filter_data_resp))
        print('dict_base_filter_data_resp dataa==',dict_base_filter_data_resp)

        facts_object_index_resp11 = request.POST.get('facts_object_index')
        facts_object_index_resp = json.loads(facts_object_index_resp11)
        print('facts_object_index_resp',facts_object_index_resp)
        print('facts_object_index_resp type',type(facts_object_index_resp))

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

        selected_full_period = [request.POST.get('Time_val')]
        comparative_full_period =[request.POST.get('comparative_time_period')]


        seperator_param =request.POST.get('currency_type')
        print('seperator_param 1254',seperator_param)
        # exit('seperator_param')
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

        ######################## 04-06-2024 - BLANK COLNAME ####################
        if col_name == [''] or col_name == ['undefined']:
            col_name = []
        else:
            col_name = col_name 

        if row_name == [''] or row_name == ['undefined']:
            row_name = []
        else:
            row_name = row_name 
        ######################## 04-06-2024 - BLANK COLNAME ####################

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

        display_grand_total_flag = request.POST.get('display_grand_total_flag')
        # if (display_grand_total_flag == 'gt_all') and ((len(col_name)==0 and len(row_name)==1) or (len(col_name)==1 and len(row_name)==1)):
        #     grand_total_LOGIC_Status = 'Yes'
        # else:
        #     grand_total_LOGIC_Status = 'No'
        # display_grand_total_flag = 'gt_all'
        # display_grand_total_flag = 'gt_among_filtered'

        # base_sales_index_colname = 'Shiseido'
        # base_sales_index_colname = '1996 EDP'

        ####################### ASCENDING-DESCENDING SORTING - 05-06-2024 #####################
        # if len(column_name_sort_table_lst) == 2:
        #     column_to_sort = (column_name_sort_table_lst[0],column_name_sort_table_lst[1])

        # elif len(column_name_sort_table_lst) == 3:
        #     column_to_sort = (column_name_sort_table_lst[0],column_name_sort_table_lst[1],column_name_sort_table_lst[2])

        # elif len(column_name_sort_table_lst) == 4:
        #     column_to_sort = (column_name_sort_table_lst[0],column_name_sort_table_lst[1],column_name_sort_table_lst[2],column_name_sort_table_lst[3])
        column_to_sort = tuple(column_name_sort_table_lst)
        print('column_to_sort 1333333',column_to_sort)

        # exit('column_to_sort')
        # column_to_sort = ('Facts','Sales (M JPY)_ Q1 2024')

        if table_sort_flag == 'asc_sort':
            asc_desc_param = True
        elif table_sort_flag == 'desc_sort':
            asc_desc_param = False
        elif table_sort_flag == 'no_sort':
            asc_desc_param = 'no_sort'
        ####################### ASCENDING-DESCENDING SORTING - 05-06-2024 #####################

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

        try:
            dict_base_filter_data = ensure_list(dict_base_filter_data)
        except:
            pass

        # Dictionary comprehension to replace keys
        try:
            dict_base_filter_data = {k.replace('&amp;', '&'): v for k, v in dict_base_filter_data.items()}
            # dict_base_filter_data = {('B&M Channel Split' if k == 'B&amp;M Channel Split' else k): v for k, v in dict_base_filter_data.items()}
        except:
            pass
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
        filename = list(dict_table.keys())[0] + ".csv"
        # df = pd.read_csv(settings.TEMP_UPLOAD + filename)
        ##############################################################################
        db_flag = list(dict_table.keys())[0].split('_', 1)[0]
        print('dfff 12222 db_flag',db_flag)
        filename = list(dict_table.keys())[0] + ".csv"
        # Open the file in binary mode and detect the encoding
        # with open(settings.TEMP_UPLOAD + filename, 'rb') as f:
        #     result = chardet.detect(f.read(100000))  # Read the first 100000 bytes
        #     detected_encoding = result['encoding']

        # print(f"Detected encoding: {detected_encoding}")

        # Read the CSV file using the detected encoding
        df = pd.read_csv(settings.TEMP_UPLOAD + filename,low_memory=False,engine='c')
        # Remove leading and trailing spaces from all categorical columns
        df[df.select_dtypes(include=['object']).columns] = df.select_dtypes(include=['object']).apply(lambda x: x.str.strip())
        ##############################################################################
        # df = pl.read_excel(settings.TEMP_UPLOAD + filename)
        # df = df.to_pandas()
        print('df colss before reading==',df.columns)
        df = df.rename(columns=rename_input_cols_dict)
        print('df colss after reading==',df.columns)

        end_time_read = time.time()
        print("Time taken to read file using pandas was ", end_time_read - start_time_read, "seconds!")

        ################# ADDED ON 10-06-2024 ######################################

        print('colsSS',df.columns)
        print('selected_weight_column22 1809==',selected_weight_column22)

        # if seperator_param == "thousands":
        #     df.rename(columns={col: col.replace('Sales (M', 'Sales (K') for col in df.columns}, inplace=True)
        #     selected_weight_column22 = [col.replace('Sales (M', 'Sales (K') for col in selected_weight_column22]
        #     facts_object_index_resp = {key.replace("Sales (M", "Sales (K"): value for key, value in facts_object_index_resp.items()}
        #     print('facts_object_index_resp 1471',facts_object_index_resp)

        if (seperator_param == "millions") and (any("Sales (K" in col for col in selected_weight_column22)):
            print('condition 1 1477')
            sales_columns = [col for col in selected_weight_column22 if 'Sales (K' in col]
            sales_columns = [col.replace('K', 'M') for col in sales_columns if 'Sales (K' in col]
            selected_weight_column22 = [col.replace('Sales (K', 'Sales (M') for col in selected_weight_column22]
            df.rename(columns={col: col.replace('Sales (K', 'Sales (M') for col in df.columns}, inplace=True)
            facts_object_index_resp = {key.replace("Sales (K", "Sales (M"): value for key, value in facts_object_index_resp.items()}

        elif (seperator_param == "thousands"):
        # elif (seperator_param == "thousands") and (any("Sales (M" in col for col in selected_weight_column22)):
            sales_columns = [col for col in selected_weight_column22 if 'Sales (M' in col]
            sales_columns = [col.replace('M', 'K') for col in sales_columns if 'Sales (M' in col]
            selected_weight_column22 = [col.replace('Sales (M', 'Sales (K') for col in selected_weight_column22]
            df.rename(columns={col: col.replace('Sales (M', 'Sales (K') for col in df.columns}, inplace=True)
            facts_object_index_resp = {key.replace("Sales (M", "Sales (K"): value for key, value in facts_object_index_resp.items()}

        sales_columns = [col for col in selected_weight_column22 if 'Sales' in col]

        if seperator_param == "thousands":

            for loop_col in sales_columns:
                df[loop_col] = df[loop_col] * 1000

        ################# ADDED ON 10-06-2024 ########################################

        ##################################### POLARS #####################################

        ######## Added By Mihir Pawar 24-04-2023 - READ FILE LOGIC FOR CROSSTAB FUNCTION 2 ONLY ###############################################

        ############## ADDED BY MIHIR PAWAR - 30-08-2023 - DERIVED COUMNS ###
        # time_derived_start = time.time()

        # replace_values = {-np.inf: 0, np.inf: 0, 'null': 0, np.nan: 0}
        # df.replace(replace_values, inplace=True)

        # # df.to_excel('df_SALES_FINAL.xlsx')

        # time_derived_end = time.time()
        # print("DERIVED FN TIME",time_derived_end - time_derived_start,"SECONDS!")
        ############## ADDED BY MIHIR PAWAR - 30-08-2023 - DERIVED COUMNS ###

        ####################################################################################
        filter_dict_resp = base_filter_resp(df,dict_table,row_name,col_name)
        filter_dict_resp = remove_duplicate_keys_and_values(filter_dict_resp)

        # Function to replace NaN with "Not Available"
        # def replace_nan(d):
        #     for key, value in d.items():
        #         if isinstance(value, dict):
        #             replace_nan(value)  # Recur for nested dictionaries
        #         elif isinstance(value, list):
        #             d[key] = [v if not pd.isna(v) else "Not Available" for v in value]
        #         elif pd.isna(value):
        #             d[key] = "Not Available"
        #     return d

        def replace_nan(d):
            # Predefine the "Not Available" value once to avoid redundant creation
            na_value = "Not Available"

            for key, value in d.items():
                if isinstance(value, dict):
                    # Use recursion for nested dictionaries
                    d[key] = replace_nan(value)
                elif isinstance(value, list):
                    # List comprehension avoids multiple function calls to pd.isna()
                    d[key] = [v if not pd.isna(v) else na_value for v in value]
                elif pd.isna(value):
                    d[key] = na_value

            return d


        # Replace NaN values in the dictionary
        filter_dict_resp = replace_nan(filter_dict_resp)
        #####################################################################################
        ######################## CODE TO TRANSFORM THE DATA 08-04-2024 ##################
        print('1850 colnamesss',df.columns)

        if (db_flag != 'Doors') or ((db_flag == 'Doors') and ('Door' not in selected_weight_column22)):
            df,selected_full_period_str,comparative_full_period_str = data_transformation(df,selected_weight_column22,selected_full_period,comparative_full_period)
        elif ((db_flag == 'Doors') and ('Door' in selected_weight_column22)):
            df,selected_full_period_str,comparative_full_period_str = data_transformation_doors(filename,selected_weight_column22,selected_full_period,comparative_full_period,seperator_param)
        # df.to_excel('data_transformed.xlsx')
        print('selected_full_period_str 1158',selected_full_period_str)
        print('comparative_full_period 11590',comparative_full_period)
        column_list = list(df.columns)

        selected_weight_column_all = [column_name for column_name in column_list if any(substring in column_name for substring in selected_weight_column22)]

        ###########################################################################################

        ####################### added on 24-06-2024 #################################################
        # if ("Brand" in row_name) and (len(row_name)==1) and (measure_row_column_position == 'measure_in_column'):
        #     df['Brand sales index'] = 'Shiseido'
        print('base_filter_col_lst 1669',base_filter_col_lst)
        # if 'Brand sales index' in base_filter_col_lst:

        # if 'Brand sales index' in base_filter_col_lst and ("Brand" in row_name) and len(row_name)!=1:

        if 'Brand sales index' in base_filter_col_lst:
            val_selected_brand_sales = dict_base_filter_data['Brand sales index']
            print('val_selected_brand_sales 1917',val_selected_brand_sales)
            dict_base_filter_data["Brand sales index"] = val_selected_brand_sales
            df['Brand sales index'] = val_selected_brand_sales[0]

            base_sales_index_colname = val_selected_brand_sales[0]
        else:
            base_sales_index_colname = ''
        # elif (len(base_filter_col_lst)==0) and ((measure_row_column_position == 'measure_in_column') and (len(row_name) == 1) and (("Brand" in row_name) or ("Product Name" in row_name))):
        #     base_sales_index_colname = 'Shiseido'
            # print('1671!')

        print('dict_base_filter_data 1924',dict_base_filter_data)
        # df.to_csv('dict_base_filter_data 1924.csv')
        #################### NEW CODE TO EMPTY DF IF BRAND SALES INDEX AND SELECTED BRANDS ARE NOT MATCHING ###############
        # if 'Brand' not in base_filter_col_lst and 'Brand sales index' in base_filter_col_lst:

        if ((measure_row_column_position == 'measure_in_column') and (len(row_name) == 1) and ((brand_var_name in row_name) or ("Product Name" in row_name))) and ('Brand sales index' in base_filter_col_lst) and ('Brand' in base_filter_col_lst):
            # dict_base_filter_data2 = dict_base_filter_data.copy()
            val_selected_brand_sales = dict_base_filter_data['Brand sales index']
            val_selected_brand_sales = val_selected_brand_sales[0]
            print('val_selected_brand_sales 1932',val_selected_brand_sales)
            if val_selected_brand_sales not in dict_base_filter_data["Brand"]:
                print('1934 if condition')
                dict_base_filter_data["Brand"].append(val_selected_brand_sales)
                brand_sales_index_value_flag = 'No'
            else:
                brand_sales_index_value_flag = 'Yes'
        else:
            # brand_sales_index_value_flag = 'No'
            brand_sales_index_value_flag = 'Yes'
        #################### NEW CODE TO EMPTY DF IF BRAND SALES INDEX AND SELECTED BRANDS ARE NOT MATCHING ###############
        # filter_dict_resp = base_filter_resp(df,dict_table,row_name,col_name)
        # filter_dict_resp = remove_duplicate_keys_and_values(filter_dict_resp)
        print('filter_dict_resp 1902',filter_dict_resp)
        all_categories_vals = base_filter_resp_all(df,dict_table,row_name,col_name)
        # print('all_categories_vals 1904',all_categories_vals)

        ########################## ADDED ON 09-10-2024 - REMOVE ROW/COLUMN FROM UNFILTERED_DF FOR GRAND TOTAL #############################################
        df_UNFILTERED = df.copy()
        print('dict_base_filter_data 2197=',dict_base_filter_data)

        df = base_filter_data(df,dict_base_filter_data)
        # df.to_csv('df_after_filtered.csv')
        filtered_dict_base_filter_data = dict_base_filter_data.copy()
        if measure_row_column_position == 'measure_in_column':
            for key in row_name:
                filtered_dict_base_filter_data.pop(key, None)
        elif measure_row_column_position == 'measure_in_row':
            if (len(row_name) == 1 and len(col_name) == 0):
                for key in row_name:
                    filtered_dict_base_filter_data.pop(key, None)
            elif (len(row_name) == 1 and len(col_name) == 1):
                for key in col_name:
                    filtered_dict_base_filter_data.pop(key, None)

        print('filtered_dict_base_filter_data 2215==',filtered_dict_base_filter_data)
        print('dict_base_filter_data==',dict_base_filter_data)
        try:
            df_UNFILTERED = base_filter_data(df_UNFILTERED,filtered_dict_base_filter_data)
        except:
            pass
        # df_UNFILTERED.to_csv('df_UNFILTERED_after_filtered.csv')
        ########################## ADDED ON 09-10-2024 - REMOVE ROW/COLUMN FROM UNFILTERED_DF FOR GRAND TOTAL #############################################

        ######## CODE TO BRING BRAND AT FIRST POSITION IF PRESENT IN FILTER RESPONSE ####
        keys_to_check = ['Brand', 'Brand sales index']
        dicts_to_update = [(filter_dict_resp, 'filter_dict_resp'), (dict_base_filter_data, 'dict_base_filter_data')]        
        dicts_to_update = [(all_categories_vals, 'all_categories_vals'), (dict_base_filter_data, 'dict_base_filter_data')]
        # dicts_to_update = [(filter_dict_resp, 'filter_dict_resp'), (dict_base_filter_data, 'dict_base_filter_data')]

        for key in keys_to_check:
            for d, name in dicts_to_update:
                if key in d:
                    d = bring_key_to_first(d, key)
        # if 'Brand' in filter_dict_resp:
        #     filter_dict_resp = bring_key_to_first(filter_dict_resp, 'Brand')

        # if 'Brand' in dict_base_filter_data:
        #     dict_base_filter_data = bring_key_to_first(dict_base_filter_data, 'Brand')

        # if 'Brand sales index' in filter_dict_resp:
        #     filter_dict_resp = bring_key_to_first(filter_dict_resp, 'Brand sales index')

        # if 'Brand sales index' in dict_base_filter_data:
        #     dict_base_filter_data = bring_key_to_first(dict_base_filter_data, 'Brand sales index')
        ######## CODE TO BRING BRAND AT FIRST POSITION IF PRESENT IN FILTER RESPONSE ####

        ############### CODE TO ORDER CATEGORIES - 22-04-2024 #########################################
        if (category_var_name in row_name) or (category_var_name in col_name):
            mapping_category_dict = {'Skincare':'01}Skincare','Make-up':'02}Make-up','Fragrance':'03}Fragrance'}
            df[category_var_name] = df[category_var_name].replace(mapping_category_dict)
            df_UNFILTERED[category_var_name] = df_UNFILTERED[category_var_name].replace(mapping_category_dict)
        ############### CODE TO ORDER CATEGORIES - 22-04-2024 #########################################

        ############### CODE TO ORDER CHANNEL - 26-04-2024 ##############################
        if (channel_var_name in row_name) or (channel_var_name in col_name):
            mapping_channel_dict = {'Department Stores':'01}Department Stores','E-Commerce':'02}E-Commerce','Specialty Stores':'03}Specialty Stores','Standalone Boutiques':'04}Standalone Boutiques'}
            df[channel_var_name] = df[channel_var_name].replace(mapping_channel_dict)
            df_UNFILTERED[channel_var_name] = df_UNFILTERED[channel_var_name].replace(mapping_channel_dict)
        ############### CODE TO ORDER CHANNEL - 26-04-2024 #########################################

        ############### CODE TO ORDER Brand - 26-04-2024 ###########################
        # if (brand_var_name in row_name) or (brand_var_name in col_name):
        #     mapping_brand_dict = {'(Other panel)':'~}(Other panel)'}
        #     df[brand_var_name] = df[brand_var_name].replace(mapping_brand_dict)
        #     df_UNFILTERED[brand_var_name] = df_UNFILTERED[brand_var_name].replace(mapping_brand_dict)
        ############### CODE TO ORDER Brand - 26-04-2024 ###########################

        ############ logic for CAGR - 29-08-2024 #################
        Current_yr = int(selected_full_period[0].split()[-1])
        Previous_yr = int(comparative_full_period[0].split()[-1])

        selected_time_range = selected_full_period[0].split()[0]

        if selected_time_range == 'FY':
            print('if condition cagr')
            cagr_power_val = Current_yr - Previous_yr
            
        else:
            cagr_power_val = 989898
        # exit('selected_full_period_str')
        ############ logic for CAGR - 29-08-2024 #################


        # #################### NEW CODE TO EMPTY DF IF BRAND SALES INDEX AND SELECTED BRANDS ARE NOT MATCHING ###############
        # if 'Brand sales index' in base_filter_col_lst:
        #     val_selected_brand_sales = dict_base_filter_data['Brand sales index']
        #     val_selected_brand_sales = val_selected_brand_sales[0]
        #     print('val_selected_brand_sales 1932',val_selected_brand_sales)
        #     if val_selected_brand_sales not in dict_base_filter_data["Brand"]:
        #         print('1934 if condition')
        #         df = pd.DataFrame()
        # #################### NEW CODE TO EMPTY DF IF BRAND SALES INDEX AND SELECTED BRANDS ARE NOT MATCHING ###############

        if len(df) > 0:
            ################ ADDED BY MIHIR PAWAR - 04-08-2023 - TIME FILTER ##################
            time_period_vals = df['Time'].unique().tolist() #distinct/unique of time periods

            time_period_filter_val = [time_period_vals[0]]
            time_period_filter_val_resp = {'selected_time_period':time_period_filter_val}
            
            ################ ADDED BY MIHIR PAWAR - 04-08-2023 - TIME FILTER ##################

            ######################## CODE TO TRANSFORM THE DATA 08-04-2024 ################

        ######################## NEW LOGIC PIVOT 11-03-2024 ############################
        #####################################################################################
        #####################################################################################
        #####################################################################################
            if (len(row_name) > 0) and (len(col_name) > 0):
                no_row_col_flag = 'row_col_present'
            else:
                no_row_col_flag = 'no_row_col_present'

            if no_row_col_flag == 'row_col_present':
                if measure_row_column_position == "measure_in_row":

                    cross_df = sales_crosstab_logic_MAIN(selected_weight_column_all, dict_table, df, percent_calc, col_name, row_name,
                                              data_type_resp,seperated_flag_col,
                                              seperated_flag_row, totals_nested_flag,agg_func,measure_row_column_position)

                    total_levels = cross_df.columns.nlevels
                    print('total_levels',total_levels)

                    if total_levels == 2:
                        cross_df = cross_df.swaplevel(0, 1, axis=1).sort_index(axis=1)

                    elif total_levels == 3:
                        cross_df = cross_df.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, total_levels - 1, axis=1).sort_index(axis=1)

                    elif total_levels == 4:
                        cross_df = cross_df.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, 3, axis=1).swaplevel(3, total_levels - 1, axis=1).sort_index(axis=1)

                    # cross_df = cross_df.T

                elif measure_row_column_position == "measure_in_column":

                    cross_df = sales_crosstab_logic_MAIN(selected_weight_column_all, dict_table, df, percent_calc, row_name, col_name,
                                              data_type_resp,
                                              seperated_flag_row, seperated_flag_col, totals_nested_flag,agg_func,measure_row_column_position)

                    total_levels = cross_df.columns.nlevels
                    print('total_levels',total_levels)

                    if total_levels == 2:
                        cross_df = cross_df.swaplevel(0, 1, axis=1).sort_index(axis=1)

                    elif total_levels == 3:
                        cross_df = cross_df.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, total_levels - 1, axis=1).sort_index(axis=1)

                    elif total_levels == 4:
                        cross_df = cross_df.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, 3, axis=1).swaplevel(3, total_levels - 1, axis=1).sort_index(axis=1)

            ###########################################################################
            elif no_row_col_flag == 'no_row_col_present':
                print('row_name 1528',row_name)
                print('row_name 13333',col_name)
                print('measrrrr',measure_row_column_position)
                cross_df = single_dimension_logic(df,row_name,col_name,seperated_flag_row,selected_weight_column_all,agg_func)

            if measure_row_column_position == "measure_in_row":
                cross_df = cross_df.T
            elif measure_row_column_position == "measure_in_column":
                pass
            ###########################################################################
                    
            try:
               cross_df = cross_df[~cross_df.columns.duplicated(keep='first')]
            except:
                pass

            try:
                cross_df = cross_df[~cross_df.index.duplicated(keep='first')]
            except:
                pass
            # 
            # cross_df.to_excel('cross_df_MAIN.xlsx')
            ############ RENAMING GRAND TOTAL TO TOTALS (AMONSGT DISPLAYED) - 04102024 ####
            ############ RENAMING GRAND TOTAL TO TOTALS (AMONSGT DISPLAYED) - 04102024 ####
            # Dynamic replacement in the last level of the MultiIndex
            # cross_df.to_excel('cross_df_MAIN.xlsx')

            if (display_grand_total_flag == 'gt_all') and ((len(col_name)==0 and len(row_name)==1) or (len(col_name)==1 and len(row_name)==1)):
                print('2362=====')
                if measure_row_column_position == 'measure_in_column':
                    filtered_df_gt = cross_df[cross_df.index.get_level_values(1) == 'Grand Total']
                    last_level_index = filtered_df_gt.index.get_level_values(-1)  # Get the last level
                    new_last_level_index = last_level_index.map(lambda x: 'Total (Among Displayed)' if x == 'Grand Total' else x)

                    # Set the new MultiIndex with the modified last level
                    # filtered_df_gt.index = filtered_df_gt.index.set_levels(new_last_level_index, level=-1)
                    # Reconstruct the MultiIndex with the modified last level
                    filtered_df_gt.index = pd.MultiIndex.from_tuples(
                        [(filtered_df_gt.index[i][0], new_last_level_index[i]) for i in range(len(filtered_df_gt.index))]
                    )

                    cross_df = cross_df[~cross_df.index.get_level_values(1).isin(['Grand Total'])]
                    cross_df = pd.concat([cross_df,filtered_df_gt],axis=0)
                    # cross_df.to_excel('cross_df_MAIN_gt_changed.xlsx')

                elif measure_row_column_position == 'measure_in_row':
                     # Filter the DataFrame for 'Grand Total' in the columns
                    filtered_df_gt = cross_df.loc[:, cross_df.columns.get_level_values(1) == 'Grand Total']
                    
                    # Get the last level of the columns
                    last_level_columns = filtered_df_gt.columns.get_level_values(-1)
                    
                    # Create a new list for the last level columns
                    new_last_level_columns = [
                        'Total (Among Displayed)' if col == 'Grand Total' else col
                        for col in last_level_columns
                    ]
                    
                    # Reconstruct the columns MultiIndex with the modified last level
                    filtered_df_gt.columns = pd.MultiIndex.from_tuples(
                        [(filtered_df_gt.columns[i][0], new_last_level_columns[i]) for i in range(len(filtered_df_gt.columns))]
                    )
                
                    # Remove original 'Grand Total' columns from cross_df
                    cross_df = cross_df.loc[:, ~cross_df.columns.get_level_values(1).isin(['Grand Total'])]
                    
                    # Concatenate the modified columns back into cross_df
                    cross_df = pd.concat([cross_df, filtered_df_gt], axis=1)
                    
                    # Save the updated DataFrame to an Excel file
                    # cross_df.to_excel('cross_df_MAIN_gt_changed.xlsx')
            else:
                cross_df = cross_df.copy()

            # cross_df.to_excel('cross_df_MAIN_gt_renamed.xlsx')
            ############ RENAMING GRAND TOTAL TO TOTALS (AMONSGT DISPLAYED) - 04102024 ####
            ############ RENAMING GRAND TOTAL TO TOTALS (AMONSGT DISPLAYED) - 04102024 ####

            ################### ADDED ON 30-09-2024 - GRAND TOTAL ALL PIVOT #############
            ################### ADDED ON 30-09-2024 - GRAND TOTAL ALL PIVOT #############
            if (len(row_name) > 0) and (len(col_name) > 0):
                no_row_col_flag = 'row_col_present'
            else:
                no_row_col_flag = 'no_row_col_present'

            if no_row_col_flag == 'row_col_present':
                if measure_row_column_position == "measure_in_row":

                    cross_df_UNFILTERED = sales_crosstab_logic_MAIN(selected_weight_column_all, dict_table,df_UNFILTERED, percent_calc, col_name, row_name,
                                              data_type_resp,seperated_flag_col,
                                              seperated_flag_row, totals_nested_flag,agg_func,measure_row_column_position)

                    total_levels = cross_df_UNFILTERED.columns.nlevels
                    print('total_levels',total_levels)

                    if total_levels == 2:
                        cross_df_UNFILTERED = cross_df_UNFILTERED.swaplevel(0, 1, axis=1).sort_index(axis=1)

                    elif total_levels == 3:
                        cross_df_UNFILTERED = cross_df_UNFILTERED.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, total_levels - 1, axis=1).sort_index(axis=1)

                    elif total_levels == 4:
                        cross_df_UNFILTERED = cross_df_UNFILTERED.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, 3, axis=1).swaplevel(3, total_levels - 1, axis=1).sort_index(axis=1)

                    # cross_df = cross_df.T

                elif measure_row_column_position == "measure_in_column":

                    cross_df_UNFILTERED = sales_crosstab_logic_MAIN(selected_weight_column_all, dict_table, df_UNFILTERED, percent_calc, row_name, col_name,
                                              data_type_resp,
                                              seperated_flag_row, seperated_flag_col, totals_nested_flag,agg_func,measure_row_column_position)

                    total_levels = cross_df_UNFILTERED.columns.nlevels
                    print('total_levels',total_levels)

                    if total_levels == 2:
                        cross_df_UNFILTERED = cross_df_UNFILTERED.swaplevel(0, 1, axis=1).sort_index(axis=1)

                    elif total_levels == 3:
                        cross_df_UNFILTERED = cross_df_UNFILTERED.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, total_levels - 1, axis=1).sort_index(axis=1)

                    elif total_levels == 4:
                        cross_df_UNFILTERED = cross_df_UNFILTERED.swaplevel(0, 1, axis=1).swaplevel(1, 2, axis=1).swaplevel(2, 3, axis=1).swaplevel(3, total_levels - 1, axis=1).sort_index(axis=1)

            ###########################################################################
            elif no_row_col_flag == 'no_row_col_present':
                print('row_name 1528',row_name)
                print('row_name 13333',col_name)
                print('measrrrr',measure_row_column_position)
                cross_df_UNFILTERED = single_dimension_logic(df_UNFILTERED,row_name,col_name,seperated_flag_row,selected_weight_column_all,agg_func)

            if measure_row_column_position == "measure_in_row":
                cross_df_UNFILTERED = cross_df_UNFILTERED.T
            elif measure_row_column_position == "measure_in_column":
                pass
            ###########################################################################
                    
            try:
               cross_df_UNFILTERED = cross_df_UNFILTERED[~cross_df_UNFILTERED.columns.duplicated(keep='first')]
            except:
                pass

            try:
                cross_df_UNFILTERED = cross_df_UNFILTERED[~cross_df_UNFILTERED.index.duplicated(keep='first')]
            except:
                pass
            # cross_df_UNFILTERED.to_excel('cross_df_UNFILTERED_MAIN.xlsx')
            ################### ADDED ON 30-09-2024 - GRAND TOTAL ALL PIVOT #############
            ################### ADDED ON 30-09-2024 - GRAND TOTAL ALL PIVOT #############

            ############ ADD UNFILTERED Grand Total to rows - 04102024 ########################
            ############ ADD UNFILTERED Grand Total to rows - 04102024 ########################
            # if (len(col_name)==1) and ((len(row_name)==0) or (len(row_name)==1)) and (display_grand_total_flag == 'gt_all'):
            if (display_grand_total_flag == 'gt_all') and ((len(col_name)==0 and len(row_name)==1) or (len(col_name)==1 and len(row_name)==1)):
                print('2486=====')
                if measure_row_column_position == 'measure_in_column':
                    filtered_cross_df_UNFILTERED_gt = cross_df_UNFILTERED[cross_df_UNFILTERED.index.get_level_values(1) == 'Grand Total']
                    cross_df = pd.concat([cross_df,filtered_cross_df_UNFILTERED_gt],axis=0)
                    # cross_df.to_excel('cross_df_MAIN_FINAL_ABS.xlsx')
                elif measure_row_column_position == 'measure_in_row':
                    #Filter the DataFrame for columns where the second level is 'Grand Total'
                    filtered_cross_df_UNFILTERED_gt = cross_df_UNFILTERED.loc[:, cross_df_UNFILTERED.columns.get_level_values(1) == 'Grand Total']

                    # Concatenate the filtered columns back into cross_df
                    cross_df = pd.concat([cross_df, filtered_cross_df_UNFILTERED_gt], axis=1)
                    # cross_df.to_excel('cross_df_MAIN_FINAL_ABS.xlsx')
            else:
                cross_df = cross_df.copy()
            # cross_df.to_excel('CROSS_DF_FINAL-GT_CHANGED.xlsx')
            ############ ADD UNFILTERED Grand Total to rows - 04102024 ########################
            ############ ADD UNFILTERED Grand Total to rows - 04102024 ########################

            #####################################################################################
            #####################################################################################
            #####################################################################################
            #################### DERIVED COLUMNS - 11-03-2024 ###################################
            cross_df.fillna(0,inplace=True)

            ########################################## ADDED ON 04-10-2024 #############################
            ########################################## ADDED ON 04-10-2024 #############################

            ########################################## ADDED ON 04-10-2024 #############################
            ########################################## ADDED ON 04-10-2024 #############################
            if measure_row_column_position == "measure_in_row":

                cross_df = cross_df.T
                # cross_df.to_excel('cross_T.xlsx')
                # exit('cross_dfrrr')
                cross_df = derived_MAIN_fn(cross_df,base_sales_index_colname,row_name,col_name,measure_row_column_position,cagr_power_val,brand_sales_index_value_flag='No')
                cross_df = cross_df.T

            elif measure_row_column_position == "measure_in_column":
                cross_df = derived_MAIN_fn(cross_df,base_sales_index_colname,row_name,col_name,measure_row_column_position,cagr_power_val,brand_sales_index_value_flag)

            cross_df.fillna(0,inplace=True)
            cross_df.replace('nan%','0%', inplace=True)
            cross_df.replace('-inf%','0%', inplace=True)
            cross_df.replace('inf%','0%', inplace=True)
            # ########### CODE TO REMOVE SELECTED BRAND ROW FROM BRAND SALES INDEX IF NOT IN BRAND ###
            # if 'Brand sales index' in base_filter_col_lst:
            #     val_selected_brand_sales = dict_base_filter_data2['Brand sales index']
            #     val_selected_brand_sales = val_selected_brand_sales[0]
            #     print('val_selected_brand_sales 1932',val_selected_brand_sales)
            #     if val_selected_brand_sales not in dict_base_filter_data2["Brand"]:
            #         print('2053 if condition')
            #         filtered_selected_brand = cross_df[cross_df.index.get_level_values(1) == val_selected_brand_sales]
            #         filtered_selected_brand.to_excel('filtered_selected_brand.xlsx')
            #         filtered_grand_total = cross_df[cross_df.index.get_level_values(1) == 'Grand Total']
            #         filtered_grand_total.to_excel('filtered_grand_total.xlsx')

            #         cross_df = cross_df[~(cross_df.index.get_level_values(1) == 'Grand Total')]
            #         cross_df.to_excel('cross_df_removed_gt.xlsx')
            #         subtracted_grand_total_df = filtered_selected_brand - filtered_grand_total
            #         subtracted_grand_total_df.to_excel('subtracted_grand_total_df.xlsx')
            #         cross_df = cross_df[~(cross_df.index.get_level_values(1) == val_selected_brand_sales)]

            #         cross_df = pd.concat([cross_df,subtracted_grand_total_df],axis=0)
            # ########### CODE TO REMOVE SELECTED BRAND ROW FROM BRAND SALES INDEX IF NOT IN BRAND ###
            # cross_df.to_excel('cross_df_FFFF.xlsx')
            # ################## CODE TO REPLACE CY AND YA WITH ACTUAL PERIOD - 19-04-2024 ####

            cross_df = replace_cy_ya_with_actual_period(cross_df,measure_row_column_position,selected_full_period_str,comparative_full_period_str)
            # cross_df.to_excel('cross_df_gggg.xlsx')

            if measure_row_column_position == "measure_in_column": 
                last_level_values_list = cross_df.columns.get_level_values(-1).unique().tolist()
            elif measure_row_column_position == "measure_in_row":
                last_level_values_list = cross_df.index.get_level_values(-1).unique().tolist()

            ################# NEW LOGIC FACTS - 10-05-2024 ############################
            print('facts_object_index_resp 1474',facts_object_index_resp)
            # facts_object_index_lst11 = facts_object_index_resp.values()
            # facts_object_index_lst = list(chain.from_iterable(facts_object_index_lst11))
            # print('facts_object_index_lst',facts_object_index_lst)

            # lst_measures_vals = [last_level_values_list[i] for i in facts_object_index_lst]
            # print('lst_measures_vals',lst_measures_vals)

            dict_selected_measures_lst = {}

            print('selected_weight_column22 598',selected_weight_column22)
            for key in selected_weight_column22:
                dict_selected_measures_lst[key] = [item for item in last_level_values_list if item.startswith(key)]
            print('dict_selected_measures_lst 3333',dict_selected_measures_lst)

            ############# ADDED ON 19-06-2024 ################################################
            # if (measure_row_column_position == 'measure_in_column') and (len(row_name) == 1) and (("Brand" in row_name) or ("Product Name" in row_name)):
            #     for key, value in data.items():
            #         if 7 in value:
            #             value.remove(7)
            ############# ADDED ON 19-06-2024 ################################################

            ########################### NEW CODE - 29-05-2024 ###################################
            print('1910 facts_object_index_resp==',facts_object_index_resp)
            print('1911 dict_selected_measures_lst==',dict_selected_measures_lst)

            ###########################################################################################
            ###########################################################################################
            ###########################################################################################
            for key, indexes in facts_object_index_resp.items():
                print('key2209:', key)
                print('indexes2210:', indexes)
                if (9 in indexes) and ('Brand sales index' not in filter_dict_resp.keys()):
                    print('2212 index mismatch error')
                    indexes = [-1 if x == 9 else x for x in indexes]
                    facts_object_index_resp[key] = indexes
                    print('2214indexes',indexes)

            measure_selected_key_val_resp = {}

            if ((measure_row_column_position == 'measure_in_column') and (len(row_name) == 1) and (("Brand" in row_name) or ("Product Name" in row_name))):
                for key, indexes in facts_object_index_resp.items():
                    if key in dict_selected_measures_lst:
                        print('keyy 1935',key)
                        print('dict_selected_measures_lst 2208',dict_selected_measures_lst)
                        measure_selected_key_val_resp[key] = [dict_selected_measures_lst[key][i] for i in indexes]
                    print('measure_selected_key_val_resp2210',measure_selected_key_val_resp)

            else:
                print('else condition!')
                for key, indexes in facts_object_index_resp.items():
                    print('key:', key)
                    print('indexes:', indexes)
                    print('2217')

                    # # Remove index 8 if it exists
                    # if (8 in indexes) and (~(measure_row_column_position == 'measure_in_column') and (len(row_name) == 1) and (("Brand" in row_name) or ("Product Name" in row_name))):
                    #     indexes = [-1 if x == 8 else x for x in indexes]
                    #     print('indexes 11222244',indexes)
                    #     # indexes.remove(8)
                    
                    print('Removed index 8, facts_object_index_resp:', facts_object_index_resp)

                    # Check if the key exists in dict_selected_measures_lst
                    if key in dict_selected_measures_lst:
                        print('key:', key)
                        print('dict_selected_measures_lst length:', len(dict_selected_measures_lst))
                        print('dict_selected_measures_lst:', dict_selected_measures_lst)
                        # Extract the measures using indexes
                        measure_selected_key_val_resp[key] = [dict_selected_measures_lst[key][i] for i in indexes if i < len(dict_selected_measures_lst[key])]
                        print('measure_selected_key_val_resp:', measure_selected_key_val_resp)
                ###########################olderror##########################
                # print('else condition!')
                # for key, indexes in facts_object_index_resp.items():
                #     print('key',key)
                #     print('indexes',indexes)
                #     if 7 in indexes:
                #         try:
                #             indexes.remove(7)
                #         except:
                #             pass

                #     print('2219 REMOVED 7',facts_object_index_resp)
                #     if key in dict_selected_measures_lst:
                #         print('2223 key',key)
                #         print('dict_selected_measures_lst legggd',len(dict_selected_measures_lst))
                #         print('dict_selected_measures_lst ===00',dict_selected_measures_lst)
                #         measure_selected_key_val_resp[key] = [dict_selected_measures_lst[key][i] for i in indexes]
            ######################## olderror########################################
            # else:
                

            # try:
            #     for key, indexes in facts_object_index_resp.items():
            #         if key in dict_selected_measures_lst:
            #             print('keyy 1935',key)
            #             measure_selected_key_val_resp[key] = [dict_selected_measures_lst[key][i] for i in indexes]
            # except:
            #     for key, indexes in facts_object_index_resp.items():
            #         if 7 in indexes:
            #             try:
            #                 indexes.remove(7)
            #             except:
            #                 pass
            #         if key in dict_selected_measures_lst:
            #             measure_selected_key_val_resp[key] = [dict_selected_measures_lst[key][i] for i in indexes]
            # print('measure_selected_key_val_resp 1495555',measure_selected_key_val_resp)
            ############################################################################################
            ############################################################################################
            ############################################################################################

            # measure_selected_key_val_resp = {}

            # for key, indexes in facts_object_index_resp.items():
            #     if key in dict_selected_measures_lst:
            #         print('keyy 1935',key)
            #         measure_selected_key_val_resp[key] = [dict_selected_measures_lst[key][i] for i in indexes]
            # print('measure_selected_key_val_resp 1495555',measure_selected_key_val_resp)

            facts_object_str_lst11 = measure_selected_key_val_resp.values()
            lst_measures_vals = [item for sublist in facts_object_str_lst11 for item in sublist]
            print('lst_measures_vals 1498--0',lst_measures_vals)
            ########################### NEW CODE - 29-05-2024 ###################################

            # cross_df.to_excel('cross_df_reree.xlsx')
            if measure_row_column_position == "measure_in_row":
                cross_df = cross_df.loc[cross_df.index.get_level_values(-1).isin(list(lst_measures_vals)),:]
            elif measure_row_column_position == 'measure_in_column':
                cross_df = cross_df.loc[:,cross_df.columns.get_level_values(-1).isin(list(lst_measures_vals))]

            # cross_df.to_excel('cross_df_HHHH.xlsx')
            # ##### CODE TO REPLACE QUARTER - 19-04-2024 ###########################
            period_to_be_replaced_str = [selected_full_period_str][0].split()[0]
            if period_to_be_replaced_str =='QUARTER':

                if measure_row_column_position == "measure_in_column":
                    try:
                        cross_df.rename(columns=lambda x: re.sub('QUARTER','', x), inplace=True)
                    except:
                        pass
                elif measure_row_column_position == "measure_in_row":
                    try:
                        cross_df.rename(index=lambda x: re.sub('QUARTER','', x), inplace=True)
                    except:
                        pass

            elif period_to_be_replaced_str =='HY':

                if measure_row_column_position == "measure_in_column":
                    try:
                        cross_df.rename(columns=lambda x: re.sub('HY','', x), inplace=True)
                    except:
                        pass
                elif measure_row_column_position == "measure_in_row":
                    try:
                        cross_df.rename(index=lambda x: re.sub('HY','', x), inplace=True)
                    except:
                        pass

            ############## new code to replace sales currency with sales - 10-05-2024 ###
            # cross_df = replace_sales_currency_with_SALES(selected_weight_column22,cross_df,measure_row_column_position)
            # cross_df.to_excel('saless.xlsx')
            ############## new code to replace sales currency with sales - 10-05-2024 ###

                # cross_df.to_excel('dfdfd_cross_df.xlsx')
            ##### CODE TO REPLACE QUARTER - 19-04-2024 ###########################

            #################### DERIVED COLUMNS - 11-03-2024 ###################################


            #### CODE TO DROP GRAND TOTAL WHEN SALES LC  IS SELECTED - 18-04-2024 ####
            # if (any('Sales (LC)' in item for item in selected_weight_column_all)):
            #     if measure_row_column_position == "measure_in_column":
            #         if seperated_flag_row == 1 and seperated_flag_col == 1:
            #             if ('Country' in row_name):

            #                 cross_df = drop_grand_total_from_rows(cross_df)

            #             elif ('Country' in col_name):

            #                 cross_df = drop_grand_total_from_columns(cross_df)

            #         elif seperated_flag_row == 0 and seperated_flag_col == 0:
            #             print('rowwww 2nd country',row_name[-1])
            #             if ('Country' in row_name) and (row_name[-1] == 'Country'):
            #                 cross_df = drop_grand_total_from_rows(cross_df)


            #         elif seperated_flag_row == 0 and seperated_flag_col == 1:
            #             if ('Country' in row_name) and (row_name[-1] == 'Country'):
            #                 cross_df = drop_grand_total_from_rows(cross_df)

                    # cross_df = drop_grand_total_from_columns(cross_df)

                # elif seperated_flag_row == 1 and seperated_flag_col == 0:
                #     if ('Country' in col_name) and (col_name[-1] == 'Country'):
                    
                #         cross_df = drop_grand_total_from_columns(cross_df)

        #### CODE TO DROP GRAND TOTAL WHEN SALES LC  IS SELECTED - 18-04-2024 ####

            ######################################### GRAND TOTAL 2024 ############################
            if measure_row_column_position == "measure_in_row":
                pass
                # try:
                #     for level in cross_df.index.levels:
                #         if 'Grand Total' in level:
                #             cross_df = cross_df.drop('Grand Total', axis=0, level=level.name)
                # except:
                #     pass

                try:
                    cross_df.drop(('Grand Total','Grand Total'), axis=0, inplace=True)
                except:
                    pass

                # try:
                #     cross_df.drop(('Grand Total',''), axis=0, inplace=True)
                # except:
                #     pass

                # try:
                #     cross_df.drop(('Grand Total','Grand Total'), axis=1, inplace=True)
                # except:
                #     pass

                try:
                    cross_df.drop(('Grand Total',''), axis=1, inplace=True)
                except:
                    pass

            elif measure_row_column_position == "measure_in_column":
                # pass
            #     try:
            #         for level in cross_df.columns.levels:
            #             if 'Grand Total' in level:
            #                 cross_df = cross_df.drop('Grand Total', axis=1, level=level.name)
            #     except:
            #         pass

                # try:
                #     cross_df.drop(('Grand Total','Grand Total'), axis=0, inplace=True)
                # except:
                #     pass

                try:
                    cross_df.drop(('Grand Total',''), axis=0, inplace=True)
                except:
                    pass

                # try:
                #     cross_df.drop(('Grand Total','Grand Total'), axis=1, inplace=True)
                # except:
                #     pass

                try:
                    cross_df.drop(('Grand Total',''), axis=1, inplace=True)
                except:
                    pass

                ######################################### GRAND TOTAL 2024 ###########################

            cross_df.fillna(0,inplace=True)
            cross_df = cross_df.replace([np.nan, np.inf, -np.inf], 0)
            # cross_df.to_excel('NULL_CROSSDF.xlsx')

            ###################### code to remove prefix } - 22-04-2024 ###############################
            if ((category_var_name in row_name) or (category_var_name in col_name)) or ((channel_var_name in row_name) or (channel_var_name in col_name)) or ((brand_var_name in row_name) or (brand_var_name in col_name)):
                try:
                    cross_df = remove_prefix(cross_df)
                except:
                    pass

            if measure_row_column_position == "measure_in_column":
                    try:
                        cross_df.rename(columns=lambda x: re.sub('~}(Other panel)','(Other panel)', x), inplace=True)
                    except:
                        pass
            elif measure_row_column_position == "measure_in_row":
                try:
                    cross_df.rename(index=lambda x: re.sub('~}(Other panel)','(Other panel)', x), inplace=True)
                except:
                    pass
            ###################### code to remove prefix } - 22-04-2024 ###############################

            ############################### NEW LOGIC DERIVED COLUMNS - 29-09-2023 ############################

            #################################### ascending/descending order - 04-06-2024 #########
            if asc_desc_param != 'no_sort':
                try:
                    cross_df = sort_columns(cross_df,measure_row_column_position,column_to_sort,asc_desc_param)
                    # cross_df.to_excel('cross_df_sorted.xlsx')
                except:
                    pass
            #################################### ascending/descending order - 04-06-2024 #########
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

            ######################## CROSSTAB LOGIC #####################################################

            ############### added on 22-10-2024 - Metrics filter #################################
            # selected_full_period_str = '\t'.join(selected_full_period)
            # comparative_full_period_str = '\t'.join(comparative_full_period)

            # dict_selected_measures_lst_NEW = {}
            # for measure in selected_weight_column22:
            #     print('measure --4136',measure)
            #     dict_selected_measures_lst11 = {
            #             measure: [
            #             measure + '_' + selected_full_period_str + ' Rank',
            #             measure + '_' + selected_full_period_str,
            #             measure + '_' + comparative_full_period_str,
            #             measure + '_GR% vs ' + comparative_full_period_str,
            #             measure + '_Share% ' + selected_full_period_str,
            #             measure + '_Share% ' + comparative_full_period_str,
            #             measure + '_BPS vs ' + comparative_full_period_str,
            #             measure + '_CAGR% ' + selected_full_period_str + ' vs ' + comparative_full_period_str,
            #         ]}

            #     if ((measure_row_column_position == 'measure_in_column') and (len(row_name) == 1) and ((brand_var_name in row_name) or ("Product Name" in row_name))) and ('Brand sales index' in base_filter_col_lst) and ('Brand' in base_filter_col_lst):

            #         bsi = measure + '_' + selected_full_period_str + ' Brand Sales Index'
            #         dict_selected_measures_lst11[measure].append(bsi)
            #     dict_selected_measures_lst_NEW.update(dict_selected_measures_lst11)

            # print('4134==dict_selected_measures_lst_NEW',dict_selected_measures_lst_NEW)
            ############### added on 22-10-2024 - Metrics filter #################################
                  
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
            if (len(row_name) == 1 and len(col_name) == 1) or (len(row_name) == 1 and len(col_name) == 0):
                try:

                    # Remove the row with the specific MultiIndex
                    cross_df = cross_df.drop(index=pd.IndexSlice[:, 'Grand Total'])
                except:
                    pass
            # cross_df.to_excel(settings.FINAL_CROSSTAB_OUTPUT +'NULL_CROSSDF.xlsx')
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
            selected_weight_column_str = ','.join([str(elem) for elem in selected_weight_column22])

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

            # # Write the JSON data to a text file
            # with open('filter_dict_resp.json', 'w') as json_file:
            #     json.dump(filter_dict_resp, json_file)

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
                    "dict_selected_measures_lst": dict_selected_measures_lst,
                    "dict_selected_measures_filtered_lst": measure_selected_key_val_resp,
                    # "base_column_names_indices_resp": base_column_names_indices_resp,
                    "filter_dict_resp":filter_dict_resp,
                    "selected_filter_dict_resp":dict_base_filter_data,
                    "all_categories_vals":all_categories_vals,
                    "time_period_flag": time_period_flag,
                    "time_period_vals": time_period_vals,
                    "time_period_filter_val_resp": time_period_filter_val_resp,
                    # "df_cross_json_test": df_cross_json21,
                    "error": "Correct Data",
                    "seperated_flag_col":seperated_flag_col,
                    "current_time_period_resp":selected_full_period_str,
                    "comparative_time_period_resp":comparative_full_period_str,
                     "measure_type":measure_row_column_position,
                     # "unique_base_index_brand_product_resp":unique_base_index_brand_product_resp,
                    # "merge_filename": filename_merged,
                    'message':'Data is Correct',
                    "display_table":'Yes',

                }
        else:
            responseValue = {
                    "status": 404,
                    'message':'No Data is Available for this Filter combination!'

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

######## ADDED ON 24-09-2024 ###############################################
def current_time_period_resp(request):
    if request.method == "POST":
        start_time = time.time()

        print('current_time_period_resp FUNCTION START')
        filename = request.POST.get('filename') + '.csv'
        selected_time_range = [request.POST.get('time_range')]
        selected_time_period = selected_time_range[0].split()[0]

        # Read the CSV file once
        data = pd.read_csv(settings.TEMP_UPLOAD + filename, low_memory=False, engine='c')
        df = data.copy()

        # Get unique years sorted
        yr_unique = sorted(df['Year'].unique().tolist())
        print('yr_unique', yr_unique)

        time_period_dict = {}
        lst_fy_condn_match = []

        # Pre-calculate unique periods for each year to avoid repeated filtering
        periods_by_year = {yr: df[df['Year'] == yr]['Period'].unique().tolist() for yr in yr_unique}

        for yr_loop in yr_unique:
            period_unique = sorted(periods_by_year[yr_loop])

            if selected_time_period in ['MAT', 'QUARTER', 'YTD']:
                if selected_time_period == 'MAT' and yr_loop == min(yr_unique):
                    period_unique = [item for item in period_unique if item == 'Q4']
                
                time_period_lst11 = [
                    f"{selected_time_period} {period_loop} {yr_loop}"
                    for period_loop in period_unique
                ]
                time_period_dict[yr_loop] = time_period_lst11

            elif selected_time_period == 'HY':
                if all(q in period_unique for q in ['Q1', 'Q2', 'Q3', 'Q4']):
                    time_period_dict[yr_loop] = [f"{selected_time_period} H1 {yr_loop}", f"{selected_time_period} H2 {yr_loop}"]
                elif all(q in period_unique for q in ['Q1', 'Q2']):
                    time_period_dict[yr_loop] = [f"{selected_time_period} H1 {yr_loop}"]

            elif selected_time_period == 'FY':
                if all(q in period_unique for q in ['Q1', 'Q2', 'Q3', 'Q4']):
                    lst_fy_condn_match.append(yr_loop)
                    time_period_dict[yr_loop] = [f"{selected_time_period} {yr_loop}"]

        # Filter time_period_dict based on FY matches if needed
        if selected_time_period == 'FY':
            time_period_dict = {k: v for k, v in time_period_dict.items() if k in lst_fy_condn_match}

        print('Final time_period_dict', time_period_dict)

        end_time = time.time()
        print('Execution time:', end_time - start_time, 'sec')

        responseValue = {
            "status": 200,
            "current_time_period_resp": time_period_dict,
            "error": "Correct Data",
        }
    else:
        responseValue = {
            "status": 404,
            "error": "Incorrect Data",
        }

    return JsonResponse(responseValue, safe=False)

######## ADDED ON 24-09-2024 ###############################################
######## ADDED ON 06-05-2024 ###############################################

def current_time_period_resp_ORIGINAL(request):
    if request.method == "POST":
        start_time=time.time()

        print('current_time_period_resp FUNCTION START')
        filename = request.POST.get('filename')+ '.csv'
        # selected_time_range = ['FY']
        selected_time_range =[request.POST.get('time_range')]
        selected_time_period = selected_time_range[0].split()[0]
        start_time = time.time()

        # data = pd.read_csv(settings.TEMP_UPLOAD + filename )
        ##############################################################################
        # with open(settings.TEMP_UPLOAD + filename, 'rb') as f:
        #     result = chardet.detect(f.read(100000))  # Read the first 100000 bytes
        #     detected_encoding = result['encoding']

        # print(f"Detected encoding: {detected_encoding}")

        # Read the CSV file using the detected encoding
        data = pd.read_csv(settings.TEMP_UPLOAD + filename,low_memory=False,engine='c')
        ##############################################################################
        df = data.copy()

        # df['Period_Year'] = df.apply(lambda row: f"{row['Period']} {row['Year']}", axis=1)

        time_period_dict = {}
        yr_unique = df['Year'].unique().tolist()
        yr_unique = sorted(yr_unique)
        min_yr = yr_unique[0]
        print('yr_unique',yr_unique)
        lst_fy_condn_match = []
        if selected_time_period in ['MAT','QUARTER','YTD']:
            for yr_loop in yr_unique:
                df = pd.read_csv(settings.TEMP_UPLOAD + filename,low_memory=False,engine='c')
                df = df[df['Year'] == yr_loop]
                period_unique = df['Period'].unique().tolist()
                period_unique = sorted(period_unique)

                if selected_time_period == 'MAT' and yr_loop == min_yr:
                    period_unique = [item for item in period_unique if item == 'Q4']

                time_period_lst11 = []
                for period_loop in period_unique:
                    time_period_str = selected_time_period + " " + str(period_loop) + " " + str(yr_loop)
                    time_period_lst11.append(time_period_str)

                time_period_dict11 = {yr_loop: time_period_lst11}
                time_period_dict.update(time_period_dict11)

        elif selected_time_period in ['HY']:
            for yr_loop in yr_unique:
                df = pd.read_csv(settings.TEMP_UPLOAD + filename,low_memory=False,engine='c')
                df = df[df['Year'] == yr_loop]
                period_unique = df['Period'].unique().tolist()

                time_period_lst11 = []
                if all(q in period_unique for q in ['Q1', 'Q2','Q3','Q4']):
                    selected_time_period_all_fy_hy = ['H1','H2']

                    for selected_time_period_2 in selected_time_period_all_fy_hy:

                        time_period_str = selected_time_period + " " + str(selected_time_period_2) + " " + str(yr_loop)
                        time_period_lst11.append(time_period_str)

                    time_period_dict11 = {yr_loop: time_period_lst11}
                    time_period_dict.update(time_period_dict11)

                elif all(q in period_unique for q in ['Q1', 'Q2']):
                    selected_time_period_2 = 'H1'

                    time_period_str = selected_time_period + " " + str(selected_time_period_2) + " " + str(yr_loop)
                    time_period_lst11.append(time_period_str)

                time_period_dict11 = {yr_loop: time_period_lst11}
                time_period_dict.update(time_period_dict11)

        elif selected_time_period in ['FY']:

            for yr_loop in yr_unique:
                df = pd.read_csv(settings.TEMP_UPLOAD + filename,low_memory=False,engine='c')
                df = df[df['Year'] == yr_loop]
                period_unique = df['Period'].unique().tolist()

                if all(q in period_unique for q in ['Q1', 'Q2','Q3','Q4']):
                    lst_fy_condn_match.append(yr_loop)
                    selected_time_period_2 = 'FY'
                    time_period_lst11 = []

                    time_period_str = selected_time_period + " " + str(yr_loop)
                    time_period_lst11.append(time_period_str)

                time_period_dict11 = {yr_loop: time_period_lst11}
                time_period_dict.update(time_period_dict11)

            print('lst_fy_condn_match',lst_fy_condn_match)

        if selected_time_period in ['FY']:
            time_period_dict = {k: v for k, v in time_period_dict.items() if k in lst_fy_condn_match}
        print('305 time_period_dictttt', time_period_dict)
        
        print('30545 time_period_dictttt', time_period_dict)

        end_time=time.time()
        print('end_time',end_time-start_time,'sec')

        responseValue = {
            "status": 200,
            "current_time_period_resp": time_period_dict,
            "error": "Correct Data",
        }
    else:
        responseValue = {
            "status": 404,
            "error": "Incorrect Data",
        }

    return JsonResponse(responseValue, safe=False)

######## ADDED ON 06-05-2024 ###############################################

def current_time_period_resp_old_06_05_2024(request): #OLD WALA
    if request.method == "POST":
        start_time=time.time()
        print('======================start_time=================')
        filename = request.POST.get('filename')+ '.csv'
        data = pd.read_csv(settings.TEMP_UPLOAD + filename )
        # data=data.to_pandas()
        # Constructing Period_Year directly
        # data['Period_Year'] = data['Period'] + ' ' + data['Year'].astype(str)

        CY = data['Year'].max()
        max_year_df = data[data['Year'] == CY]
        latest_period = max_year_df['Period'].max()

        # Constructing time_period_lst using list comprehension
        time_period_lst = [f"{time_period_loop}{latest_period} {CY}" for time_period_loop in ['QUARTER ', 'YTD ', 'MAT ']]

        # current_time_period_resp = {'current_time_period': time_period_lst}
        end_time=time.time()
        print('end_time',end_time-start_time,'sec')
        responseValue = {
            "status": 200,
            "current_time_period_resp": time_period_lst,
            "error": "Correct Data",
        }
    else:
        responseValue = {
            "status": 404,
            "error": "Incorrect Data",
        }

    return JsonResponse(responseValue, safe=False)

###################### added on 24-09-2024 ###########################################

def comparative_time_period_resp(request):
    if request.method == "POST":
        start_time = time.time()
        current_timeperiod = [request.POST.get('current_timeperiod')]
        filename = request.POST.get('filename') + '.csv'
        
        # Read the CSV file once
        data = pd.read_csv(settings.TEMP_UPLOAD + filename, low_memory=False, engine='c')
        df = data.copy()

        CY = int(current_timeperiod[0].split()[-1])
        selected_time_period = current_timeperiod[0].split()[0]
        selected_full_period_str = '\t'.join(current_timeperiod)
        latest_period = current_timeperiod[0].split()[1] if selected_time_period in ['MAT', 'YTD', 'QUARTER'] else None

        time_period_dict = {}
        yr_unique = sorted(df['Year'].unique().tolist())
        lst_fy_condn_match = []

        # Pre-calculate unique periods for each year
        periods_by_year = {yr: df[df['Year'] == yr]['Period'].unique().tolist() for yr in yr_unique}

        if selected_time_period in ['MAT', 'QUARTER']:
            for yr_loop in yr_unique:
                period_unique = sorted(periods_by_year[yr_loop])

                if selected_time_period == 'MAT' and yr_loop == min(yr_unique):
                    period_unique = [item for item in period_unique if item == 'Q4']

                time_period_dict[yr_loop] = [
                    f"{selected_time_period} {period_loop} {yr_loop}"
                    for period_loop in period_unique
                ]

        elif selected_time_period == 'YTD':
            for yr_loop in yr_unique:
                time_period_dict[yr_loop] = [f"{selected_time_period} {latest_period} {yr_loop}"]

        elif selected_time_period == 'HY':
            for yr_loop in yr_unique:
                period_unique = periods_by_year[yr_loop]
                time_period_lst = []

                if all(q in period_unique for q in ['Q1', 'Q2', 'Q3', 'Q4']):
                    time_period_lst = [
                        f"{selected_time_period} H1 {yr_loop}",
                        f"{selected_time_period} H2 {yr_loop}"
                    ]
                elif all(q in period_unique for q in ['Q1', 'Q2']):
                    time_period_lst = [f"{selected_time_period} H1 {yr_loop}"]

                time_period_dict[yr_loop] = time_period_lst

        elif selected_time_period == 'FY':
            for yr_loop in yr_unique:
                period_unique = periods_by_year[yr_loop]

                if all(q in period_unique for q in ['Q1', 'Q2', 'Q3', 'Q4']):
                    lst_fy_condn_match.append(yr_loop)
                    time_period_dict[yr_loop] = [f"{selected_time_period} {yr_loop}"]

        # Filter out entries containing the selected full period string
        time_period_dict = {
            key: [val for val in value if selected_full_period_str not in val]
            for key, value in time_period_dict.items() if value
        }

        # Further filter for FY if necessary
        if selected_time_period == 'FY':
            time_period_dict = {k: v for k, v in time_period_dict.items() if k in lst_fy_condn_match}

        print('Final time_period_dict:', time_period_dict)

        end_time=time.time()
        print('end_time',end_time-start_time,'sec')

        responseValue = {
            "status": 200,
            "comparative_time_period_resp": time_period_dict,
            "error": "Correct Data",
        }
    else:
        responseValue = {
            "status": 404,
            "error": "Incorrect Data",
        }

    return JsonResponse(responseValue, safe=False)

############# added by 22-10-2024 - Metric Filter ################################
def metrics_filter_call(request):
    if request.method == "POST":
        selected_time_range = request.POST.get('time_range')

        selected_time_period = [request.POST.get('time_period')]
        comparative_time_period = [request.POST.get('comparison_time_period')]

        facts_group_filter = request.POST.get('facts_group_filter')
        facts_group_filter = json.loads(facts_group_filter)

        facts_group_filter_index_json = request.POST.get('facts_group_filter_index')
        print('facts_group_filter_index_json 5303',facts_group_filter_index_json)
        facts_group_filter_index = json.loads(facts_group_filter_index_json)

        # measure_type_value = request.POST.get('measure_type_value')
        measure_row_column_position = 'measure_in_column'

        rowfilter = request.POST.get('rowfilter_sort')
        columnfilter = request.POST.get('columnfilter_sort')

        row_name = ast.literal_eval(rowfilter)
        col_name = ast.literal_eval(columnfilter)

        # print('selected_time_range',selected_time_range)
        # print('selected_time_period',selected_time_period)
        # print('comparative_time_period',comparative_time_period)
        # print('facts_group_filter',facts_group_filter)
        # print('measure_type_value',measure_type_value)
        # print('row_name',row_name)
        # print('col_name',col_name)

        # print("#############################################################")
        # print('type(selected_time_range)',type(selected_time_range))
        # print('type(selected_time_period)',type(selected_time_period))
        # print('type(comparative_time_period)',type(comparative_time_period))
        # print('type(facts_group_filter)',type(facts_group_filter))
        # print('type(measure_type_value)',type(measure_type_value))
        # print('type(rowfilter_sort)',type(row_name))
        # print('type(columnfilter_sort)',type(col_name))
        # print("#################################################################")

        selected_weight_column22 = list(facts_group_filter.keys())

        print('#################################################################')
        ############### SELECTED - Metrics filter #################################
        selected_full_period_str = '\t'.join(selected_time_period)
        comparative_full_period_str = '\t'.join(comparative_time_period)

        dict_selected_measures_lst_NEW = {}
        for measure in selected_weight_column22:
            print('measure --4136',measure)
            dict_selected_measures_lst11 = {
                    measure: [
                    measure + '_' + selected_full_period_str + ' Rank',
                    measure + '_' + selected_full_period_str,
                    measure + '_' + comparative_full_period_str,
                    measure + '_GR% vs ' + comparative_full_period_str,
                    measure + '_GR% Contribution',
                    measure + '_Share% ' + selected_full_period_str,
                    measure + '_Share% ' + comparative_full_period_str,
                    measure + '_BPS vs ' + comparative_full_period_str,
                    measure + '_CAGR% ' + selected_full_period_str + ' vs ' + comparative_full_period_str,
                ]}

            if ((measure_row_column_position == 'measure_in_column') and (len(row_name) == 1) and ((brand_var_name in row_name) or ("Product Name" in row_name))) and ('Brand sales index' in base_filter_col_lst) and ('Brand' in base_filter_col_lst):

                bsi = measure + '_' + selected_full_period_str + ' Brand Sales Index'
                dict_selected_measures_lst11[measure].append(bsi)
            dict_selected_measures_lst_NEW.update(dict_selected_measures_lst11)

        print('4134==dict_selected_measures_lst_NEW',dict_selected_measures_lst_NEW)
        ############### SELECTED - Metrics filter #################################

        ############### FILTERED - Metrics filter #################################
        print('facts_group_filter_index 5362--',facts_object_index_resp)

        for key, indexes in facts_object_index_resp.items():
            print('key2209:', key)
            print('indexes2210:', indexes)
            if (9 in indexes) and ('Brand sales index' not in filter_dict_resp.keys()):
                print('2212 index mismatch error')
                indexes = [-1 if x == 9 else x for x in indexes]
                facts_object_index_resp[key] = indexes
                print('2214indexes',indexes)

        measure_selected_key_val_resp = {}

        if ((measure_row_column_position == 'measure_in_column') and (len(row_name) == 1) and (("Brand" in row_name) or ("Product Name" in row_name))):
            for key, indexes in facts_object_index_resp.items():
                if key in dict_selected_measures_lst:
                    print('keyy 1935',key)
                    print('dict_selected_measures_lst 2208',dict_selected_measures_lst)
                    measure_selected_key_val_resp[key] = [dict_selected_measures_lst[key][i] for i in indexes]
                print('measure_selected_key_val_resp2210',measure_selected_key_val_resp)

        else:
            print('else condition!')
            for key, indexes in facts_object_index_resp.items():
                print('key:', key)
                print('indexes:', indexes)
                print('2217')

                # # Remove index 8 if it exists
                # if (8 in indexes) and (~(measure_row_column_position == 'measure_in_column') and (len(row_name) == 1) and (("Brand" in row_name) or ("Product Name" in row_name))):
                #     indexes = [-1 if x == 8 else x for x in indexes]
                #     print('indexes 11222244',indexes)
                #     # indexes.remove(8)
                
                print('Removed index 8, facts_object_index_resp:', facts_object_index_resp)

                # Check if the key exists in dict_selected_measures_lst
                if key in dict_selected_measures_lst:
                    print('key:', key)
                    print('dict_selected_measures_lst length:', len(dict_selected_measures_lst))
                    print('dict_selected_measures_lst:', dict_selected_measures_lst)
                    # Extract the measures using indexes
                    measure_selected_key_val_resp[key] = [dict_selected_measures_lst[key][i] for i in indexes if i < len(dict_selected_measures_lst[key])]
                    print('measure_selected_key_val_resp:', measure_selected_key_val_resp)
        ############### FILTERED - Metrics filter #################################

        responseValue = {
                "status": 200,
                "comparative_time_period_resp":'time_period_dict',
                "error": "Correct Data",
                # "merge_filename": filename_merged,

            }
    else:
        responseValue = {
            "status": 404,
            "error": "Incorrect Data",
        }


    return JsonResponse(responseValue, safe=False)

############# added by 22-10-2024 - Metric Filter ################################

###################### added on 24-09-2024 ###########################################

def comparative_time_period_resp_ORIGINAL(request):
    if request.method == "POST":
        current_timeperiod = [request.POST.get('current_timeperiod')]
        # current_timeperiod = ['YTD Q2 2022']
        filename = request.POST.get('filename')+ '.csv'
        # data = pd.read_csv(settings.TEMP_UPLOAD + filename)
        ##############################################################################
        # with open(settings.TEMP_UPLOAD + filename, 'rb') as f:
        #     result = chardet.detect(f.read(100000))  # Read the first 100000 bytes
        #     detected_encoding = result['encoding']

        # print(f"Detected encoding: {detected_encoding}")

        # Read the CSV file using the detected encoding
        data = pd.read_csv(settings.TEMP_UPLOAD + filename,low_memory=False,engine='c')
        ##############################################################################
        # data=data.to_pandas()

        CY = int(current_timeperiod[0].split()[-1])

        selected_time_period = current_timeperiod[0].split()[0]

        selected_full_period_str = '\t'.join(current_timeperiod)

        if selected_time_period in ['MAT','YTD','QUARTER']:
            latest_period = current_timeperiod[0].split()[1]

        data = pd.read_csv(settings.TEMP_UPLOAD + filename,low_memory=False,engine='c')
        df = data.copy()
        time_period_dict= {}
        yr_unique = df['Year'].unique().tolist()
        yr_unique = sorted(yr_unique)
        min_yr = yr_unique[0]
        lst_fy_condn_match = []
        if selected_time_period in ['MAT','QUARTER']:

            for yr_loop in yr_unique:
                df = pd.read_csv(settings.TEMP_UPLOAD + filename,low_memory=False,engine='c')
                df = df[df['Year'] == yr_loop]
                period_unique = df['Period'].unique().tolist()
                period_unique = sorted(period_unique)

                if selected_time_period == 'MAT' and yr_loop == min_yr:
                    period_unique = [item for item in period_unique if item == 'Q4']

                time_period_lst11 = []
                for period_loop in period_unique:
                    time_period_str = selected_time_period + " " + str(period_loop) + " " + str(yr_loop)
                    time_period_lst11.append(time_period_str)

                time_period_dict11 = {yr_loop:time_period_lst11}
                time_period_dict.update(time_period_dict11)

        elif selected_time_period in ['YTD']:
            for yr_loop in yr_unique:
                df = pd.read_csv(settings.TEMP_UPLOAD + filename,low_memory=False,engine='c')
                df = df[df['Year'] == yr_loop]
                time_period_str = selected_time_period + " " + latest_period + " " + str(yr_loop)

                time_period_dict11 = {yr_loop: [time_period_str]}
                time_period_dict.update(time_period_dict11)

    ################################### added on 06-05-2024 #################################       
        elif selected_time_period in ['HY']:
            for yr_loop in yr_unique:
                df = pd.read_csv(settings.TEMP_UPLOAD + filename,low_memory=False,engine='c')
                df = df[df['Year'] == yr_loop]
                period_unique = df['Period'].unique().tolist()

                time_period_lst11 = []
                if all(q in period_unique for q in ['Q1', 'Q2', 'Q3', 'Q4']):
                    selected_time_period_all_fy_hy = ['H1', 'H2']

                    for selected_time_period_2 in selected_time_period_all_fy_hy:
                        time_period_str = selected_time_period + " " + str(selected_time_period_2) + " " + str(yr_loop)
                        time_period_lst11.append(time_period_str)

                    time_period_dict11 = {yr_loop: time_period_lst11}
                    time_period_dict.update(time_period_dict11)

                elif all(q in period_unique for q in ['Q1', 'Q2']):
                    selected_time_period_2 = 'H1'

                    time_period_str = selected_time_period + " " + str(selected_time_period_2) + " " + str(yr_loop)
                    time_period_lst11.append(time_period_str)

                time_period_dict11 = {yr_loop: time_period_lst11}
                time_period_dict.update(time_period_dict11)

        elif selected_time_period in ['FY']:
            for yr_loop in yr_unique:
                df = pd.read_csv(settings.TEMP_UPLOAD + filename,low_memory=False,engine='c')
                df = df[df['Year'] == yr_loop]
                period_unique = df['Period'].unique().tolist()

                if all(q in period_unique for q in ['Q1', 'Q2', 'Q3', 'Q4']):
                    lst_fy_condn_match.append(yr_loop)
                    selected_time_period_2 = 'FY'
                    time_period_lst11 = []

                    time_period_str = selected_time_period + " " + str(yr_loop)
                    time_period_lst11.append(time_period_str)

                time_period_dict11 = {yr_loop: time_period_lst11}
                time_period_dict.update(time_period_dict11)

        ########################################### added on 06-05-2024 ##############################
        # time_period_dict = {key: [val for val in value if selected_full_period_str not in val] for key, value in
        #                     time_period_dict.items()}
        ###################################################################################################################
        time_period_dict = {key: [val for val in value if selected_full_period_str not in val] for key, value in
                            time_period_dict.items() if any(selected_full_period_str not in val for val in value)}

        if selected_time_period in ['FY']:
            try:
                time_period_dict = {k: v for k, v in time_period_dict.items() if k in lst_fy_condn_match}
            except:
                pass   
        ##################################################################################################  

        # time_period_dict = {key: value[:value.index(selected_full_period_str)] if selected_full_period_str in value else value
        #                  for key, value in time_period_dict.items() if
        #                  (value[:value.index(selected_full_period_str)] if selected_full_period_str in value else value)}

        print('305 time_period_dict AFTER', time_period_dict)

        responseValue = {
                "status": 200,
                "comparative_time_period_resp":time_period_dict,
                "error": "Correct Data",
                # "merge_filename": filename_merged,

            }
    else:
        responseValue = {
            "status": 404,
            "error": "Incorrect Data",
        }


    return JsonResponse(responseValue, safe=False)


def comparative_time_period_resp_old(request):
    if request.method == "POST":
        current_timeperiod = [request.POST.get('current_timeperiod')]
        filename = request.POST.get('filename')+ '.csv'
        data = pd.read_csv(settings.TEMP_UPLOAD + filename)
        # data=data.to_pandas()
        CY = int(current_timeperiod[0].split()[-1])
        latest_period = current_timeperiod[0].split()[1]
        selected_time_period = current_timeperiod[0].split()[0]

        print('CY',CY)
        print('latest_period',latest_period)
        print('selected_time_period',selected_time_period)

        data = pd.read_csv(settings.TEMP_UPLOAD + filename)
        df = data.copy()

        yr_unique = df['Year'].unique().tolist()
        print('yr_unique',yr_unique)

        time_period_lst = []
        for yr_loop in yr_unique:
            time_period_str = selected_time_period + " " + latest_period + " " + str(yr_loop)
            time_period_lst.append(time_period_str)

        # comparative_time_period_resp = {'comparative_time_period': time_period_lst}
        # print('comparative_time_period_resp', comparative_time_period_resp)

        responseValue = {
                "status": 200,
                "comparative_time_period_resp":time_period_lst,
                "error": "Correct Data",
                # "merge_filename": filename_merged,

            }
    else:
        responseValue = {
            "status": 404,
            "error": "Incorrect Data",
        }

    return JsonResponse(responseValue, safe=False)

######  ADDED ON 21-10-2024 - ADDED TRAILING PERIODS ###################################
def marketwise_latest_quarter(request):
    start_time = time.time()  # Start timing

    market_types = ['Multichannel', 'Sales', 'Doors']
    data_lst = {}

    df_multichannel = pd.read_excel(settings.PYTHONPATH_MARKET_MASTER+'Markets_Availibility_Checks.xlsx',sheet_name = 'Multichannel')
    df_sales = pd.read_excel(settings.PYTHONPATH_MARKET_MASTER+'Markets_Availibility_Checks.xlsx',sheet_name = 'Sales')
    df_doors = pd.read_excel(settings.PYTHONPATH_MARKET_MASTER+'Markets_Availibility_Checks.xlsx',sheet_name = 'Doors')

    DF_lst = [df_multichannel,df_sales,df_doors]

    for loop in range(len(market_types)):
        data_lst2 = {market_types[loop]:json.loads(DF_lst[loop].to_json(orient='split'))}
        data_lst.update(data_lst2)

    print('5597==',data_lst)
    # Measure execution time
    execution_time = time.time() - start_time
    print('Time taken to fetch available markets table is-', execution_time, 'seconds')

    response_value = {
        "status": 200 if data_lst else 404,
        "error": "Correct Data" if data_lst else "Incorrect Data",
        "data": data_lst,
    }

    return JsonResponse(response_value, safe=False)



def marketwise_latest_quarter_V2(request):
    start_time = time.time()  # Start timing

    market_types = ['Multichannel', 'Sales', 'Doors']
    data_lst = {market_type: {} for market_type in market_types}

    # Get all relevant files at once
    files = os.listdir(settings.TEMP_UPLOAD)

    # Filter files by market type and store them in dictionaries
    file_dict = {market_type: [] for market_type in market_types}
    for file_name in files:
        for market_type in market_types:
            if market_type in file_name:
                file_dict[market_type].append(file_name)

    # Process files for each market type
    for market_type, file_names in file_dict.items():
        # Get the filenames for consolidated, marketwise, and trailing
        filename_consolidated = next((file for file in file_names if 'Consolidated' in file), None)
        filename_marketwise = next((file for file in file_names if 'Marketwise' in file), None)
        filename_trailing = next((file for file in file_names if 'Trailing' in file), None)

        # Initialize empty lists for unique markets and DataFrames for checks
        df_uploaded_chks = pd.DataFrame({'Markets': [], 'Marketwise': 'No'})
        df_cnsld_chks = pd.DataFrame({'Markets': [], 'Consolidated': 'No'})
        df_trailing_chks = pd.DataFrame({'Markets': [], 'Trailing': 'No'})

        if filename_marketwise:
            df_market = pd.read_csv(os.path.join(settings.TEMP_UPLOAD, filename_marketwise), usecols=['Market'])
            uploaded_market_lst = df_market['Market'].unique()
            df_uploaded_chks = pd.DataFrame({'Markets': uploaded_market_lst, 'Marketwise': 'Yes'})
        else:
            df_uploaded_chks = pd.DataFrame({'Markets': [], 'Marketwise': 'No'})

        if filename_consolidated:
            df_cnsld = pd.read_csv(os.path.join(settings.TEMP_UPLOAD, filename_consolidated), usecols=['Market'])
            consolidated_markets_lst = df_cnsld['Market'].unique()
            df_cnsld_chks = pd.DataFrame({'Markets': consolidated_markets_lst, 'Consolidated': 'Yes'})
        else:
            df_cnsld_chks = pd.DataFrame({'Markets': [], 'Consolidated': 'No'})

        if filename_trailing:
            df_trailing = pd.read_csv(os.path.join(settings.TEMP_UPLOAD, filename_trailing), usecols=['Market'])
            trailing_markets_lst = df_trailing['Market'].unique()
            df_trailing_chks = pd.DataFrame({'Markets': trailing_markets_lst, 'Trailing': 'Yes'})
        else:
            df_trailing_chks = pd.DataFrame({'Markets': [], 'Trailing': 'No'})

        # Merge DataFrames, fill missing markets with "No"
        df_final = pd.concat([df_cnsld_chks.set_index('Markets'),
                              df_uploaded_chks.set_index('Markets'),
                              df_trailing_chks.set_index('Markets')],
                             axis=1, join='outer').fillna('No')

        df_final.columns = df_final.columns.to_flat_index()  # Flatten MultiIndex columns if needed

        # df_final.to_excel('df_final_markets.xlsx')

        # Convert to JSON
        data_lst[market_type] = json.loads(df_final.reset_index().to_json(orient='split'))

    # Measure execution time
    execution_time = time.time() - start_time
    print('Time taken to fetch available markets table is-', execution_time, 'seconds')

    response_value = {
        "status": 200 if data_lst else 404,
        "error": "Correct Data" if data_lst else "Incorrect Data",
        "data": data_lst,
    }

    return JsonResponse(response_value, safe=False)



def marketwise_latest_quarter_V1(request):
    start_time = time.time()  # Start timing

    market_types = ['Multichannel', 'Sales', 'Doors']
    data_lst = {market_type: {} for market_type in market_types}

    # Get all relevant files at once
    files = os.listdir(settings.TEMP_UPLOAD)

    # Filter files by market type and store them in dictionaries
    file_dict = {market_type: [] for market_type in market_types}
    for file_name in files:
        for market_type in market_types:
            if market_type in file_name:
                file_dict[market_type].append(file_name)

    # Process files for each market type
    for market_type, file_names in file_dict.items():
        # Get the filenames for consolidated, marketwise, and trailing
        filename_consolidated = next((file for file in file_names if 'Consolidated' in file), None)
        filename_marketwise = next((file for file in file_names if 'Marketwise' in file), None)
        filename_trailing = next((file for file in file_names if 'Trailing' in file), None)

        if filename_consolidated and filename_marketwise and filename_trailing:
            filename_consolidated_str = filename_consolidated.replace('.csv', '')
            filename_marketwise_str = filename_marketwise.replace('.csv', '')
            filename_trailing_str = filename_trailing.replace('.csv', '')

            # Read CSV files in one go
            df_market = pd.read_csv(os.path.join(settings.TEMP_UPLOAD, filename_marketwise), usecols=['Market'])
            df_cnsld = pd.read_csv(os.path.join(settings.TEMP_UPLOAD, filename_consolidated), usecols=['Market'])
            df_trailing = pd.read_csv(os.path.join(settings.TEMP_UPLOAD, filename_trailing), usecols=['Market'])

            # Get unique markets
            uploaded_market_lst = df_market['Market'].unique()
            consolidated_markets_lst = df_cnsld['Market'].unique()
            trailing_markets_lst = df_trailing['Market'].unique()

            # Create DataFrames for checks
            df_uploaded_chks = pd.DataFrame({'Markets': uploaded_market_lst, filename_marketwise_str: 'Yes'})
            df_cnsld_chks = pd.DataFrame({'Markets': consolidated_markets_lst, filename_consolidated_str: 'Yes'})
            df_trailing_chks = pd.DataFrame({'Markets': trailing_markets_lst, filename_trailing_str: 'Yes'})

            # Merge DataFrames
            df_final = pd.concat([df_cnsld_chks.set_index('Markets'),
                                  df_uploaded_chks.set_index('Markets'),
                                  df_trailing_chks.set_index('Markets')],
                                 axis=1, join='outer')
            df_final.columns = df_final.columns.to_flat_index()  # Flatten MultiIndex columns if needed

            # df_final.to_excel('df_final_markets.xlsx')

            # Convert to JSON
            data_lst[market_type] = json.loads(df_final.reset_index().to_json(orient='split'))
        else:
            data_lst[market_type] = {}

    # Measure execution time
    execution_time = time.time() - start_time
    print('Time taken to fetch available markets table is-', execution_time, 'seconds')

    response_value = {
        "status": 200 if data_lst else 404,
        "error": "Correct Data" if data_lst else "Incorrect Data",
        "data": data_lst,
    }

    return JsonResponse(response_value, safe=False)

######  ADDED ON 21-10-2024 - ADDED TRAILING PERIODS ###################################

########## added on 24-09-2024 ######################################

def marketwise_latest_quarter_consolidated_and_marketise(request):
    start_time = time.time()  # Start timing

    market_types = ['Multichannel', 'Sales', 'Doors']
    data_lst = {market_type: {} for market_type in market_types}

    # Get all relevant files at once
    files = os.listdir(settings.TEMP_UPLOAD)

    # Filter files by market type and store them in dictionaries
    file_dict = {market_type: [] for market_type in market_types}
    for file_name in files:
        for market_type in market_types:
            if market_type in file_name:
                file_dict[market_type].append(file_name)

    # Process files for each market type
    for market_type, file_names in file_dict.items():
        # Get the filenames for consolidated and marketwise
        filename_consolidated = next((file for file in file_names if 'Consolidated' in file), None)
        filename_marketwise = next((file for file in file_names if 'Marketwise' in file), None)

        if filename_consolidated and filename_marketwise:
            filename_consolidated_str = filename_consolidated.replace('.csv', '')
            filename_marketwise_str = filename_marketwise.replace('.csv', '')

            # Read CSV files in one go
            df_market = pd.read_csv(os.path.join(settings.TEMP_UPLOAD, filename_marketwise), usecols=['Market'])
            df_cnsld = pd.read_csv(os.path.join(settings.TEMP_UPLOAD, filename_consolidated), usecols=['Market'])

            # Get unique markets
            uploaded_market_lst = df_market['Market'].unique()
            consolidated_markets_lst = df_cnsld['Market'].unique()

            # Create a DataFrame for checks
            df_uploaded_chks = pd.DataFrame({'Markets': uploaded_market_lst, filename_marketwise_str: 'Yes'})
            df_cnsld_chks = pd.DataFrame({'Markets': consolidated_markets_lst, filename_consolidated_str: 'Yes'})

            # Merge DataFrames
            df_final = pd.concat([df_cnsld_chks.set_index('Markets'), df_uploaded_chks.set_index('Markets')], axis=1, join='outer')
            df_final.columns = df_final.columns.to_flat_index()  # Flatten MultiIndex columns if needed

            # df_final.to_excel('df_final_markets.xlsx')
            
            # Convert to JSON
            data_lst[market_type] = json.loads(df_final.reset_index().to_json(orient='split'))
        else:
            data_lst[market_type] = {}

    # Measure execution time
    execution_time = time.time() - start_time
    print('Time taken to fetch available markets table is-', execution_time, 'seconds')

    response_value = {
        "status": 200 if data_lst else 404,
        "error": "Correct Data" if data_lst else "Incorrect Data",
        "data": data_lst,
    }

    return JsonResponse(response_value, safe=False)


########## added on 24-09-2024 ######################################

def marketwise_latest_quarter_ORIGINAL(request):
    start_time = time.time()  # Start timing

    market_types = ['Multichannel', 'Sales', 'Doors']
    data_lst = {}

    # Get all relevant files at once
    files = os.listdir(settings.TEMP_UPLOAD)
    
    # Filter files by market type and store them in dictionaries
    file_dict = {market_type: [] for market_type in market_types}
    for file_name in files:
        for market_type in market_types:
            if market_type in file_name:
                file_dict[market_type].append(file_name)
    
    # Process files for each market type
    for market_type, file_names in file_dict.items():
        filename_consolidated = next((file for file in file_names if 'Consolidated' in file), None)
        filename_marketwise = next((file for file in file_names if 'Marketwise' in file), None)

        if filename_consolidated and filename_marketwise:
            filename_consolidated_str = filename_consolidated.replace('.csv', '')
            filename_marketwise_str = filename_marketwise.replace('.csv', '')

            df_market = pd.read_csv(os.path.join(settings.TEMP_UPLOAD, filename_marketwise))
            df_cnsld = pd.read_csv(os.path.join(settings.TEMP_UPLOAD, filename_consolidated))

            uploaded_market_lst = df_market['Market'].unique()
            consolidated_markets_lst = df_cnsld['Market'].unique()

            df_uploaded_chks = pd.DataFrame({'Markets': uploaded_market_lst, filename_marketwise_str: 'Yes'})
            df_cnsld_chks = pd.DataFrame({'Markets': consolidated_markets_lst, filename_consolidated_str: 'Yes'})

            df_final = df_cnsld_chks.merge(df_uploaded_chks, how='outer', on='Markets')

            df_table_json = df_final.to_json(orient='split')
            data_lst[market_type] = json.loads(df_table_json)
        else:
            data_lst[market_type] = {}

    # Measure execution time
    execution_time = time.time() - start_time
    print('Time taken to fetch available markets table is-',execution_time,' seconds')

    response_value = {
        "status": 404,
        "error": "Incorrect Data",
        "data": data_lst,
    }

    return JsonResponse(response_value, safe=False)


def marketwise_latest_quarter_OLD(request):

    Multichannel_lst = []
    market_type = 'Multichannel'
    for file_name in [file for file in os.listdir(settings.TEMP_UPLOAD) if market_type in file]:
        # file_name=file_name.replace('.json','')
        # file_name = file_name.replace('.csv', '')
        Multichannel_lst.append(file_name)

    Sales_lst = []
    market_type = 'Sales'
    for file_name in [file for file in os.listdir(settings.TEMP_UPLOAD) if market_type in file]:
        # file_name = file_name.replace('.csv', '')
        Sales_lst.append(file_name)

    Doors_lst = []
    market_type = 'Doors'
    for file_name in [file for file in os.listdir(settings.TEMP_UPLOAD) if market_type in file]:
        # file_name=file_name.replace('.json','')
        # file_name = file_name.replace('.csv', '')
        Doors_lst.append(file_name)

    # print('Multichannel_lst',Multichannel_lst)
    # print('Sales_lst',Sales_lst)
    # print('Doors_lst',Doors_lst)

    dict_filenames = {'Multichannel':Multichannel_lst,'Sales':Sales_lst,'Doors':Doors_lst}
    lst_vals_filenames = list(dict_filenames.values())
    data_lst = {}
    for key_data_type, value_data_lst in dict_filenames.items():
        data_type_name = key_data_type
        lst_filename = value_data_lst
        # print('data_type_name',data_type_name)
        # print('lst_filename',lst_filename)

        filename_consolidated = next((file for file in lst_filename if 'Consolidated' in file), None)
        filename = next((file for file in lst_filename if 'Marketwise' in file), None)

        filename_consolidated_str = filename_consolidated.replace('.csv', '')
        filename_str = filename.replace('.csv', '')

        df_market = pd.read_csv(settings.TEMP_UPLOAD + filename)
        df_cnsld = pd.read_csv(settings.TEMP_UPLOAD + filename_consolidated)

        uploaded_market_lst = df_market['Market'].unique()
        consolidated_markets_lst = df_cnsld['Market'].unique()

        df_uploaded_chks = pd.DataFrame(columns=['Markets',filename_str])
        df_cnsld_chks = pd.DataFrame(columns=['Markets',filename_consolidated_str])

        df_uploaded_chks['Markets'] = uploaded_market_lst
        df_uploaded_chks[filename_str] = 'Yes'

        df_cnsld_chks['Markets'] = consolidated_markets_lst
        df_cnsld_chks[filename_consolidated_str] = 'Yes'

        df_final = df_cnsld_chks.merge(df_uploaded_chks,how='outer',on='Markets')
        # df_final.to_excel('df_final.xlsx')

        df_table_json1 = df_final.to_json(orient='split')
        df_table_json = json.loads(df_table_json1)

        final_dict = {data_type_name:df_table_json}
        data_lst.update(final_dict)
        print('data_lst==',data_lst)

        responseValue = {
            "status": 404,
            "error": "Incorrect Data",
            "data": data_lst,
        }

    return JsonResponse(responseValue, safe=False)
