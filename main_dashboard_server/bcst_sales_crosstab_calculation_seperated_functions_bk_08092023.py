
import numpy
import pandas as pd
import numpy as np
import os,json
import time
import statistics as st

# from django.conf import settings
import copy
# from main_dashboard.crosstab_calculation_functions import *
from main_dashboard.bcst_sales_crosstab_calculation_functions import *
from main_dashboard.response_functions import *
from collections import Counter

totals_nested_flag = 1


def seperated_rows(df,row_name,col_name,row_list_vals,col_list_vals,percent_calc,
                                     parameter_calc,selected_weight_column):
    print("seperated_rows function started!")

    if len(col_name) == 1:
        print("WEIGHTED rowname equal to 1 condition seperated ROWS")

        cross_df_list = []
        for row_loop in row_name:
            # print(" FIRST CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH EQUAL TO 1!")
            row_name_str = ''.join([str(elem) for elem in row_loop])
            col_name_str = ''.join([str(elem) for elem in col_name])

            cross_df = pd.crosstab(index=[df[row_name_str]], columns=[df[col_name_str]],
                                   rownames=[row_name_str],
                                   colnames=[col_name_str], values=df[selected_weight_column], aggfunc=sum,
                                   normalize=parameter_calc,margins=True, margins_name='Grand Total')
            #
            # if percent_calc == 'actual_count':
            #     cross_df = cross_df / 100

            cross_df = pd.concat([cross_df], keys=[row_name_str], axis=0)  ####### 31-03-2023
            cross_df = pd.concat([cross_df], keys=[col_name_str], axis=1)  ####### 31-03-2023

            cross_df_list.append(cross_df)

        cross_df = pd.concat(cross_df_list, axis=0)

    elif len(col_name) > 1:
        print("WEIGHTED colname greater than 1 condition seperated ROWS")
        cross_df_list = []
        for row_loop in row_name:
            row_name_str = ''.join([str(elem) for elem in row_loop])

            if percent_calc == 'column_percent' or percent_calc == 'actual_count' or percent_calc == 'table_percent':
                cross_df = pd.crosstab(index=[df[row_name_str]], columns=col_list_vals, rownames=[row_name_str],
                                       colnames=col_name, values=df[selected_weight_column], aggfunc=sum,
                                       # normalize=parameter_calc, margins=True, margins_name='Grand Total')
                                       normalize=parameter_calc)

            elif percent_calc == 'row_percent':
                cross_df = pd.crosstab(index=[df[row_name_str]], columns=col_list_vals, rownames=[row_name_str],
                                       colnames=col_name, values=df[selected_weight_column], aggfunc=sum,
                                       normalize=parameter_calc, margins=True, margins_name='Grand Total')

            # if percent_calc == 'actual_count':
            #     cross_df = cross_df / 100

            # if percent_calc == 'column_percent':
            #     cross_df = cross_df.drop('Total',axis=1)

            # cross_df = pd.concat([cross_df], keys=[row_name_str], axis=0)  ####### 31-03-2023

            #################### SUBTOTALS #####################################################################

            if percent_calc == 'column_percent' or percent_calc == 'actual_count' or percent_calc == 'table_percent':
                cross_df_subtotals_single_dict = subtotals_single_cols_seperated_rows(df, percent_calc, row_name_str, row_name,
                                                                                      col_name,parameter_calc,
                                                                                      selected_weight_column)

                cross_df = subtotals_calc_seperated_rows(cross_df, percent_calc, row_name, col_name, cross_df_subtotals_single_dict)
                print("FUNCTION subtotals_single_cols_seperated_rows DONE!")

            print("SUBTOTALS ADDED TO TABLE SUCCESSFULLY!")

            # #################### SUBTOTALS #####################################################################
            cross_df = pd.concat([cross_df], keys=[row_name_str], axis=0)  ####### 31-03-2023

            cross_df_list.append(cross_df)

        cross_df = pd.concat(cross_df_list, axis=0)

        ########## ADDED BY MIHIR PAWAR ON 12-05-2023 - TOTAL ###########################################################
        print('12-05-2023 ===')

        if percent_calc == 'column_percent' or percent_calc == 'actual_count' or percent_calc == 'table_percent':
            cross_df_nested_total = totals_nested_seperated_cols(df,row_name,col_name,row_list_vals,col_list_vals,percent_calc,parameter_calc,
                    selected_weight_column)

            cross_df = pd.concat([cross_df,cross_df_nested_total], axis=1)

        # # ######################### ADDED BY MIHIR PAWAR - REMOVING DUPLICATES ########################################
        print("line 391 ========================== 391 ================================ resp col stacked =====")


    return cross_df

