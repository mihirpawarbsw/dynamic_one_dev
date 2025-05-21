
import numpy
import pandas as pd
import numpy as np
import os,json
import time
import statistics as st
import copy
# from django.conf import settings
from main_dashboard.bcst_sales_derived_measures import *
import warnings
warnings.filterwarnings('ignore')
import random


# PYTHONPATH = r"C:\Mihir_Python_Projects\BCST_Tool_Core_Python_Logic\ccv_tool_Sales\\BCST_Sales_Data\\"
# PYTHONPATH = r"C:\Users\MihirPawar\Desktop\Python Project BSW\Python Files1\ccv_tool\ccv_survey_data\\"
# MERGED_PYTHONPATH = merged_pythonpath = r"C:\Mihir_Python_Projects\BCST_Tool_Core_Python_Logic\ccv_tool_Sales\merged_data_files\\"

def single_dimension_logic(df,row_name,col_name,seperated_flag_row,selected_weight_column_all,agg_func):
    if (len(row_name) >= 1) and len(col_name) == 0:

        if seperated_flag_row == 0:
            cross_df = pd.DataFrame(df.groupby(row_name)[selected_weight_column_all].sum())
            row_name_str = ''.join([str(elem) for elem in row_name])

            if (len(row_name) == 1):
                cross_df = pd.concat([cross_df], keys=[row_name_str], axis=0)

            if (len(row_name) > 1):
                row_name_outer = row_name[-1]
                # print('row_name_outer--32',row_name_outer)
                cross_df_outer = pd.DataFrame(df.groupby(row_name_outer)[selected_weight_column_all].sum())
                cross_df_outer = pd.concat([cross_df_outer], keys=['Grand Total'], axis=0)
                cross_df = pd.concat([cross_df, cross_df_outer])
                # cross_df.to_excel('cross_df_outer.xlsx')

        elif seperated_flag_row == 1:
            cross_df_stacked_lst = []
            for row_name_loop in row_name:
                cross_df = pd.DataFrame(df.groupby(row_name_loop)[selected_weight_column_all].sum())

                row_name_str = ''.join([str(elem) for elem in row_name_loop])

                cross_df = pd.concat([cross_df], keys=[row_name_str], axis=0)
                cross_df_stacked_lst.append(cross_df)

            cross_df = pd.concat(cross_df_stacked_lst)

        if len(row_name) == 1:

            df_level1 = cross_df.groupby(level=0).agg(agg_func)
            df_level1.index = df_level1.index = pd.MultiIndex.from_arrays([df_level1.index.values,
                                                                           len(df_level1.index) * ['Grand Total']])
            # Concatenate the totals row to the original DataFrame
            cross_df = pd.concat([cross_df, df_level1])

        elif len(row_name) > 1:

            cross_df = subtotals_multi_actuals_new(cross_df, row_name, agg_func)

    cross_df = pd.concat([cross_df], keys=['Metrics'], axis=1)
    # Create a copy of the original DataFrame
    df_gt = cross_df.copy()

    df_gt = df_gt.droplevel(0, axis=1)
    # Rename the level 0 column to "Grand Total"
    df_gt = pd.concat([df_gt], keys=['Grand Total'], axis=1)

    # Concatenate the original and copied DataFrames side by side
    cross_df = pd.concat([cross_df, df_gt], axis=1)
    # cross_df.to_excel('cross_df_singlee.xlsx')
    return cross_df

def sort_columns(cross_df, measure_row_column_position, column_to_sort, asc_desc_param):
    if measure_row_column_position == "measure_in_column":
        cross_df_dataframes_lst2 = []
        level_0_index = cross_df.index.get_level_values(0).unique().tolist()

        cross_df_index_grp = cross_df.groupby(axis=0, level=0)

        # Access each group
        for cross_df_index_loop in level_0_index:
            # print('====cross_df_col_loop 2365', cross_df_index_loop)
            cross_df_index = cross_df_index_grp.get_group(cross_df_index_loop)
            cross_df_index_df = pd.DataFrame(cross_df_index)

            # Filter for 'Grand Total' and 'Total (Among Displayed)'
            filtered_df = cross_df_index_df[cross_df_index_df.index.get_level_values(1).isin(['Grand Total', 'Total (Among Displayed)'])]

            # Check for 'cagr_none' in the sortable column
            if cross_df_index_df[column_to_sort].apply(lambda x: isinstance(x, str) and 'cagr_none' in x).any():
                # If 'cagr_none' is present, skip sorting
                # print(f"Skipping sorting for {cross_df_index_loop} due to 'cagr_none'.")
                final_cross_df_index = pd.concat([cross_df_index_df, filtered_df])
            else:
                # Create a new column for sorting and check for original % presence
                cross_df_index_df['sortable'] = cross_df_index_df[column_to_sort].apply(
                    lambda x: (float(x.replace('%', '')), True) if isinstance(x, str) and '%' in x else (x, False)
                )

                # Sort the DataFrame based on the numeric value
                cross_df_index_df = cross_df_index_df.sort_values(by='sortable', key=lambda col: col.apply(lambda x: x[0]), ascending=asc_desc_param)

                # Restore the original format, keeping % if it was originally present
                cross_df_index_df[column_to_sort] = cross_df_index_df['sortable'].apply(
                    lambda x: f"{x[0]}%" if x[1] else x[0]  # Append % if it was stripped
                )
                cross_df_index_df.drop(columns=['sortable'], inplace=True)

                final_cross_df_index = pd.concat([cross_df_index_df, filtered_df])

            cross_df_dataframes_lst2.append(final_cross_df_index)

        cross_df = pd.concat(cross_df_dataframes_lst2, axis=0)

    elif measure_row_column_position == "measure_in_row":
        cross_df = cross_df.copy()

    return cross_df

def convert_to_single_level(df):
    # Flatten MultiIndex columns by concatenating level names with '||'
    df_single = df.copy()
    df_single.columns = ['||'.join(map(str, col)) for col in df_single.columns]
    return df_single

def revert_to_multiindex(df_single):
    # Revert back to MultiIndex DataFrame
    df_multi = df_single.copy()
    levels = [tuple(col.split("||")) for col in df_single.columns]
    df_multi.columns = pd.MultiIndex.from_tuples(levels)
    return df_multi


