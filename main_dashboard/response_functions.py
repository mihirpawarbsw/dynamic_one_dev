import json
import os
import re
import time
import ast
import pandas as pd
import numpy as np
from django.conf import settings

from datetime import date
from datetime import datetime
from io import StringIO

def allign_grand_total_headers_fn_dynamic(cross_df):
    Columns_df_lst = []
    
    # Determine the number of levels in the multi-index columns
    num_levels = cross_df.columns.nlevels
    
    for i in range(num_levels):
        level_names = cross_df.columns.get_level_values(i).unique().tolist()
        cross_df_grp = cross_df.groupby(axis=1, level=i)
        
        for name in level_names:
            cross_df_col = cross_df_grp.get_group(name)
            cross_df_col_df = pd.DataFrame(cross_df_col)
            next_level = i + 1
            if next_level < num_levels:
                unique_groups_next_level = cross_df_col_df.columns.get_level_values(next_level).unique().tolist()
                
                if 'Grand Total' in unique_groups_next_level:
                    unique_groups_next_level.remove('Grand Total')
                    unique_groups_next_level.insert(0, 'Grand Total')
                    
                cross_df_col_df_reordered = cross_df_col_df.loc[:, cross_df_col_df.columns.get_level_values(next_level).isin(unique_groups_next_level)]
                
                # Remove duplicate columns
                cross_df_col_df_reordered = cross_df_col_df_reordered.loc[:, ~cross_df_col_df_reordered.columns.duplicated()]
                
                cross_df_col_df_reordered = cross_df_col_df_reordered.reindex(columns=unique_groups_next_level, level=next_level)
                
                Columns_df_lst.append(cross_df_col_df_reordered)
    
    if len(Columns_df_lst) > 0:
        cross_df = pd.concat(Columns_df_lst, axis=1)
    
        if 'Grand Total' in cross_df.columns.get_level_values(0).unique():
            grand_total_name = 'Grand Total'
            level_names_cols = cross_df.columns.get_level_values(0).unique().tolist()
            level_names_cols.remove(grand_total_name)
            level_names_cols.insert(0, grand_total_name)
            cross_df = cross_df.reindex(columns=level_names_cols, level=0)
    else:
        cross_df = pd.DataFrame()
    
    return cross_df

############ ADDED ON 04-10-2024 - ALLIGNING TOTALS #####################################
def allign_grand_total_headers_fn(cross_df):

    Columns_df_lst = []
    # Get the level 0 names in the columns
    level_0_names_cols = cross_df.columns.get_level_values(0).unique().tolist()

    cross_df_col_grp = cross_df.groupby(axis=1, level=0)

    # Access the first group
    for cross_df_col_loop in level_0_names_cols:
        cross_df_col = cross_df_col_grp.get_group(cross_df_col_loop)
        cross_df_col_df = pd.DataFrame(cross_df_col)

        unique_groups_level1 = cross_df_col_df.columns.get_level_values(1).unique().tolist()
        level0_grp_names = cross_df_col_df.columns.get_level_values(0).unique().tolist()
        # print('level0_grp_names', level0_grp_names)
        # print('unique_groups_level1', unique_groups_level1)

        if 'Total (Among Displayed)' in unique_groups_level1:
            unique_groups_level1.remove('Total (Among Displayed)')
            unique_groups_level1.append('Total (Among Displayed)')
        else:
            pass
            
        if 'Grand Total' in unique_groups_level1:
            # Remove 'Total' from the original list
            unique_groups_level1.remove('Grand Total')
            

            # Insert 'Total' at the first position
            # unique_groups_level1.insert(-1, 'Grand Total')
            
            unique_groups_level1.append('Grand Total')
            # print('unique_groups_level1=====',unique_groups_level1)
        else:
            pass

        cross_df_col_df_reordered = cross_df_col_df.loc[:,
                      cross_df_col_df.columns.get_level_values(1).isin(list(unique_groups_level1))]
        # cross_df_col_df_reordered.to_excel('cross_df_col_df_reordered_ggg.xlsx')

        try:
            # print('====688 duplicate')
            cross_df_col_df_reordered = cross_df_col_df_reordered.loc[:, ~cross_df_col_df_reordered.columns.duplicated(keep='first')]
        except:
            pass
        ########################################################################################
        # cross_df_col_df_reordered = cross_df_col_df_reordered.iloc[:, [0, 1]]
        cross_df = cross_df_col_df_reordered.reindex(columns=unique_groups_level1, level=1)
        # cross_df.to_excel('cross_df_col_df_reordered_ffff.xlsx')

        Columns_df_lst.append(cross_df)
    cross_df = pd.concat(Columns_df_lst,axis=1)

    ########################## ADDED ON 23-01-2024 #####################################
    if 'Grand Total' in level_0_names_cols:

        # Move "Total" to the first position in the list
        level_0_names_cols.remove("Grand Total")
        level_0_names_cols =  level_0_names_cols + ["Grand Total"]

        cross_df = cross_df.reindex(columns=level_0_names_cols, level=0)

    else:
        cross_df = cross_df.copy()

    ########################## ADDED ON 23-01-2024 #####################################
    # cross_df.to_excel('CROSS_DF_Before_return.xlsx')
    return cross_df