def subtotals_single_cols_seperated_rows(df, percent_calc, row_name_str, row_name, col_name,parameter_calc,
                                         selected_weight_column):

    print(" subtotals_single_cols_seperated_rows FUNCTION STARTED")
    print("====== length of col_name====== before ",len(col_name))
    # exit("end at subtotals")
    cross_df_subtotals_single_dict={}

    if percent_calc == 'column_percent' or percent_calc == 'actual_count' or percent_calc == 'table_percent':
        col_name_og = col_name[:]
        col_name1 = col_name[:]
        col_name1 = col_name1[:-1]

        for loop_col in range(len(col_name1)):

            print("loop_col loop_col", loop_col)
            col_name = col_name1[0:loop_col + 1]
            print("col_name col_name", col_name)

            col_list_vals = []
            df_col = df[col_name]
            if len(col_name) > 1:
                for loop_row2 in range(len(col_name)):
                    str_col = numpy.array(df_col.iloc[:, loop_row2])
                    col_list_vals.append(str_col)

            col_name_str = ''.join([str(elem) for elem in col_name])

            if len(col_name) == 1:
                cross_df = pd.crosstab(index=[df[row_name_str]], columns=[df[col_name_str]],
                                       rownames=[row_name_str],
                                       colnames=[col_name_str],values=df[selected_weight_column], aggfunc=sum,
                                       normalize=parameter_calc, margins=True, margins_name='Grand Total')

            else:
                cross_df = pd.crosstab(index=[df[row_name_str]], columns=col_list_vals, rownames=[row_name_str],
                                       colnames=col_name,values=df[selected_weight_column], aggfunc=sum,
                                       normalize=parameter_calc)

            # if len(col_name) == 1:
            #     cross_df = cross_df.drop('Total', axis=1)

            # cross_df.to_excel('cross_df_subtotals.xlsx')

            cross_df_subtotals_single_dict11 = {str(col_name): cross_df}
            cross_df_subtotals_single_dict.update(cross_df_subtotals_single_dict11)

    return cross_df_subtotals_single_dict


def subtotals_calc_seperated_rows(cross_df,percent_calc,row_name,col_name,cross_df_subtotals_single_dict):

    print("subtotals_calc function Running...")
    # print("===cross_df_subtotals_single_dict===",cross_df_subtotals_single_dict)
    # exit("end code at subtotals!")

    # if percent_calc == 'row_percent':
    #
    #     print("multi_subtotals FUNCTION Running..")
    #     #########################################################################################################
    #     cross_df=multi_subtotals_seperated_rows(cross_df,row_name,cross_df_subtotals_single_dict,percent_calc)
    #     #########################################################################################################

    if percent_calc == 'column_percent' or percent_calc == 'actual_count' or percent_calc == 'table_percent':

        # cross_df=cross_df.drop('Total',axis=1)
        cross_df = cross_df.T
        # cross_df_subtotals_single = cross_df_subtotals_single.T
        ##########################################################################################################
        cross_df = multi_subtotals_seperated_rows(cross_df, col_name,cross_df_subtotals_single_dict,percent_calc)
        ##########################################################################################################

        cross_df = cross_df.T

    return cross_df

