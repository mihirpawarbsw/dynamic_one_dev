import re
import json
import os
import subprocess
import warnings

import polars as pl

from matplotlib import pyplot as plt

warnings.filterwarnings('ignore')
# import pandasql as ps
import numpy
import pandas as pd
import numpy as np
import os,json
import time
from scipy import stats

from itertools import combinations

import openpyxl
from openpyxl.worksheet.dimensions import ColumnDimension, DimensionHolder
from openpyxl.utils import get_column_letter
from main_dashboard.bcst_sales_data_constants import *

# from bcst_sales_crosstab_calculation_functions import *
# from bcst_sales_crosstab_calculation_seperated_functions import *
# from bcst_sales_crosstab_table_resp import *
# from bcst_sales_response_functions import *

# PYTHONPATH = r"C:\Users\MihirPawar\Desktop\Python Project BSW\Python Files1\ccv_tool\ccv_survey_data\electrolux\\"
# PYTHONPATH = r"C:\Mihir_Python_Projects\BCST_Tool_Core_Python_Logic\ccv_tool_Sales\BCST_Sales_Data\\"

# rename_input_cols_dict = {'Volume_Sales':'Volume','YA_(Volume_Sales)':'Volume YA','PP_(Volume_Sales)':
#                           'Volume PP','Value_Sales_(JPY)':'Value (JPY)','YA_(Value_Sales_(JPY))':'Value YA (JPY)','PP_(Value_Sales_(JPY))':
#                           'Value PP (JPY)','TDP_TY':'TDP TY','YA_(TDP_TY)':'TDP YA','PP_(TDP_TY)':'TDP PP','Wtd_Dist_(Max)':'WD',
#                           'PP_(Wtd_Dist_(Max))':'WD PP','YA_(Wtd_Dist_(Max))':'WD YA'}

rename_input_cols_dict = {'Volume':'Volume','Volume_YA':'Volume YA','Volume_PP':
                          'Volume PP','Sales_(JPY)':'Sales (JPY)','Sales_YA_(JPY)':'Sales YA (JPY)','Sales_PP_(JPY)':
                          'Sales PP (JPY)','TDP_TY':'TDP TY','TDP_YA':'TDP YA','TDP_PP':'TDP PP','WD':'WD',
                          'WD_PP':'WD PP','WD_YA':'WD YA',
                          'ND':'ND',
                          'ND_PP':'ND PP','ND_YA':'ND YA'}
#
derived_metrics_grouping_key_val_full = {'Volume':['Volume','Volume YA', 'Volume PP','Volume Share',
                            'Volume Share YA', 'Volume Share PP', 'Volume Growth vs YA','Volume Growth vs PP',
                            'Volume Share bps Chg. vs YA', 'Volume Share bps Chg. vs PP'],

                            'Sales':['Sales (JPY)','Sales YA (JPY)','Sales PP (JPY)','Sales Share',
                            'Sales Share YA', 'Sales Share PP', 'Sales Growth vs YA','Sales Growth vs PP',
                            'Sales Share bps Chg. vs YA', 'Sales Share bps Chg. vs PP'],

                            'TDP':['TDP TY','TDP YA', 'TDP PP','TDP Share','TDP Share YA','TDP Share PP',
                                   'TDP Growth vs YA','TDP Growth vs PP','TDP Share bps Chg. vs YA','TDP Share bps Chg. vs PP'],

                            'WD':['WD','WD YA','WD PP','WD bps Chg. vs YA','WD bps Chg. vs PP'],
                            'ND':['ND','ND YA','ND PP','ND bps Chg. vs YA','ND bps Chg. vs PP'],

                            'Avg Price':['Avg Price','Avg Price YA','Avg Price PP','Avg Price Growth vs YA','Avg Price Growth vs PP'],

                            'API':['API','API YA','API PP','API Chg. Vs YA','API Chg. Vs PP']}


derived_metrics_grouping_key_val = {'Volume':['Volume','Volume YA', 'Volume PP'],

                            'Sales':['Sales (JPY)','Sales YA (JPY)','Sales PP (JPY)'],

                            'TDP':['TDP TY','TDP YA', 'TDP PP'],

                            'WD':['WD','WD YA','WD PP'],
                            'ND':['ND','ND YA','ND PP'],

                            'Avg Price':['Avg Price','Avg Price YA','Avg Price PP'],

                            'API':['API','API YA','API PP']}

derived_metrics_grouping = ['Volume','Sales','TDP','WD','ND','Avg Price','API']

def measures_facts_groups(selected_weight_column22,measure_selected_key_val_resp,crosstab_function_name):
    print('======+++++=========')
    print('selected_weight_column22==',selected_weight_column22)
    print('measure_selected_key_val_resp==',measure_selected_key_val_resp)
    print('crosstab_function_name==',crosstab_function_name)
    print('======+++++=========')

    lst_measures = []
    lst_measures_vals = []
    dict_selected_measures_lst = {}

    # val_dict_final = list(dict_table.values())[0]
    # val_dict_final = selected_weight_column22

    if crosstab_function_name == 'crosstab1':

        for dict_val in selected_weight_column22:
            print('dict_val==', dict_val)

            if dict_val in derived_metrics_grouping_key_val_full.keys():
                print('==dict_val 39', dict_val)
                lst_measures.append(dict_val)

                values_of_dict_val = derived_metrics_grouping_key_val_full[dict_val]
                lst_measures_vals.extend(values_of_dict_val)

                dict_selected_measures = {dict_val:values_of_dict_val}
                # dict_selected_measures_lst.append(dict_selected_measures)
                dict_selected_measures_lst.update(dict_selected_measures)

        print('lst_measures==', lst_measures)
        print('lst_measures_vals==', lst_measures_vals)

    elif crosstab_function_name == 'crosstab2':
        print('measure_selected_key_val_resp==114',measure_selected_key_val_resp)
 
        measure_selected_key_val_LIST = list(measure_selected_key_val_resp.keys())
        print('measure_selected_key_val_LIST==',measure_selected_key_val_LIST)
        for dict_val in measure_selected_key_val_LIST:
            print('dict_val==', dict_val)

            if dict_val in measure_selected_key_val_resp.keys():
                print('==dict_val 39', dict_val)
                lst_measures.append(dict_val)

                values_of_dict_val = measure_selected_key_val_resp[dict_val]
                lst_measures_vals.extend(values_of_dict_val)

                dict_selected_measures = {dict_val:values_of_dict_val}
                # dict_selected_measures_lst.append(dict_selected_measures)
                dict_selected_measures_lst.update(dict_selected_measures)

    print('lst_measures 123',lst_measures)
    print('lst_measures_vals 124',lst_measures_vals)
    print('dict_selected_measures_lst 125',dict_selected_measures_lst)

    return lst_measures,lst_measures_vals,dict_selected_measures_lst

def add_groupings_measures(dict_table,measure_selected_key_val_resp,crosstab_function_name):

    val_dict_final = list(dict_table.values())[0]

    lst_measures = []
    lst_measures_vals = []
    dict_selected_measures_lst = {}

    if crosstab_function_name == 'crosstab1':
        for dict_val in val_dict_final:
            print('dict_val==', dict_val)

            if dict_val in derived_metrics_grouping_key_val.keys():
                print('==dict_val 39', dict_val)
                lst_measures.append(dict_val)

                values_of_dict_val = derived_metrics_grouping_key_val[dict_val]
                lst_measures_vals.extend(values_of_dict_val)

                dict_selected_measures = {dict_val:values_of_dict_val}
                # dict_selected_measures_lst.append(dict_selected_measures)
                dict_selected_measures_lst.update(dict_selected_measures)

    elif crosstab_function_name == 'crosstab2':
        for dict_val in val_dict_final:
            print('dict_val==', dict_val)

            if dict_val in measure_selected_key_val_resp.keys():
                print('==dict_val 39', dict_val)
                lst_measures.append(dict_val)

                values_of_dict_val = measure_selected_key_val_resp[dict_val]
                lst_measures_vals.extend(values_of_dict_val)

                dict_selected_measures = {dict_val:values_of_dict_val}
                # dict_selected_measures_lst.append(dict_selected_measures)
                dict_selected_measures_lst.update(dict_selected_measures)


    # for item in lst_measures:
    #     if item in val_dict_final:
    #         val_dict_final.remove(item)
    #         val_dict_final.extend(lst_measures_vals)

    val_dict_final = [item for item in val_dict_final if item not in lst_measures]
    val_dict_final.extend(lst_measures_vals)

    print('lst_measures---45', lst_measures)
    print('lst_measures_vals---52', lst_measures_vals)

    key_str = ','.join([str(key) for key in dict_table.keys()])
    # exit('edff')

    # dict_table[key_str] = list(set(val_dict_final))
    dict_table[key_str] = val_dict_final

    # for key, values in dict_table.items():
    #     unique_values = list(set(values))  # Convert values to set to remove duplicates, then back to list
    #     dict_table[key] = unique_values
    print('DICT TABLE FINAL',dict_table)

    return dict_table,lst_measures_vals,val_dict_final,dict_selected_measures_lst