def derived_MAIN_fn(cross_df,base_sales_index_colname,row_name,col_name,measure_row_column_position,cagr_power_val,brand_sales_index_value_flag):

    ############################### NEW CODE - 10-05-2025 #############################
    # Step 1: Get unique last-level column names from cross_df
    last_level_listt = cross_df.columns.get_level_values(-1).unique().tolist()
    last_level_listt = [col.strip() for col in last_level_listt]
    # print('last_level_listt -', last_level_listt)

    # Build mapping dictionary with conditional suffixes
    mapping_dict = {}
    for col in last_level_listt:
        if 'Door' in col:
            suffix = ' Door'
        elif 'Unit' in col:
            suffix = ' Units'
        else:
            suffix = ' Sales'
        mapping_dict[col] = col + suffix

    # print('146 -', mapping_dict)


    ############################### NEW CODE - 10-05-2025 #############################

    # cross_df.to_csv('cross_dfff_182.csv')

    df_single = convert_to_single_level(cross_df)
    # df_single.to_excel('df_single.xlsx')

    cross_df_dataframes_lst2 = []
    level_0_index = df_single.index.get_level_values(0).unique().tolist()

    cross_df_index_grp = df_single.groupby(axis=0, level=0)
    # Access the first group
    for cross_df_index_loop in level_0_index:
        # print('====cross_df_col_loop 2365', cross_df_index_loop)
        cross_df_index = cross_df_index_grp.get_group(cross_df_index_loop)
        cross_df_index_df = pd.DataFrame(cross_df_index)
        cross_df_index_df.columns = cross_df_index_df.columns.str.replace(r'\s*Sales$', '', regex=True)
        # print('cross_df_index_df 191--',cross_df_index_df.columns)
        # cross_df_index_df.to_excel('cross_df_index_df.xlsx')
        filtered_df = cross_df_index_df[cross_df_index_df.index.get_level_values(1) == 'Grand Total']
        # filtered_df.to_excel('filtered_df_cross_df_col_df_xxdfd.xlsx')

        cross_df_index_df = derived_measures_after_crosstab(cross_df_index_df, filtered_df,base_sales_index_colname,row_name,col_name,measure_row_column_position,cagr_power_val,brand_sales_index_value_flag)


        # cross_df_index_df.to_excel('cross_df_col_df_xxdfd.xlsx')
        # exit('dfsdf')
        cross_df_dataframes_lst2.append(cross_df_index_df)

    cross_df_temp = pd.concat(cross_df_dataframes_lst2, axis=0)
    # cross_df_temp.to_excel('CROSS_DF_CAUCULATIONS11.xlsx')
    cross_df = revert_to_multiindex(cross_df_temp)

    ############################ new code - 10-05-2025 ###############################
    # Step 4: Apply mapping only to last level of MultiIndex in cross_df2
    new_cols = []
    for col in cross_df.columns:
        *upper, last = col
        if last in mapping_dict:
            new_col = tuple(upper + [mapping_dict[last]])
        else:
            new_col = col
        new_cols.append(new_col)

    cross_df.columns = pd.MultiIndex.from_tuples(new_cols)
    ############################ new code - 10-05-2025 ###############################
    # cross_df.to_excel('CROSS_DF_CAUCULATIONS.xlsx')
    return cross_df


def subtotals_multi_actuals_new(cross_df, row_name,agg_func):
    # print('subtotals_multi_actuals_new== BEGINS!')

    if len(row_name) == 2:
        # print('multilevel 2')
        df_level1 = cross_df.groupby(level=0).agg(agg_func)
        df_level1.index = df_level1.index = pd.MultiIndex.from_arrays([df_level1.index.values,
                                                                       len(df_level1.index) * ['Grand Total']])

        # concat all dataframes together, sort index
        cross_df = pd.concat([cross_df, df_level1]).sort_index(level=[0])

    elif len(row_name) == 3:
        # print("multi_subtotals three rows")

        df_level1 = cross_df.groupby(level=[0, 1]).agg(agg_func)
        df_level1.index = pd.MultiIndex.from_arrays([df_level1.index.get_level_values(0),
                                                     df_level1.index.get_level_values(1),
                                                     len(df_level1.index) * ['Grand Total']])

        df_level2 = cross_df.groupby(level=0).agg(agg_func)
        df_level2.index = pd.MultiIndex.from_arrays([df_level2.index.values,
                                                     len(df_level2.index) * ['Grand Total'],
                                                     len(df_level2.index) * ['']])

        # concat all dataframes together, sort index
        cross_df = pd.concat([cross_df, df_level1, df_level2]).sort_index(level=[0, 1])

    return cross_df


# def concat_data(dict_table):
def concat_data(dict_table,loop_vals_lst,base_filter_col_lst,selected_weight_column):
    start_time_concat = time.time()

    # loop_vals_lst = loop_vals_lst + ['LinkID','weighting'] #new code modified on 05-12-2022
    loop_vals_lst = loop_vals_lst + ['LinkID'] + base_filter_col_lst + [selected_weight_column] #new code modified on 11-04-2023

    loop_vals_lst = list(set(loop_vals_lst))

    table_name_cols = []
    for data_concat_loop in dict_table.keys():
        # print("dict_table.keys===",data_concat_loop)

        table_name = data_concat_loop + ".json"
        # print("table_name",table_name)

        df_table = pd.read_json(PYTHONPATH + table_name, orient='records', lines=True)

        df_table1_final = df_table[loop_vals_lst]

        table_name_cols.append(df_table1_final)
    df = pd.concat(table_name_cols).reset_index(drop=True)
    # #df.to_excel("df_concatt.xlsx",index=False)

    # exit("end it!")
    return df,loop_vals_lst

def merge_data(dict_table):
    start_time_merge=time.time()

    # print("dict_table keys",dict_table.keys())
    # print("dict_table values",dict_table.values())

    table_name1_filename = list(dict_table.keys())[0] + ".json"
    table_name2_filename = list(dict_table.keys())[1] + ".json"

    table_name1_cols = list(dict_table.values())[0] + ['LinkID','weighting']
    table_name2_cols = list(dict_table.values())[1] + ['LinkID','Volume']

    df_table1 = pd.read_json(PYTHONPATH + table_name1_filename, orient='records', lines=True)
    df_table2 = pd.read_json(PYTHONPATH + table_name2_filename, orient='records', lines=True)

    df_table1_final = df_table1[table_name1_cols]
    df_table2_final = df_table2[table_name2_cols]

    # print("length df_table1",len(df_table1_final))
    # print("length df_table2",len(df_table1_final))

    # df_table1_final.set_index('LinkID',inplace=True)
    # df_table1_final.set_index('LinkID',inplace=True)
    # exit("enddd!")

    # if len(df_table1_final) > len(df_table2_final):
    #     df = df_table1_final.merge(df_table2_final, how='left', on='LinkID')
    # elif len(df_table2_final) > len(df_table1_final):
    df = df_table2_final.merge(df_table1_final, how='left', on='LinkID')  #24-01-22
    # df = df_table2_final.join(df_table1_final, how='left', on='LinkID')  #24-01-22
    # df = pd.concat([df_table2_final.set_index('LinkID'),df_table1_final.set_index('LinkID')], axis=1, join='inner').reset_index()

    end_time_merge=time.time()

    # print("TIME TAKEN TO MERGE:-",end_time_merge-start_time_merge," seconds")

    # df.to_csv("df_merged22.csv",index=False)
    if 'Volume' not in df_table2:
        # print("Volume is not Present in Data")
        df['Volume'] = 1
    else:
        # print("Volume is Present in Data")
        pass

    if 'weighting' not in df_table1.columns:
        # print("weighting is not Present in Data")
        df['weighting'] = 1
    else:
        pass

    # filename_merged = list(dict_table.keys())
    # filename_merged = '_'.join([str(elem) for i, elem in enumerate(filename_merged)])
    # # print("filename_merged", filename_merged)
    # # exit("filename_merged")
    # df.to_json(MERGED_PYTHONPATH + filename_merged + ".json", orient='records', lines=True)
    # table_colnames_before_merge = list(table_name1_cols+table_name2_cols)
    # exit("filename_merged")
    return df

