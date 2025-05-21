import numpy
import pandas as pd
import numpy as np
import os,json
import time
import statistics as st
import copy
from main_dashboard.crosstab_calculation_functions import *
from main_dashboard.crosstab_calculation_seperated_functions import *
from django.conf import settings

import warnings
warnings.filterwarnings('ignore')

# PYTHONPATH = r"C:\Users\MihirPawar\Desktop\Python Project BSW\Python Files1\ccv_tool\ccv_survey_data\electrolux\\"
# PYTHONPATH = r"C:\Users\MihirPawar\Desktop\Python Project BSW\Python Files1\ccv_tool\ccv_survey_data\\"
# MERGED_PYTHONPATH = merged_pythonpath = r"C:\Users\MihirPawar\Desktop\Python Project BSW\Python Files1\ccv_tool\merged_data_files\\"

def crosstab_main(df,dict_table,Measure,weight_param, row_name, col_name,data_type_resp,
                  percent_calc,seperated_flag_row, seperated_flag_col, totals_nested_flag):
    
    ################### Code to Fill Null Values ####################################################
    df.fillna(0, inplace=True)


    df = vol_weight_check(df)

    # exit("end volume!")
    ################ Code to check whether Volume is present in Data #################################

    df['Occasion'] = 1

    selected_weight_column = create_selected_weight_column(Measure)

    final_cols = create_list_final_cols(weight_param,row_name,col_name,selected_weight_column,Measure,data_type_resp)
    # print('weight_param==>',weight_param)
    # print('row_name==>',row_name)
    # print('col_name==>',col_name)
    # print('selected_weight_column==>',selected_weight_column)
    # print('Measure==>',Measure)
    # print('final_cols==>',final_cols)
    print("final column namesss before ", df.columns)
    df = df[final_cols]

    print("final column namesss", df.columns)
    print("line 241 final_cols", final_cols)

    ##################################### Save File Merged - 24-01-2023 #############
    filename_merged = list(dict_table.keys())
    filename_merged = '_'.join([str(elem) for i, elem in enumerate(filename_merged)])
    print("filename_merged", filename_merged)
    # exit("filename_merged")
    df.to_json(settings.MERGED_PYTHONPATH + filename_merged + ".json", orient='records', lines=True)
    # #df.to_excel(settings.MERGED_PYTHONPATH + filename_merged + ".xlsx")
    ####### added by MIHIR PAWAR 19-08-2022 
    ##################################### Save File Merged - 24-01-2023 #############

    df['Count'] = 1

    if (Measure == 'People') and (data_type_resp == 'response' or data_type_resp == 'merged'):
        df = df.groupby(by=final_cols)['Count'].value_counts()
        print("Groupby successful!")

        # df.rename(columns = {'Count':'Count_temp'}, inplace = True)

        list_len_level_cols = [*range(0, len(final_cols), 1)]
        list_len_df = [*range(0, len(df), 1)]
        print("list_len_level_cols", list_len_level_cols)

        df = df.reset_index(level=list_len_level_cols)
        df['index_data'] = list_len_df

        df.set_index('index_data', inplace=True)

        print("DATAFRAME DIMENSIONS DISTINCT", df.shape)
        df.to_csv("grouped_data.csv")

        # print("list_len_level_cols", len(final_cols))
        # print("list_len_df", len(df))
        # exit("end!")

    df['Occasion'] = 1
    ############################## new added on 04-11-2022 ########################################
    # df = df[df['LinkID'] == 76]
    # df_sql = ps.sqldf("""(SELECT `Main Reason Chose Beverage`,count(distinct LinkID) FROM df GROUP BY `Main Reason Chose Beverage`) UNION
    #                   (SELECT 'total' as `Main Reason Chose Beverage`,count(distinct LinkID) FROM df);""")
    # q1 = """(SELECT `Main Reason Chose Beverage`,count(distinct LinkID) FROM df GROUP BY `Main Reason Chose Beverage`) UNION (SELECT 'total' as `Main Reason Chose Beverage`,count(distinct LinkID) FROM df);"""

    # print("df_sql",ps.sqldf(q1, locals()))
    # print("df_sql",df_sql)
    # df_sql.to_csv('df_sql.csv')
    # exit("end it df_sql")
    ############################## new added on 04-11-2022 ########################################
    df = create_measure_calc_column(df, weight_param, Measure)

    selected_weight_column = 'measure_calc'
    ############################ CODE FOR VOL X WEIHTING ###################################################

    ####################### BASE FILTER #####################################################################
    # dict_base_filter = {
    #     'Gender': ['Male'],
    #     'GBL Age Groups':['20-29 Years','60-69 Years']
    # }
    #
    # keys = list(dict_base_filter.keys())
    # values = list(dict_base_filter.values())
    # print("keys", keys)
    # print("values", values)
    #
    # for loop_keys in range(len(keys)):
    #     keys_temp = keys[loop_keys]
    #     values_temp = values[loop_keys]
    #     df = df[df[keys_temp].isin(values_temp)]

    # df = df[df['Gender'].isin(['Male'])]
    # df = df[df['GBL Age Groups'].isin(['20-29 Years','60-69 Years'])]
    ####################### BASE FILTER #####################################################################

    # filename_merged = list(dict_table.keys())
    # filename_merged = '_'.join([str(elem) for i, elem in enumerate(filename_merged)])
    # print("filename_merged", filename_merged)
    # # exit("filename_merged")
    # df.to_json(settings.MERGED_PYTHONPATH + filename_merged + ".json", orient='records', lines=True)
    # #df.to_excel(settings.MERGED_PYTHONPATH + filename_merged + ".xlsx")
    ####### added by MIHIR PAWAR 19-08-2022 ##########################################################
    print("df shape before prefix final", df.shape)
    print("Prefix Function starts...")

    #df.to_excel("df_before_prefixed.xlsx")

    # df = df_filter_temp(df)                                   ##function!
    df_before_prefix = df.drop(['Count', 'Occasion', 'measure_calc'], axis=1)
    df_no_prefix = df[['Count', 'Occasion', 'measure_calc']]

    for colname_obj_loop in df_before_prefix.columns:
        df_before_prefix[colname_obj_loop] = df_before_prefix[colname_obj_loop].astype('str')

    df_prefixed = prefix_values(df_before_prefix)

    df = pd.concat([df_no_prefix, df_prefixed], axis=1)
    print("Prefix Function ends...")

    # df = create_prefix(df)
    #df.to_excel("PREFIXED_DATAFRAME.xlsx")
    # exit("sssssss")

    df.to_excel("final_prefixed_df.xlsx")
    print("Prefix Function ends...")
    # exit("end it")

    parameter_calc = create_parameter_calc(percent_calc)

    # df = df['LinkID'] == 76
    #################################################################################################################
    row_list_vals, col_list_vals = row_col_vals(df, row_name, col_name)
    cross_df = data_type_resp_fn(df, row_name, col_name,row_list_vals,col_list_vals,percent_calc,
                                         parameter_calc, selected_weight_column, weight_param,
                                         seperated_flag_row, seperated_flag_col, totals_nested_flag)

    #################################################################################################################
    if percent_calc == 'column_percent' or percent_calc == 'row_percent':
        cross_df = cross_df.mul(100)

    cross_df.fillna(0, axis=1, inplace=True)

    return cross_df