######### BRAND SALES INDEX NEW LOGIC - 23-09-2024 ##############################
def derived_measures_after_crosstab_seperated_logic(df_time, filtered_df,base_sales_index_colname,row_name,col_name,measure_row_column_position,cagr_power_val,brand_sales_index_value_flag):
    ####################################### Sales ##########################################
    cy_cols_lst = df_time.filter(like='CY').columns.tolist()
    ya_cols_lst = df_time.filter(like='YA').columns.tolist()

    try:
        replace_values = {-np.inf: 0, np.inf: 0, 'null': 0, np.nan: 0}
        df_time.replace(replace_values, inplace=True)
        df_time.fillna(0,inplace=True)
    except:
        pass

    print('cy_cols_lst',cy_cols_lst)
    print('ya_cols_lst',ya_cols_lst)

    if (measure_row_column_position == 'measure_in_column') and (len(row_name) == 1) and ((brand_var_name in row_name)):
        df_time_lst22 = []
        for cy_col_loop in range(len(cy_cols_lst)):
            print('21333',cy_col_loop)
            sales_col_cy = cy_cols_lst[cy_col_loop]
            sales_col_ya = ya_cols_lst[cy_col_loop]

            cy_cols_modified = sales_col_cy.rsplit('_', 1)[0]
            cy_cols_modified = cy_cols_modified + '_'
            ya_cols_modified = sales_col_ya.rsplit('_', 1)[0]
            ya_cols_modified = ya_cols_modified + '_'

            print('cy_cols_modified',cy_cols_modified)
            print('ya_cols_modified',ya_cols_modified)

            ######################### BRAND SALES INDEX - 20-09-2024 #################################
            ######################### BRAND SALES INDEX - 20-09-2024 #################################
            df_time_bsi = df_time.copy()
            base_index_colname_df = df_time_bsi[df_time_bsi.index.get_level_values(1) == base_sales_index_colname]

            # base_index_colname_df.to_excel('base_index_colname_df.xlsx')

            print('df_time_bsi----285')
            sales_base_index_colname_val = base_index_colname_df[sales_col_cy].values[0]

            if (brand_var_name in row_name):
                base_colname_brand_or_product = 'Brand Sales Index'

            df_time_bsi[cy_cols_modified + 'CY ' + base_colname_brand_or_product] = (df_time_bsi[sales_col_cy] / sales_base_index_colname_val) * 100

            df_time_bsi = df_time_bsi.loc[:, df_time_bsi.columns.str.contains("Brand Sales Index")]

            replace_values = {-np.inf: 0, np.inf: 0, 'null': 0, np.nan: 0}
            df_time_bsi.replace(replace_values, inplace=True)

            # name_unique_bsi = 'df_time_bsi_' + str(cy_col_loop) + '.xlsx'
            # df_time_bsi.to_excel(name_unique_bsi)
            df_time_lst22.append(df_time_bsi)

        df_time_bsi_final2 = pd.concat(df_time_lst22,axis=1)
        # df_time_bsi_final2.to_excel('df_time_bsi_final.xlsx')

        df_time_bsi_final22 = pd.concat([df_time,df_time_bsi_final2],axis=1)
        # df_time_bsi_final22.to_excel('df_time_with_bsi.xlsx')

        ######################### BRAND SALES INDEX - 20-09-2024 #################################
        ######################### BRAND SALES INDEX - 20-09-2024 #################################
        if brand_sales_index_value_flag == 'No':

            #removed the row where compare with is not in selected brands
            df_time_bsi_final22 = df_time_bsi_final22[~df_time_bsi_final22.index.get_level_values(1).isin([base_sales_index_colname])]
            df_time_bsi_final22 = df_time_bsi_final22[~df_time_bsi_final22.index.get_level_values(1).isin(['Grand Total'])]

            # df_time_bsi_final22.to_excel('removed_compare.xlsx')

            ########## recalculate Grand Total ######################################
            # Calculate the Grand Total
            grand_total = df_time_bsi_final22.groupby(level=0).sum()

            # Create the new MultiIndex for the Grand Total row
            grand_total.index = pd.MultiIndex.from_product([grand_total.index, ['Grand Total']], names=['level_0', 'level_1'])

            # Concatenate the Grand Total row to df_time
            df_time_bsi_final22 = pd.concat([df_time_bsi_final22, grand_total])
            ########## recalculate Grand Total ######################################

            df_time_bsi_final22 = df_time_bsi_final22.loc[:, ~df_time_bsi_final22.columns.duplicated(keep='last')].copy()

            # df_time_bsi_final22.to_excel('recalculated_grand_total.xlsx')
            # exit('df_time_bsi_final22')

            df_time = df_time_bsi_final22.copy()

        else:
            df_time = df_time_bsi_final22.copy()

    else:
        df_time = df_time.copy()

    try:
        replace_values = {-np.inf: 0, np.inf: 0, 'null': 0, np.nan: 0}
        df_time.replace(replace_values, inplace=True)
        df_time.fillna(0,inplace=True)
    except:
        pass
    # df_time.to_excel('df_time_bSI.xlsx')
    #####################################################################################################
    df_time_others_lst = []
    for cy_col_loop in range(len(cy_cols_lst)):
        sales_col_cy = cy_cols_lst[cy_col_loop]
        sales_col_ya = ya_cols_lst[cy_col_loop]

        cy_cols_modified = sales_col_cy.rsplit('_', 1)[0]
        cy_cols_modified = cy_cols_modified + '_'
        ya_cols_modified = sales_col_ya.rsplit('_', 1)[0]
        ya_cols_modified = ya_cols_modified + '_'

        filtered_df = df_time[df_time.index.get_level_values(1).isin(['Grand Total'])]
        # filtered_df.to_excel('filtered_dfttt.xlsx')

        try:
            Value_Sales = filtered_df[sales_col_cy].values[0]
            YA_Value_Sales = filtered_df[sales_col_ya].values[0]
        except:
            Value_Sales = filtered_df[sales_col_cy].values[0][0]
            YA_Value_Sales = filtered_df[sales_col_ya].values[0][0]

        print('Value_Sales',Value_Sales)
        print('YA_Value_Sales',YA_Value_Sales)

        df_time[cy_cols_modified + 'Share% CY'] = (df_time[sales_col_cy] / Value_Sales) * 100
        df_time[cy_cols_modified + 'Share% YA'] = (df_time[sales_col_ya] / YA_Value_Sales) * 100

        df_time[cy_cols_modified + 'GR% vs YA'] = (df_time[sales_col_cy] - df_time[sales_col_ya]) / df_time[
            sales_col_ya] * 100

        # df_time[cy_cols_modified + '%Pts vs YA'] = (df_time[cy_cols_modified + 'Share% CY'] - df_time[cy_cols_modified + 'Share% YA'])

        # df_time[cy_cols_modified + 'BPS vs YA'] = df_time[cy_cols_modified + '%Pts vs YA'] * 100

        df_time[cy_cols_modified + 'BPS vs YA'] = (df_time[cy_cols_modified + 'Share% CY'] - df_time[cy_cols_modified + 'Share% YA']) * 100

        df_time[cy_cols_modified + 'Share% CY'] = df_time[cy_cols_modified + 'Share% CY'].astype(str) + '%'

        df_time[cy_cols_modified + 'Share% YA'] = df_time[cy_cols_modified + 'Share% YA'].astype(str) + '%'

        df_time[cy_cols_modified + 'GR% vs YA'] = df_time[cy_cols_modified + 'GR% vs YA'].astype(str) + '%'

        df_time_others_lst.append(df_time)

    df_time = pd.concat(df_time_others_lst,axis=1)
    df_time = df_time.loc[:,~df_time.columns.duplicated(keep='last')].copy()
    # df_time.to_excel('df_time_others_lst.xlsx')
    ##################### CAGR - 29-08-2024 #####################################
    cagr_df_lst = []
    CAGR_str = 'CAGR% CY vs YA'
    for cy_col_loop in range(len(cy_cols_lst)):
        sales_col_cy = cy_cols_lst[cy_col_loop]
        sales_col_ya = ya_cols_lst[cy_col_loop]

        cy_cols_modified = sales_col_cy.rsplit('_', 1)[0]
        cy_cols_modified = cy_cols_modified + '_'
        ya_cols_modified = sales_col_ya.rsplit('_', 1)[0]
        ya_cols_modified = ya_cols_modified + '_'
        print('cagr_power_val 246',cagr_power_val)

        if cagr_power_val != 989898:

            if cagr_power_val > 0:
                # CAGR_str = 'CAGR% CY vs YA'
                df_time[cy_cols_modified + CAGR_str] = (((df_time[sales_col_cy] / df_time[sales_col_ya]) ** (1 / cagr_power_val)) - 1)* 100
                df_time[cy_cols_modified + CAGR_str] = df_time[cy_cols_modified + CAGR_str].astype(str) + '%'
                cagr_df_lst.append(df_time)

            elif cagr_power_val < 0:
                # CAGR_str = 'CAGR% YA vs CY'
                cagr_power_val = abs(cagr_power_val)
                df_time[cy_cols_modified + CAGR_str] = (((df_time[sales_col_ya] / df_time[sales_col_cy]) ** (1 / cagr_power_val)) - 1)* 100
                df_time[cy_cols_modified + CAGR_str] = df_time[cy_cols_modified + CAGR_str].astype(str) + '%'
                cagr_df_lst.append(df_time)

            elif cagr_power_val == 0:
                # CAGR_str = 'CAGR% CY vs YA'
                df_time[cy_cols_modified + CAGR_str] = 0
                df_time[cy_cols_modified + CAGR_str] = '0%'
                cagr_df_lst.append(df_time)

        elif cagr_power_val == 989898:
            # CAGR_str = 'CAGR% CY vs YA'
            # df_time[cy_cols_modified + CAGR_str] = '--%'
            df_time[cy_cols_modified + CAGR_str] = 'cagr_none'
            cagr_df_lst.append(df_time)

    df_time = pd.concat(cagr_df_lst,axis=1)
    df_time = df_time.loc[:,~df_time.columns.duplicated(keep='last')].copy()
    # df_time.to_excel('df_time_CAGR.xlsx')
    # exit('ere')
    ##################### CAGR - 29-08-2024 #####################################

    ################################### RANK - 09-05-2024 ###################################
    rank_df_lst = []
    CAGR_str = 'CAGR% CY vs YA'
    for cy_col_loop in range(len(cy_cols_lst)):
        sales_col_cy = cy_cols_lst[cy_col_loop]
        sales_col_ya = ya_cols_lst[cy_col_loop]

        cy_cols_modified = sales_col_cy.rsplit('_', 1)[0]
        cy_cols_modified = cy_cols_modified + '_'
        ya_cols_modified = sales_col_ya.rsplit('_', 1)[0]
        ya_cols_modified = ya_cols_modified + '_'
        print('cagr_power_val 246',cagr_power_val)
        #Add rank_cy column
        if 'Grand Total' not in df_time.index.get_level_values(0):
            df_time[cy_cols_modified + 'rank_cy'] = df_time[sales_col_cy].rank(ascending=False)
            df_time[cy_cols_modified + 'rank_cy'] = df_time[cy_cols_modified + 'rank_cy'] - 1

            # # Add rank_ya column
            df_time[cy_cols_modified + 'rank_ya'] = df_time[sales_col_ya].rank(ascending=False)
            df_time[cy_cols_modified + 'rank_ya'] = df_time[cy_cols_modified + 'rank_ya'] - 1
        else:
            df_time[cy_cols_modified + 'rank_cy'] = df_time[sales_col_cy].rank(ascending=False)
            df_time[cy_cols_modified + 'rank_cy'] = df_time[cy_cols_modified + 'rank_cy'] - 2

            # # Add rank_ya column
            df_time[cy_cols_modified + 'rank_ya'] = df_time[sales_col_ya].rank(ascending=False)
            df_time[cy_cols_modified + 'rank_ya'] = df_time[cy_cols_modified + 'rank_ya'] - 2
        ###############################################################################################
        ###############################################################################################
        # First, check for non-finite values and fill them with 0 (or another appropriate value)
        df_time[cy_cols_modified + 'rank_ya'] = df_time[cy_cols_modified + 'rank_ya'].fillna(0).replace([float('inf'), float('-inf')], 0)
        df_time[cy_cols_modified + 'rank_cy'] = df_time[cy_cols_modified + 'rank_cy'].fillna(0).replace([float('inf'), float('-inf')], 0)
        # Calculate Rank column (difference between rank_ya and rank_cy)
        df_time[cy_cols_modified + 'Rank Difference'] = df_time[cy_cols_modified + 'rank_ya'].astype(int) - df_time[cy_cols_modified + 'rank_cy'].astype(int)

        # Create RANK column
        df_time[cy_cols_modified + 'CY' +' Rank'] = df_time[cy_cols_modified + 'rank_cy'].astype(str) + ' (' + df_time[cy_cols_modified + 'Rank Difference'].astype(str) + ')'

        ############ format rank function ###########################
        # Custom function to format the rank
        def format_rank(row):
            rank_cy = int(row[cy_cols_modified + 'rank_cy'])
            rank_difference = int(row[cy_cols_modified + 'Rank Difference'])
            if rank_difference == 0:
                return str(rank_cy)
            elif rank_difference > 0:
                return f"{rank_cy} (↑{abs(rank_difference)})"
            else:
                return f"{rank_cy} (↓{abs(rank_difference)})"
        ############ format rank function ###########################
        df_time[cy_cols_modified + 'CY' + ' Rank'] = df_time.apply(format_rank, axis=1)
        print('df_time colss 279',df_time.columns)

        ##################### CODE TO RENAME GRAND TOTAL RANK WITH -- #######
        df_time_gt = df_time[df_time.index.get_level_values(1) == 'Grand Total']

        if len(df_time_gt) > 0:
            df_time = df_time[df_time.index.get_level_values(1) != 'Grand Total']

            df_time_gt[cy_cols_modified + 'rank_cy'] = '--'
            df_time_gt[cy_cols_modified + 'rank_ya'] = '--'
            df_time_gt[cy_cols_modified + 'Rank Difference'] = '--'
            df_time_gt[cy_cols_modified + 'CY' + ' Rank'] = '--'
            # df_time_gt.to_excel('df_time_gt.xlsx')

            df_time = pd.concat([df_time,df_time_gt],axis=0)
            rank_df_lst.append(df_time)
        else:
            df_time = df_time.copy()
            rank_df_lst.append(df_time)

    df_time = pd.concat(rank_df_lst,axis=1)
    df_time = df_time.loc[:,~df_time.columns.duplicated(keep='last')].copy()
    df_time.to_excel('df_time_RANK.xlsx')
    ##################### CODE TO RENAME GRAND TOTAL RANK WITH -- #######

    ############################# ADDED ON 19-06-2024 ##########################################
    FINAL_Lst = []
    for cy_col_loop in range(len(cy_cols_lst)):
        sales_col_cy = cy_cols_lst[cy_col_loop]
        sales_col_ya = ya_cols_lst[cy_col_loop]

        cy_cols_modified = sales_col_cy.rsplit('_', 1)[0]
        cy_cols_modified = cy_cols_modified + '_'
        ya_cols_modified = sales_col_ya.rsplit('_', 1)[0]
        ya_cols_modified = ya_cols_modified + '_'
        print('cagr_power_val 246',cagr_power_val)
        if (measure_row_column_position == 'measure_in_column') and (len(row_name) == 1) and ((brand_var_name in row_name)):


            df_time.loc[(slice(None), 'Grand Total'), df_time.columns.str.contains("Brand Sales Index")] = '--'

            df_time2 = df_time.copy()
            df_time2 = df_time2[[cy_cols_modified + 'CY' + ' Rank',sales_col_cy,sales_col_ya,cy_cols_modified + 'GR% vs YA',cy_cols_modified + 'Share% CY',cy_cols_modified + 'Share% YA',cy_cols_modified + 'BPS vs YA',cy_cols_modified + CAGR_str,cy_cols_modified + 'CY ' + base_colname_brand_or_product]]
            FINAL_Lst.append(df_time2)
        ############################# ADDED ON 19-06-2024 ##########################################

        else:
            df_time2 = df_time.copy()
            df_time2 = df_time2[[cy_cols_modified + 'CY' + ' Rank',sales_col_cy,sales_col_ya,cy_cols_modified + 'GR% vs YA',cy_cols_modified + 'Share% CY',cy_cols_modified + 'Share% YA',cy_cols_modified + 'BPS vs YA',cy_cols_modified + CAGR_str]]
            FINAL_Lst.append(df_time2)

    df_time_all = pd.concat(FINAL_Lst,axis=1)

    # df_time_all.to_excel('df_time_all.xlsx')
    return df_time_all