def prefix_values(df):

    df_obj = df.copy()

    for selected_column in df_obj.columns:

        freq_vals = df_obj[selected_column].value_counts()

        df_Freq = pd.DataFrame(columns=['Values'])
        # df_Freq['Column']=df.columns
        df_Freq['Values'] = freq_vals

        alpha_list = []
        # alpha = '1' #A
        # for i in range(0, len(df_Freq)):
        #     alpha_list.append(alpha)
        #     alpha = chr(ord(alpha) + 1)

        for i in range(0, len(df_Freq)):
            nums='{:d}'.format(i).zfill(3)
            alpha_list.append(nums)

        # df_Freq.to_excel('df_Freq.xlsx')
        # exit('df_Freq')
        df_Freq = df_Freq.reset_index().rename(columns={'index': 'Columns'})
        df_Freq['Columns'] = df_Freq['Columns'].apply(str)

        df_Freq.sort_values(by=['Columns'], inplace=True)  # new added on 03-11-2022
        df_Freq['alpha_prefix'] = alpha_list
        #
        # if selected_column == 'Gender' or 'Age_:_Post_code':
        #
        #     df_Freq.sort_values(by=['Columns'],ascending=False, inplace=True)  # new added on 03-11-2022
        #     df_Freq['alpha_prefix'] = alpha_list
        #
        # else:
        #     df_Freq['alpha_prefix'] = alpha_list

        df_Freq['prefix_col'] = df_Freq['alpha_prefix'].astype(str) + "}" + df_Freq['Columns'].astype(str)
        #########################################################################################################
        # df_Freq['prefix_col'].replace(' ', '_', regex=True, inplace=True)
        #########################################################################################################

        codeframe_key = df_Freq['Columns'].astype(str).to_list()
        codeframe_value = df_Freq['prefix_col'].to_list()

        codeframe_dict = {}
        for loop in range(len(codeframe_key)):
            update_dict = {df_Freq['Columns'][loop]: df_Freq['prefix_col'][loop]}
            codeframe_dict.update(update_dict)

        # print('codeframe_dict', codeframe_dict)

        df[selected_column] = df[selected_column].map(codeframe_dict)

    return df

def nested_crosstab(df,row_name,col_name,row_list_vals,col_list_vals,percent_calc,parameter_calc,
                    selected_weight_column,totals_nested_flag,agg_func,measure_row_column_position):
    # print("nested_crosstab starts")
    # print('df shapee 549---',df.shape)

    cross_df = crosstab_actual_counts(df,row_name,col_name,row_list_vals,col_list_vals,percent_calc,parameter_calc,
                selected_weight_column,agg_func)
    # cross_df.to_excel('cross_553.xlsx')

    # random_suffix = random.randint(1000, 9999)  # Generates a 4-digit random number

    # output_filename = f"your_file_{random_suffix}.xlsx"

    # cross_df.to_excel(output_filename)
    ######## ADDED BY MIHIR PAWAR - 17-05-2023 ######################################################################
    if len(col_name) == 1 and len(row_name) == 1:
        row_name_str = ''.join([str(elem) for elem in row_name])
        col_name_str = ''.join([str(elem) for elem in col_name])

        cross_df = pd.concat([cross_df], keys=[row_name_str], axis=0)
        cross_df = pd.concat([cross_df], keys=[col_name_str], axis=1)

    ######## ADDED BY MIHIR PAWAR - 17-05-2023 ######################################################################

    # print("CROSSTAB TABLE CREATED SUCCESSFULLY=======!")
    # exit("End it!!")

    ############### TEMP CODE NESTED SUPER GRAND TOTALS - 10-05-2024 ##
    weight_param = 'unweighted'

    if len(row_name) > 1 and len(col_name) > 1: 

        cross_df = multi_subtotals_ACTUALS_TABLE(cross_df, row_name)
        cross_df = cross_df.T
        cross_df = multi_subtotals_ACTUALS_TABLE(cross_df, col_name)
        cross_df = cross_df.T
        # cross_df.to_excel('crouuuu.xlsx')

        #####$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4
        # if measure_row_column_position == 'measure_in_row':
        #     cross_df_cols_nested = table_or_actual_totals_nested_COLS(df,row_name,col_name,row_list_vals,col_list_vals,percent_calc,parameter_calc,
        #         selected_weight_column,weight_param)

        #     cross_df_cols_nested = cross_df_cols_nested.loc[:, ~cross_df_cols_nested.columns.duplicated(keep='last')].copy()

        #     for loop_nested_totals in range(len(col_name)-2):
        #         print('loop_nested_totals====',loop_nested_totals)
        #         cross_df_cols_nested = pd.concat([cross_df_cols_nested], keys=[''], axis=1)
        #     #
        #     cross_df_cols_nested = pd.concat([cross_df_cols_nested], keys=['Grand Total'], axis=1)

        #     try:
        #         cross_df_cols_nested.drop(('Grand Total', ''), axis=0, inplace=True)
        #     except:
        #         pass

        #     cross_df_cols_nested = multi_subtotals_ACTUALS_TABLE(cross_df_cols_nested, col_name)
        #     cross_df_cols_nested.to_excel('CROSS_DF1.xlsx')

        #     cross_df = pd.concat([cross_df,cross_df_cols_nested],axis=1)

        # elif measure_row_column_position == 'measure_in_column':
        #     cross_df_rows_nested = table_or_actual_totals_nested_ROWS(df, row_name, col_name, row_list_vals,
        #                                                               col_list_vals, percent_calc, parameter_calc,
        #                                                               selected_weight_column, weight_param)

        #     cross_df_rows_nested = cross_df_rows_nested[~cross_df_rows_nested.index.duplicated(keep='last')]

        #     for loop_nested_totals in range(len(row_name) - 2):
        #         cross_df_rows_nested = pd.concat([cross_df_rows_nested], keys=[''], axis=0)

        #     cross_df_rows_nested = pd.concat([cross_df_rows_nested], keys=['Grand Total'], axis=0)

        #     cross_df_rows_nested = cross_df_rows_nested.T
        #     cross_df_rows_nested = multi_subtotals_ACTUALS_TABLE(cross_df_rows_nested, col_name)
        #     cross_df_rows_nested = cross_df_rows_nested.T

        #     try:
        #         cross_df_rows_nested.drop(('Grand Total', ''), axis=1, inplace=True)
        #     except:
        #         pass
        #     try:
        #         cross_df_rows_nested.drop(('Grand Total', 'Grand Total'), axis=1, inplace=True)
        #     except:
        #         pass

        #     # cross_df_rows_nested.to_excel('CROSS_DF2.xlsx')

        #     cross_df = pd.concat([cross_df,cross_df_rows_nested],axis = 0)

    #####$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4
    ############### TEMP CODE NESTED SUPER GRAND TOTALS - 10-05-2024 ##

    ######################### TRAIL CODE - SUPER NESTD GRAND TOTALS ####################
    ######################### TRAIL CODE - SUPER NESTD GRAND TOTALS ####################
        cross_df_cols_nested = table_or_actual_totals_nested_COLS(df,row_name,col_name,row_list_vals,col_list_vals,percent_calc,parameter_calc,
            selected_weight_column,weight_param)

        cross_df_cols_nested = cross_df_cols_nested.loc[:, ~cross_df_cols_nested.columns.duplicated(keep='first')].copy()

        for loop_nested_totals in range(len(col_name)-2):
            # print('loop_nested_totals====',loop_nested_totals)
            cross_df_cols_nested = pd.concat([cross_df_cols_nested], keys=[''], axis=1)
        #
        cross_df_cols_nested = pd.concat([cross_df_cols_nested], keys=['Grand Total'], axis=1)

        try:
            cross_df_cols_nested.drop(('Grand Total', ''), axis=0, inplace=True)
        except:
            pass

        cross_df_cols_nested = multi_subtotals_ACTUALS_TABLE(cross_df_cols_nested, col_name)
        # cross_df_cols_nested.to_excel('CROSS_DF1.xlsx')

        ##################################### ADDING NESTED COLUMNS #############################################

        ######################################## ADDING NESTED ROWS #################################################
        cross_df_rows_nested = table_or_actual_totals_nested_ROWS(df, row_name, col_name, row_list_vals,
                                                                  col_list_vals, percent_calc, parameter_calc,
                                                                  selected_weight_column, weight_param)

        cross_df_rows_nested = cross_df_rows_nested[~cross_df_rows_nested.index.duplicated(keep='first')]

        for loop_nested_totals in range(len(row_name) - 2):
            cross_df_rows_nested = pd.concat([cross_df_rows_nested], keys=[''], axis=0)

        cross_df_rows_nested = pd.concat([cross_df_rows_nested], keys=['Grand Total'], axis=0)

        cross_df_rows_nested = cross_df_rows_nested.T
        cross_df_rows_nested = multi_subtotals_ACTUALS_TABLE(cross_df_rows_nested, col_name)
        cross_df_rows_nested = cross_df_rows_nested.T

        try:
            cross_df_rows_nested.drop(('Grand Total', ''), axis=1, inplace=True)
        except:
            pass
        try:
            cross_df_rows_nested.drop(('Grand Total', 'Grand Total'), axis=1, inplace=True)
        except:
            pass

        # cross_df_rows_nested.to_excel('CROSS_DF2.xlsx')

        ######################################## ADDING NESTED ROWS #################################################

        ###################################################################################################################
        row_name = row_name[-1]
        col_name = col_name[-1]
        row_name_str = ''.join([str(elem) for elem in row_name])
        col_name_str = ''.join([str(elem) for elem in col_name])

        cross_df_1x1 = pd.crosstab(index=[df[row_name_str]], columns=[df[col_name_str]],
                               rownames=[row_name_str],
                               colnames=[col_name_str], values=df[selected_weight_column], aggfunc=sum,
                               normalize=parameter_calc, margins=True, margins_name='Grand Total')

        cross_df_1x1 = pd.concat([cross_df_1x1], keys=['Grand Total'], axis=0)
        cross_df_1x1 = pd.concat([cross_df_1x1], keys=['Grand Total'], axis=1)
        # cross_df_1x1.to_excel('CROSS_DF3.xlsx')

        cross_df_cols_nested2 = pd.concat([cross_df_1x1,cross_df_rows_nested], axis=1)
        # cross_df_cols_nested2.to_excel('CROSS_DF4.xlsx')

        cross_df33 = pd.concat([cross_df_cols_nested, cross_df], axis=1)

        try:
            cross_df33.drop(('Grand Total', ''), axis=1, inplace=True)
        except:
            pass
        try:
            cross_df33.drop(('Grand Total', 'Grand Total'), axis=1, inplace=True)
        except:
            pass
        # cross_df33.to_excel('CROSS_DF8.xlsx')

        #####################################################################################
        cross_df = pd.concat([cross_df_cols_nested2, cross_df33], axis=0)
        try:
            cross_df.drop(('Grand Total', ''), axis=1, inplace=True)
        except:
            pass
        try:
            cross_df33.drop(('Grand Total', 'Grand Total'), axis=1, inplace=True)
        except:
            pass
        # cross_df.to_excel('NESTED_WITH_TOTALS.xlsx')
        #####################################################################################
            # exit('cross_dfdddfdg396')
    ######################### TRAIL CODE - SUPER NESTD GRAND TOTALS ####################
    ######################### TRAIL CODE - SUPER NESTD GRAND TOTALS ####################
    # ############################ ADDED BY MIHIR PAWAR ON 17-05-2023 ##############################################
    if len(col_name) > 1 and len(row_name) == 1:
        row_name_str = ''.join([str(elem) for elem in row_name])

        cross_df = pd.concat([cross_df], keys=[row_name_str], axis=0)
    # ############################ ADDED BY MIHIR PAWAR ON 17-05-2023 ##############################################
    # print("SUBTOTALS ADDED TO TABLE SUCCESSFULLY!")
    # # exit('emd!!!')
    # # cross_#df.to_excel("cross_df_1112.xlsx")
    # # exit("cross_df exit nesteed")
    #
    if (len(col_name) == 1 and len(row_name) > 1):
        col_name_str = ''.join([str(elem) for elem in col_name])
        cross_df = pd.concat([cross_df], keys=[col_name_str], axis=1)  ####### 31-03-2023

    # elif (len(col_name) > 1 and len(row_name) == 1):
    #     row_name_str = ''.join([str(elem) for elem in row_name])
    #     cross_df = pd.concat([cross_df], keys=[row_name_str], axis=0)  ####### 31-03-2023
    #
    #
    # try:
    #     if percent_calc == 'table_percent':
    #         cross_df = cross_df.drop(('Grand Total',''),axis = 1)
    # except:
    #     pass
    # print("nested_crosstab ends!")
    return cross_df

