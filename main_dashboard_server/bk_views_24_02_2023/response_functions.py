import json
import os
import time

import pandas as pd
import numpy as np
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
# Create your views here.
# from CCV_Tool.CCV_Tool.settings import pythonpath
from django.conf import settings

from datetime import date
from datetime import datetime
from io import StringIO

def codeframe(list_resp):
    
    # df = pd.read_json(PYTHONPATH + "Electrolux_India.json",orient='records', lines=True)
    # codeframe_df = pd.read_json(PYTHONPATH + "Electrolux- India_codeframe.json",orient='records', lines=True)
    df = pd.DataFrame(list_resp[0])
    codeframe_df = pd.DataFrame(list_resp[1])

    codeframe_df['Variable Level'].fillna('None',inplace=True)
    codeframe_df['Variable Name'].fillna('None',inplace=True)

    encode_dict = {}
    for loop_vals in range(len(codeframe_df)):
        codeframe_dict = {codeframe_df['Variable Name'][loop_vals]:codeframe_df['Variable Level'][loop_vals]}
        encode_dict.update(codeframe_dict)

    df.rename(columns=encode_dict, inplace=True)

    new_col_names_lst = []
    for loop in df.columns:
        # print("loop",loop)
        loop = loop.replace(" ", "_")
        new_col_names_lst.append(loop)

    df.columns = new_col_names_lst
    return df


def column_dtypes(list_all_files):
        colname_dict_final={}
        for loop_filename in list_all_files:

            # pythonpath=r"C:/Users/MihirPawar/Desktop/Python Project BSW/Python Files1/ccv_tool//"
            df = pd.read_json(settings.PYTHONPATH + loop_filename, orient='records', lines=True)
           #print("df", df.head(2))

            # colname_obj = []
            # for x in df.columns:
            #         colname_obj.append(x)

            # colname_obj = [x for x in df.columns]
            # colname_obj = [x for x in df.columns.values]
            colname_obj = list(df.columns.values)
                    
           #print("colname_num", colname_num)
           #print("colname_obj", colname_obj)

            col_dtype_dict = {'filename':loop_filename,'colname_obj': colname_obj}
            filename11=loop_filename.replace(".json","")

            colname_dict_final1={filename11:col_dtype_dict}

           #print("col_dtype_dict",col_dtype_dict)
            colname_dict_final.update(colname_dict_final1)

        return colname_dict_final

def column_data_display(list_all_files):
        colname_data_dict_final = {}
        for loop_filename in list_all_files:
            df=pd.read_json(settings.PYTHONPATH+loop_filename, orient='records',lines=True)
           #print("df", df.head(2))

            colname_data_dict_final_22={}
            # selected_column='Age_Group'
            for selected_column in df.columns:
               #print("selected_column selected_column",selected_column)
                freq_percent=df[selected_column].value_counts(normalize=True).mul(100)
                ##print("freq_percent",freq_percent)

                freq_vals=df[selected_column].value_counts()

                df_Freq=pd.DataFrame(columns=['Count','Percent'])
                # df_Freq['Column']=df.columns
                df_Freq['Count']=freq_vals
                df_Freq['Percent']=freq_percent

                df_Freq['Count']=round(df_Freq['Count'],2)
                df_Freq['Percent']=round(df_Freq['Percent'],2)

                df_Freq['Percent']=df_Freq['Percent'].astype(str) + " %"

                df_Freq=df_Freq.reset_index().rename(columns={'index':'Column_data'})
               #print('df_Freq-->')
               #print('typee df_Freq',type(df_Freq))

                df_Freq_json1 = df_Freq.to_json(orient='index')
                df_Freq_json = json.loads(df_Freq_json1)

                # df_Freq.to_excel('df_Freq.xlsx')

                colname_data_dict_final_selected_column = {selected_column: df_Freq_json}
                colname_data_dict_final_22.update(colname_data_dict_final_selected_column)

            filename22 = loop_filename.replace(".json", "")

            colname_data_dict_final1 = {filename22: colname_data_dict_final_22}
           #print(" ===== resp out of loop ===")
           #print("colname_data_dict_final1", colname_data_dict_final1)

            colname_data_dict_final.update(colname_data_dict_final1)
           #print("======= resp enddd =====")
        return colname_data_dict_final


def value_count_freq(df,filename,row_name,col_name):

    df = pd.read_json(settings.PYTHONPATH + filename, orient='records', lines=True)
    ##print("df", df.head(2))
    ##print("df colsss", df.columns)

    rowcount_dict = {}
    for selected_column in row_name:

        freq_vals = df[selected_column].value_counts()

        df_Freq = pd.DataFrame(columns=['Values'])
        # df_Freq['Column']=df.columns
        df_Freq['Values'] = freq_vals
        df_Freq = df_Freq.reset_index().rename(columns={'index': 'Columns'})

       #print('df_Freq colnames', df_Freq.columns)

        col_categories = df_Freq['Columns']

       #print('col_categories col_categories===', col_categories)

        df_Freq_json = dict(col_categories)

       #print('df_Freq shapeee', len(df_Freq))

        if selected_column == row_name[0]:
            temp_dict = {len(df_Freq): 'All'}

            df_Freq_json.update(temp_dict)

       #print("df_Freq_json df_Freq_json updatedd roww", df_Freq_json)

        rowcount_dict1 = {selected_column: df_Freq_json}
        rowcount_dict.update(rowcount_dict1)

   #print("rowcount_dict ", rowcount_dict)

    columncount_dict = {}
    for selected_column in col_name:

        freq_vals = df[selected_column].value_counts()

        df_Freq = pd.DataFrame(columns=['Values'])
        # df_Freq['Column']=df.columns
        df_Freq['Values'] = freq_vals
        df_Freq = df_Freq.reset_index().rename(columns={'index': 'Columns'})

       #print('df_Freq colnames', df_Freq.columns)

        col_categories = df_Freq['Columns']

       #print('col_categories col_categories===', col_categories)

        df_Freq_json = dict(col_categories)

       #print('df_Freq shapeee', len(df_Freq))

        if selected_column == col_name[0]:
            temp_dict = {len(df_Freq): 'All'}

            df_Freq_json.update(temp_dict)

       #print("df_Freq_json df_Freq_json updatedd colll", df_Freq_json)

        columncount_dict1 = {selected_column: df_Freq_json}
        columncount_dict.update(columncount_dict1)

   #print("columncount_dict ", columncount_dict)

    return rowcount_dict,columncount_dict


def col_class_display():

        filename = "BLS141_Test_Brand.json"
        selected_column = 'Age_Group'

        df=pd.read_json(settings.PYTHONPATH+filename, orient='records',lines=True)

        freq_vals = df[selected_column].value_counts()
        df_Categories = freq_vals.reset_index().rename(columns={'index': 'Categories'})

       #print("Categories",df_Categories)

        # Categories=df_Categories['Categories']
        Categories=df_Categories['Categories'].to_dict()

        Categories_dict={selected_column:Categories}

       #print('Categories_dict',Categories_dict)

        return Categories_dict