######### BRAND SALES INDEX NEW LOGIC - 23-09-2024 ##############################

######### BRAND SALES INDEX NEW LOGIC - 23-09-2024 ##############################
def derived_measures_after_crosstab(df_time, filtered_df,base_sales_index_colname,row_name,col_name,measure_row_column_position,cagr_power_val,brand_sales_index_value_flag):
    ####################################### Sales ##########################################
    cy_cols_lst = df_time.filter(like='CY').columns.tolist()
    ya_cols_lst = df_time.filter(like='YA').columns.tolist()

    try:
        replace_values = {-np.inf: 0, np.inf: 0, 'null': 0, np.nan: 0}
        df_time.replace(replace_values, inplace=True)
        df_time.fillna(0,inplace=True)
    except:
        pass

    print('cy_cols_lst',cy_cols_lst)
    print('ya_cols_lst',ya_cols_lst)

    if (measure_row_column_position == 'measure_in_column') and (len(row_name) == 1) and ((brand_var_name in row_name)):
        df_time_lst22 = []
        for cy_col_loop in range(len(cy_cols_lst)):
            print('21333',cy_col_loop)
            sales_col_cy = cy_cols_lst[cy_col_loop]
            sales_col_ya = ya_cols_lst[cy_col_loop]

            cy_cols_modified = sales_col_cy.rsplit('_', 1)[0]
            cy_cols_modified = cy_cols_modified + '_'
            ya_cols_modified = sales_col_ya.rsplit('_', 1)[0]
            ya_cols_modified = ya_cols_modified + '_'

            print('cy_cols_modified',cy_cols_modified)
            print('ya_cols_modified',ya_cols_modified)

            ######################### BRAND SALES INDEX - 20-09-2024 #################################
            ######################### BRAND SALES INDEX - 20-09-2024 #################################
            df_time_bsi = df_time.copy()
            base_index_colname_df = df_time_bsi[df_time_bsi.index.get_level_values(1) == base_sales_index_colname]

            # base_index_colname_df.to_excel('base_index_colname_df.xlsx')

            print('df_time_bsi----285')
            sales_base_index_colname_val = base_index_colname_df[sales_col_cy].values[0]

            if (brand_var_name in row_name):
                base_colname_brand_or_product = 'Brand Sales Index'

            df_time_bsi[cy_cols_modified + 'CY ' + base_colname_brand_or_product] = (df_time_bsi[sales_col_cy] / sales_base_index_colname_val) * 100

            df_time_bsi = df_time_bsi.loc[:, df_time_bsi.columns.str.contains("Brand Sales Index")]

            replace_values = {-np.inf: 0, np.inf: 0, 'null': 0, np.nan: 0}
            df_time_bsi.replace(replace_values, inplace=True)

            # name_unique_bsi = 'df_time_bsi_' + str(cy_col_loop) + '.xlsx'
            # df_time_bsi.to_excel(name_unique_bsi)
            df_time_lst22.append(df_time_bsi)

        df_time_bsi_final2 = pd.concat(df_time_lst22,axis=1)
        # df_time_bsi_final2.to_excel('df_time_bsi_final.xlsx')

        df_time_bsi_final22 = pd.concat([df_time,df_time_bsi_final2],axis=1)
        # df_time_bsi_final22.to_excel('df_time_with_bsi.xlsx')

        ######################### BRAND SALES INDEX - 20-09-2024 #################################
        ######################### BRAND SALES INDEX - 20-09-2024 #################################
        if brand_sales_index_value_flag == 'No':
            df_time_bsi_final33 = df_time_bsi_final22.copy()
            df_time_bsi_22 = df_time_bsi_final22[df_time_bsi_final22.index.get_level_values(1).isin([base_sales_index_colname])]

            if 'Total (Among Displayed)' in df_time_bsi_final33.index.get_level_values(1):
                df_time_among_total = df_time_bsi_final22[df_time_bsi_final22.index.get_level_values(1).isin(['Total (Among Displayed)'])]
                # df_time_among_total.to_excel('df_time_among_total.xlsx')

            df_time_grand_total = df_time_bsi_final22[df_time_bsi_final22.index.get_level_values(1).isin(['Grand Total'])]

            # df_time_bsi_22.to_excel('df_time_bsi_22.xlsx')
            # df_time_grand_total.to_excel('df_time_grand_total.xlsx')

            df_time_bsi_final22 = df_time_bsi_final22[~df_time_bsi_final22.index.get_level_values(1).isin([base_sales_index_colname,'Grand Total'])]

            if 'Total (Among Displayed)' in df_time_bsi_final22.index.get_level_values(1):
                df_time_bsi_final22 = df_time_bsi_final22[~df_time_bsi_final22.index.get_level_values(1).isin(['Total (Among Displayed)'])]

            ########## recalculate Grand Total ######################################
            if 'Total (Among Displayed)' not in df_time_bsi_final33.index.get_level_values(1):
                # Calculate the Grand Total
                grand_total = df_time_bsi_final22.groupby(level=0).sum()

                # Create the new MultiIndex for the Grand Total row
                grand_total.index = pd.MultiIndex.from_product([grand_total.index, ['Grand Total']], names=['level_0', 'level_1'])

                # Concatenate the Grand Total row to df_time
                df_time_bsi_final22 = pd.concat([df_time_bsi_final22, grand_total])
                ########## recalculate Among Grand Total ######################################

                df_time_bsi_final22 = df_time_bsi_final22.loc[:, ~df_time_bsi_final22.columns.duplicated(keep='last')].copy()

                # df_time_bsi_final22.to_excel('recalculated_grand_total.xlsx')
                # exit('df_time_bsi_final22')

                df_time = df_time_bsi_final22.copy()

            elif 'Total (Among Displayed)' in df_time_bsi_final33.index.get_level_values(1):
                ################ RECALCULATE Grand Total ###############################
                # recalc_gt = pd.DataFrame(df_time_grand_total.values - df_time_bsi_22.values, 
                #              columns=df_time_grand_total.columns)
                # recalc_gt.to_excel('recalc_gt.xlsx')
                
                # new_index_gtt = pd.MultiIndex.from_product([df_time_bsi_22.index.get_level_values(0), ['Grand Total']],names=['level_0', 'level_1'])

                # recalc_gt.index = new_index_gtt

                ################ RECALCULATE Grand Total ###############################
                # Calculate the Among Grand Total
                amng_grand_total = df_time_bsi_final22.groupby(level=0).sum()

                # Create the new MultiIndex for the Among Grand Total row
                amng_grand_total.index = pd.MultiIndex.from_product([amng_grand_total.index, ['Total (Among Displayed)']], names=['level_0', 'level_1'])

                # Concatenate the Among Grand Total row to df_time
                df_time_bsi_final22 = pd.concat([df_time_bsi_final22, amng_grand_total,df_time_grand_total])

                #REPLACE VALUES OF 'Brand Sales Index' IN COLUMN AND 'Total (Among Displayed)' IN ROW WITH "--"
                #Step 1: Select rows where index level 1 is 'Total (Among Displayed)'
                row_condition = df_time_bsi_final22.index.get_level_values(1) == 'Total (Among Displayed)'

                #Step 2: Select columns where column name is 'Brand Sales Index' using .isin()
                column_condition = df_time_bsi_final22.columns.str.contains('Brand Sales Index')
                #Step 3: Assign '--' to the selected locations
                df_time_bsi_final22.loc[row_condition, column_condition] = '--'

                #REPLACE VALUES OF 'Brand Sales Index' IN COLUMN AND 'Grand Total' IN ROW WITH "--"
                ########## recalculate Among Grand Total ######################################

                df_time_bsi_final22 = df_time_bsi_final22.loc[:, ~df_time_bsi_final22.columns.duplicated(keep='last')].copy()

                # df_time_bsi_final22.to_excel('recalculated_grand_total.xlsx')
                # exit('df_time_bsi_final22')

                df_time = df_time_bsi_final22.copy()

        else:
            df_time = df_time_bsi_final22.copy()

    else:
        df_time = df_time.copy()

    try:
        replace_values = {-np.inf: 0, np.inf: 0, 'null': 0, np.nan: 0}
        df_time.replace(replace_values, inplace=True)
        df_time.fillna(0,inplace=True)
    except:
        pass

    df_time_lst = []
    for cy_col_loop in range(len(cy_cols_lst)):
        sales_col_cy = cy_cols_lst[cy_col_loop]
        sales_col_ya = ya_cols_lst[cy_col_loop]

        cy_cols_modified = sales_col_cy.rsplit('_', 1)[0]
        cy_cols_modified = cy_cols_modified + '_'
        ya_cols_modified = sales_col_ya.rsplit('_', 1)[0]
        ya_cols_modified = ya_cols_modified + '_'

        filtered_df = df_time[df_time.index.get_level_values(1).isin(['Grand Total'])]
        # filtered_df.to_excel('filtered_dfttt.xlsx')

        try:
            Value_Sales = filtered_df[sales_col_cy].values[0]
            YA_Value_Sales = filtered_df[sales_col_ya].values[0]
        except:
            Value_Sales = filtered_df[sales_col_cy].values[0][0]
            YA_Value_Sales = filtered_df[sales_col_ya].values[0][0]

        print('Value_Sales',Value_Sales)
        print('YA_Value_Sales',YA_Value_Sales)

        df_time[cy_cols_modified + 'Share% CY'] = (df_time[sales_col_cy] / Value_Sales) * 100
        df_time[cy_cols_modified + 'Share% YA'] = (df_time[sales_col_ya] / YA_Value_Sales) * 100

        df_time[cy_cols_modified + 'GR% vs YA'] = (df_time[sales_col_cy] - df_time[sales_col_ya]) / df_time[
            sales_col_ya] * 100

        # df_time[cy_cols_modified + '%Pts vs YA'] = (df_time[cy_cols_modified + 'Share% CY'] - df_time[cy_cols_modified + 'Share% YA'])

        # df_time[cy_cols_modified + 'BPS vs YA'] = df_time[cy_cols_modified + '%Pts vs YA'] * 100

        df_time[cy_cols_modified + 'BPS vs YA'] = (df_time[cy_cols_modified + 'Share% CY'] - df_time[cy_cols_modified + 'Share% YA']) * 100

        df_time[cy_cols_modified + 'Share% CY'] = df_time[cy_cols_modified + 'Share% CY'].astype(str) + '%'

        df_time[cy_cols_modified + 'Share% YA'] = df_time[cy_cols_modified + 'Share% YA'].astype(str) + '%'

        df_time[cy_cols_modified + 'GR% vs YA'] = df_time[cy_cols_modified + 'GR% vs YA'].astype(str) + '%'

        ######################## added on 21-10-2024 - Growth Contribution ##############
        df_time[cy_cols_modified + 'Variance'] = (df_time[sales_col_cy] - df_time[sales_col_ya])
        # df_time.to_excel('df_time_VARIANCE.xlsx')
        df_time_variance_GT = df_time[df_time.index.get_level_values(1).isin(['Grand Total'])]
        df_time_variance_GT_value = df_time_variance_GT[cy_cols_modified + 'Variance'].values[0]

        # df_time_variance_GT_value = abs(df_time_variance_GT[cy_cols_modified + 'Variance'].values[0])
        # print('df_time_variance_GT_value 705=',df_time_variance_GT_value)
        # df_time_variance_GT.to_excel('df_time_variance_GT.xlsx')
        if df_time_variance_GT_value<0:
            print('if condition--710')
            df_time[cy_cols_modified + 'GR% Contribution'] = df_time[cy_cols_modified + 'Variance']/(-df_time_variance_GT_value)
        else:
            print('else condition--713')
            df_time[cy_cols_modified + 'GR% Contribution'] = df_time[cy_cols_modified + 'Variance']/df_time_variance_GT_value
        df_time[cy_cols_modified + 'GR% Contribution'] = df_time[cy_cols_modified + 'GR% Contribution']*100
        df_time[cy_cols_modified + 'GR% Contribution'] = df_time[cy_cols_modified + 'GR% Contribution'].astype(str) + '%'
        ######################## added on 21-10-2024 - Growth Contribution ##############

        ##################### CAGR - 29-08-2024 #####################################
        print('cagr_power_val 246',cagr_power_val)

        # if cagr_power_val != 989898:
        #     if cagr_power_val > 0:

        #         CAGR_str = 'CAGR% CY vs YA'
        #         df_time[cy_cols_modified + CAGR_str] = (((df_time[sales_col_cy] / df_time[sales_col_ya]) ** (1 / cagr_power_val)) - 1)* 100
        #         df_time[cy_cols_modified + CAGR_str] = df_time[cy_cols_modified + CAGR_str].astype(str) + '%'

        #     elif cagr_power_val < 0:
        #         CAGR_str = 'CAGR% YA vs CY'
        #         cagr_power_val = abs(cagr_power_val)
        #         df_time[cy_cols_modified + CAGR_str] = (((df_time[sales_col_ya] / df_time[sales_col_cy]) ** (1 / cagr_power_val)) - 1)* 100
        #         df_time[cy_cols_modified + CAGR_str] = df_time[cy_cols_modified + CAGR_str].astype(str) + '%'

        CAGR_str = 'CAGR% CY vs YA'
        if cagr_power_val != 989898:

            if cagr_power_val > 0:
                # CAGR_str = 'CAGR% CY vs YA'
                df_time[cy_cols_modified + CAGR_str] = (((df_time[sales_col_cy] / df_time[sales_col_ya]) ** (1 / cagr_power_val)) - 1)* 100
                df_time[cy_cols_modified + CAGR_str] = df_time[cy_cols_modified + CAGR_str].astype(str) + '%'

            elif cagr_power_val < 0:
                # CAGR_str = 'CAGR% YA vs CY'
                cagr_power_val = abs(cagr_power_val)
                df_time[cy_cols_modified + CAGR_str] = (((df_time[sales_col_ya] / df_time[sales_col_cy]) ** (1 / cagr_power_val)) - 1)* 100
                df_time[cy_cols_modified + CAGR_str] = df_time[cy_cols_modified + CAGR_str].astype(str) + '%'

            elif cagr_power_val == 0:
                # CAGR_str = 'CAGR% CY vs YA'
                df_time[cy_cols_modified + CAGR_str] = 0
                df_time[cy_cols_modified + CAGR_str] = '0%'

        elif cagr_power_val == 989898:
            # CAGR_str = 'CAGR% CY vs YA'
            # df_time[cy_cols_modified + CAGR_str] = '--%'
            df_time[cy_cols_modified + CAGR_str] = 'cagr_none'

        # df_time.to_excel('df_time_CAGR.xlsx')
        ##################### CAGR - 29-08-2024 #####################################

        ################################### RANK - 09-05-2024 ###################################
        #Add rank_cy column
        # df_time_gt = df_time[df_time.index.get_level_values(1) == 'Grand Total']
        # df_time = df_time[df_time.index.get_level_values(1) != 'Grand Total']

        GT_df = df_time[df_time.index.get_level_values(1).isin(['Grand Total', 'Total (Among Displayed)'])]
        df_time = df_time[~df_time.index.get_level_values(1).isin(['Grand Total', 'Total (Among Displayed)'])]
        
        if 'Grand Total' not in df_time.index.get_level_values(0):
            df_time[cy_cols_modified + 'rank_cy'] = df_time[sales_col_cy].rank(ascending=False)
            # df_time[cy_cols_modified + 'rank_cy'] = df_time[cy_cols_modified + 'rank_cy'] - 1

            # # Add rank_ya column
            df_time[cy_cols_modified + 'rank_ya'] = df_time[sales_col_ya].rank(ascending=False)
            # df_time[cy_cols_modified + 'rank_ya'] = df_time[cy_cols_modified + 'rank_ya'] - 1
        else:
            df_time[cy_cols_modified + 'rank_cy'] = df_time[sales_col_cy].rank(ascending=False)
            df_time[cy_cols_modified + 'rank_cy'] = df_time[cy_cols_modified + 'rank_cy'] - 1

            # # Add rank_ya column
            df_time[cy_cols_modified + 'rank_ya'] = df_time[sales_col_ya].rank(ascending=False)
            df_time[cy_cols_modified + 'rank_ya'] = df_time[cy_cols_modified + 'rank_ya'] - 1
        ###############################################################################################
        ###############################################################################################
        # First, check for non-finite values and fill them with 0 (or another appropriate value)
        df_time[cy_cols_modified + 'rank_ya'] = df_time[cy_cols_modified + 'rank_ya'].fillna(0).replace([float('inf'), float('-inf')], 0)
        df_time[cy_cols_modified + 'rank_cy'] = df_time[cy_cols_modified + 'rank_cy'].fillna(0).replace([float('inf'), float('-inf')], 0)
        # Calculate Rank column (difference between rank_ya and rank_cy)
        df_time[cy_cols_modified + 'Rank Difference'] = df_time[cy_cols_modified + 'rank_ya'].astype(int) - df_time[cy_cols_modified + 'rank_cy'].astype(int)

        # Create RANK column
        df_time[cy_cols_modified + 'CY' +' Rank'] = df_time[cy_cols_modified + 'rank_cy'].astype(str) + ' (' + df_time[cy_cols_modified + 'Rank Difference'].astype(str) + ')'

        ############ format rank function ###########################
        # Custom function to format the rank
        def format_rank(row):
            rank_cy = int(row[cy_cols_modified + 'rank_cy'])
            rank_difference = int(row[cy_cols_modified + 'Rank Difference'])
            if rank_difference == 0:
                return str(rank_cy)
            elif rank_difference > 0:
                return f"{rank_cy} (↑{abs(rank_difference)})"
            else:
                return f"{rank_cy} (↓{abs(rank_difference)})"
        ############ format rank function ###########################
        df_time[cy_cols_modified + 'CY' + ' Rank'] = df_time.apply(format_rank, axis=1)
        print('df_time colss 279',df_time.columns)

        df_time = pd.concat([df_time,GT_df],axis=0)

        ##################### CODE TO RENAME GRAND TOTAL RANK WITH -- #######
        df_time_gt = df_time[df_time.index.get_level_values(1) == 'Grand Total']

        if len(df_time_gt) > 0:
            df_time = df_time[df_time.index.get_level_values(1) != 'Grand Total']

            df_time_gt[cy_cols_modified + 'rank_cy'] = '--'
            df_time_gt[cy_cols_modified + 'rank_ya'] = '--'
            df_time_gt[cy_cols_modified + 'Rank Difference'] = '--'
            df_time_gt[cy_cols_modified + 'CY' + ' Rank'] = '--'
            # df_time_gt.to_excel('df_time_gt.xlsx')

            df_time = pd.concat([df_time,df_time_gt],axis=0)

        else:
            df_time = df_time.copy()
        ##################### CODE TO RENAME GRAND TOTAL RANK WITH -- #######

        ##################### CODE TO RENAME GRAND TOTAL RANK WITH -- #######
        df_time_tal = df_time[df_time.index.get_level_values(1) == 'Total (Among Displayed)']
        
        if len(df_time_tal) > 0:
            df_time = df_time[df_time.index.get_level_values(1) != 'Total (Among Displayed)']
            df_time_tal[cy_cols_modified + 'rank_cy'] = '--'
            df_time_tal[cy_cols_modified + 'rank_ya'] = '--'
            df_time_tal[cy_cols_modified + 'Rank Difference'] = '--'
            df_time_tal[cy_cols_modified + 'CY' + ' Rank'] = '--'
            # df_time_gt.to_excel('df_time_gt.xlsx')

            df_time = pd.concat([df_time,df_time_tal],axis=0)

        else:
            df_time = df_time.copy()
        ##################### CODE TO RENAME GRAND TOTAL RANK WITH -- #######

        ############################# ADDED ON 19-06-2024 ##########################################
        if (measure_row_column_position == 'measure_in_column') and (len(row_name) == 1) and ((brand_var_name in row_name)):

            df_time.loc[(slice(None), 'Grand Total'), df_time.columns.str.contains("Brand Sales Index")] = '--'

            df_time2 = df_time.copy()
            df_time2 = df_time2[[cy_cols_modified + 'CY' + ' Rank',sales_col_cy,sales_col_ya,cy_cols_modified + 'GR% vs YA',cy_cols_modified + 'GR% Contribution',cy_cols_modified + 'Share% CY',cy_cols_modified + 'Share% YA',cy_cols_modified + 'BPS vs YA',cy_cols_modified + CAGR_str,cy_cols_modified + 'CY ' + base_colname_brand_or_product]]

        ############################# ADDED ON 19-06-2024 ##########################################

        else:
            df_time2 = df_time.copy()
            df_time2 = df_time2[[cy_cols_modified + 'CY' + ' Rank',sales_col_cy,sales_col_ya,cy_cols_modified + 'GR% vs YA',cy_cols_modified + 'GR% Contribution',cy_cols_modified + 'Share% CY',cy_cols_modified + 'Share% YA',cy_cols_modified + 'BPS vs YA',cy_cols_modified + CAGR_str]]
        
        # df_time2.to_excel('df_time_VALUE.xlsx')
        df_time_lst.append(df_time2)

    df_time_all = pd.concat(df_time_lst,axis=1)

    # df_time_all.to_excel('df_time_all.xlsx')
    return df_time_all