def multi_subtotals_ACTUALS_TABLE(cross_df, row_name):
    if len(row_name) == 2:
        # print("multi_subtotals two rows")
        df1 = cross_df.groupby(level=0).sum()
        # df1.to_excel("df1_df1_after_transpose.xlsx")
        # df1.index=pd.MultiIndex.from_arrays([df1.index.values + '_total', len(df1.index) * ['']])
        # ############### COMMENTED BY MIHIR PAWAR 21-04-2023
        df1.index = pd.MultiIndex.from_arrays([df1.index.values, len(df1.index) * ['Grand Total']])

        # df1.to_excel('df1_subtotals.xlsx')f
        # df2.index = pd.MultiIndex.from_arrays([df2.index.values + '_total',len(df2.index) * ['']])

        cross_df = pd.concat([cross_df, df1]).sort_index(level=0)

    if len(row_name) == 3:
        # print("multi_subtotals three rows")
        df1 = cross_df.groupby(level=[0,1]).sum()
        df1.index = pd.MultiIndex.from_arrays([df1.index.get_level_values(0),
                                               df1.index.get_level_values(1),
                                               len(df1.index) * ['Grand Total']])

        df2 = cross_df.groupby(level=0).sum()

        df2.index = pd.MultiIndex.from_arrays([df2.index.values,
                                               len(df2.index) * ['Grand Total'],
                                               len(df2.index) * ['']])

        # concat all dataframes together, sort index
        cross_df = pd.concat([cross_df, df1, df2]).sort_index(level=[0, 1])
        # cross_df = pd.concat([cross_df, df1, df2]).sort_index()

    if len(row_name) == 4:
        # print("multi_subtotals four rows")
        df1 = cross_df.groupby(level=[0, 1, 2]).sum()

        df1.index = pd.MultiIndex.from_arrays([df1.index.get_level_values(0),
                                               df1.index.get_level_values(1),
                                               df1.index.get_level_values(2),
                                               len(df1.index) * ['Grand Total']])

        # print("multi_subtotals three rows")

        df2 = cross_df.groupby(level=[0, 1]).sum()
        df2.index = pd.MultiIndex.from_arrays([df2.index.get_level_values(0),
                                               df2.index.get_level_values(1),
                                               len(df2.index) * ['Grand Total'],
                                               len(df2.index) * ['']])

        df3 = cross_df.groupby(level=0).sum()

        df3.index = pd.MultiIndex.from_arrays([df3.index.values,
                                               len(df3.index) * ['Grand Total'],
                                               len(df3.index) * [''],
                                               len(df3.index) * ['']])

        # concat all dataframes together, sort index
        cross_df = pd.concat([cross_df, df1, df2, df3]).sort_index(level=[0, 1, 2])

    if len(row_name) == 5:
        # print("row_name>>>", row_name)

        df1 = cross_df.groupby(level=[0, 1, 2, 3]).sum()
        df1.index = pd.MultiIndex.from_arrays([df1.index.get_level_values(0),
                                               df1.index.get_level_values(1),
                                               df1.index.get_level_values(2),
                                               df1.index.get_level_values(3),
                                               len(df1.index) * ['Grand Total']])

        df2 = cross_df.groupby(level=[0, 1, 2]).sum()
        df2.index = pd.MultiIndex.from_arrays([df2.index.get_level_values(0),
                                               df2.index.get_level_values(1),
                                               df2.index.get_level_values(2),
                                               len(df2.index) * ['Grand Total'],
                                               len(df2.index) * ['']])

        df3 = cross_df.groupby(level=[0, 1]).sum()
        df3.index = pd.MultiIndex.from_arrays([df3.index.get_level_values(0),
                                               df3.index.get_level_values(1),
                                               len(df3.index) * ['Grand Total'],
                                               len(df3.index) * [''],
                                               len(df3.index) * ['']])

        df4 = cross_df.groupby(level=0).sum()
        df4.index = pd.MultiIndex.from_arrays([df4.index.values,
                                               len(df4.index) * ['Grand Total'],
                                               len(df4.index) * [''],
                                               len(df4.index) * [''],
                                               len(df4.index) * ['']])

        # concat all dataframes together, sort index
        cross_df = pd.concat([cross_df, df1, df2, df3, df4]).sort_index(level=[0, 1, 2, 3])

    return cross_df