############ ADDED ON 04-10-2024 - ALLIGNING TOTALS #####################################

#################################### added on 18-02-2025 #####################################
def base_filter_data(df, dict_base_filter_data):
    for key, value in dict_base_filter_data.items():
        df = df[df[key].isin(value)]
    return df
#################################### added on 18-02-2025 #####################################

def base_filter_resp(df, dict_base_filter, row_name, col_name):

    keys = list(dict_base_filter.keys())[0]
    values = list(dict_base_filter.values())[0]
    if 'Time' in values:
        values.remove('Time')
    filter_dict_resp = {}

    table_name = keys + ".xlsx"

    df = df[values]

    for selected_column in df.columns:
        categories_list = df[selected_column].unique().tolist()
        filter_dict_resp11 = {selected_column: list(categories_list)}
        filter_dict_resp.update(filter_dict_resp11)
    ####################### BASE FILTER #####################################################################

    if 'Time' in list(filter_dict_resp.keys()):
        filter_dict_resp.pop('Time')
    return filter_dict_resp

def base_filter_resp_all(df, dict_table, row_name, col_name):
    filter_dict_resp = {}
 
    # Extract table names and filter conditions
    for table_name, values_temp in dict_table.items():
        # Filter the dataframe based on the values in dict_table
        df_filtered = df[values_temp]
 
        for selected_column in df_filtered.columns:
            # Get unique categories and prepend 'Total'
            categories_list = ['Total'] + df_filtered[selected_column].unique().tolist()
 
            # Update the dictionary with the column categories
            filter_dict_resp[selected_column] = categories_list
 
    return filter_dict_resp