######### BRAND SALES INDEX NEW LOGIC - 23-09-2024 ##############################

#################### NEW CODE - 11-03-2024 #####################################
def derived_measures_after_crosstab_OG_BRAND_SALES_INDEX_OLD(df_time, filtered_df,base_sales_index_colname,row_name,col_name,measure_row_column_position,cagr_power_val,brand_sales_index_value_flag):
    ####################################### Sales ##########################################
    cy_cols_lst = df_time.filter(like='CY').columns.tolist()
    ya_cols_lst = df_time.filter(like='YA').columns.tolist()

    print('cy_cols_lst',cy_cols_lst)
    print('ya_cols_lst',ya_cols_lst)

    df_time_lst = []
    for cy_col_loop in range(len(cy_cols_lst)):
        sales_col_cy = cy_cols_lst[cy_col_loop]
        sales_col_ya = ya_cols_lst[cy_col_loop]

        print('sales_col_cy',sales_col_cy)
        print('sales_col_ya',sales_col_ya)

        cy_cols_modified = sales_col_cy.rsplit('_', 1)[0]
        cy_cols_modified = cy_cols_modified + '_'
        ya_cols_modified = sales_col_ya.rsplit('_', 1)[0]
        ya_cols_modified = ya_cols_modified + '_'

        print('cy_cols_modified',cy_cols_modified)
        print('ya_cols_modified',ya_cols_modified)

        Value_Sales = filtered_df[sales_col_cy].values[0]
        YA_Value_Sales = filtered_df[sales_col_ya].values[0]

        print('Value_Sales',Value_Sales)
        print('YA_Value_Sales',YA_Value_Sales)

        df_time[cy_cols_modified + 'Share% CY'] = (df_time[sales_col_cy] / Value_Sales) * 100

        df_time[cy_cols_modified + 'Share% YA'] = (df_time[sales_col_ya] / YA_Value_Sales) * 100

        df_time[cy_cols_modified + 'GR% vs YA'] = (df_time[sales_col_cy] - df_time[sales_col_ya]) / df_time[
            sales_col_ya] * 100

        # df_time[cy_cols_modified + '%Pts vs YA'] = (df_time[cy_cols_modified + 'Share% CY'] - df_time[cy_cols_modified + 'Share% YA'])

        # df_time[cy_cols_modified + 'BPS vs YA'] = df_time[cy_cols_modified + '%Pts vs YA'] * 100

        df_time[cy_cols_modified + 'BPS vs YA'] = (df_time[cy_cols_modified + 'Share% CY'] - df_time[cy_cols_modified + 'Share% YA']) * 100


        df_time[cy_cols_modified + 'Share% CY'] = df_time[cy_cols_modified + 'Share% CY'].astype(str) + '%'

        df_time[cy_cols_modified + 'Share% YA'] = df_time[cy_cols_modified + 'Share% YA'].astype(str) + '%'

        df_time[cy_cols_modified + 'GR% vs YA'] = df_time[cy_cols_modified + 'GR% vs YA'].astype(str) + '%'

        ##################### CAGR - 29-08-2024 #####################################
        print('cagr_power_val 246',cagr_power_val)

        if cagr_power_val != 989898:
            if cagr_power_val > 0:

                CAGR_str = 'CAGR% CY vs YA'
                df_time[cy_cols_modified + CAGR_str] = (((df_time[sales_col_cy] / df_time[sales_col_ya]) ** (1 / cagr_power_val)) - 1)* 100
                df_time[cy_cols_modified + CAGR_str] = df_time[cy_cols_modified + CAGR_str].astype(str) + '%'

            elif cagr_power_val < 0:
                CAGR_str = 'CAGR% YA vs CY'
                cagr_power_val = abs(cagr_power_val)
                df_time[cy_cols_modified + CAGR_str] = (((df_time[sales_col_ya] / df_time[sales_col_cy]) ** (1 / cagr_power_val)) - 1)* 100
                df_time[cy_cols_modified + CAGR_str] = df_time[cy_cols_modified + CAGR_str].astype(str) + '%'

            elif cagr_power_val == 0:
                CAGR_str = 'CAGR% CY vs YA'
                df_time[cy_cols_modified + CAGR_str] = '0%'

        elif cagr_power_val == 989898:
            CAGR_str = 'CAGR% CY vs YA'
            # df_time[cy_cols_modified + CAGR_str] = '--'
            df_time[cy_cols_modified + CAGR_str] = 'cagr_none'


        # df_time.to_excel('df_time_CAGR.xlsx')
        ##################### CAGR - 29-08-2024 #####################################

        ################################### RANK - 09-05-2024 ###################################
        #Add rank_cy column
        # df_time_gt = df_time[df_time.index.get_level_values(1) == 'Grand Total']
        # df_time = df_time[df_time.index.get_level_values(1) != 'Grand Total']
        
        if 'Grand Total' not in df_time.index.get_level_values(0):
            df_time[cy_cols_modified + 'rank_cy'] = df_time[sales_col_cy].rank(ascending=False)
            df_time[cy_cols_modified + 'rank_cy'] = df_time[cy_cols_modified + 'rank_cy'] - 1

            # # Add rank_ya column
            df_time[cy_cols_modified + 'rank_ya'] = df_time[sales_col_ya].rank(ascending=False)
            df_time[cy_cols_modified + 'rank_ya'] = df_time[cy_cols_modified + 'rank_ya'] - 1
        else:
            df_time[cy_cols_modified + 'rank_cy'] = df_time[sales_col_cy].rank(ascending=False)
            df_time[cy_cols_modified + 'rank_cy'] = df_time[cy_cols_modified + 'rank_cy'] - 2

            # # Add rank_ya column
            df_time[cy_cols_modified + 'rank_ya'] = df_time[sales_col_ya].rank(ascending=False)
            df_time[cy_cols_modified + 'rank_ya'] = df_time[cy_cols_modified + 'rank_ya'] - 2
        ###############################################################################################
        ###############################################################################################

        # Calculate Rank column (difference between rank_ya and rank_cy)
        df_time[cy_cols_modified + 'Rank Difference'] = df_time[cy_cols_modified + 'rank_ya'].astype(int) - df_time[cy_cols_modified + 'rank_cy'].astype(int)

        # Create RANK column
        df_time[cy_cols_modified + 'CY' +' Rank'] = df_time[cy_cols_modified + 'rank_cy'].astype(str) + ' (' + df_time[cy_cols_modified + 'Rank Difference'].astype(str) + ')'

        ############ format rank function ###########################
        # Custom function to format the rank
        def format_rank(row):
            rank_cy = int(row[cy_cols_modified + 'rank_cy'])
            rank_difference = int(row[cy_cols_modified + 'Rank Difference'])
            if rank_difference == 0:
                return str(rank_cy)
            elif rank_difference > 0:
                return f"{rank_cy} (↑{abs(rank_difference)})"
            else:
                return f"{rank_cy} (↓{abs(rank_difference)})"
        ############ format rank function ###########################
        df_time[cy_cols_modified + 'CY' + ' Rank'] = df_time.apply(format_rank, axis=1)
        print('df_time colss 279',df_time.columns)

        ##################### CODE TO RENAME GRAND TOTAL RANK WITH -- #######
        df_time_gt = df_time[df_time.index.get_level_values(1) == 'Grand Total']

        if len(df_time_gt) > 0:
            df_time = df_time[df_time.index.get_level_values(1) != 'Grand Total']
            df_time_gt[cy_cols_modified + 'rank_cy'] = '--'
            df_time_gt[cy_cols_modified + 'rank_ya'] = '--'
            df_time_gt[cy_cols_modified + 'Rank Difference'] = '--'
            df_time_gt[cy_cols_modified + 'CY' + ' Rank'] = '--'
            # df_time_gt.to_excel('df_time_gt.xlsx')

            df_time = pd.concat([df_time,df_time_gt],axis=0)

        else:
            df_time = df_time.copy()
        ##################### CODE TO RENAME GRAND TOTAL RANK WITH -- #######

        ############################# ADDED ON 19-06-2024 ##########################################
        if (measure_row_column_position == 'measure_in_column') and (len(row_name) == 1) and ((brand_var_name in row_name)):
            
            base_index_colname_df = df_time[df_time.index.get_level_values(1) == base_sales_index_colname]
            # base_index_colname_df.to_excel('base_index_colname_df.xlsx')
            # print('base_index_colname_df 281',len(base_index_colname_df))

            if len(base_index_colname_df) > 0:
                print('df_time----285')
                sales_base_index_colname_val = base_index_colname_df[sales_col_cy].values[0]

                if (brand_var_name in row_name):
                    base_colname_brand_or_product = 'Brand Sales Index'

                df_time[cy_cols_modified + 'CY ' + base_colname_brand_or_product] = (df_time[sales_col_cy] / sales_base_index_colname_val) * 100

                # df_time.to_excel('df_timeeeee.xlsx')

                df_time2 = df_time.copy()
                df_time2 = df_time2[[cy_cols_modified + 'CY' + ' Rank',sales_col_cy,sales_col_ya,cy_cols_modified + 'GR% vs YA',cy_cols_modified + 'Share% CY',cy_cols_modified + 'Share% YA',cy_cols_modified + 'BPS vs YA',cy_cols_modified + CAGR_str,cy_cols_modified + 'CY ' + base_colname_brand_or_product]]

            ############################# ADDED ON 19-06-2024 ##########################################

            else:
                df_time2 = df_time.copy()
                df_time2 = df_time2[[cy_cols_modified + 'CY' + ' Rank',sales_col_cy,sales_col_ya,cy_cols_modified + 'GR% vs YA',cy_cols_modified + 'Share% CY',cy_cols_modified + 'Share% YA',cy_cols_modified + 'BPS vs YA',cy_cols_modified + CAGR_str]]

        else:
            df_time2 = df_time.copy()
            df_time2 = df_time2[[cy_cols_modified + 'CY' + ' Rank',sales_col_cy,sales_col_ya,cy_cols_modified + 'GR% vs YA',cy_cols_modified + 'Share% CY',cy_cols_modified + 'Share% YA',cy_cols_modified + 'BPS vs YA',cy_cols_modified + CAGR_str]]
        
        # df_time2.to_excel('df_time_VALUE.xlsx')
        df_time_lst.append(df_time2)

    df_time_all = pd.concat(df_time_lst,axis=1)

    # df_time_all.to_excel('df_time_all.xlsx')
    return df_time_all