def multi_subtotals_seperated_cols(cross_df,row_name,cross_df_subtotals_single_dict,percent_calc):

    if len(row_name)==2:
        print("multi_subtotals two rows")
        # cross_df.to_excel("cross_df_transposed.xlsx")

        df1 = list(cross_df_subtotals_single_dict.values())[0]
        # df1.to_excel("df1_df1_before_transpose.xlsx")
        # if percent_calc == 'column_percent' or percent_calc == 'actual_count' or percent_calc =='table_percent':
        #     df1=df1.T
            # pass

        df1.index=pd.MultiIndex.from_arrays([df1.index.values , len(df1.index) * ['Total']])
        # df1.to_excel("df1_df1_after_transpose.xlsx")

        # df1.to_excel('df1_subtotals.xlsx')
        # df2.index = pd.MultiIndex.from_arrays([df2.index.values + '_total',len(df2.index) * ['']])

        cross_df = pd.concat([cross_df, df1]).sort_index(level=0)


    if len(row_name)==3:
        print("multi_subtotals three rows")

        df1 = list(cross_df_subtotals_single_dict.values())[1]
        # if percent_calc == 'column_percent':
        #     df1 = df1.T

        df1.index = pd.MultiIndex.from_arrays([df1.index.get_level_values(0),
                                               df1.index.get_level_values(1),
                                               len(df1.index) * ['Total']])

        # df2 = cross_df.groupby(level=0).sum()
        df2 = list(cross_df_subtotals_single_dict.values())[0]

        # if percent_calc == 'column_percent':
        #     df2 = df2.T

        df2.index = pd.MultiIndex.from_arrays([df2.index.values,
                                               len(df2.index) * ['Total'],
                                               len(df2.index) * ['']])

        # concat all dataframes together, sort index
        cross_df = pd.concat([cross_df, df1, df2]).sort_index(level=[0,1])
        # cross_df = pd.concat([cross_df, df1, df2]).sort_index()

    if len(row_name)==4:
        print("multi_subtotals four rows")
        # df1 = cross_df.groupby(level=[0, 1, 2]).sum()

        df1 = list(cross_df_subtotals_single_dict.values())[2]
        # if percent_calc == 'column_percent':
        #     df1 = df1.T
        df1.index = pd.MultiIndex.from_arrays([df1.index.get_level_values(0),
                                               df1.index.get_level_values(1),
                                               df1.index.get_level_values(2),
                                               len(df1.index) * ['Total']])

        print("multi_subtotals three rows")

        df2 = list(cross_df_subtotals_single_dict.values())[1]
        # if percent_calc == 'column_percent':
        #     df2 = df2.T
        # df2 = cross_df.groupby(level=[0, 1]).sum()
        df2.index = pd.MultiIndex.from_arrays([df2.index.get_level_values(0),
                                               df2.index.get_level_values(1),
                                               len(df2.index) * ['Total'],
                                               len(df2.index) * ['']])

        # df3 = cross_df.groupby(level=0).sum()

        df3 = list(cross_df_subtotals_single_dict.values())[0]
        # if percent_calc == 'column_percent':
        #     df3 = df3.T
        df3.index = pd.MultiIndex.from_arrays([df3.index.values,
                                               len(df3.index) * ['Total'],
                                               len(df3.index) * [''],
                                               len(df3.index) * ['']])

        # concat all dataframes together, sort index
        cross_df = pd.concat([cross_df, df1, df2, df3]).sort_index(level=[0, 1, 2])

    if len(row_name) == 5:
        print("row_name>>>",row_name)

        # df1 = cross_df.groupby(level=[0, 1, 2, 3]).sum()
        df1 = list(cross_df_subtotals_single_dict.values())[3]
        # if percent_calc == 'column_percent':
        #     df1 = df1.T

        df1.index = pd.MultiIndex.from_arrays([df1.index.get_level_values(0),
                                               df1.index.get_level_values(1),
                                               df1.index.get_level_values(2),
                                               df1.index.get_level_values(3),
                                               len(df1.index) * ['Total']])


        # df2 = cross_df.groupby(level=[0, 1, 2]).sum()
        df2 = list(cross_df_subtotals_single_dict.values())[2]
        # if percent_calc == 'column_percent':
        #     df2 = df2.T

        df2.index = pd.MultiIndex.from_arrays([df2.index.get_level_values(0),
                                               df2.index.get_level_values(1),
                                               df2.index.get_level_values(2),
                                               len(df2.index) * ['Total'],
                                               len(df2.index) * ['']])

        # df3 = cross_df.groupby(level=[0, 1]).sum()

        df3 = list(cross_df_subtotals_single_dict.values())[1]
        # if percent_calc == 'column_percent':
        #     df3 = df3.T

        df3.index = pd.MultiIndex.from_arrays([df3.index.get_level_values(0),
                                               df3.index.get_level_values(1),
                                               len(df3.index) * ['Total'],
                                               len(df3.index) * [''],
                                               len(df3.index) * ['']])

        # df4 = cross_df.groupby(level=0).sum()

        df4 = list(cross_df_subtotals_single_dict.values())[0]
        # if percent_calc == 'column_percent':
        #     df4 = df4.T

        df4.index = pd.MultiIndex.from_arrays([df4.index.values,
                                               len(df4.index) * ['Total'],
                                               len(df4.index) * [''],
                                               len(df4.index) * [''],
                                               len(df4.index) * ['']])

        # concat all dataframes together, sort index
        cross_df = pd.concat([cross_df, df1, df2, df3, df4]).sort_index(level=[0, 1, 2, 3])

    return cross_df