def vol_weight_check(df):
    if 'Volume' not in df.columns:
        print("Volume is not Present in Data")
        df['Volume'] = 1
    else:
        print("Volume is Present in Data")
        pass

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

    elif Measure == 'Volume':
        selected_weight_column = 'Volume'

    return selected_weight_column

def create_list_final_cols(weight_param,row_name,col_name,selected_weight_column,Measure,data_type_resp):
    print("LINE NO 196 >>>>>>>>>> data_type_resp",data_type_resp)
    print("LINE NO 197 >>>>>>>>>> selected_weight_column",selected_weight_column)
    print("LINE NO 197 >>>>>>>>>> weight_param",weight_param)

    final_cols = ['LinkID'] + row_name + col_name + ['weighting','Volume']


    # if selected_weight_column == 'Volume':
    #     final_cols = ['LinkID'] + row_name + col_name + ['weighting','Volume']
    # else:
    #     final_cols = ['LinkID'] + row_name + col_name + ['weighting']


    # if weight_param == 'unweighted' :
    #     if data_type_resp == 'respondent' or 'concat':
    #         final_cols = ['LinkID'] + row_name + col_name + ['weighting']
    #     elif data_type_resp == 'merged' or 'response':
    #         final_cols = ['LinkID'] + row_name + col_name + ['weighting','Volume']

    # elif weight_param == 'weighted':
        # if data_type_resp == 'respondent' or 'concat':
        #     print("data_type_resp == respondent or concat")
        #     final_cols = ['LinkID'] + row_name + col_name + ['weighting']
        # elif data_type_resp == 'merged' or 'response':
        #     print("data_type_resp == merged or response")
        #     final_cols = ['LinkID'] + row_name + col_name + ['weighting','Volume']
    # exit("end 220!")
    print('final_cols>>>>>',final_cols)

        # final_cols = ['LinkID'] + row_name + col_name + ['weighting','Volume']

        # if Measure == 'People':
        #     final_cols = ['LinkID'] + row_name + col_name + ['weighting'] + list(selected_weight_column.split("-"))
        # elif Measure == 'Volume':
        #     final_cols = ['LinkID'] + row_name + col_name + ['weighting'] + list(selected_weight_column.split("-"))
        # elif Measure == 'Occasion':
        #     final_cols = ['LinkID'] + row_name + col_name + ['weighting']

    # try:
    #     final_cols = final_cols + ['Country']
    #     final_cols = list(set(final_cols))
    #     df = df[final_cols]
    # except:
    #     final_cols = list(set(final_cols))
    #     df = df[final_cols]

    final_cols = list(set(final_cols))
    final_cols = sorted(final_cols)

    return final_cols