#################### NEW CODE - 11-03-2024 #####################################
def derived_measures_after_crosstab_OLD(df_time,filtered_df):

    ####################################### VOLUME ##########################################
    Volume_Sales = filtered_df['Volume'].values[0]
    # Volume_Sales = filtered_df.loc[:, (cross_df_col_loop, 'Volume')].values[0]
    YA_Volume_Sales = filtered_df['Volume YA'].values[0]
    PP_Volume_Sales = filtered_df['Volume PP'].values[0]

    df_time['Volume Share'] = (df_time['Volume'] / Volume_Sales) * 100
    df_time['Volume Share YA'] = (df_time['Volume YA'] / YA_Volume_Sales) * 100
    df_time['Volume Share PP'] = (df_time['Volume PP'] / PP_Volume_Sales) * 100

    df_time['Volume Growth vs YA'] = (df_time['Volume'] - df_time['Volume YA']) / df_time[
        'Volume YA']* 100
    df_time['Volume Growth vs PP'] = (df_time['Volume'] - df_time['Volume PP']) / df_time[
        'Volume PP']* 100

    df_time['Volume Share bps Chg. vs YA'] = (df_time['Volume Share'] - df_time['Volume Share YA'])* 100
    df_time['Volume Share bps Chg. vs PP'] = (df_time['Volume Share'] - df_time['Volume Share PP'])* 100

    # df_time.to_excel('df_Volume_%_Share.xlsx')
    ####################################### VOLUME ##########################################

    ####################################### Sales ##########################################
    Value_Sales = filtered_df['Sales (JPY)'].values[0]
    YA_Value_Sales = filtered_df['Sales YA (JPY)'].values[0]
    PP_Value_Sales = filtered_df['Sales PP (JPY)'].values[0]

    df_time['Sales Share'] = (df_time['Sales (JPY)'] / Value_Sales) * 100
    df_time['Sales Share YA'] = (df_time['Sales YA (JPY)'] / YA_Value_Sales) * 100
    df_time['Sales Share PP'] = (df_time['Sales PP (JPY)'] / PP_Value_Sales) * 100

    df_time['Sales Growth vs YA'] = (df_time['Sales (JPY)'] - df_time['Sales YA (JPY)']) / df_time['Sales YA (JPY)']* 100
    df_time['Sales Growth vs PP'] = (df_time['Sales (JPY)'] - df_time['Sales PP (JPY)']) / df_time['Sales PP (JPY)']* 100

    df_time['Sales Share bps Chg. vs YA'] = (df_time['Sales Share'] - df_time['Sales Share YA'])* 100
    df_time['Sales Share bps Chg. vs PP'] = (df_time['Sales Share'] - df_time['Sales Share PP'])* 100
    # df_time.to_excel('df_time_VALUE.xlsx')
    ####################################### VALUE ##########################################

    ########################################### TDP #######################################
    tdp = filtered_df['TDP TY'].values[0]
    tdp_ya = filtered_df['TDP YA'].values[0]
    tdp_pp = filtered_df['TDP PP'].values[0]

    df_time['TDP Share'] = (df_time['TDP TY'] / tdp) * 100
    df_time['TDP Share YA'] = (df_time['TDP YA'] / tdp_ya) * 100
    df_time['TDP Share PP'] = (df_time['TDP PP'] / tdp_pp) * 100

    df_time['TDP Growth vs YA'] = (df_time['TDP TY'] - df_time['TDP YA']) / df_time[
        'TDP YA']* 100
    df_time['TDP Growth vs PP'] = (df_time['TDP TY'] - df_time['TDP PP']) / df_time[
        'TDP PP']* 100

    df_time['TDP Share bps Chg. vs YA'] = (df_time['TDP Share'] - df_time['TDP Share YA']) * 100
    df_time['TDP Share bps Chg. vs PP'] = (df_time['TDP Share'] - df_time['TDP Share PP']) * 100
    # df_time['TDP Growth-YA'] = (df_time['TDP TY'] - df_time['TDP YA'])/df_time['TDP YA']
    # df_time['TDP Growth-PP'] = (df_time['TDP TY'] - df_time['TDP PP'])/df_time['TDP PP']
    ########################################### TDP #######################################

    ########################################### WD Bps Chg. vs #######################################
    df_time['WD bps Chg. vs YA'] = (df_time['WD'] - df_time['WD YA']) * 100
    df_time['WD bps Chg. vs PP'] = (df_time['WD'] - df_time['WD PP']) * 100
    ########################################### WD Bps Chg. vs #######################################

    ########################################### ND Bps Chg. vs #######################################
    df_time['ND bps Chg. vs YA'] = (df_time['ND'] - df_time['ND YA']) * 100
    df_time['ND bps Chg. vs PP'] = (df_time['ND'] - df_time['ND PP']) * 100
    ########################################### ND Bps Chg. vs #######################################

    ####################################### AVG PRICE AND API ##########################################
    average_price_total = filtered_df['Sales (JPY)'].values[0] / filtered_df['Volume'].values[0]
    print('==average_price_total==', average_price_total)

    df_time['Avg Price'] = df_time['Sales (JPY)'] / df_time['Volume']
    df_time['API'] = df_time['Avg Price'] / average_price_total * 100
    ####################################### AVG PRICE AND API ##########################################

    ####################################### AVG PRICE-YA AND API-YA ##########################################
    average_price_total = filtered_df['Sales YA (JPY)'].values[0] / filtered_df['Volume YA'].values[0]
    print('==average_price_total==', average_price_total)
    df_time['Avg Price YA'] = df_time['Sales YA (JPY)'] / df_time['Volume YA']
    df_time['API YA'] = df_time['Avg Price YA'] / average_price_total * 100
    ####################################### AVG PRICE-YA AND API-YA ##########################################

    ####################################### AVG PRICE-PP AND API-PP ##########################################
    average_price_total = filtered_df['Sales PP (JPY)'].values[0] / filtered_df['Volume PP'].values[0]
    print('==average_price_total==', average_price_total)
    df_time['Avg Price PP'] = df_time['Sales PP (JPY)'] / df_time['Volume PP']
    df_time['API PP'] = df_time['Avg Price PP'] / average_price_total * 100
    ####################################### AVG PRICE-PP AND API-PP ##########################################

    ####################################### AVG PRICE GROWTH ##########################################
    df_time['Avg Price Growth vs YA'] = (df_time['Avg Price'] - df_time['Avg Price YA']) / df_time['Avg Price YA']* 100
    df_time['Avg Price Growth vs PP'] = (df_time['Avg Price'] - df_time['Avg Price PP']) / df_time['Avg Price PP']* 100
    ####################################### AVG PRICE-GROWTH ##########################################

    ########################################### API Change Vs. ################################################
    df_time['API Chg. Vs YA'] = df_time['API'] - df_time['API YA']
    df_time['API Chg. Vs PP'] = df_time['API'] - df_time['API PP']
    ########################################### API Change Vs. ################################################

    df_time = df_time[['Volume','Volume YA', 'Volume PP','Volume Share','Volume Share YA', 'Volume Share PP',
                       'Volume Growth vs YA','Volume Growth vs PP','Volume Share bps Chg. vs YA', 'Volume Share bps Chg. vs PP',
                       'Sales (JPY)', 'Sales YA (JPY)', 'Sales PP (JPY)', 'Sales Share',
                       'Sales Share YA', 'Sales Share PP', 'Sales Growth vs YA','Sales Growth vs PP',
                       'Sales Share bps Chg. vs YA', 'Sales Share bps Chg. vs PP',
                       'TDP TY','TDP YA', 'TDP PP','TDP Share','TDP Share YA','TDP Share PP',
                     'TDP Growth vs YA','TDP Growth vs PP','TDP Share bps Chg. vs YA','TDP Share bps Chg. vs PP',
                       'WD', 'WD YA', 'WD PP', 'WD bps Chg. vs YA', 'WD bps Chg. vs PP',
                       'ND', 'ND YA', 'ND PP', 'ND bps Chg. vs YA', 'ND bps Chg. vs PP',
                    'Avg Price', 'Avg Price YA', 'Avg Price PP', 'Avg Price Growth vs YA', 'Avg Price Growth vs PP',
                       'API','API YA','API PP','API Chg. Vs YA','API Chg. Vs PP']]
    # df_time.to_excel('df_time_RRRRR.xlsx')
    return df_time