def table_or_actual_totals_nested_ROWS(df, row_name, col_name, row_list_vals, col_list_vals, percent_calc,
                                       parameter_calc,
                                       selected_weight_column, weight_param):
    if len(col_name) == 1:
        # print("WEIGHTED rowname equal to 1 condition seperated ROWS")

        # cross_df_list = []
        # for row_loop in row_name:
        row_loop = row_name[-1]
        # print(" FIRST CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH EQUAL TO 1!")
        row_name_str = ''.join([str(elem) for elem in row_loop])
        col_name_str = ''.join([str(elem) for elem in col_name])

        cross_df = pd.crosstab(index=[df[row_name_str]], columns=[df[col_name_str]],
                               rownames=[row_name_str],
                               colnames=[col_name_str], values=df[selected_weight_column], aggfunc=sum,
                               normalize=parameter_calc,margins=True,margins_name='Grand Total')
        # if percent_calc == 'actual_count':
        #     cross_df = cross_df / 100

        # cross_df_list.append(cross_df)

        # cross_df = pd.concat(cross_df_list, axis=0)

    elif len(col_name) > 1:
        # print("WEIGHTED colname greater than 1 condition seperated ROWS")
        # cross_df_list = []
        # for row_loop in row_name:
        row_loop = row_name[-1]
        row_name_str = ''.join([str(elem) for elem in row_loop])

        if percent_calc == 'column_percent' or percent_calc == 'actual_count' or percent_calc == 'table_percent':
            cross_df = pd.crosstab(index=[df[row_name_str]], columns=col_list_vals, rownames=[row_name_str],
                                   colnames=col_name, values=df[selected_weight_column], aggfunc=sum,
                                   normalize=parameter_calc,margins=True,margins_name='Grand Total')

        # if percent_calc == 'actual_count':
        #     cross_df = cross_df.drop('Total', axis=0)
        #     cross_df = cross_df / 100

        # if percent_calc == 'column_percent':
        #     cross_df = cross_df.drop('Total', axis=1)

        # cross_df_list.append(cross_df)

        # cross_df = pd.concat(cross_df_list, axis=0)

    cross_df_rows_nested = cross_df.copy()

    return cross_df_rows_nested


def table_or_actual_totals_nested_COLS(df, row_name, col_name, row_list_vals, col_list_vals, percent_calc,
                                       parameter_calc,
                                       selected_weight_column, weight_param):
    if len(row_name) == 1:
        # print("UNWEIGHTED rowname equal to 1 condition seperated COLUMNS")

        cross_df_list = []
        # for col_loop in col_name:
        col_loop = col_name[-1]
        # print(" FIRST CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH EQUAL TO 1!")
        row_name_str = ''.join([str(elem) for elem in row_name])
        col_name_str = ''.join([str(elem) for elem in col_loop])

        cross_df = pd.crosstab(index=[df[row_name_str]], columns=[df[col_name_str]],
                               rownames=[row_name_str],
                               colnames=[col_name_str], values=df[selected_weight_column], aggfunc=sum,
                               normalize=parameter_calc,margins=True,margins_name='Grand Total')

        # if percent_calc == 'actual_count':
        #     cross_df = cross_df.drop('Total', axis=0)

        # cross_df_list.append(cross_df)

        # cross_df = pd.concat(cross_df_list, axis=1)
        # cross_#df.to_excel("Cross_df_nested_collll_rows.xlsx")

    elif len(row_name) > 1:
        # print("UNWEIGHTED colname greater than 1 condition seperated COLUMNS")
        # cross_df_list = []
        # for col_loop in col_name:
        col_loop = col_name[-1]
        col_name_str = ''.join([str(elem) for elem in col_loop])

        if percent_calc == 'column_percent' or percent_calc == 'actual_count' or percent_calc == 'table_percent':
            cross_df = pd.crosstab(index=row_list_vals, columns=[df[col_name_str]], rownames=row_name,
                                   colnames=[col_name_str], values=df[selected_weight_column], aggfunc=sum,
                                   normalize=parameter_calc,margins=True,margins_name='Grand Total')

    cross_df_cols_nested = cross_df.copy()
    # cross_df_cols_nested.to_excel('cross_df_cols_nested_tttttt.xlsx')

    return cross_df_cols_nested

def subtotals_calc(cross_df,percent_calc,row_name,col_name,cross_df_subtotals_single_dict):

    # print("subtotals_calc function Running...")
    # print("===cross_df_subtotals_single_dict===",cross_df_subtotals_single_dict)
    # exit("end code at subtotals!")

    # if percent_calc == 'column_percent' or percent_calc == 'actual_count':
    if percent_calc == 'row_percent':

        # print("multi_subtotals FUNCTION Running..")
        #########################################################################################################
        cross_df=multi_subtotals(cross_df,row_name,cross_df_subtotals_single_dict,percent_calc)
        #########################################################################################################

    # if percent_calc == 'column_percent':
    if percent_calc == 'column_percent' or percent_calc == 'actual_count' or percent_calc == 'table_percent':

        # cross_df=cross_df.drop('Total',axis=1)
        cross_df = cross_df.T
        # cross_df_subtotals_single = cross_df_subtotals_single.T
        ##########################################################################################################
        cross_df = multi_subtotals(cross_df, col_name,cross_df_subtotals_single_dict,percent_calc)
        # cross_df = multi_subtotals(cross_df,row_name)
        ##########################################################################################################

        cross_df = cross_df.T

    return cross_df



