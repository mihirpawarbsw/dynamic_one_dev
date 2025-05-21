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

# from django.conf import settings
# from main_dashboard.crosstab_calculation_functions import *
# from main_dashboard.crosstab_calculation_seperated_functions import *

from main_dashboard.bcst_sales_crosstab_calculation_functions import *
from main_dashboard.bcst_sales_crosstab_calculation_seperated_functions import *

import warnings
warnings.filterwarnings('ignore')

# PYTHONPATH = r"C:\Mihir_Python_Projects\BCST_Tool_Core_Python_Logic\ccv_tool_Sales\BCST_Sales_Data\\"
# PYTHONPATH = r"C:\Users\MihirPawar\Desktop\Python Project BSW\Python Files1\ccv_tool\ccv_survey_data\\"
# MERGED_PYTHONPATH = merged_pythonpath = r"C:\Mihir_Python_Projects\BCST_Tool_Core_Python_Logic\ccv_tool_Sales\merged_data_files\\"

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

        if (slice(None, None, None), 'Grand Total') in cross_df_temp.index:
            try:
                cross_df_temp.drop((slice(None, None, None), 'Grand Total'), axis=0, inplace=True)
            except:
                pass
 
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
####################################### added on 18-02-2025 ###################################################

def sales_crosstab_logic_MAIN_OLD_18022025(selected_weight_column_all,dict_table, df, percent_calc, row_name, col_name,
                                             data_type_resp,
                                             seperated_flag_row, seperated_flag_col, totals_nested_flag,agg_func,measure_row_column_position):
    crosstab_lst_final = []


    for selected_weight_column in selected_weight_column_all:
        print('df 35 shapee==',df.shape)
        df_copy22 = df.copy()
        cross_df_temp = crosstab_main(df_copy22, dict_table, selected_weight_column, row_name,
                                 col_name,
                                 data_type_resp,
                                 percent_calc, seperated_flag_row, seperated_flag_col,
                                 totals_nested_flag, agg_func,measure_row_column_position)
        

        try:
            cross_df_temp.drop(('Grand Total',''), axis=1, inplace=True)
        except:
            pass
        # cross_df_temp.to_excel('cross_df_temp.xlsx')

        if seperated_flag_row == 1 and seperated_flag_col == 1:
            pass

        else:
            if len(row_name) == 1:
                pass

                df_level1 = cross_df_temp.groupby(level=0).agg(agg_func)
                df_level1.index = df_level1.index = pd.MultiIndex.from_arrays([df_level1.index.values,
                                                                               len(df_level1.index) * ['Grand Total']])

                #Concatenate the totals row to the original DataFrame
                cross_df_temp = pd.concat([cross_df_temp, df_level1])

            elif len(row_name) > 1:

                cross_df_temp = subtotals_multi_actuals_new(cross_df_temp, row_name, agg_func)

        # cross_df_temp = cross_df_temp.droplevel(0, axis=1)
        # CY_YA_var = 'cross_DFF'+ str(selected_weight_column) + '.xlsx'
        # cross_df_temp.to_excel(CY_YA_var)
        cross_df_temp = pd.concat([cross_df_temp], keys=[selected_weight_column], axis=1)
        # cross_df_temp.to_excel('cross_df_temp_doneerr.xlsx')

        crosstab_lst_final.append(cross_df_temp)

    cross_df = pd.concat(crosstab_lst_final, axis=1)

    # cross_df = cross_df.droplevel(1, axis=1)
    #
    # cross_df = cross_df.swaplevel(0, 1, axis=1).sort_index(axis=1)
    # cross_df = cross_df.reindex(columns=selected_weight_column_all, level=1)

    # cross_df.to_excel('SUBTOTALS_Cross_df.xlsx')

    return cross_df

