
import numpy
import pandas as pd
import numpy as np
import os,json
import time
import statistics as st
import copy
from main_dashboard.bcst_sales_crosstab_calculation_functions import *
from main_dashboard.response_functions import *
from collections import Counter

totals_nested_flag = 1

def seperated_rows(df,row_name,col_name,row_list_vals,col_list_vals,percent_calc,
                                     parameter_calc,selected_weight_column,agg_func):

    if len(col_name) == 1:
        # print("WEIGHTED rowname equal to 1 condition seperated ROWS")

        cross_df_list = []
        for row_loop in row_name:
            # print(" FIRST CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH EQUAL TO 1!")
            row_name_str = ''.join([str(elem) for elem in row_loop])
            col_name_str = ''.join([str(elem) for elem in col_name])

            cross_df = pd.crosstab(index=[df[row_name_str]], columns=[df[col_name_str]],
                                   rownames=[row_name_str],
                                   colnames=[col_name_str], values=df[selected_weight_column], aggfunc=agg_func,
                                   normalize=parameter_calc, margins=True, margins_name='Grand Total')

            cross_df = pd.concat([cross_df], keys=[row_name_str], axis=0)  ####### 31-03-2023
            cross_df = pd.concat([cross_df], keys=[col_name_str], axis=1)  ####### 31-03-2023

            cross_df_list.append(cross_df)

        cross_df = pd.concat(cross_df_list, axis=0)

    elif len(col_name) > 1:
        # print("WEIGHTED colname greater than 1 condition seperated ROWS")
        cross_df_list = []
        for row_loop in row_name:
            row_name_str = ''.join([str(elem) for elem in row_loop])

            cross_df = pd.crosstab(index=[df[row_name_str]], columns=col_list_vals, rownames=[row_name_str],
                                   colnames=col_name, values=df[selected_weight_column], aggfunc=agg_func,
                                   # normalize=parameter_calc, margins=True, margins_name='Grand Total')
                                   normalize=parameter_calc, margins=True, margins_name='Grand Total')

            # #################### SUBTOTALS #####################################################################
            cross_df = pd.concat([cross_df], keys=[row_name_str], axis=0)  ####### 31-03-2023

            cross_df_list.append(cross_df)

        cross_df = pd.concat(cross_df_list, axis=0)

        weight_param = 'unweighted'
        cross_df_nested_total = totals_nested_seperated_cols(df,row_name,col_name,row_list_vals,col_list_vals,percent_calc,parameter_calc,
                selected_weight_column,weight_param)

        cross_df = pd.concat([cross_df,cross_df_nested_total], axis=1)

    return cross_df

def subtotals_calc_seperated_rows(cross_df,percent_calc,row_name,col_name,cross_df_subtotals_single_dict):

    cross_df = cross_df.T
    cross_df = multi_subtotals_seperated_rows(cross_df, col_name,cross_df_subtotals_single_dict,percent_calc)
    cross_df = cross_df.T

    return cross_df

