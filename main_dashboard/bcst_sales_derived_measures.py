import re
import json
import os
import subprocess
import warnings
import polars as pl
from matplotlib import pyplot as plt
warnings.filterwarnings('ignore')
import numpy
import pandas as pd
import numpy as np
import os,json
import time
from scipy import stats
import time
from itertools import combinations
import openpyxl
from openpyxl.worksheet.dimensions import ColumnDimension, DimensionHolder
from openpyxl.utils import get_column_letter
from main_dashboard.bcst_sales_data_constants import *

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

    # print('cy_cols_lst',cy_cols_lst)
    # print('ya_cols_lst',ya_cols_lst)

    if (measure_row_column_position == 'measure_in_column') and (len(row_name) == 1) and ((brand_var_name in row_name)):
        df_time_lst22 = []
        for cy_col_loop in range(len(cy_cols_lst)):
            # print('21333',cy_col_loop)
            sales_col_cy = cy_cols_lst[cy_col_loop]
            sales_col_ya = ya_cols_lst[cy_col_loop]

            cy_cols_modified = sales_col_cy.rsplit('_', 1)[0]
            cy_cols_modified = cy_cols_modified + '_'
            ya_cols_modified = sales_col_ya.rsplit('_', 1)[0]
            ya_cols_modified = ya_cols_modified + '_'

            # print('cy_cols_modified',cy_cols_modified)
            # print('ya_cols_modified',ya_cols_modified)

            ######################### BRAND SALES INDEX - 20-09-2024 #################################
            ######################### BRAND SALES INDEX - 20-09-2024 #################################
            df_time_bsi = df_time.copy()
            base_index_colname_df = df_time_bsi[df_time_bsi.index.get_level_values(1) == base_sales_index_colname]

            # base_index_colname_df.to_excel('base_index_colname_df.xlsx')

            # print('df_time_bsi----285')
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

        # print('Value_Sales',Value_Sales)
        # print('YA_Value_Sales',YA_Value_Sales)

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
        # print('cagr_power_val 246',cagr_power_val)

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
        # print('cagr_power_val 246',cagr_power_val)
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
        # print('df_time colss 279',df_time.columns)

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
    # df_time.to_excel('df_time_RANK.xlsx')
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
        # print('cagr_power_val 246',cagr_power_val)
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
    print('derived_measures_after_crosstab starts..')
    start_derived_fn = time.time()
    # print('start time-',start_derived_fn)
    ####################################### Sales ##########################################
    cy_cols_lst = df_time.filter(like='CY').columns.tolist()
    ya_cols_lst = df_time.filter(like='YA').columns.tolist()

    try:
        replace_values = {-np.inf: 0, np.inf: 0, 'null': 0, np.nan: 0}
        df_time.replace(replace_values, inplace=True)
        df_time.fillna(0,inplace=True)
    except:
        pass

    # # print('cy_cols_lst',cy_cols_lst)
    # print('ya_cols_lst',ya_cols_lst)

    if (measure_row_column_position == 'measure_in_column') and (len(row_name) == 1) and ((brand_var_name in row_name)):
        df_time_lst22 = []
        for cy_col_loop in range(len(cy_cols_lst)):
            # print('21333',cy_col_loop)
            sales_col_cy = cy_cols_lst[cy_col_loop]
            sales_col_ya = ya_cols_lst[cy_col_loop]

            cy_cols_modified = sales_col_cy.rsplit('_', 1)[0]
            cy_cols_modified = cy_cols_modified + '_'
            ya_cols_modified = sales_col_ya.rsplit('_', 1)[0]
            ya_cols_modified = ya_cols_modified + '_'

            # print('cy_cols_modified',cy_cols_modified)
            # print('ya_cols_modified',ya_cols_modified)

            ######################### BRAND SALES INDEX - 20-09-2024 #################################
            ######################### BRAND SALES INDEX - 20-09-2024 #################################
            print('base_sales_index_colname==',base_sales_index_colname)
            df_time_bsi = df_time.copy()
            base_index_colname_df = df_time_bsi[df_time_bsi.index.get_level_values(1) == base_sales_index_colname]

            # print('df_time_bsi----285')
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

        # print('672---filtered_df[sales_col_cy]',filtered_df[sales_col_cy])

        try:
            Value_Sales = filtered_df[sales_col_cy].values[0]
            YA_Value_Sales = filtered_df[sales_col_ya].values[0]
        except:
            Value_Sales = filtered_df[sales_col_cy].values[0][0]
            YA_Value_Sales = filtered_df[sales_col_ya].values[0][0]

        # print('Value_Sales-679',Value_Sales)
        # print('YA_Value_Sales-680',YA_Value_Sales)

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
            # print('if condition--710')
            df_time[cy_cols_modified + 'GR% Contribution'] = df_time[cy_cols_modified + 'Variance']/(-df_time_variance_GT_value)
        else:
            # print('else condition--713')
            df_time[cy_cols_modified + 'GR% Contribution'] = df_time[cy_cols_modified + 'Variance']/df_time_variance_GT_value
        df_time[cy_cols_modified + 'GR% Contribution'] = df_time[cy_cols_modified + 'GR% Contribution']*100
        df_time[cy_cols_modified + 'GR% Contribution'] = df_time[cy_cols_modified + 'GR% Contribution'].astype(str) + '%'
        ######################## added on 21-10-2024 - Growth Contribution ##############

        ##################### CAGR - 29-08-2024 #####################################
        # print('cagr_power_val 246',cagr_power_val)

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
        # print('df_time colss 279',df_time.columns)

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
    end_derived_fn = time.time()
    print('end time-',end_derived_fn)
    print('time taken to run derived function-',end_derived_fn - start_derived_fn," seconds!")
    return df_time_all
######### BRAND SALES INDEX NEW LOGIC - 23-09-2024 ##############################