def significance_fn(cross_df_sig, cross_df_actual_vals,base_var_sig):
    ##################### code to equalize rows of the dataframes ###################################
    try:
        cross_df_actual_vals = cross_df_actual_vals.drop(('Total', 'Total'), axis=0)
    except:
        pass
    # cross_df_actual_vals.to_excel('cross_df_actual_vals.xlsx')

    significance_val_lst = []

    # Get the level 0 names in the columns
    level_0_names_cols = cross_df_sig.columns.get_level_values(0).unique().tolist()

    cross_df_sig_col_grp = cross_df_sig.groupby(axis=1, level=0)

    # Access the first group
    for cross_df_sig_col_loop in level_0_names_cols:
        cross_df_sig_col = cross_df_sig_col_grp.get_group(cross_df_sig_col_loop)
        cross_df_sig_col_df = pd.DataFrame(cross_df_sig_col)

    # for index, cross_df_sig_col in cross_df_sig_col_grp:
        significance_val_lst_cols = []


        print('cross_df_sig_col_df shapee=',cross_df_sig_col_df.shape)
        # Get the unique values from the MultiIndex column names
        unique_groups = cross_df_sig_col_df.columns.get_level_values(1).unique()
        level0_grp_names = cross_df_sig_col_df.columns.get_level_values(0).unique()
        print('level0_grp_names',level0_grp_names)
        print('unique_groups',unique_groups)

        # combinations_list = [[val0, 'Total'] for val0 in unique_groups[:-1]]
        combinations_list = []

        for group in unique_groups:
            if group != base_var_sig:
                combinations_list.append([group, base_var_sig])
        print('====combinations_list==93',combinations_list)

        # Filter the MultiIndex DataFrame based on the combination of column names
        for loop_comb_lst in combinations_list:
            # significance_val_lst_cols = []
            print('loop_comb_lst===',loop_comb_lst)
            ##############################################################################
            #Filter the DataFrame based on the tuple value in level 1
            cross_df_sig_col_df_filtered = cross_df_sig_col_df.loc[:,
                          cross_df_sig_col_df.columns.get_level_values(1).isin(list(loop_comb_lst))]
            # cross_df_sig_col_df_filtered.to_excel('cross_df_sig_col_df_filtered_ffff.xlsx')
            ########################################################################################
            cross_df_sig_col_df_filtered = cross_df_sig_col_df_filtered.iloc[:, [0, 1]]
            cross_df_sig_col_df_filtered = cross_df_sig_col_df_filtered.reindex(columns=loop_comb_lst, level=1)
            # cross_df_sig_col_df_filtered.to_excel('cross_df_sig_col_df_filtered.xlsx')

            cross_df_sig_col_df_filtered_total = cross_df_sig_col_df.loc[:,
                          cross_df_sig_col_df.columns.get_level_values(1).isin([base_var_sig])]
            # cross_df_sig_col_df_filtered_total.to_excel('cross_df_sig_col_df_filtered_total.xlsx')
            # exit('cross_df_sig_col_df_filtered_total end!')

            cross_df_actual_vals_subtotals = cross_df_actual_vals.loc[(slice(None), 'Total'), :]
            repeat_times = len(cross_df_sig_col_df_filtered) // len(cross_df_actual_vals_subtotals)
            cross_df_actual_vals_subtotals = cross_df_actual_vals_subtotals.loc[
                cross_df_actual_vals_subtotals.index.repeat(repeat_times)].reset_index(drop=True)
            ##############################################################################################
            cross_df_actual_vals_subtotals_filtered = cross_df_actual_vals_subtotals.loc[:,
                          cross_df_actual_vals_subtotals.columns.get_level_values(1).isin(loop_comb_lst)]
            cross_df_actual_vals_subtotals_filtered = cross_df_actual_vals_subtotals_filtered.reindex(columns=loop_comb_lst, level=1)
            ##############################################################################################
            # cross_df_actual_vals_subtotals_filtered.to_excel('cross_df_actual_vals_subtotals_filtered_ffff.xlsx')

            cross_df_actual_vals_subtotals_filtered = cross_df_actual_vals_subtotals_filtered.iloc[:, [0, 1]]
            # cross_df_actual_vals_subtotals_filtered.to_excel('cross_df_actual_vals_subtotals_filtered.xlsx')

            cross_df_sig_col_df_filtered.reset_index(inplace=True,drop=True)
            cross_df_actual_vals_subtotals_filtered.reset_index(inplace=True,drop=True)
            significance_calc_df = pd.concat([cross_df_sig_col_df_filtered,cross_df_actual_vals_subtotals_filtered],axis=1, ignore_index=True)
            significance_calc_df.columns = ['exposed_avg1', 'control_avg1','exposed_base', 'control_base']

            significance_calc_df = calculate_significance(significance_calc_df)
            # significance_calc_df.to_excel('significance_calc_df.xlsx')
    #
            significance_val_lst_cols.append(significance_calc_df)
        sig_df = pd.concat(significance_val_lst_cols,axis = 1)
        sig_df.index = cross_df_sig_col_df.index

        combinations_list = [pair[0] for pair in combinations_list]
        print('combinations_list edited', combinations_list)
        sig_df.columns = combinations_list

        # sig_df = pd.concat([sig_df, cross_df_sig_col_df_filtered_total], axis=1)

        for loop_level0 in level0_grp_names:
            sig_df = pd.concat([sig_df], keys=[loop_level0], axis=1)

        # sig_df.to_excel('sig_df.xlsx')

        significance_val_lst.append(sig_df)
    significance_df = pd.concat(significance_val_lst, axis=1)
    significance_df.index = cross_df_sig.index

    # significance_df.to_excel('significance_df_final11.xlsx')
    return significance_df