def multi_subtotals_seperated_cols(cross_df,row_name,cross_df_subtotals_single_dict,percent_calc):

    if len(row_name)==2:

        df1 = list(cross_df_subtotals_single_dict.values())[0]
        df1.index=pd.MultiIndex.from_arrays([df1.index.values , len(df1.index) * ['Grand Total']])
        cross_df = pd.concat([cross_df, df1]).sort_index(level=0)

    if len(row_name)==3:

        df1 = list(cross_df_subtotals_single_dict.values())[1]
        df1.index = pd.MultiIndex.from_arrays([df1.index.get_level_values(0),
                                               df1.index.get_level_values(1),
                                               len(df1.index) * ['Grand Total']])

        df2 = list(cross_df_subtotals_single_dict.values())[0]
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
        # if percent_calc == 'column_percent':
        #     df1 = df1.T
        df1.index = pd.MultiIndex.from_arrays([df1.index.get_level_values(0),
                                               df1.index.get_level_values(1),
                                               df1.index.get_level_values(2),
                                               len(df1.index) * ['Grand Total']])

        # print("multi_subtotals three rows")

        df2 = list(cross_df_subtotals_single_dict.values())[1]
        df2.index = pd.MultiIndex.from_arrays([df2.index.get_level_values(0),
                                               df2.index.get_level_values(1),
                                               len(df2.index) * ['Grand Total'],
                                               len(df2.index) * ['']])

        df3 = list(cross_df_subtotals_single_dict.values())[0]
        df3.index = pd.MultiIndex.from_arrays([df3.index.values,
                                               len(df3.index) * ['Grand Total'],
                                               len(df3.index) * [''],
                                               len(df3.index) * ['']])

        # concat all dataframes together, sort index
        cross_df = pd.concat([cross_df, df1, df2, df3]).sort_index(level=[0, 1, 2])

    if len(row_name) == 5:
        df1 = list(cross_df_subtotals_single_dict.values())[3]
        df1.index = pd.MultiIndex.from_arrays([df1.index.get_level_values(0),
                                               df1.index.get_level_values(1),
                                               df1.index.get_level_values(2),
                                               df1.index.get_level_values(3),
                                               len(df1.index) * ['Grand Total']])


        # df2 = cross_df.groupby(level=[0, 1, 2]).sum()
        df2 = list(cross_df_subtotals_single_dict.values())[2]
        df2.index = pd.MultiIndex.from_arrays([df2.index.get_level_values(0),
                                               df2.index.get_level_values(1),
                                               df2.index.get_level_values(2),
                                               len(df2.index) * ['Grand Total'],
                                               len(df2.index) * ['']])

        # df3 = cross_df.groupby(level=[0, 1]).sum()

        df3 = list(cross_df_subtotals_single_dict.values())[1]
        df3.index = pd.MultiIndex.from_arrays([df3.index.get_level_values(0),
                                               df3.index.get_level_values(1),
                                               len(df3.index) * ['Grand Total'],
                                               len(df3.index) * [''],
                                               len(df3.index) * ['']])

        # df4 = cross_df.groupby(level=0).sum()

        df4 = list(cross_df_subtotals_single_dict.values())[0]
        df4.index = pd.MultiIndex.from_arrays([df4.index.values,
                                               len(df4.index) * ['Grand Total'],
                                               len(df4.index) * [''],
                                               len(df4.index) * [''],
                                               len(df4.index) * ['']])

        # concat all dataframes together, sort index
        cross_df = pd.concat([cross_df, df1, df2, df3, df4]).sort_index(level=[0, 1, 2, 3])

    return cross_df

def multi_subtotals_seperated_rows(cross_df,row_name,cross_df_subtotals_single_dict,percent_calc):

    if len(row_name)==2:
        df1 = list(cross_df_subtotals_single_dict.values())[0]
        df1=df1.T

        df1.index=pd.MultiIndex.from_arrays([df1.index.values , len(df1.index) * ['Grand Total']])

        cross_df = pd.concat([cross_df, df1]).sort_index(level=0)

    if len(row_name)==3:
        # print("multi_subtotals three rows")

        df1 = list(cross_df_subtotals_single_dict.values())[1]
        if percent_calc == 'column_percent':
            df1 = df1.T

        df1.index = pd.MultiIndex.from_arrays([df1.index.get_level_values(0),
                                               df1.index.get_level_values(1),
                                               len(df1.index) * ['Grand Total']])

        # df2 = cross_df.groupby(level=0).sum()
        df2 = list(cross_df_subtotals_single_dict.values())[0]
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
        df1.index = pd.MultiIndex.from_arrays([df1.index.get_level_values(0),
                                               df1.index.get_level_values(1),
                                               df1.index.get_level_values(2),
                                               len(df1.index) * ['Grand Total']])

        # print("multi_subtotals three rows")

        df2 = list(cross_df_subtotals_single_dict.values())[1]
        # df2 = cross_df.groupby(level=[0, 1]).sum()
        df2.index = pd.MultiIndex.from_arrays([df2.index.get_level_values(0),
                                               df2.index.get_level_values(1),
                                               len(df2.index) * ['Grand Total'],
                                               len(df2.index) * ['']])

        # df3 = cross_df.groupby(level=0).sum()

        df3 = list(cross_df_subtotals_single_dict.values())[0]
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
        df1.index = pd.MultiIndex.from_arrays([df1.index.get_level_values(0),
                                               df1.index.get_level_values(1),
                                               df1.index.get_level_values(2),
                                               df1.index.get_level_values(3),
                                               len(df1.index) * ['Grand Total']])


        # df2 = cross_df.groupby(level=[0, 1, 2]).sum()
        df2 = list(cross_df_subtotals_single_dict.values())[2]
        df2.index = pd.MultiIndex.from_arrays([df2.index.get_level_values(0),
                                               df2.index.get_level_values(1),
                                               df2.index.get_level_values(2),
                                               len(df2.index) * ['Grand Total'],
                                               len(df2.index) * ['']])

        # df3 = cross_df.groupby(level=[0, 1]).sum()

        df3 = list(cross_df_subtotals_single_dict.values())[1]
        df3.index = pd.MultiIndex.from_arrays([df3.index.get_level_values(0),
                                               df3.index.get_level_values(1),
                                               len(df3.index) * ['Grand Total'],
                                               len(df3.index) * [''],
                                               len(df3.index) * ['']])

        # df4 = cross_df.groupby(level=0).sum()

        df4 = list(cross_df_subtotals_single_dict.values())[0]
        df4.index = pd.MultiIndex.from_arrays([df4.index.values,
                                               len(df4.index) * ['Grand Total'],
                                               len(df4.index) * [''],
                                               len(df4.index) * [''],
                                               len(df4.index) * ['']])

        # concat all dataframes together, sort index
        cross_df = pd.concat([cross_df, df1, df2, df3, df4]).sort_index(level=[0, 1, 2, 3])

    return cross_df