##################################### ALLIGN HEADERS ##########################
def allign_headers_condn(cross_df, percent_calc, seperated_flag_row, seperated_flag_col, row_name, col_name):
    if (percent_calc == 'column_percent') or (percent_calc == 'Indices'):
        ######## Allign Columns Total ##############################
        cross_df = allign_headers_fn(cross_df, percent_calc)
        ######## Allign Columns Total ##############################

    elif (percent_calc == 'row_percent'):
        ################### Allign Rows Total ##############################
        cross_df = cross_df.T
        cross_df = allign_headers_fn(cross_df, percent_calc)
        cross_df = cross_df.T
        ################## Allign Rows Total ##############################

    elif (percent_calc == 'table_percent') or (percent_calc == 'actual_count'):

        # cross_df_total_row = cross_df.loc[:, cross_df.columns.get_level_values(1).isin(['Total', 'Total'])]

        # Remove ['total', 'total'] from the index
        # cross_df = cross_df.drop(('Total', 'Total'))
        ####### Allign Columns Total ##############################
        cross_df_cols = allign_headers_fn(cross_df, percent_calc)
        ####### Allign Columns Total ##############################

        ################### Allign Rows Total ##############################
        cross_df_rows = cross_df_cols.T
        cross_df = allign_headers_fn(cross_df_rows, percent_calc)
        cross_df = cross_df.T
        ################### Allign Rows Total ##############################
        # cross_df = pd.concat([cross_df_total_row,cross_df], axis=0)

    if ((len(row_name) > 1) and (len(col_name) > 1)):
        if ((seperated_flag_row == 0 and seperated_flag_col == 0 and percent_calc != 'row_percent') or
                (seperated_flag_row == 1 and seperated_flag_col == 0 and percent_calc != 'row_percent')):
            unique_groups_level0 = cross_df.columns.get_level_values(0).unique().tolist()
            # Remove 'Total' from the original list
            unique_groups_level0.remove('Total')

            # Insert 'Total' at the first position
            unique_groups_level0.insert(0, 'Total')
            print('unique_groups_level0=====', unique_groups_level0)

            cross_df = cross_df.loc[:, unique_groups_level0]

            cross_df = cross_df.reindex(columns=unique_groups_level0, level=0)

        elif ((seperated_flag_row == 0 and seperated_flag_col == 0 and percent_calc == 'row_percent') or
              (seperated_flag_row == 0 and seperated_flag_col == 1 and percent_calc == 'row_percent')):
            print('699===row_perc condn')
            cross_df = cross_df.T
            unique_groups_level0 = cross_df.columns.get_level_values(0).unique().tolist()
            # Remove 'Total' from the original list
            unique_groups_level0.remove('Total')

            # Insert 'Total' at the first position
            unique_groups_level0.insert(0, 'Total')
            print('unique_groups_level0=====', unique_groups_level0)

            cross_df = cross_df.loc[:, unique_groups_level0]

            cross_df = cross_df.reindex(columns=unique_groups_level0, level=0)
            cross_df = cross_df.T

        if ((percent_calc == 'actual_count' or percent_calc == 'table_percent') and seperated_flag_row == 0):
            # cross_df = cross_df.T
            unique_groups_level0_act_tab = cross_df.index.get_level_values(0).unique().tolist()
            print('unique_groups_level0_act_tab', unique_groups_level0_act_tab)

            unique_groups_level0_act_tab.remove('Total')

            # Insert 'Total' at the first position
            unique_groups_level0_act_tab.insert(0, 'Total')

            cross_df = cross_df.loc[unique_groups_level0_act_tab, :]

            cross_df = cross_df.reindex(index=unique_groups_level0_act_tab, level=0)

    return cross_df


def allign_headers_fn(cross_df, percent_calc):
    Columns_df_lst = []
    # Get the level 0 names in the columns
    level_0_names_cols = cross_df.columns.get_level_values(0).unique().tolist()

    cross_df_col_grp = cross_df.groupby(axis=1, level=0)

    # Access the first group
    for cross_df_col_loop in level_0_names_cols:
        cross_df_col = cross_df_col_grp.get_group(cross_df_col_loop)
        cross_df_col_df = pd.DataFrame(cross_df_col)

        unique_groups_level1 = cross_df_col_df.columns.get_level_values(1).unique().tolist()
        level0_grp_names = cross_df_col_df.columns.get_level_values(0).unique().tolist()
        print('level0_grp_names', level0_grp_names)
        print('unique_groups_level1', unique_groups_level1)

        # Remove 'Total' from the original list
        unique_groups_level1.remove('Total')

        # Insert 'Total' at the first position
        unique_groups_level1.insert(0, 'Total')
        print('unique_groups_level1=====', unique_groups_level1)

        cross_df_col_df_reordered = cross_df_col_df.loc[:,
                                    cross_df_col_df.columns.get_level_values(1).isin(list(unique_groups_level1))]
        # cross_df_col_df_reordered.to_excel('cross_df_col_df_reordered_ggg.xlsx')s

        try:
            print('====688 duplicate')
            cross_df_col_df_reordered = cross_df_col_df_reordered.loc[:,
                                        ~cross_df_col_df_reordered.columns.duplicated(keep='first')]
        except:
            pass
        ########################################################################################
        # cross_df_col_df_reordered = cross_df_col_df_reordered.iloc[:, [0, 1]]
        cross_df = cross_df_col_df_reordered.reindex(columns=unique_groups_level1, level=1)
        # cross_df.to_excel('cross_df_col_df_reordered_ffff.xlsx')

        Columns_df_lst.append(cross_df)
    cross_df = pd.concat(Columns_df_lst, axis=1)

    return cross_df