def multi_subtotals(cross_df,row_name,cross_df_subtotals_single_dict,percent_calc):

    if len(row_name)==2:
        # print("multi_subtotals two rows")

        df1 = list(cross_df_subtotals_single_dict.values())[0]
        # df1.to_excel("df1_df1_before_transpose.xlsx")
        if percent_calc == 'column_percent' or percent_calc == 'actual_count' or percent_calc == 'table_percent':
            df1=df1.T
            # pass
        # df1.to_excel("df1_df1_after_transpose.xlsx")
        # df1.index=pd.MultiIndex.from_arrays([df1.index.values + '_total', len(df1.index) * ['']])
        # ############### COMMENTED BY MIHIR PAWAR 21-04-2023
        df1.index=pd.MultiIndex.from_arrays([df1.index.values, len(df1.index) * ['Grand Total']])

        # df1.to_excel('df1_subtotals.xlsx')f
        # df2.index = pd.MultiIndex.from_arrays([df2.index.values + '_total',len(df2.index) * ['']])

        cross_df = pd.concat([cross_df, df1]).sort_index(level=0)


    if len(row_name)==3:
        # print("multi_subtotals three rows")

        df1 = list(cross_df_subtotals_single_dict.values())[1]
        if percent_calc == 'column_percent' or percent_calc == 'actual_count' or percent_calc == 'table_percent':
            df1 = df1.T

        df1.index = pd.MultiIndex.from_arrays([df1.index.get_level_values(0),
                                               df1.index.get_level_values(1),
                                               len(df1.index) * ['Grand Total']])

        # df2 = cross_df.groupby(level=0).sum()
        df2 = list(cross_df_subtotals_single_dict.values())[0]

        if percent_calc == 'column_percent' or percent_calc == 'actual_count' or percent_calc == 'table_percent':
            df2 = df2.T

        df2.index = pd.MultiIndex.from_arrays([df2.index.values,
                                               len(df2.index) * ['Grand Total'],
                                               len(df2.index) * ['']])

        # concat all dataframes together, sort index
        cross_df = pd.concat([cross_df, df1, df2]).sort_index(level=[0,1])
        # cross_df = pd.concat([cross_df, df1, df2]).sort_index()

    if len(row_name)==4:
        # print("multi_subtotals four rows")
        # df1 = cross_df.groupby(level=[0, 1, 2]).sum()

        df1 = list(cross_df_subtotals_single_dict.values())[2]
        if percent_calc == 'column_percent' or percent_calc == 'actual_count' or percent_calc == 'table_percent':
            df1 = df1.T
        df1.index = pd.MultiIndex.from_arrays([df1.index.get_level_values(0),
                                               df1.index.get_level_values(1),
                                               df1.index.get_level_values(2),
                                               len(df1.index) * ['Grand Total']])

        # print("multi_subtotals three rows")

        df2 = list(cross_df_subtotals_single_dict.values())[1]
        if percent_calc == 'column_percent' or percent_calc == 'actual_count' or percent_calc == 'table_percent':
            df2 = df2.T
        # df2 = cross_df.groupby(level=[0, 1]).sum()
        df2.index = pd.MultiIndex.from_arrays([df2.index.get_level_values(0),
                                               df2.index.get_level_values(1),
                                               len(df2.index) * ['Grand Total'],
                                               len(df2.index) * ['']])

        # df3 = cross_df.groupby(level=0).sum()

        df3 = list(cross_df_subtotals_single_dict.values())[0]
        if percent_calc == 'column_percent' or percent_calc == 'actual_count' or percent_calc == 'table_percent':
            df3 = df3.T
        df3.index = pd.MultiIndex.from_arrays([df3.index.values,
                                               len(df3.index) * ['Grand Total'],
                                               len(df3.index) * [''],
                                               len(df3.index) * ['']])

        # concat all dataframes together, sort index
        cross_df = pd.concat([cross_df, df1, df2, df3]).sort_index(level=[0, 1, 2])

    if len(row_name) == 5:
        # print("row_name>>>",row_name)

        # df1 = cross_df.groupby(level=[0, 1, 2, 3]).sum()
        df1 = list(cross_df_subtotals_single_dict.values())[3]
        if percent_calc == 'column_percent' or percent_calc == 'actual_count' or percent_calc == 'table_percent':
            df1 = df1.T

        df1.index = pd.MultiIndex.from_arrays([df1.index.get_level_values(0),
                                               df1.index.get_level_values(1),
                                               df1.index.get_level_values(2),
                                               df1.index.get_level_values(3),
                                               len(df1.index) * ['Grand Total']])


        # df2 = cross_df.groupby(level=[0, 1, 2]).sum()
        df2 = list(cross_df_subtotals_single_dict.values())[2]
        if percent_calc == 'column_percent' or percent_calc == 'actual_count' or percent_calc == 'table_percent':
            df2 = df2.T

        df2.index = pd.MultiIndex.from_arrays([df2.index.get_level_values(0),
                                               df2.index.get_level_values(1),
                                               df2.index.get_level_values(2),
                                               len(df2.index) * ['Grand Total'],
                                               len(df2.index) * ['']])

        # df3 = cross_df.groupby(level=[0, 1]).sum()

        df3 = list(cross_df_subtotals_single_dict.values())[1]
        if percent_calc == 'column_percent' or percent_calc == 'actual_count' or percent_calc == 'table_percent':
            df3 = df3.T

        df3.index = pd.MultiIndex.from_arrays([df3.index.get_level_values(0),
                                               df3.index.get_level_values(1),
                                               len(df3.index) * ['Grand Total'],
                                               len(df3.index) * [''],
                                               len(df3.index) * ['']])

        # df4 = cross_df.groupby(level=0).sum()

        df4 = list(cross_df_subtotals_single_dict.values())[0]
        if percent_calc == 'column_percent' or percent_calc == 'actual_count' or percent_calc == 'table_percent':
            df4 = df4.T

        df4.index = pd.MultiIndex.from_arrays([df4.index.values,
                                               len(df4.index) * ['Grand Total'],
                                               len(df4.index) * [''],
                                               len(df4.index) * [''],
                                               len(df4.index) * ['']])

        # concat all dataframes together, sort index
        cross_df = pd.concat([cross_df, df1, df2, df3, df4]).sort_index(level=[0, 1, 2, 3])

    return cross_df

def subtotals_single_cols(df,percent_calc,row_name,col_name,parameter_calc,col_list_vals,row_list_vals,
                          selected_weight_column):
    if percent_calc == 'column_percent' or percent_calc == 'actual_count' or percent_calc == 'table_percent':
    # if percent_calc == 'column_percent':
        col_name1 = col_name[:-1]

        # print('col_name_single_lst initial', col_name1)

        cross_df_subtotals_single_dict = {}
        for loop_col in range(len(col_name1)):

            # print("loop_col loop_col", loop_col)
            col_name = col_name1[0:loop_col + 1]
            # print("col_name col_name", col_name)

            row_list_vals = []
            df_row = df[row_name]
            if len(row_name) > 1:
                for loop_row in range(len(row_name)):
                    str_row = numpy.array(df_row.iloc[:, loop_row])
                    row_list_vals.append(str_row)

            col_list_vals = []
            df_col = df[col_name]
            if len(col_name) > 1:
                for loop_row2 in range(len(col_name)):
                    str_col = numpy.array(df_col.iloc[:, loop_row2])
                    col_list_vals.append(str_col)

            cross_df = crosstab_basic_table(df, percent_calc, row_name, col_name, parameter_calc, col_list_vals,
                                            row_list_vals,
                                            selected_weight_column)

            if percent_calc == 'actual_count' or percent_calc == 'table_percent':
                cross_df = crosstab_actual_counts(df, row_name, col_name, row_list_vals, col_list_vals, percent_calc,
                                                  parameter_calc,
                                                  selected_weight_column,agg_func)

            try:
                # pass
                # cross_df = cross_df[cross_df.columns.drop(list(cross_df.filter(regex='Total total')))]
                cross_df = cross_df.loc[:, ~cross_df.columns.str.contains('^Grand Total', case=False)]           #####Line 471 ACTUAL_COMMENT
            except:
                pass

            # if len(col_name) == 1 and percent_calc == 'column_percent':
            # if len(col_name) == 1:
            #     cross_df = cross_df.drop('Total', axis=1)

            cross_df_subtotals_single_dict11 = {str(col_name): cross_df}
            cross_df_subtotals_single_dict.update(cross_df_subtotals_single_dict11)

    if percent_calc == 'row_percent':
        row_name1 = row_name[:-1]

        # print('row_name1 initial', row_name1)

        cross_df_subtotals_single_dict = {}
        for loop_col in range(len(row_name1)):

            # print("loop_col loop_col", loop_col)
            row_name = row_name1[0:loop_col + 1]
            # print("row_name row_name", row_name)

            row_list_vals = []
            df_row = df[row_name]
            if len(row_name) > 1:
                for loop_row in range(len(row_name)):
                    str_row = numpy.array(df_row.iloc[:, loop_row])
                    row_list_vals.append(str_row)

            col_list_vals = []
            df_col = df[col_name]
            if len(col_name) > 1:
                for loop_row2 in range(len(col_name)):
                    str_col = numpy.array(df_col.iloc[:, loop_row2])
                    col_list_vals.append(str_col)

            cross_df = crosstab_basic_table(df, percent_calc, row_name, col_name, parameter_calc, col_list_vals,
                                            row_list_vals,
                                            selected_weight_column)

            if len(row_name) == 1:
                # pass
                # print("cross df index",cross_df.index)
                try:
                    cross_df = cross_df.drop(['Grand Total'], axis='index')
                except:
                    pass
                # cross_df = cross_df.drop('Total', axis=1)

            cross_df_subtotals_single_dict11 = {str(row_name): cross_df}
            cross_df_subtotals_single_dict.update(cross_df_subtotals_single_dict11)

    # print("cross_df_subtotals_single_dict keyss", cross_df_subtotals_single_dict.keys())
    # exit("end the cross_df_subtotals_single_dict")
    return cross_df_subtotals_single_dict