################################### ADDED ON 18-02-2025 ##################################################
def seperated_cols(df, row_name, col_name, row_list_vals, col_list_vals, percent_calc,
                   parameter_calc, selected_weight_column, agg_func):
    """
    Create a cross-tabulation table with separated columns based on the specified parameters.
    """
 
    def create_crosstab(index, columns, rownames, colnames, values, agg_func, normalize, margins, margins_name):
        """
        A helper function to create a crosstab with consistent arguments.
        """
        return pd.crosstab(
            index=index,
            columns=columns,
            rownames=rownames,
            colnames=colnames,
            values=values,
            aggfunc=agg_func,
            normalize=normalize,
            margins=margins,
            margins_name=margins_name,
        )
 
    # If there's a single row_name, handle separated columns differently
    cross_df_list = []
    if len(row_name) == 1:
        row_name_str = ''.join(map(str, row_name))
        for col_loop in col_name:
            col_name_str = ''.join(map(str, col_loop))
           
            cross_df = create_crosstab(
                index=[df[row_name_str]],
                columns=[df[col_name_str]],
                rownames=[row_name_str],
                colnames=[col_name_str],
                values=df[selected_weight_column],
                agg_func=agg_func,
                normalize=parameter_calc,
                margins=True,
                margins_name='Grand Total',
            )
           
            cross_df = pd.concat([cross_df], keys=[row_name_str], axis=0)
            cross_df = pd.concat([cross_df], keys=[col_name_str], axis=1)
            cross_df_list.append(cross_df)
       
        cross_df = pd.concat(cross_df_list, axis=1)
 
    elif len(row_name) > 1:
        for col_loop in col_name:
            col_name_str = ''.join(map(str, col_loop))
 
            cross_df = create_crosstab(
                index=row_list_vals,
                columns=[df[col_name_str]],
                rownames=row_name,
                colnames=[col_name_str],
                values=df[selected_weight_column],
                agg_func=agg_func,
                normalize=parameter_calc,
                margins=True,
                margins_name='Grand Total',
            )
           
            cross_df = pd.concat([cross_df], keys=[col_name_str], axis=1)
            cross_df_list.append(cross_df)
 
        cross_df = pd.concat(cross_df_list, axis=1)
 
        # Add totals
        cross_df_nested_total = totals_nested_seperated_rows(
            df, row_name, col_name, row_list_vals, col_list_vals, percent_calc, parameter_calc,
            selected_weight_column, weight_param='unweighted'
        )
        cross_df = pd.concat([cross_df, cross_df_nested_total], axis=0)
 
    return cross_df