###################### SIGNIFICANCE LOGIC ENDS ###########################################################


def calculate_significance(df):
    # loop_comb_lst = [' x '.join(pair) for pair in loop_comb_lst]
    # print('loop_comb_lst in function',loop_comb_lst)
    try:
        print('try block')

        df['exposed_term'] = df['exposed_avg1'] * (1 - df['exposed_avg1']) / df['exposed_base']
        df['control_term'] = df['control_avg1'] * (1 - df['control_avg1']) / df['control_base']
        # print('exposed_term', exposed_term)
        # print('control_term', control_term)

        df['addition_val_exp_control'] = df['exposed_term'] + df['control_term']
        # print('addition_val_exp_control', addition_val_exp_control)

        df['numerator'] = df['exposed_avg1'] - df['control_avg1']
        df['denominator'] = np.sqrt(df['addition_val_exp_control'])

        df['Significance'] = df['numerator'] / df['denominator']

    except:
        df['Significance'] = 0

    df = df['Significance']
    print('df Significance',df)

    return df



def calculate_significance_bk(exposed_avg1, control_avg1, exposed_base, control_base):
    try:
        print('try block')
        exposed_avg1 = float(exposed_avg1)
        control_avg1 = float(control_avg1)
        exposed_base = float(exposed_base)
        control_base = float(control_base)

        print('exposed_avg1', exposed_avg1)
        print('control_avg1', control_avg1)
        print('exposed_base', exposed_base)
        print('control_base', control_base)

        exposed_term = exposed_avg1 * (1 - exposed_avg1) / exposed_base
        control_term = control_avg1 * (1 - control_avg1) / control_base
        print('exposed_term', exposed_term)
        print('control_term', control_term)

        addition_val_exp_control = exposed_term + control_term
        print('addition_val_exp_control', addition_val_exp_control)

        numerator = exposed_avg1 - control_avg1
        denominator = math.sqrt(addition_val_exp_control)

        significance_arrow = numerator / denominator

    except:
        print('except block')
        # significance_arrow = 0
        exposed_avg1 = float(exposed_avg1)
        control_avg1 = float(control_avg1)

        significance_arrow = (exposed_avg1 - control_avg1) / math.sqrt(
            ((control_avg1 * control_base + exposed_avg1 * exposed_base) /
             (float(control_base) + float(exposed_base))) *
            (1 - ((control_avg1 * control_base + exposed_avg1 * exposed_base) /
                  (float(control_base) + float(exposed_base)))) *
            (1 / control_base + 1 / exposed_base)
        )

    return significance_arrow

def crosstab_main(df, dict_table, selected_weight_column, row_name, col_name,
                                     data_type_resp,
                                     percent_calc, seperated_flag_row, seperated_flag_col,
                                     totals_nested_flag,agg_func,measure_row_column_position):

    ########################### prefix code ##########################################
    # df.to_excel('df_BEFORE_PREFIX_SALES.xlsx')

    # print("df shape before prefix final", df.shape)
    # print("Prefix Function starts...")
    #
    # df_before_prefix = df.drop(selected_weight_column, axis=1)
    # df_no_prefix = df[selected_weight_column]
    # # df_before_prefix.to_excel('df_before_prefix_SALES.xlsx')
    # # df_no_prefix.to_excel('df_no_prefix_SALES.xlsx')
    #
    #
    # for colname_obj_loop in df_before_prefix.columns:
    #     df_before_prefix[colname_obj_loop] = df_before_prefix[colname_obj_loop].astype('str')
    #
    # df_prefixed = prefix_values(df_before_prefix)
    #
    # df = pd.concat([df_no_prefix, df_prefixed], axis=1)
    # print("Prefix Function ends...")
    # df.to_excel('df_AFTER_PREFIX_SALES.xlsx')

    ########################### prefix code ##########################################
    parameter_calc = create_parameter_calc(percent_calc)
    #################################################################################################################
    row_list_vals, col_list_vals = row_col_vals(df, row_name, col_name)
    # row_list_vals, col_list_vals = row_col_vals(df, row_name, col_name, selected_weight_column, parameter_calc)
    print('292==',row_list_vals)
    print('293==',col_list_vals)
    cross_df = data_type_resp_fn(df, row_name, col_name, row_list_vals, col_list_vals, percent_calc, parameter_calc,
                                 selected_weight_column, seperated_flag_row, seperated_flag_col, totals_nested_flag,agg_func,measure_row_column_position)

    #################################################################################################################
    cross_df.fillna(0, axis=1, inplace=True)

    # cross_df.to_excel('cross_dff.before_condn.xlsx')

    return cross_df