def crosstab_basic_table(df,percent_calc,row_name,col_name,parameter_calc,col_list_vals,row_list_vals,
                         selected_weight_column):

    # print("crosstab_basic_table function started!!")

    if len(row_name) == 1 and len(col_name) == 1:

        # print(" FIRST CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH EQUAL TO 1!")
        row_name_str = ''.join([str(elem) for elem in row_name])
        col_name_str = ''.join([str(elem) for elem in col_name])

        cross_df = pd.crosstab(index=[df[row_name_str]], columns=[df[col_name_str]],
                               rownames=[row_name_str],
                               colnames=[col_name_str], values=df[selected_weight_column], aggfunc=sum,
                               normalize=parameter_calc, margins=True, margins_name='Grand Total')

        ## BOTH ROWS AND COLUMNS HAVE LENGTH GREATER THAN 1
    elif len(row_name) > 1 and len(col_name) > 1:

        # print(" SECOND CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH GREATER THAN 1!")
        cross_df = pd.crosstab(index=row_list_vals, columns=col_list_vals, rownames=row_name,
                               colnames=col_name,
                               values=df[selected_weight_column], aggfunc=sum,
                               normalize=parameter_calc)

        ## IF ROW = 1 AND COLUMNS GREATER THAN 1
    elif len(row_name) == 1 and len(col_name) > 1:
        # print("THIRD CONDTION SATISFIED :- IF ROW = 1 AND COLUMNS GREATER THAN 1!")
        row_name_str = ''.join([str(elem) for elem in row_name])

        if percent_calc == 'column_percent' or percent_calc == 'actual_count' or percent_calc == 'table_percent':
            cross_df = pd.crosstab(index=[df[row_name_str]], columns=col_list_vals, rownames=[row_name_str],
                                   colnames=col_name, values=df[selected_weight_column], aggfunc=sum,
                                   normalize=parameter_calc)

        elif percent_calc == 'row_percent':
            cross_df = pd.crosstab(index=[df[row_name_str]], columns=col_list_vals, rownames=[row_name_str],
                                   colnames=col_name, values=df[selected_weight_column], aggfunc=sum,
                                   normalize=parameter_calc, margins=True, margins_name='Grand Total')

        ## IF ROWS GREATER THAN 1 AND COLUMN = 1
    elif len(row_name) > 1 and len(col_name) == 1:
        # print("FOURTH CONDTION SATISFIED :- IF ROWS GREATER THAN 1 AND COLUMN = 1!")
        col_name_str = ''.join([str(elem) for elem in col_name])

        if percent_calc == 'column_percent':
            cross_df = pd.crosstab(index=row_list_vals, columns=[df[col_name_str]], rownames=row_name,
                                   colnames=[col_name_str], values=df[selected_weight_column], aggfunc=sum,
                                   normalize=parameter_calc, margins=True, margins_name='Grand Total')

        elif percent_calc == 'row_percent' or percent_calc == 'actual_count' or percent_calc == 'table_percent':
            cross_df = pd.crosstab(index=row_list_vals, columns=[df[col_name_str]], rownames=row_name,
                                   colnames=[col_name_str], values=df[selected_weight_column], aggfunc=sum,
                                   normalize=parameter_calc)

        # if percent_calc == 'actual_count':
        #     cross_df = cross_df / 100
    # cross_#df.to_excel("cross_df_11.xlsx")
    # print("ended at crosstab basic===",df['Country'].unique())
    # if df['Country'].unique() == ['000}China']:
    #     #df.to_excel("dfdf_inner_crosstab.xlsx")
        # exit("china exitt")
    # print("row_name",row_name)
    # print("col_name",col_name)

    # cross_df_11 = cross_df.copy()
    return cross_df