def multi_subtotals_seperated_rows(cross_df,row_name,cross_df_subtotals_single_dict,percent_calc):

    if len(row_name)==2:
        print("multi_subtotals two rows")
        # cross_df.to_excel("cross_df_transposed.xlsx")

        df1 = list(cross_df_subtotals_single_dict.values())[0]
        # df1.to_excel("df1_df1_before_transpose.xlsx")
        if percent_calc == 'column_percent' or percent_calc == 'actual_count' or percent_calc == 'table_percent':
            df1=df1.T
            # pass

        df1.index=pd.MultiIndex.from_arrays([df1.index.values , len(df1.index) * ['Total']])
        # df1.to_excel("df1_df1_after_transpose.xlsx")

        # df1.to_excel('df1_subtotals.xlsx')
        # df2.index = pd.MultiIndex.from_arrays([df2.index.values + '_total',len(df2.index) * ['']])

        cross_df = pd.concat([cross_df, df1]).sort_index(level=0)


    if len(row_name)==3:
        print("multi_subtotals three rows")

        df1 = list(cross_df_subtotals_single_dict.values())[1]
        if percent_calc == 'column_percent':
            df1 = df1.T

        df1.index = pd.MultiIndex.from_arrays([df1.index.get_level_values(0),
                                               df1.index.get_level_values(1),
                                               len(df1.index) * ['Total']])

        # df2 = cross_df.groupby(level=0).sum()
        df2 = list(cross_df_subtotals_single_dict.values())[0]

        if percent_calc == 'column_percent':
            df2 = df2.T

        df2.index = pd.MultiIndex.from_arrays([df2.index.values,
                                               len(df2.index) * ['Total'],
                                               len(df2.index) * ['']])

        # concat all dataframes together, sort index
        cross_df = pd.concat([cross_df, df1, df2]).sort_index(level=[0,1])
        # cross_df = pd.concat([cross_df, df1, df2]).sort_index()

    if len(row_name)==4:
        print("multi_subtotals four rows")
        # df1 = cross_df.groupby(level=[0, 1, 2]).sum()

        df1 = list(cross_df_subtotals_single_dict.values())[2]
        if percent_calc == 'column_percent':
            df1 = df1.T
        df1.index = pd.MultiIndex.from_arrays([df1.index.get_level_values(0),
                                               df1.index.get_level_values(1),
                                               df1.index.get_level_values(2),
                                               len(df1.index) * ['Total']])

        print("multi_subtotals three rows")

        df2 = list(cross_df_subtotals_single_dict.values())[1]
        if percent_calc == 'column_percent':
            df2 = df2.T
        # df2 = cross_df.groupby(level=[0, 1]).sum()
        df2.index = pd.MultiIndex.from_arrays([df2.index.get_level_values(0),
                                               df2.index.get_level_values(1),
                                               len(df2.index) * ['Total'],
                                               len(df2.index) * ['']])

        # df3 = cross_df.groupby(level=0).sum()

        df3 = list(cross_df_subtotals_single_dict.values())[0]
        if percent_calc == 'column_percent':
            df3 = df3.T
        df3.index = pd.MultiIndex.from_arrays([df3.index.values,
                                               len(df3.index) * ['Total'],
                                               len(df3.index) * [''],
                                               len(df3.index) * ['']])

        # concat all dataframes together, sort index
        cross_df = pd.concat([cross_df, df1, df2, df3]).sort_index(level=[0, 1, 2])

    if len(row_name) == 5:
        print("row_name>>>",row_name)

        # df1 = cross_df.groupby(level=[0, 1, 2, 3]).sum()
        df1 = list(cross_df_subtotals_single_dict.values())[3]
        if percent_calc == 'column_percent':
            df1 = df1.T

        df1.index = pd.MultiIndex.from_arrays([df1.index.get_level_values(0),
                                               df1.index.get_level_values(1),
                                               df1.index.get_level_values(2),
                                               df1.index.get_level_values(3),
                                               len(df1.index) * ['Total']])


        # df2 = cross_df.groupby(level=[0, 1, 2]).sum()
        df2 = list(cross_df_subtotals_single_dict.values())[2]
        if percent_calc == 'column_percent':
            df2 = df2.T

        df2.index = pd.MultiIndex.from_arrays([df2.index.get_level_values(0),
                                               df2.index.get_level_values(1),
                                               df2.index.get_level_values(2),
                                               len(df2.index) * ['Total'],
                                               len(df2.index) * ['']])

        # df3 = cross_df.groupby(level=[0, 1]).sum()

        df3 = list(cross_df_subtotals_single_dict.values())[1]
        if percent_calc == 'column_percent':
            df3 = df3.T

        df3.index = pd.MultiIndex.from_arrays([df3.index.get_level_values(0),
                                               df3.index.get_level_values(1),
                                               len(df3.index) * ['Total'],
                                               len(df3.index) * [''],
                                               len(df3.index) * ['']])

        # df4 = cross_df.groupby(level=0).sum()

        df4 = list(cross_df_subtotals_single_dict.values())[0]
        if percent_calc == 'column_percent':
            df4 = df4.T

        df4.index = pd.MultiIndex.from_arrays([df4.index.values,
                                               len(df4.index) * ['Total'],
                                               len(df4.index) * [''],
                                               len(df4.index) * [''],
                                               len(df4.index) * ['']])

        # concat all dataframes together, sort index
        cross_df = pd.concat([cross_df, df1, df2, df3, df4]).sort_index(level=[0, 1, 2, 3])

    return cross_df