def weight_check(df):

    if 'weighting' not in df.columns:
        print("weighting is not Present in Data")
        df['weighting'] = 1
    else:
        print("weighting is Present in Data")
        pass

    return df

def create_selected_weight_column(Measure):
    if Measure == 'People':
        selected_weight_column = 'weighting'

    elif Measure == 'Occasion':
        selected_weight_column = 'Occasion'

    else:
        selected_weight_column = Measure

    return selected_weight_column

def create_list_final_cols(weight_param,row_name,col_name,selected_weight_column,Measure,data_type_resp):

    final_cols = ['LinkID'] + row_name + col_name + ['weighting', selected_weight_column]

    final_cols = list(set(final_cols))
    final_cols = sorted(final_cols)

    return final_cols

def create_measure_calc_column(df,Measure,weight_param,selected_weight_column):

    print('weight_param==== 290',weight_param)
    print('selected_weight_column==== 291',selected_weight_column)
    # exit("endd...")
    # df['measure_calc'] = df[selected_weight_column] * df['weighting']

    if weight_param == 'weighted':
        if Measure == 'People':
            df['measure_calc'] = df['weighting'].copy()

        elif Measure == Measure:
            df['measure_calc'] = df[Measure] * df['weighting']

    elif weight_param == 'unweighted':
        if Measure == 'People':
            df['measure_calc'] = 1

        elif Measure == Measure:
            df['measure_calc'] = df[Measure].copy()

    return df

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

def df_filter_temp(df):
    print("df_filter_temp started!")

    list_country = []
    # country_temp = ['India', 'China']
    country_temp = df['Country'].unique().tolist()
    for country_stacked in range(len(country_temp)):

        df_country = df[df['Country'] == country_temp[country_stacked]]
        df_before_prefix = df_country.drop(['weighting', 'Count', 'Occasion', 'measure_calc'], axis=1)
        df_no_prefix = df_country[['weighting', 'Count', 'Occasion', 'measure_calc']]

        for colname_obj_loop in df_before_prefix.columns:
            df_before_prefix[colname_obj_loop] = df_before_prefix[colname_obj_loop].astype('str')

        df_prefixed = prefix_values(df_before_prefix)

        df = pd.concat([df_no_prefix, df_prefixed], axis=1)

        list_country.append(df)

    df = pd.concat(list_country, axis=0)

    #df.to_excel("concatt_dff_fn.xlsx")

    return df

def create_prefix(df):
    prefix_country = []
    country_temp = df['Country'].unique().tolist()
    for country_stacked in range(len(country_temp)):
        print("country_stacked country_stacked prefixx", country_stacked)

        #df.to_excel("inside for df before pre.xlsx")
        country_name = country_temp[country_stacked]
        print("country_name====",country_name)
        print("country_name df====",df['Country'].head(10))

        df_prefix_country = df[df['Country'] == country_name]
        print("df_prefix_country headd",df_prefix_country.head(5))
        # df_prefix_country.to_excel("df_for_loop_prefixed_" + country_name + ".xlsx")

        df_before_prefix = df_prefix_country.drop(['weighting', 'Count', 'Occasion', 'measure_calc'], axis=1)
        df_no_prefix = df_prefix_country[['weighting', 'Count', 'Occasion', 'measure_calc']]

        print("df_before_prefix===",country_name,"df_before_prefix shape==",df_no_prefix.shape)
        print("df_no_prefix===",country_name,"df_no_prefix shape==",df_no_prefix.shape)

        for colname_obj_loop in df_before_prefix.columns:
            df_before_prefix[colname_obj_loop] = df_before_prefix[colname_obj_loop].astype('str')

        df_prefixed = prefix_values(df_before_prefix)

        df_final_prefixed = pd.concat([df_no_prefix,df_prefixed],axis=1)
        prefix_country.append(df_final_prefixed)

        # df_final_prefixed.to_excel("df_after_prefixed_" + country_name + ".xlsx")
        print("df_prefix_country done save")

    df = pd.concat(prefix_country)

    return df

# def row_col_vals(df,row_name,col_name):
#     row_list_vals = []
#     df_row = df[row_name]
#     if len(row_name) > 1:
#         for loop_row in range(len(row_name)):
#             str_row = numpy.array(df_row.iloc[:, loop_row])
#             row_list_vals.append(str_row)