############################### ALLIGN HEADERS BK ########################################################
def remove_duplicate_keys_and_values(dictionary):

    updated_dict = {key: list(set(value)) for key, value in dictionary.items()}
    # updated_dict = {}

    # for key, value in dictionary.items():
    #     value_upd = set(value)
    #     value_upd = list(value_upd)
    #     # print('value_upd',value_upd)
    #     updated_dict[key] = value_upd

    return updated_dict

def remove_prefix(cross_df):
    try:
        cross_df.rename(columns=lambda x: re.sub('.*}', '', x), inplace=True)
    except:
        pass
    try:
        cross_df.rename(index=lambda x: re.sub('.*}', '', x), inplace=True)
    except:
        pass

    # cross_df.rename(columns=lambda x: re.sub('_', ' ', x), inplace=True)
    # cross_df.rename(index=lambda x: re.sub('_', ' ', x), inplace=True)

    # cross_df.rename(columns=lambda x: re.sub('total', '_total', x), inplace=True)
    # cross_df.rename(index=lambda x: re.sub('total', '_total', x), inplace=True)

    return cross_df

####################### ADDED ON 18-02-2025 ################################################
def replace_cy_ya_with_actual_period(cross_df, measure_row_column_position, selected_full_period_str, comparative_full_period_str):
    # Define replacements for 'CY' and 'YA' for both periods
    replacements = {
        'CY': selected_full_period_str,
        '_CY': selected_full_period_str,
        'YA': comparative_full_period_str,
        '_YA': comparative_full_period_str
    }
   
    # Function to apply replacements
    def apply_replacements(axis):
        for key, value in replacements.items():
            if axis == 'columns':
                cross_df.rename(columns=lambda x: re.sub(key, value, x), inplace=True)
            elif axis == 'index':
                cross_df.rename(index=lambda x: re.sub(key, value, x), inplace=True)

 
    # Apply replacements based on position
    if measure_row_column_position == "measure_in_column":
        apply_replacements(axis='columns')
    elif measure_row_column_position == "measure_in_row":
        apply_replacements(axis='index')
   
    return cross_df

# def replace_cy_ya_with_actual_period(cross_df, measure_row_column_position, selected_full_period_str, comparative_full_period_str):
#     # Define replacements for 'CY' and 'YA' for both periods
#     replacements = {
#         'CY': selected_full_period_str,
#         '_CY': selected_full_period_str,
#         'YA': comparative_full_period_str,
#         '_YA': comparative_full_period_str
#     }

#     # Function to apply replacements
#     def apply_replacements(axis):
#         if axis == 'columns':
#             cross_df.rename(columns=lambda x: re.sub('|'.join(re.escape(k) for k in replacements), 
#                                                       lambda m: replacements[m.group(0)], str(x)), inplace=True)
#         elif axis == 'index':
#             cross_df.rename(index=lambda x: re.sub('|'.join(re.escape(k) for k in replacements), 
#                                                    lambda m: replacements[m.group(0)], str(x)), inplace=True)

#     # Apply replacements based on position
#     if measure_row_column_position == "measure_in_column":
#         apply_replacements(axis='columns')
#     elif measure_row_column_position == "measure_in_row":
#         apply_replacements(axis='index')

#     return cross_df

####################### ADDED ON 18-02-2025 ################################################