def seperated_cols(df,row_name,col_name,row_list_vals,col_list_vals,percent_calc,
                                     parameter_calc,selected_weight_column):
    print("seperated_cols function started!")

    if len(row_name) == 1:
        print("UNWEIGHTED rowname equal to 1 condition seperated COLUMNS")

        cross_df_list = []
        for col_loop in col_name:
            # print(" FIRST CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH EQUAL TO 1!")
            row_name_str = ''.join([str(elem) for elem in row_name])
            col_name_str = ''.join([str(elem) for elem in col_loop])

            cross_df = pd.crosstab(index=[df[row_name_str]], columns=[df[col_name_str]],
                                   rownames=[row_name_str],
                                   colnames=[col_name_str], values=df[selected_weight_column], aggfunc=sum,
                                   normalize=parameter_calc, margins=True, margins_name='Grand Total')

            # if percent_calc == 'actual_count':
            #     cross_df = cross_df / 100

            cross_df = pd.concat([cross_df], keys=[row_name_str], axis=0)  ####### 31-03-2023
            cross_df = pd.concat([cross_df], keys=[col_name_str], axis=1)  ####### 31-03-2023

            cross_df_list.append(cross_df)

        cross_df = pd.concat(cross_df_list, axis=1)
        # cross_df.to_excel("Cross_df_seperated_rows.xlsx")

    elif len(row_name) > 1:
        print("UNWEIGHTED colname greater than 1 condition seperated COLUMNS")
        cross_df_list = []
        for col_loop in col_name:
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
            #     cross_df = cross_df / 100


            #################### SUBTOTALS #####################################################################

            if percent_calc == 'row_percent':
                cross_df_subtotals_single_dict = subtotals_single_cols_seperated_cols(df, percent_calc, col_name_str, row_name,
                                                                                      col_name,parameter_calc,
                                                                                      selected_weight_column)
                print("cross_df_subtotals_single_dict===",cross_df_subtotals_single_dict.keys())
                # exit("end")

                cross_df = subtotals_calc_seperated_cols(cross_df, percent_calc, row_name, col_name, cross_df_subtotals_single_dict)
                print("FUNCTION subtotals_single_cols_seperated_rows DONE!")


            print("SUBTOTALS ADDED TO TABLE SUCCESSFULLY!")

            # #################### SUBTOTALS #####################################################################
            cross_df = pd.concat([cross_df], keys=[col_name_str], axis=1)  ####### 31-03-2023

            cross_df_list.append(cross_df)

        cross_df = pd.concat(cross_df_list, axis=1)

        ########## ADDED BY MIHIR PAWAR ON 12-05-2023 - TOTAL ###########################################################
        print('12-05-2023 ===')

        if percent_calc == 'row_percent':
            cross_df_nested_total = totals_nested_seperated_rows(df, row_name, col_name, row_list_vals,
                                                                 col_list_vals, percent_calc, parameter_calc,
                                                                 selected_weight_column)

            cross_df = pd.concat([cross_df,cross_df_nested_total], axis=0)

    print('====cross_df_nested_total===index==', cross_df.index)

    if percent_calc == 'row_percent':
        try:
            cross_df = cross_df.drop(('Total', ''), axis=0)
        except:
            pass

    return cross_df


