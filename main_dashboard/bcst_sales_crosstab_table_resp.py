import math
import re
import numpy
import pandas as pd
import numpy as np
import os,json
import time
import statistics as st
import copy
from itertools import combinations
from main_dashboard.bcst_sales_crosstab_calculation_functions import *
from main_dashboard.bcst_sales_crosstab_calculation_seperated_functions import *
import warnings
warnings.filterwarnings('ignore')

####################################### added on 18-02-2025 ###################################################
def sales_crosstab_logic_MAIN(selected_weight_column_all, dict_table, df, percent_calc, row_name, col_name,
                              data_type_resp, separated_flag_row, separated_flag_col, totals_nested_flag,
                              agg_func, measure_row_column_position):
    crosstab_list_final = []
 
    for selected_weight_column in selected_weight_column_all:
        # Generate crosstab for the current weight column
        cross_df_temp = crosstab_main(
            df, dict_table, selected_weight_column, row_name, col_name,
            data_type_resp, percent_calc, separated_flag_row, separated_flag_col,
            totals_nested_flag, agg_func, measure_row_column_position
        )
 
        # Drop 'Grand Total' column if it exists
        if ('Grand Total', '') in cross_df_temp.columns:
            cross_df_temp.drop(('Grand Total', ''), axis=1, inplace=True)

        # if (slice(None, None, None), 'Grand Total') in cross_df_temp.index:
        #     try:
        #         cross_df_temp.drop((slice(None, None, None), 'Grand Total'), axis=0, inplace=True)
        #     except:
        #         pass
 
        # Process row subtotals if required
        if not (separated_flag_row == 1 and separated_flag_col == 1):
            if len(row_name) == 1:
                # Add a 'Grand Total' row for single-level row grouping
                df_level1 = cross_df_temp.groupby(level=0).agg(agg_func)
                df_level1.index = pd.MultiIndex.from_arrays([
                    df_level1.index.values,
                    ['Grand Total'] * len(df_level1.index)
                ])
                cross_df_temp = pd.concat([cross_df_temp, df_level1])
            elif len(row_name) > 1:
                # Add multi-level subtotals
                cross_df_temp = subtotals_multi_actuals_new(cross_df_temp, row_name, agg_func)
 
        # Add the current crosstab to the final list, keyed by weight column
        crosstab_list_final.append(pd.concat([cross_df_temp], keys=[selected_weight_column], axis=1))
 
    # Concatenate all crosstabs into a single dataframe
    cross_df = pd.concat(crosstab_list_final, axis=1)
 
    return cross_df

def crosstab_main(df, dict_table, selected_weight_column, row_name, col_name,
                                     data_type_resp,
                                     percent_calc, seperated_flag_row, seperated_flag_col,
                                     totals_nested_flag,agg_func,measure_row_column_position):

    parameter_calc = create_parameter_calc(percent_calc)

    row_list_vals, col_list_vals = row_col_vals(df, row_name, col_name)
    cross_df = data_type_resp_fn(df, row_name, col_name, row_list_vals, col_list_vals, percent_calc, parameter_calc,
                                 selected_weight_column, seperated_flag_row, seperated_flag_col, totals_nested_flag,agg_func,measure_row_column_position)

    cross_df.fillna(0, axis=1, inplace=True)

    return cross_df

def create_parameter_calc(percent_calc):
    if percent_calc == 'column_percent':
        parameter_calc='columns'
    elif percent_calc == 'row_percent':
        parameter_calc = 'index'
    elif percent_calc == 'actual_count':
        parameter_calc = False
    elif percent_calc == 'table_percent':
        parameter_calc = 'all'

    return parameter_calc

def row_col_vals(df, row_name, col_name):
 
    if len(row_name) > 1:
        row_list_vals = [df[name].to_numpy() for name in row_name]
    else:
        row_list_vals = [df[row_name[0]].to_numpy()] if row_name else []
 
    # Extract column values
    if len(col_name) > 1:
        col_list_vals = [df[name].to_numpy() for name in col_name]
    else:
        col_list_vals = [df[col_name[0]].to_numpy()] if col_name else []
 
    return row_list_vals, col_list_vals

def data_type_resp_fn(df, row_name, col_name,row_list_vals,col_list_vals,percent_calc,parameter_calc,
                      selected_weight_column,seperated_flag_row, seperated_flag_col, totals_nested_flag,agg_func,measure_row_column_position):
    ################# CROSSTAB BOTH NESTED ##################################################

    if seperated_flag_row == 0 and seperated_flag_col == 0:

        return nested_crosstab(df, row_name, col_name, row_list_vals, col_list_vals, percent_calc,
                                   parameter_calc, selected_weight_column, totals_nested_flag,agg_func,measure_row_column_position)

    ################# CROSSTAB BOTH NESTED ##################################################

    ################# CROSSTAB STACKED ROWS ##################################################
    elif seperated_flag_row == 1 and seperated_flag_col == 0:
        return seperated_rows(df, row_name, col_name, row_list_vals, col_list_vals, percent_calc,
                                  parameter_calc, selected_weight_column,agg_func)

    ################# CROSSTAB STACKED ROWS ##################################################

    ################# CROSSTAB STACKED COLUMNS ##################################################
    elif seperated_flag_col == 1 and seperated_flag_row == 0:
        return seperated_cols(df, row_name, col_name, row_list_vals, col_list_vals, percent_calc,
                                  parameter_calc, selected_weight_column,agg_func)

    ################# CROSSTAB STACKED COLUMNS ##################################################

    ################# CROSSTAB BOTH STACKED ##################################################
    elif seperated_flag_col == 1 and seperated_flag_row == 1:
        return stacked_crosstab(df, row_name, col_name, percent_calc,
                                    parameter_calc, selected_weight_column,agg_func)

    else:
        raise ValueError("Invalid combination of seperated_flag_row and seperated_flag_col.")
################# CROSSTAB BOTH STACKED ##################################################

    return cross_df