def create_measure_calc_column(df,weight_param,Measure):
    if weight_param == 'weighted':

        if Measure == 'Volume':
            df['measure_calc'] = df['Volume'] * df['weighting']

        elif Measure == 'Occasion':
            # df['measure_calc'] = df['Occasion'].copy()
            df['measure_calc'] = df['Occasion'] * df['weighting']

        elif Measure == 'People':
            df['measure_calc'] = df['weighting'].copy()

    elif weight_param == 'unweighted':
        if Measure == 'People':
            df['measure_calc'] = 1

        elif Measure == 'Occasion':
            df['measure_calc'] = 1

        elif Measure == 'Volume':
            df['measure_calc'] = df['Volume'].copy()

    return df

def create_parameter_calc(percent_calc):
    if percent_calc == 'column_percent':
        parameter_calc='columns'
    elif percent_calc == 'row_percent':
        parameter_calc = 'index'
    elif percent_calc == 'actual_count':
        parameter_calc = False
    elif percent_calc == 'grand_total_count':
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

def row_col_vals(df,row_name,col_name):
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

    return row_list_vals,col_list_vals

def data_type_resp_fn(df, row_name, col_name,row_list_vals,col_list_vals,percent_calc,
                                         parameter_calc, selected_weight_column, weight_param,
                                         seperated_flag_row, seperated_flag_col, totals_nested_flag):
    #
    # row_list_vals = []
    # df_row=df[row_name]
    # if len(row_name) > 1:
    #     for loop_row in range(len(row_name)):
    #         str_row = numpy.array(df_row.iloc[:,loop_row])
    #         row_list_vals.append(str_row)
    #
    #
    # col_list_vals = []
    # df_col=df[col_name]
    # if len(col_name) > 1:
    #     for loop_row2 in range(len(col_name)):
    #         str_col = numpy.array(df_col.iloc[:,loop_row2])
    #         col_list_vals.append(str_col)

    print("row_list_vals len",len(row_list_vals))
    print("col_list_vals len",len(col_list_vals))
    ################# CROSSTAB BOTH NESTED ##################################################

    if seperated_flag_row == 0 and seperated_flag_col == 0:
        # print("country_stacked=====")
        # #df.to_excel("00_cross_df_" + country_stacked + ".xlsx")

        cross_df = nested_crosstab(df, row_name, col_name, row_list_vals, col_list_vals, percent_calc,
                                   parameter_calc, selected_weight_column, weight_param, totals_nested_flag)
    # exit("end !")

    ################# CROSSTAB BOTH NESTED ##################################################

    ################# CROSSTAB STACKED ROWS ##################################################
    if seperated_flag_row == 1 and seperated_flag_col == 0:
        cross_df = seperated_rows(df, row_name, col_name, row_list_vals, col_list_vals, percent_calc,
                                  parameter_calc, selected_weight_column, weight_param)

        # cross_#df.to_excel("Cross_df_seperated_rows.xlsx")
    ################# CROSSTAB STACKED ROWS ##################################################

    ################# CROSSTAB STACKED COLUMNS ##################################################
    print('CROSSTAB STACKED COLUMNS=====')
    if seperated_flag_col == 1 and seperated_flag_row == 0:
        cross_df = seperated_cols(df, row_name, col_name, row_list_vals, col_list_vals, percent_calc,
                                  parameter_calc, selected_weight_column, weight_param)
        # cross_#df.to_excel("Cross_df_seperated_cols.xlsx")
    ################# CROSSTAB STACKED COLUMNS ##################################################

    ################# CROSSTAB BOTH STACKED ##################################################
    if seperated_flag_col == 1 and seperated_flag_row == 1:
        cross_df = stacked_crosstab(df, row_name, col_name, percent_calc,
                                    parameter_calc, selected_weight_column, weight_param)
################# CROSSTAB BOTH STACKED ##################################################
    return cross_df