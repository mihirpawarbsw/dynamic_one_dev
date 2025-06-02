
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

def single_dimension_logic(df,row_name,col_name,seperated_flag_row,selected_weight_column_all,agg_func):
    if (len(row_name) >= 1) and len(col_name) == 0:

        if seperated_flag_row == 0:
            cross_df = pd.DataFrame(df.groupby(row_name)[selected_weight_column_all].sum())
            row_name_str = ''.join([str(elem) for elem in row_name])

            if (len(row_name) == 1):
                cross_df = pd.concat([cross_df], keys=[row_name_str], axis=0)

            if (len(row_name) > 1):
                row_name_outer = row_name[-1]
                cross_df_outer = pd.DataFrame(df.groupby(row_name_outer)[selected_weight_column_all].sum())
                cross_df_outer = pd.concat([cross_df_outer], keys=['Grand Total'], axis=0)
                cross_df = pd.concat([cross_df, cross_df_outer])

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

    df_single = convert_to_single_level(cross_df)

    cross_df_dataframes_lst2 = []
    level_0_index = df_single.index.get_level_values(0).unique().tolist()

    cross_df_index_grp = df_single.groupby(axis=0, level=0)

    for cross_df_index_loop in level_0_index:
        cross_df_index = cross_df_index_grp.get_group(cross_df_index_loop)
        cross_df_index_df = pd.DataFrame(cross_df_index)

        cross_df_index_df.columns = cross_df_index_df.columns.str.replace(r'\s*Sales$', '', regex=True)
        filtered_df = cross_df_index_df[cross_df_index_df.index.get_level_values(1) == 'Grand Total']
        cross_df_index_df = derived_measures_after_crosstab(cross_df_index_df, filtered_df,base_sales_index_colname,row_name,col_name,measure_row_column_position,cagr_power_val,brand_sales_index_value_flag)
        cross_df_dataframes_lst2.append(cross_df_index_df)
    cross_df_temp = pd.concat(cross_df_dataframes_lst2, axis=0)
    cross_df = revert_to_multiindex(cross_df_temp)

    ############################ new code - 10-05-2025 ###############################
    new_cols = []
    for col in cross_df.columns:
        *upper, last = col
        if last in mapping_dict:
            new_col = tuple(upper + [mapping_dict[last]])
        else:
            new_col = col
        new_cols.append(new_col)

    cross_df.columns = pd.MultiIndex.from_tuples(new_cols)
    return cross_df

def subtotals_multi_actuals_new(cross_df, row_name,agg_func):

    if len(row_name) == 2:
        df_level1 = cross_df.groupby(level=0).agg(agg_func)
        df_level1.index = df_level1.index = pd.MultiIndex.from_arrays([df_level1.index.values,
                                                                       len(df_level1.index) * ['Grand Total']])

        cross_df = pd.concat([cross_df, df_level1]).sort_index(level=[0])

    elif len(row_name) == 3:

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

def nested_crosstab(df,row_name,col_name,row_list_vals,col_list_vals,percent_calc,parameter_calc,
                    selected_weight_column,totals_nested_flag,agg_func,measure_row_column_position):

    cross_df = crosstab_actual_counts(df,row_name,col_name,row_list_vals,col_list_vals,percent_calc,parameter_calc,
                selected_weight_column,agg_func)

    ######## ADDED BY MIHIR PAWAR - 17-05-2023 ######################################################################
    if len(col_name) == 1 and len(row_name) == 1:
        row_name_str = ''.join([str(elem) for elem in row_name])
        col_name_str = ''.join([str(elem) for elem in col_name])

        cross_df = pd.concat([cross_df], keys=[row_name_str], axis=0)
        cross_df = pd.concat([cross_df], keys=[col_name_str], axis=1)

    ######## ADDED BY MIHIR PAWAR - 17-05-2023 ######################################################################

    ############### TEMP CODE NESTED SUPER GRAND TOTALS - 10-05-2024 ##
    weight_param = 'unweighted'

    if len(row_name) > 1 and len(col_name) > 1: 

        cross_df = multi_subtotals_ACTUALS_TABLE(cross_df, row_name)
        cross_df = cross_df.T
        cross_df = multi_subtotals_ACTUALS_TABLE(cross_df, col_name)
        cross_df = cross_df.T
    ############### TEMP CODE NESTED SUPER GRAND TOTALS - 10-05-2024 ##

    ######################### TRAIL CODE - SUPER NESTD GRAND TOTALS ####################
    ######################### TRAIL CODE - SUPER NESTD GRAND TOTALS ####################
        cross_df_cols_nested = table_or_actual_totals_nested_COLS(df,row_name,col_name,row_list_vals,col_list_vals,percent_calc,parameter_calc,
            selected_weight_column,weight_param)

        cross_df_cols_nested = cross_df_cols_nested.loc[:, ~cross_df_cols_nested.columns.duplicated(keep='first')].copy()

        for loop_nested_totals in range(len(col_name)-2):
            cross_df_cols_nested = pd.concat([cross_df_cols_nested], keys=[''], axis=1)
        cross_df_cols_nested = pd.concat([cross_df_cols_nested], keys=['Grand Total'], axis=1)

        try:
            cross_df_cols_nested.drop(('Grand Total', ''), axis=0, inplace=True)
        except:
            pass

        cross_df_cols_nested = multi_subtotals_ACTUALS_TABLE(cross_df_cols_nested, col_name)
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
    # ############################ ADDED BY MIHIR PAWAR ON 17-05-2023 ##############################################
    if len(col_name) > 1 and len(row_name) == 1:
        row_name_str = ''.join([str(elem) for elem in row_name])

        cross_df = pd.concat([cross_df], keys=[row_name_str], axis=0)
    # ############################ ADDED BY MIHIR PAWAR ON 17-05-2023 ##############################################
    if (len(col_name) == 1 and len(row_name) > 1):
        col_name_str = ''.join([str(elem) for elem in col_name])
        cross_df = pd.concat([cross_df], keys=[col_name_str], axis=1)  ####### 31-03-2023

    return cross_df