def derived_measures_weights_cols_OLD(df):

    df_copy = df.copy()
    print('===df_copy=== cols',df_copy.columns)

    print('unique timee', df_copy['Time'].unique().tolist())
    print('new func!')

    df_list = []

    for loop_time_period_unique in df_copy['Time'].unique().tolist():
        print('df colss 37',df_copy.columns)
        print('df SHAPEEEE',df_copy.shape)
        print('loop_time_period_unique==',loop_time_period_unique)

        df_time = df_copy[(df_copy['Time'] == loop_time_period_unique)]

        new_row = {'LinkID': df_time.shape[0] + 1,
                    'Country': ''.join(df_time['Country'].unique().tolist()),
                   'Category':''.join(df_time['Category'].unique().tolist()),
        # new_row = {'COUNTRY': df_time['COUNTRY'].unique().astype(str),
        #            'CATEGORY': df_time['CATEGORY'].unique().astype(str),
                   'Segment': 'Totals',
                    'Company': 'Totals',
                     'Brand': 'Totals',
                     'Volume YA': df_time['Volume YA'].sum(),
                     'Volume PP': df_time['Volume PP'].sum(),
                     'Volume': df_time['Volume'].sum(),
                     'Sales (JPY)': df_time['Sales (JPY)'].sum(),
                     'TDP TY': df_time['TDP TY'].sum(),
                     'Sales YA (JPY)': df_time['Sales YA (JPY)'].sum(),
                     'Sales PP (JPY)': df_time['Sales PP (JPY)'].sum(),
                     'TDP YA': df_time['TDP YA'].sum(),
                     'TDP PP': df_time['TDP PP'].sum(),
                     'WD PP': df_time['WD PP'].max(),
                     'WD YA': df_time['WD YA'].max(),
                     'WD': df_time['WD'].max(),
                     'WD YA': df_time['WD YA'].max(),
                    'Time':loop_time_period_unique,
                     'WD PP': df_time['WD PP'].max()}
        print('new_row===new_row',new_row)

        # Append the new row to the DataFrame
        df_time = df_time.append(new_row, ignore_index=True)

        filtered_df = df_time[(df_time['Company'] == 'Totals') & (df_time['Brand'] == 'Totals') & (df_time['Segment'] == 'Totals')]
        # filtered_df.to_excel('filtered_dffff.xlsx')
        # exit("filtered_df")
        print('length filtered_df',len(filtered_df))

        ####################################### VOLUME ##########################################
        Volume_Sales = filtered_df['Volume'].values[0]
        YA_Volume_Sales = filtered_df['Volume YA'].values[0]
        PP_Volume_Sales = filtered_df['Volume PP'].values[0]

        df_time['Volume Share'] = (df_time['Volume'] / Volume_Sales) * 100
        df_time['Volume Share YA'] = (df_time['Volume YA'] / YA_Volume_Sales) * 100
        df_time['Volume Share PP'] = (df_time['Volume PP'] / PP_Volume_Sales) * 100

        df_time['Volume Growth vs YA'] = (df_time['Volume'] - df_time['Volume YA']) / df_time[
            'Volume YA']
        df_time['Volume Growth vs PP'] = (df_time['Volume'] - df_time['Volume PP']) / df_time[
            'Volume PP']

        df_time['Volume Bps Chg. vs YA'] = df_time['Volume Share'] - df_time['Volume Share YA']
        df_time['Volume Bps Chg. vs PP'] = df_time['Volume Share'] - df_time['Volume Share PP']

        # df_time.to_excel('df_Volume_%_Share.xlsx')
        ####################################### VOLUME ##########################################

        ####################################### VALUE ##########################################
        Value_Sales = filtered_df['Sales (JPY)'].values[0]
        YA_Value_Sales = filtered_df['Sales YA (JPY)'].values[0]
        PP_Value_Sales = filtered_df['Sales PP (JPY)'].values[0]

        df_time['Sales Share'] = (df_time['Sales (JPY)'] / Value_Sales) * 100
        df_time['Sales Share YA'] = (df_time['Sales YA (JPY)'] / YA_Value_Sales) * 100
        df_time['Sales Share PP'] = (df_time['Sales PP (JPY)'] / PP_Value_Sales) * 100

        df_time['Sales Growth vs YA'] = (df_time['Sales (JPY)'] - df_time['Sales YA (JPY)'])/df_time['Sales YA (JPY)']
        df_time['Sales Growth vs PP'] = (df_time['Sales (JPY)'] - df_time['Sales PP (JPY)'])/df_time['Sales PP (JPY)']

        df_time['Sales Bps Chg. vs YA'] = df_time['Sales Share'] - df_time['Sales Share YA']
        df_time['Sales Bps Chg. vs PP'] = df_time['Sales Share'] - df_time['Sales Share PP']
        # df_time.to_excel('df_time_VALUE.xlsx')
        ####################################### VALUE ##########################################

        ########################################### TDP #######################################
        tdp = filtered_df['TDP TY'].values[0]
        tdp_ya = filtered_df['TDP YA'].values[0]
        tdp_pp = filtered_df['TDP PP'].values[0]

        df_time['TDP Share'] = (df_time['TDP TY'] / tdp) * 100
        df_time['TDP Share YA'] = (df_time['TDP YA'] / tdp_ya) * 100
        df_time['TDP Share PP'] = (df_time['TDP PP'] / tdp_pp) * 100

        df_time['TDP Growth vs YA'] = (df_time['TDP TY'] - df_time['TDP YA']) / df_time[
            'TDP YA']
        df_time['TDP Growth vs PP'] = (df_time['TDP TY'] - df_time['TDP PP']) / df_time[
            'TDP PP']

        df_time['TDP Bps Chg. vs YA'] = df_time['TDP Share'] - df_time['TDP Share YA']
        df_time['TDP Bps Chg. vs PP'] = df_time['TDP Share'] - df_time['TDP Share PP']
        # df_time['TDP Growth-YA'] = (df_time['TDP TY'] - df_time['TDP YA'])/df_time['TDP YA']
        # df_time['TDP Growth-PP'] = (df_time['TDP TY'] - df_time['TDP PP'])/df_time['TDP PP']
        ########################################### TDP #######################################

        ########################################### WD Bps Chg. vs #######################################
        df_time['WD Bps Chg. vs YA'] = df_time['WD'] - df_time['WD YA']
        df_time['WD Bps Chg. vs PP'] = df_time['WD'] - df_time['WD PP']
        ########################################### WD Bps Chg. vs #######################################

        ########################################### ND Bps Chg. vs #######################################
        df_time['ND Bps Chg. vs YA'] = df_time['ND'] - df_time['ND YA']
        df_time['ND Bps Chg. vs PP'] = df_time['ND'] - df_time['ND PP']
        ########################################### ND Bps Chg. vs #######################################

        ####################################### AVG PRICE AND API ##########################################
        average_price_total = filtered_df['Sales (JPY)'].values[0]/filtered_df['Volume'].values[0]
        print('==average_price_total==',average_price_total)

        df_time['Avg Price'] = df_time['Sales (JPY)']/df_time['Volume']
        df_time['API'] = df_time['Avg Price']/average_price_total*100
        ####################################### AVG PRICE AND API ##########################################

        ####################################### AVG PRICE-YA AND API-YA ##########################################
        average_price_total = filtered_df['Sales YA (JPY)'].values[0]/filtered_df['Volume YA'].values[0]
        print('==average_price_total==',average_price_total)
        df_time['Avg Price YA'] = df_time['Sales YA (JPY)']/df_time['Volume YA']
        df_time['API YA'] = df_time['Avg Price YA']/average_price_total*100
        ####################################### AVG PRICE-YA AND API-YA ##########################################

        ####################################### AVG PRICE-PP AND API-PP ##########################################
        average_price_total = filtered_df['Sales PP (JPY)'].values[0]/filtered_df['Volume PP'].values[0]
        print('==average_price_total==',average_price_total)
        df_time['Avg Price PP'] = df_time['Sales PP (JPY)']/df_time['Volume PP']
        df_time['API PP'] = df_time['Avg Price PP']/average_price_total*100
        ####################################### AVG PRICE-PP AND API-PP ##########################################

        ####################################### AVG PRICE GROWTH ##########################################
        df_time['Avg Price Growth vs YA'] = (df_time['Avg Price'] - df_time['Avg Price YA'])/df_time['Avg Price YA']
        df_time['Avg Price Growth vs PP'] = (df_time['Avg Price'] - df_time['Avg Price PP'])/df_time['Avg Price PP']
        ####################################### AVG PRICE-GROWTH ##########################################

        ########################################### API Change Vs. ################################################
        df_time['API Chg. Vs YA'] = df_time['API'] - df_time['API YA']
        df_time['API Chg. Vs PP'] = df_time['API'] - df_time['API PP']
        ########################################### API Change Vs. ################################################

        df_time = df_time[~df_time['Segment'].str.contains('Totals')]
        # exit('end')
        df_list.append(df_time)

    df = pd.concat(df_list,axis = 0)

    return df