#     col_list_vals = []
#     df_col = df[col_name]
#     if len(col_name) > 1:
#         for loop_row2 in range(len(col_name)):
#             str_col = numpy.array(df_col.iloc[:, loop_row2])
#             col_list_vals.append(str_col)

#     return row_list_vals,col_list_vals

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
 
    # Debug print for extracted values
    print("++++++++++++++++++++++++++++++")
    print(row_list_vals, col_list_vals)
    print("++++++++++++++++++++++++++++++")
   
    return row_list_vals, col_list_vals

def data_type_resp_fn(df, row_name, col_name,row_list_vals,col_list_vals,percent_calc,parameter_calc,
                      selected_weight_column,seperated_flag_row, seperated_flag_col, totals_nested_flag,agg_func,measure_row_column_position):
    # df.to_excel('dfff500.xlsx')
    print("row_list_vals len",len(row_list_vals))
    print("col_list_vals len",len(col_list_vals))

    print('seperated_flag_row--519-',seperated_flag_row)
    print('typee 0000',type(seperated_flag_row))
    print('seperated_flag_col--520-',seperated_flag_col)
    print('typee 1111',type(seperated_flag_col))
    ################# CROSSTAB BOTH NESTED ##################################################

    if seperated_flag_row == 0 and seperated_flag_col == 0:

        return nested_crosstab(df, row_name, col_name, row_list_vals, col_list_vals, percent_calc,
                                   parameter_calc, selected_weight_column, totals_nested_flag,agg_func,measure_row_column_position)

        # cross_df = nested_crosstab(df, row_name, col_name, row_list_vals, col_list_vals, percent_calc,
        #                            parameter_calc, selected_weight_column, totals_nested_flag,agg_func,measure_row_column_position)

        # cross_df.to_excel('cross_df_NESTED.xlsx')
    ################# CROSSTAB BOTH NESTED ##################################################

    ################# CROSSTAB STACKED ROWS ##################################################
    elif seperated_flag_row == 1 and seperated_flag_col == 0:
        return seperated_rows(df, row_name, col_name, row_list_vals, col_list_vals, percent_calc,
                                  parameter_calc, selected_weight_column,agg_func)
        # cross_df = seperated_rows(df, row_name, col_name, row_list_vals, col_list_vals, percent_calc,
        #                           parameter_calc, selected_weight_column,agg_func)

    ################# CROSSTAB STACKED ROWS ##################################################

    ################# CROSSTAB STACKED COLUMNS ##################################################
    elif seperated_flag_col == 1 and seperated_flag_row == 0:
        return seperated_cols(df, row_name, col_name, row_list_vals, col_list_vals, percent_calc,
                                  parameter_calc, selected_weight_column,agg_func)

        # cross_df = seperated_cols(df, row_name, col_name, row_list_vals, col_list_vals, percent_calc,
        #                           parameter_calc, selected_weight_column,agg_func)
        # cross_#df.to_excel("Cross_df_seperated_cols.xlsx")
    ################# CROSSTAB STACKED COLUMNS ##################################################

    ################# CROSSTAB BOTH STACKED ##################################################
    elif seperated_flag_col == 1 and seperated_flag_row == 1:
        return stacked_crosstab(df, row_name, col_name, percent_calc,
                                    parameter_calc, selected_weight_column,agg_func)

        # cross_df = stacked_crosstab(df, row_name, col_name, percent_calc,
        #                             parameter_calc, selected_weight_column,agg_func)

    else:
        raise ValueError("Invalid combination of seperated_flag_row and seperated_flag_col.")
################# CROSSTAB BOTH STACKED ##################################################

    return cross_df


# Assuming you have a DataFrame called 'df' with multilevel grouping columns and 'percent_calc' column
# def align_total_columns(cross_df):
#     group_cols = cross_df.columns.names[:-1]  # Get the names of the multilevel grouping columns
#     total_cols = cross_df.columns[cross_df.columns.get_level_values(-1).str.contains('Total')]  # Get the total columns
#
#     # Reorder columns while keeping level 0 intact
#     col_order = cross_df.columns.tolist()
#     col_order.remove('Total')  # Remove 'Total' from the list
#     col_order = col_order[:1] + total_cols.tolist() + col_order[1:]  # Add total columns at the start
#
#     # Reorder the columns in the dataframe
#     cross_df = cross_df.reindex(columns=col_order)
#
#     return cross_df

def align_total_column(df):
    total_col = df.filter(like='Grand Total', axis=1)  # Get the total column
    remaining_cols = df.drop(columns=total_col.columns)  # Get the remaining columns

    # Concatenate the total column followed by remaining columns
    df = pd.concat([total_col, remaining_cols], axis=1)

    return df