def subtotals_single_cols_seperated_cols(df, percent_calc, col_name_str, row_name, col_name,parameter_calc,
                                         selected_weight_column):

    print(" subtotals_single_cols_seperated_cols FUNCTION STARTED")

    cross_df_subtotals_single_dict={}

    if percent_calc == 'row_percent':
        # if percent_calc == 'column_percent':
        row_name_og = row_name[:]
        row_name1 = row_name[:]
        row_name1 = row_name1[:-1]

        for loop_col in range(len(row_name1)):

            print("loop_col loop_col", loop_col)
            row_name = row_name1[0:loop_col + 1]
            print("row_name row_name", row_name)

            row_list_vals = []
            df_row = df[row_name]
            if len(row_name) > 1:
                for loop_row2 in range(len(row_name)):
                    str_col = numpy.array(df_row.iloc[:, loop_row2])
                    row_list_vals.append(str_col)

            row_name_str = ''.join([str(elem) for elem in row_name])

            if len(row_name) == 1:
                cross_df = pd.crosstab(index=[df[row_name_str]], columns=[df[col_name_str]],
                                       rownames=[row_name_str],
                                       colnames=[col_name_str],values=df[selected_weight_column], aggfunc=sum,
                                       normalize=parameter_calc)

            else:
                cross_df = pd.crosstab(index=row_list_vals, columns=[df[col_name_str]], rownames=row_name,
                                       colnames=[col_name_str],values=df[selected_weight_column], aggfunc=sum,
                                       normalize=parameter_calc)

            if len(row_name) == 1:
                # cross_df = cross_df.drop('Total')
                pass

            cross_df_subtotals_single_dict11 = {str(row_name): cross_df}
            cross_df_subtotals_single_dict.update(cross_df_subtotals_single_dict11)

    return cross_df_subtotals_single_dict


def subtotals_calc_seperated_cols(cross_df,percent_calc,row_name,col_name,cross_df_subtotals_single_dict):

    print("subtotals_calc function Running...")
    # print("===cross_df_subtotals_single_dict===",cross_df_subtotals_single_dict)
    # exit("end code at subtotals!")

    # if percent_calc == 'column_percent' or percent_calc == 'actual_count':
    if percent_calc == 'row_percent':

        print("multi_subtotals FUNCTION Running..")
        #########################################################################################################
        cross_df=multi_subtotals_seperated_cols(cross_df,row_name,cross_df_subtotals_single_dict,percent_calc)
        #########################################################################################################
        print("multi_subtotals FUNCTION DONE..")

    # if percent_calc == 'row_percent':
    # if percent_calc == 'column_percent' or percent_calc == 'actual_count' or 'table_percent':
    #
    #     # cross_df=cross_df.drop('Total',axis=1)
    #     cross_df = cross_df.T
    #     # cross_df_subtotals_single = cross_df_subtotals_single.T
    #     ##########################################################################################################
    #     cross_df = multi_subtotals_seperated(cross_df, col_name,cross_df_subtotals_single_dict,percent_calc)
    #     # cross_df = multi_subtotals(cross_df,row_name)
    #     ##########################################################################################################
    #
    #     cross_df = cross_df.T

    return cross_df