def replace_cy_ya_with_actual_period_OLD_18022025(cross_df,measure_row_column_position,selected_full_period_str,comparative_full_period_str):
    ################## CODE TO REPLACE CY AND YA WITH ACTUAL PERIOD - 19-04-2024 ####
    if measure_row_column_position == "measure_in_column":
        try:
            cross_df.rename(columns=lambda x: re.sub('CY',selected_full_period_str, x), inplace=True)
            cross_df.rename(columns=lambda x: re.sub('_CY',selected_full_period_str, x), inplace=True)
            cross_df.rename(columns=lambda x: re.sub('YA',comparative_full_period_str, x), inplace=True)
            cross_df.rename(columns=lambda x: re.sub('_YA',comparative_full_period_str, x), inplace=True)
        except:
            pass
    elif measure_row_column_position == "measure_in_row":
        try:
            cross_df.rename(index=lambda x: re.sub('CY',selected_full_period_str, x), inplace=True)
            cross_df.rename(index=lambda x: re.sub('_CY',selected_full_period_str, x), inplace=True)
            cross_df.rename(index=lambda x: re.sub('YA',comparative_full_period_str, x), inplace=True)
            cross_df.rename(index=lambda x: re.sub('_YA',comparative_full_period_str, x), inplace=True)
        except:
            pass

    return cross_df


def replace_sales_currency_with_SALES(selected_weight_column22,cross_df,measure_row_column_position):
    selected_weight_column_str = ','.join([str(elem) for elem in selected_weight_column22])
    print('selected_weight_column_str 881',selected_weight_column_str)
    if measure_row_column_position == "measure_in_column":
        try:
            cross_df.rename(columns=lambda x: re.sub(selected_weight_column_str,'Sales', x), inplace=True)
        except:
            pass
    elif measure_row_column_position == "measure_in_row":
        try:
            cross_df.rename(index=lambda x: re.sub(selected_weight_column_str,'Sales', x), inplace=True)
        except:
            pass

    return cross_df

    ################## CODE TO REPLACE CY AND YA WITH ACTUAL PERIOD - 19-04-2024 ####
def drop_grand_total_from_rows(cross_df):
    try:
        # Identify columns that contain "Grand Total" in any level
        grand_total_index = [col for col in cross_df.index if any('Grand Total' in level for level in col)]

        # Drop the identified columns
        cross_df = cross_df.drop(index=grand_total_index)
    except Exception as e:
        print("An error occurred:", e)

    return cross_df

def drop_grand_total_from_columns(cross_df):
    try:
        # Identify columns that contain "Grand Total" in any level
        grand_total_columns = [col for col in cross_df.columns if any('Grand Total' in level for level in col)]

        # Drop the identified columns
        cross_df = cross_df.drop(columns=grand_total_columns)
    except Exception as e:
        print("An error occurred:", e)

    return cross_df

def code_to_replace_QUARTER(period_to_be_replaced_str,measure_selected_key_val_resp,dict_selected_measures_lst):
    ##### CODE TO REPLACE QUARTER - 19-04-2024 ###########################
    if period_to_be_replaced_str =='QUARTER':
    ################################################################################
        specific_word = period_to_be_replaced_str
        for key, value in measure_selected_key_val_resp.items():
            updated_list = []
            for element in value:
                if specific_word in element:
                    updated_list.append(element.replace(specific_word, ''))
                else:
                    updated_list.append(element)
            measure_selected_key_val_resp[key] = updated_list

        for key, value in dict_selected_measures_lst.items():
            updated_list = []
            for element in value:
                if specific_word in element:
                    updated_list.append(element.replace(specific_word, ''))
                else:
                    updated_list.append(element)
            dict_selected_measures_lst[key] = updated_list

    return measure_selected_key_val_resp,dict_selected_measures_lst

    ################################################################################


def replace_string_in_dict(original_dict, old_string, new_string):
    new_dict = {}
    for key, value in original_dict.items():
        # Check if the old string is present in the key
        if isinstance(key, str) and old_string in key:
            key = key.replace(old_string, new_string)
        # Check if the value is a list
        if isinstance(value, list):
            # Replace old string with new string in each element of the list
            value = [item.replace(old_string, new_string) if isinstance(item, str) else item for item in value]
        elif isinstance(value, str) and old_string in value:
            # If value is a string, replace old string with new string
            value = value.replace(old_string, new_string)
        new_dict[key] = value
    return new_dict