def stacked_crosstab(df, row_names, col_names, percent_calc,
                     normalize_param, weight_column, agg_func):
 
    cross_df_list = []
 
    for row in row_names:
        row_str = ''.join(map(str, row))
        row_level_dfs = []
 
        for col in col_names:
            col_str = ''.join(map(str, col))
 
            # Generate cross-tab for current row and column
            cross_tab = pd.crosstab(
                index=[df[row_str]],
                columns=[df[col_str]],
                rownames=[row_str],
                colnames=[col_str],
                values=df[weight_column],
                aggfunc=agg_func,
                normalize=normalize_param,
                margins=True,
                margins_name='Grand Total'
            )
 
            # Add hierarchical levels for rows and columns
            cross_tab = pd.concat([cross_tab], keys=[row_str], axis=0)
            cross_tab = pd.concat([cross_tab], keys=[col_str], axis=1)
 
            row_level_dfs.append(cross_tab)
 
        # Combine all column-level data for the current row
        combined_row_df = pd.concat(row_level_dfs, axis=1)
        cross_df_list.append(combined_row_df)
 
    # Combine all row-level data
    final_cross_df = pd.concat(cross_df_list, axis=0)
 
    return final_cross_df

def totals_nested_seperated_cols(df,row_name,col_name,row_list_vals,col_list_vals,percent_calc,parameter_calc,
                    selected_weight_column,weight_param):

    cross_df_totals_nested_list = []
    for row_loop in row_name:
        row_name_str = ''.join([str(elem) for elem in row_loop])

        col_loop = col_name[-1]
        # print(" FIRST CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH EQUAL TO 1!")
        col_name_str = ''.join([str(elem) for elem in col_loop])

        cross_df = pd.crosstab(index=[df[row_name_str]], columns=[df[col_name_str]],
                               rownames=[row_name_str],
                               colnames=[col_name_str], values=df[selected_weight_column], aggfunc=sum,
                               normalize=parameter_calc, margins=True, margins_name='Grand Total')

        cross_df_nested_total = pd.concat([cross_df], keys=[row_name_str], axis=0)

        cross_df_nested_total = cross_df_nested_total.loc[:,
                                ~cross_df_nested_total.columns.duplicated(keep='last')].copy()

        for loop_nested_totals in range(len(col_name) - 2):
            cross_df_nested_total = pd.concat([cross_df_nested_total], keys=[''], axis=1)
        cross_df_nested_total = pd.concat([cross_df_nested_total], keys=['Grand Total'], axis=1)
        cross_df_totals_nested_list.append(cross_df_nested_total)

    cross_df_nested_total = pd.concat(cross_df_totals_nested_list, axis=0)

    return cross_df_nested_total

def totals_nested_seperated_rows(df,row_name,col_name,row_list_vals,col_list_vals,percent_calc,parameter_calc,
                    selected_weight_column,weight_param):

    cross_df_totals_nested_list = []
    for col_loop in col_name:
        col_name_str = ''.join([str(elem) for elem in col_loop])

        row_loop = row_name[-1]
        # print(" FIRST CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH EQUAL TO 1!")
        # row_name_str = ''.join([str(elem) for elem in row_name])
        row_name_str = ''.join([str(elem) for elem in row_loop])

        cross_df = pd.crosstab(index=[df[row_name_str]], columns=[df[col_name_str]],
                               rownames=[row_name_str],
                               colnames=[col_name_str], values=df[selected_weight_column], aggfunc=sum,
                               normalize=parameter_calc, margins=True, margins_name='Grand Total')

        cross_df_nested_total = pd.concat([cross_df], keys=[col_name_str], axis=1)
        for loop_nested_totals in range(len(row_name) - 2):
            cross_df_nested_total = pd.concat([cross_df_nested_total], keys=[''], axis=0)
        #
        cross_df_nested_total = pd.concat([cross_df_nested_total], keys=['Grand Total'], axis=0)

        cross_df_totals_nested_list.append(cross_df_nested_total)

    cross_df_nested_total = pd.concat(cross_df_totals_nested_list, axis=1)


    return cross_df_nested_total