def multi_subtotals_ACTUALS_TABLE(cross_df, row_name):
    if len(row_name) == 2:
        df1 = cross_df.groupby(level=0).sum()

        # ############### COMMENTED BY MIHIR PAWAR 21-04-2023
        df1.index = pd.MultiIndex.from_arrays([df1.index.values, len(df1.index) * ['Grand Total']])
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

        row_loop = row_name[-1]
        row_name_str = ''.join([str(elem) for elem in row_loop])
        col_name_str = ''.join([str(elem) for elem in col_name])

        cross_df = pd.crosstab(index=[df[row_name_str]], columns=[df[col_name_str]],
                               rownames=[row_name_str],
                               colnames=[col_name_str], values=df[selected_weight_column], aggfunc=sum,
                               normalize=parameter_calc,margins=True,margins_name='Grand Total')

    elif len(col_name) > 1:
        row_loop = row_name[-1]
        row_name_str = ''.join([str(elem) for elem in row_loop])

        if percent_calc == 'column_percent' or percent_calc == 'actual_count' or percent_calc == 'table_percent':
            cross_df = pd.crosstab(index=[df[row_name_str]], columns=col_list_vals, rownames=[row_name_str],
                                   colnames=col_name, values=df[selected_weight_column], aggfunc=sum,
                                   normalize=parameter_calc,margins=True,margins_name='Grand Total')

    cross_df_rows_nested = cross_df.copy()

    return cross_df_rows_nested

def table_or_actual_totals_nested_COLS(df, row_name, col_name, row_list_vals, col_list_vals, percent_calc,
                                       parameter_calc,
                                       selected_weight_column, weight_param):
    if len(row_name) == 1:
        cross_df_list = []
        col_loop = col_name[-1]
        row_name_str = ''.join([str(elem) for elem in row_name])
        col_name_str = ''.join([str(elem) for elem in col_loop])

        cross_df = pd.crosstab(index=[df[row_name_str]], columns=[df[col_name_str]],
                               rownames=[row_name_str],
                               colnames=[col_name_str], values=df[selected_weight_column], aggfunc=sum,
                               normalize=parameter_calc,margins=True,margins_name='Grand Total')

    elif len(row_name) > 1:
        col_loop = col_name[-1]
        col_name_str = ''.join([str(elem) for elem in col_loop])

        if percent_calc == 'column_percent' or percent_calc == 'actual_count' or percent_calc == 'table_percent':
            cross_df = pd.crosstab(index=row_list_vals, columns=[df[col_name_str]], rownames=row_name,
                                   colnames=[col_name_str], values=df[selected_weight_column], aggfunc=sum,
                                   normalize=parameter_calc,margins=True,margins_name='Grand Total')

    cross_df_cols_nested = cross_df.copy()

    return cross_df_cols_nested

def crosstab_basic_table(df,percent_calc,row_name,col_name,parameter_calc,col_list_vals,row_list_vals,
                         selected_weight_column):

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

    return cross_df

def crosstab_actual_counts(df,row_name,col_name,row_list_vals,col_list_vals,percent_calc,parameter_calc,
                    selected_weight_column,agg_func):
    if len(row_name) == 1 and len(col_name) == 1:

        # print(" FIRST CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH EQUAL TO 1!")
        row_name_str = ''.join([str(elem) for elem in row_name])
        col_name_str = ''.join([str(elem) for elem in col_name])

        cross_df = pd.crosstab(index=[df[row_name_str]], columns=[df[col_name_str]],
                               rownames=[row_name_str],
                               colnames=[col_name_str], values=df[selected_weight_column], aggfunc=agg_func,
                               normalize=parameter_calc, margins=True, margins_name='Grand Total')

    ## BOTH ROWS AND COLUMNS HAVE LENGTH GREATER THAN 1
    if len(row_name) > 1 and len(col_name) > 1:

        cross_df = df.groupby(row_name + col_name)[selected_weight_column].sum().unstack(col_name)

    ## IF ROW = 1 AND COLUMNS GREATER THAN 1
    elif len(row_name) == 1 and len(col_name) > 1:
        # print("THIRD CONDTION SATISFIED :- IF ROW = 1 AND COLUMNS GREATER THAN 1!")
        row_name_str = ''.join([str(elem) for elem in row_name])

        cross_df = pd.crosstab(index=[df[row_name_str]], columns=col_list_vals, rownames=[row_name_str],
                               colnames=col_name, values=df[selected_weight_column], aggfunc=agg_func,
                               normalize=parameter_calc, margins=True, margins_name='Grand Total')

    ## IF ROWS GREATER THAN 1 AND COLUMN = 1
    elif len(row_name) > 1 and len(col_name) == 1:
        # print("FOURTH CONDTION SATISFIED :- IF ROWS GREATER THAN 1 AND COLUMN = 1!")
        col_name_str = ''.join([str(elem) for elem in col_name])
        cross_df = pd.crosstab(index=row_list_vals, columns=[df[col_name_str]], rownames=row_name,
                               colnames=[col_name_str], values=df[selected_weight_column], aggfunc=agg_func,
                               normalize=parameter_calc, margins=True, margins_name='Grand Total')

    cross_df_22 = cross_df.copy()
    return cross_df_22