def stacked_crosstab(df, row_name, col_name, percent_calc,
                                  parameter_calc, selected_weight_column):

    df.to_excel('df_stackedd_error.xlsx')

    print('===row_name===',row_name)
    print('===col_name===',col_name)

    row_name_str = ''.join([str(elem) for elem in row_name])
    col_name_str = ''.join([str(elem) for elem in col_name])

    cross_df_list_rows = []
    # cross_df_dict_rows = {}
    for row_loop in row_name:
        print("for loop row", row_loop)

        cross_df_list_cols = []
        # cross_df_dict_cols={}
        for col_loop in col_name:
            print("for loop col_loop", col_loop)

            #     print("row_loop",row_loop)
            #     print("col_loop",col_loop)
            #      # print(" FIRST CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH EQUAL TO 1!")
            row_name_str = ''.join([str(elem) for elem in row_loop])
            col_name_str = ''.join([str(elem) for elem in col_loop])
            print('==654==row_name_str',row_name_str)
            print('==655==col_name_str',col_name_str)

            #
            cross_df = pd.crosstab(index=[df[row_name_str]], columns=[df[col_name_str]],
                                   rownames=[row_name_str],
                                   colnames=[col_name_str], values=df[selected_weight_column], aggfunc=sum,
                                   normalize=parameter_calc, margins=True, margins_name='Grand Total')

            cross_df = pd.concat([cross_df], keys=[row_name_str], axis=0)  ####### 31-03-2023
            cross_df = pd.concat([cross_df], keys=[col_name_str], axis=1)  ####### 31-03-2023

            # if percent_calc == 'actual_count':
            #     cross_df = cross_df / 100
            cross_df.to_excel('cross_df_stacked_31.xlsx')
            print("=========================================")
            cross_df_list_cols.append(cross_df)
            cross_df = pd.concat(cross_df_list_cols, axis=1)
            filename_stacked = str(row_loop) + "_" + str(col_loop)

        cross_df_list_rows.append(cross_df)
        cross_df = pd.concat(cross_df_list_rows, axis=0)

        print("=========================================")

    return cross_df


def totals_nested_seperated_cols(df,row_name,col_name,row_list_vals,col_list_vals,percent_calc,parameter_calc,
                    selected_weight_column):

    print("====totals_nested_seperated_cols === row_name",row_name)

    cross_df_totals_nested_list = []
    for row_loop in row_name:
        row_name_str = ''.join([str(elem) for elem in row_loop])

        col_loop = col_name[-1]
        # print(" FIRST CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH EQUAL TO 1!")
        # row_name_str = ''.join([str(elem) for elem in row_name])
        col_name_str = ''.join([str(elem) for elem in col_loop])

        cross_df = pd.crosstab(index=[df[row_name_str]], columns=[df[col_name_str]],
                               rownames=[row_name_str],
                               colnames=[col_name_str], values=df[selected_weight_column], aggfunc=sum,
                               normalize=parameter_calc, margins=True, margins_name='Grand Total')

        cross_df_nested_total = pd.concat([cross_df], keys=[row_name_str], axis=0)  ####### 31-03-2023


        cross_df_nested_total = cross_df_nested_total.loc[:,
                                ~cross_df_nested_total.columns.duplicated(keep='last')].copy()

        for loop_nested_totals in range(len(col_name) - 2):
            print('loop_nested_totals====', loop_nested_totals)
            cross_df_nested_total = pd.concat([cross_df_nested_total], keys=[''], axis=1)
        #
        cross_df_nested_total = pd.concat([cross_df_nested_total], keys=['Total'], axis=1)
        #
        # # cross_df = pd.concat([cross_df,cross_df_nested_total],axis=1) #commented by mihir pawar on 21-04-2023
        # print("Added by mihir pawar on 21-04-2023")

        cross_df_totals_nested_list.append(cross_df_nested_total)

    cross_df_nested_total = pd.concat(cross_df_totals_nested_list, axis=0)

    return cross_df_nested_total

def totals_nested_seperated_rows(df,row_name,col_name,row_list_vals,col_list_vals,percent_calc,parameter_calc,
                    selected_weight_column):

    print("====totals_nested_seperated_rows === ")

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
        cross_df_nested_total.to_excel('cross_df_nested_total.xlsx')

        # cross_df_nested_total = cross_df_nested_total.loc[~cross_df_nested_total.columns.duplicated(keep='last')].copy()

        for loop_nested_totals in range(len(row_name) - 2):
            print('loop_nested_totals====', loop_nested_totals)
            cross_df_nested_total = pd.concat([cross_df_nested_total], keys=[''], axis=0)
        #
        cross_df_nested_total = pd.concat([cross_df_nested_total], keys=['Total'], axis=0)
        #
        # # cross_df = pd.concat([cross_df,cross_df_nested_total],axis=1) #commented by mihir pawar on 21-04-2023
        # print("Added by mihir pawar on 21-04-2023")

        cross_df_totals_nested_list.append(cross_df_nested_total)

    cross_df_nested_total = pd.concat(cross_df_totals_nested_list, axis=1)


    return cross_df_nested_total