def totals_nested(df,row_name,col_name,row_list_vals,col_list_vals,percent_calc,parameter_calc,
                    selected_weight_column):
    if percent_calc == 'column_percent' or percent_calc == 'actual_count' or percent_calc == 'table_percent':
    # if percent_calc == 'column_percent':
        if len(row_name) == 1:
            # print("UNWEIGHTED rowname equal to 1 condition seperated COLUMNS")

            cross_df_list = []
            # for col_loop in col_name:
            col_loop = col_name[-1]
            # print(" FIRST CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH EQUAL TO 1!")
            row_name_str = ''.join([str(elem) for elem in row_name])
            col_name_str = ''.join([str(elem) for elem in col_loop])

            cross_df = pd.crosstab(index=[df[row_name_str]], columns=[df[col_name_str]],
                                   rownames=[row_name_str],
                                   colnames=[col_name_str], values=df[selected_weight_column], aggfunc=sum,
                                   normalize=parameter_calc, margins=True, margins_name='Grand Total')

            # if percent_calc == 'actual_count':
            #     cross_df = cross_df.drop('Total', axis=0)

            # cross_df_list.append(cross_df)

            # cross_df = pd.concat(cross_df_list, axis=1)
            # cross_#df.to_excel("Cross_df_nested_collll_rows.xlsx")

        elif len(row_name) > 1:
            # print("UNWEIGHTED colname greater than 1 condition seperated COLUMNS")
            # cross_df_list = []
            # for col_loop in col_name:
            col_loop = col_name[-1]
            col_name_str = ''.join([str(elem) for elem in col_loop])

            if percent_calc == 'column_percent' or percent_calc == 'actual_count' or percent_calc == 'table_percent':
                cross_df = pd.crosstab(index=row_list_vals, columns=[df[col_name_str]], rownames=row_name,
                                       colnames=[col_name_str], values=df[selected_weight_column], aggfunc=sum,
                                       normalize=parameter_calc, margins=True, margins_name='Grand Total')

            elif percent_calc == 'row_percent':
                cross_df = pd.crosstab(index=row_list_vals, columns=[df[col_name_str]], rownames=row_name,
                                       colnames=[col_name_str], values=df[selected_weight_column], aggfunc=sum,
                                       normalize=parameter_calc)

            # if percent_calc == 'actual_count':
            #     cross_df = cross_df.drop('Total', axis=0)

            # cross_df = cross_df.loc[:,~cross_df.columns.duplicated(keep='last')].copy()

            # cross_df_list.append(cross_df)

        # cross_df = pd.concat(cross_df_list, axis=1)
            # cross_#df.to_excel("Cross_df_nested_collll_rows.xlsx")

    elif percent_calc == 'row_percent':
        if len(col_name) == 1:
            # print("WEIGHTED rowname equal to 1 condition seperated ROWS")

            # cross_df_list = []
            # for row_loop in row_name:
            row_loop = row_name[-1]
            # print(" FIRST CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH EQUAL TO 1!")
            row_name_str = ''.join([str(elem) for elem in row_loop])
            col_name_str = ''.join([str(elem) for elem in col_name])

            cross_df = pd.crosstab(index=[df[row_name_str]], columns=[df[col_name_str]],
                                   rownames=[row_name_str],
                                   colnames=[col_name_str], values=df[selected_weight_column], aggfunc=sum,
                                   normalize=parameter_calc, margins=True, margins_name='Grand Total')
            #
            # if percent_calc == 'actual_count':
            #     cross_df = cross_df / 100

            # cross_df_list.append(cross_df)

            # cross_df = pd.concat(cross_df_list, axis=0)

        elif len(col_name) > 1:
            # print("WEIGHTED colname greater than 1 condition seperated ROWS")
            # cross_df_list = []
            # for row_loop in row_name:
            row_loop = row_name[-1]
            row_name_str = ''.join([str(elem) for elem in row_loop])

            if percent_calc == 'column_percent' or percent_calc == 'actual_count' or percent_calc == 'table_percent':
                cross_df = pd.crosstab(index=[df[row_name_str]], columns=col_list_vals, rownames=[row_name_str],
                                       colnames=col_name, values=df[selected_weight_column], aggfunc=sum,
                                       normalize=parameter_calc, margins=True, margins_name='Grand Total')

            elif percent_calc == 'row_percent':
                cross_df = pd.crosstab(index=[df[row_name_str]], columns=col_list_vals, rownames=[row_name_str],
                                       colnames=col_name, values=df[selected_weight_column], aggfunc=sum,
                                       normalize=parameter_calc, margins=True, margins_name='Grand Total')

            # if percent_calc == 'actual_count':
            #     cross_df = cross_df.drop('Total', axis=0)
            #     cross_df = cross_df / 100

            if percent_calc == 'column_percent':
                cross_df = cross_df.drop('Grand Total', axis=1)

            # cross_df_list.append(cross_df)

            # cross_df = pd.concat(cross_df_list, axis=0)

    cross_df_nested_totals = cross_df.copy()
    # cross_df_nested_totals.to_excel("cross_df_nested_totals.xlsx")
    # exit("endit it!")
    return cross_df_nested_totals


def crosstab_actual_counts(df,row_name,col_name,row_list_vals,col_list_vals,percent_calc,parameter_calc,
                    selected_weight_column,agg_func):
    # print('====selected_weight_column===1401',selected_weight_column)
    # print('====df shapee===',df.shape)
    # print('====row_name===',row_name)
    # print('====col_name===',col_name)

    if len(row_name) == 1 and len(col_name) == 1:

        # print(" FIRST CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH EQUAL TO 1!")
        row_name_str = ''.join([str(elem) for elem in row_name])
        col_name_str = ''.join([str(elem) for elem in col_name])

        # print('row_name_str===953',row_name_str)
        # print('col_name_str===954',col_name_str)
        # print('selected_weight_column===955',selected_weight_column)
        # print('df shape 956===',df.shape)


        # cross_df = pd.crosstab(index=[df[row_name_str]], columns=[df[col_name_str]],
        #                        rownames=[row_name_str],
        #                        colnames=[col_name_str],values=df[selected_weight_column], aggfunc=sum,
        #                        normalize=parameter_calc, margins=True, margins_name='Grand Total')

        cross_df = pd.crosstab(index=[df[row_name_str]], columns=[df[col_name_str]],
                               rownames=[row_name_str],
                               colnames=[col_name_str], values=df[selected_weight_column], aggfunc=agg_func,
                               normalize=parameter_calc, margins=True, margins_name='Grand Total')
                               # normalize=parameter_calc)

    ## BOTH ROWS AND COLUMNS HAVE LENGTH GREATER THAN 1
    if len(row_name) > 1 and len(col_name) > 1:

        # print(" SECOND CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH GREATER THAN 1!")
        # print('row_list_vals 1433--',len(row_list_vals[1]))
        # print('col_list_vals 1434--',len(col_list_vals[1]))
        # print('1435--',df[selected_weight_column].dtype)
        # cross_df = pd.crosstab(index=row_list_vals, columns=col_list_vals,rownames=row_name,colnames=col_name,
        #                        values=df[selected_weight_column], aggfunc=sum,
        #                        normalize=parameter_calc, margins=True, margins_name='Grand Total')
        cross_df = df.groupby(row_name + col_name)[selected_weight_column].sum().unstack(col_name)
        # cross_df.to_excel('initial_crsoff.xlsx')

        ## IF ROW = 1 AND COLUMNS GREATER THAN 1
    elif len(row_name) == 1 and len(col_name) > 1:
        # print("THIRD CONDTION SATISFIED :- IF ROW = 1 AND COLUMNS GREATER THAN 1!")
        row_name_str = ''.join([str(elem) for elem in row_name])

        # cross_df = pd.crosstab(index=[df[row_name_str]], columns=col_list_vals, rownames=[row_name_str],
        #                        colnames=col_name, values=df[selected_weight_column], aggfunc=sum,
        #                        normalize=parameter_calc,margins=True,margins_name='Grand Total')

        cross_df = pd.crosstab(index=[df[row_name_str]], columns=col_list_vals, rownames=[row_name_str],
                               colnames=col_name, values=df[selected_weight_column], aggfunc=agg_func,
                               normalize=parameter_calc, margins=True, margins_name='Grand Total')
                               # normalize=parameter_calc)

        ## IF ROWS GREATER THAN 1 AND COLUMN = 1
    elif len(row_name) > 1 and len(col_name) == 1:
        # print("FOURTH CONDTION SATISFIED :- IF ROWS GREATER THAN 1 AND COLUMN = 1!")
        col_name_str = ''.join([str(elem) for elem in col_name])

        # cross_df = pd.crosstab(index=row_list_vals, columns=[df[col_name_str]], rownames=row_name,
        #                        colnames=[col_name_str], values=df[selected_weight_column], aggfunc=sum,
        #                        normalize=parameter_calc,margins=True,margins_name='Grand Total')

        cross_df = pd.crosstab(index=row_list_vals, columns=[df[col_name_str]], rownames=row_name,
                               colnames=[col_name_str], values=df[selected_weight_column], aggfunc=agg_func,
                               normalize=parameter_calc, margins=True, margins_name='Grand Total')
                               # normalize=parameter_calc)

    # cross_df = cross_df.mul(100)
    # if percent_calc == ('actual_count' or 'table_percent') and ((len(row_name) == 1 and len(col_name) > 1) or (len(row_name) > 1 and len(col_name) > 1)):
    #     cross_df = cross_df.drop('Grand Total',axis=1)
    # cross_df.to_excel("cross_df_11.xlsx")
    # exit("end at 723")
    cross_df_22 = cross_df.copy()
    return cross_df_22

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
