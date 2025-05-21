
import numpy
import pandas as pd
import numpy as np
import os,json
import time
import statistics as st
import copy
from django.conf import settings

import warnings
warnings.filterwarnings('ignore')


# PYTHONPATH = r"C:\Users\MihirPawar\Desktop\Python Project BSW\Python Files1\ccv_tool\ccv_survey_data\electrolux\\"
# MERGED_PYTHONPATH = merged_pythonpath = r"C:\Users\MihirPawar\Desktop\Python Project BSW\Python Files1\ccv_tool\merged_data_files\\"

def concat_data(dict_table):
    start_time_concat = time.time()

    loop_vals_lst = []
    for loop_vals in dict_table.values():
        loop_vals_lst.extend(loop_vals)

    # loop_vals_lst = loop_vals_lst + ['LinkID','weighting']            #old code
    loop_vals_lst = loop_vals_lst + ['LinkID','weighting'] #new code modified on 05-12-2022

    loop_vals_lst = list(set(loop_vals_lst))

    table_name_cols = []
    for data_concat_loop in dict_table.keys():
        print("dict_table.keys===",data_concat_loop)

        table_name = data_concat_loop + ".json"
        print("table_name",table_name)

        df_table = pd.read_json(settings.PYTHONPATH + table_name, orient='records', lines=True)

        df_table1_final = df_table[loop_vals_lst]

        table_name_cols.append(df_table1_final)
    df = pd.concat(table_name_cols).reset_index(drop=True)
    # #df.to_excel("df_concatt.xlsx",index=False)

    # exit("end it!")
    return df


def concat_data_bk1(dict_table):
    start_time_concat = time.time()

    loop_vals_lst = []
    for loop_vals in dict_table.values():
        loop_vals_lst.extend(loop_vals)

    # loop_vals_lst = loop_vals_lst + ['LinkID','weighting']            #old code
    loop_vals_lst = loop_vals_lst + ['LinkID','weighting'] #new code modified on 05-12-2022

    loop_vals_lst = list(set(loop_vals_lst))

    for data_concat_loop in dict_table.keys():
        print("dict_table.keys===",data_concat_loop)

        table_name = data_concat_loop + ".json"
        print("table_name",table_name)

        df_table = pd.read_json(settings.PYTHONPATH + table_name, orient='records', lines=True)

        df_table1_final = df_table[loop_vals_lst]
        # print("df_table1_final val counts",df_table1_final['Country'].value_counts())

        # cross_df = crosstab_main(df, dict_table, Measure, weight_param, row_name, col_name, data_type_resp,
        #           percent_calc, seperated_flag_row, seperated_flag_col, totals_nested_flag)

        # return df_table1_final
    # #df.to_excel("df_concatt.xlsx",index=False)

    # exit("end it!")

def merge_data(dict_table):
    start_time_merge=time.time()

    print("dict_table keys",dict_table.keys())
    print("dict_table values",dict_table.values())

    table_name1_filename = list(dict_table.keys())[0] + ".json"
    table_name2_filename = list(dict_table.keys())[1] + ".json"

    table_name1_cols = list(dict_table.values())[0] + ['LinkID','weighting']
    table_name2_cols = list(dict_table.values())[1] + ['LinkID','Volume']

    df_table1 = pd.read_json(settings.PYTHONPATH + table_name1_filename, orient='records', lines=True)
    df_table2 = pd.read_json(settings.PYTHONPATH + table_name2_filename, orient='records', lines=True)

    df_table1_final = df_table1[table_name1_cols]
    df_table2_final = df_table2[table_name2_cols]

    print("length df_table1",len(df_table1_final))
    print("length df_table2",len(df_table1_final))

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

    print("TIME TAKEN TO MERGE:-",end_time_merge-start_time_merge," seconds")

    # df.to_csv("df_merged22.csv",index=False)
    if 'Volume' not in df_table2:
        print("Volume is not Present in Data")
        df['Volume'] = 1
    else:
        print("Volume is Present in Data")
        pass

    if 'weighting' not in df_table1.columns:
        print("weighting is not Present in Data")
        df['weighting'] = 1
    else:
        pass

    # filename_merged = list(dict_table.keys())
    # filename_merged = '_'.join([str(elem) for i, elem in enumerate(filename_merged)])
    # print("filename_merged", filename_merged)
    # # exit("filename_merged")
    # df.to_json(MERGED_settings.PYTHONPATH + filename_merged + ".json", orient='records', lines=True)
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

        # df_Freq['prefix_col'] = df_Freq['alpha_prefix'] + "}" + df_Freq['Columns']
        df_Freq['prefix_col'] = df_Freq['alpha_prefix'].astype(str) + "}" + df_Freq['Columns'].astype(str)

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
                    selected_weight_column,weight_param,totals_nested_flag):
    print("nested_crosstab starts")
    # country_stacked = country_dataa
    if percent_calc=='column_percent' or percent_calc=='row_percent':

        cross_df = crosstab_basic_table(df, percent_calc, row_name, col_name, parameter_calc, col_list_vals, row_list_vals,
                             weight_param, selected_weight_column)


        # if df['Country'].unique() == ['000}China']:
        #     #df.to_excel("dfdf_inner_crosstab11111.xlsx")
        #     cross_#df.to_excel("cross_df_basic_cross_tablee22.xlsx")


    elif percent_calc=='actual_count':
        cross_df = crosstab_actual_counts(df,row_name,col_name,row_list_vals,col_list_vals,percent_calc,parameter_calc,
                    selected_weight_column,weight_param)

    print("CROSSTAB TABLE CREATED SUCCESSFULLY=======!")
    # exit("End it!!")

    if percent_calc=='column_percent' or percent_calc == 'actual_count':
        if len(col_name) > 1:
            cross_df_subtotals_single_dict = subtotals_single_cols(df,percent_calc,row_name,col_name,parameter_calc,col_list_vals,row_list_vals,
                                            weight_param,selected_weight_column)

            cross_df = subtotals_calc(cross_df,percent_calc,row_name,col_name,cross_df_subtotals_single_dict)
            # cross_#df.to_excel("cross_df_basic_cross_tablee.xlsx")
        ########## CODE FOR ADDING TOTALS TO COLUMN PERCENT ################################################
            if totals_nested_flag == 1:
                cross_df_nested_total = totals_nested(df, row_name, col_name, row_list_vals, col_list_vals, percent_calc,
                                                      parameter_calc,
                                                      selected_weight_column, weight_param)

                cross_df_nested_total = cross_df_nested_total.loc[:, ~cross_df_nested_total.columns.duplicated(keep='last')].copy()
                #

                for loop_nested_totals in range(len(col_name)-2):
                    cross_df_nested_total = pd.concat([cross_df_nested_total], keys=[''], axis=1)

                cross_df_nested_total = pd.concat([cross_df_nested_total], keys=['Total'], axis=1)

                cross_df = pd.concat([cross_df,cross_df_nested_total],axis=1)
    ########## CODE FOR ADDING TOTALS TO COLUMN PERCENT ################################################
    elif percent_calc == 'row_percent':
        if len(row_name) > 1:
            cross_df_subtotals_single_dict = subtotals_single_cols(df,percent_calc,row_name,col_name,parameter_calc,col_list_vals,row_list_vals,
                                            weight_param,selected_weight_column)

            cross_df = subtotals_calc(cross_df,percent_calc,row_name,col_name,cross_df_subtotals_single_dict)
            ########## CODE FOR ADDING TOTALS TO ROW PERCENT ################################################
            if totals_nested_flag == 1:
                cross_df_nested_total = totals_nested(df, row_name, col_name, row_list_vals, col_list_vals, percent_calc,
                                                      parameter_calc,
                                                      selected_weight_column, weight_param)

                cross_df_nested_total = cross_df_nested_total[~cross_df_nested_total.index.duplicated(keep='last')]

                for loop_nested_totals in range(len(row_name) - 2):
                    cross_df_nested_total = pd.concat([cross_df_nested_total], keys=[''], axis=0)

                cross_df_nested_total = pd.concat([cross_df_nested_total], keys=['Total'], axis=0)

                cross_df = pd.concat([cross_df,cross_df_nested_total], axis=0)
            ########## CODE FOR ADDING TOTALS TO ROW PERCENT ################################################

    elif percent_calc == 'actual_count':
        if totals_nested_flag == 1:
            if len(col_name) > 1:
                cross_df_nested_total = totals_nested(df, row_name, col_name, row_list_vals, col_list_vals, percent_calc,
                                                      parameter_calc,
                                                      selected_weight_column, weight_param)

                cross_df_nested_total = cross_df_nested_total.loc[:,
                                        ~cross_df_nested_total.columns.duplicated(keep='last')].copy()
                #

                for loop_nested_totals in range(len(col_name) - 2):
                    cross_df_nested_total = pd.concat([cross_df_nested_total], keys=[''], axis=1)

                cross_df_nested_total = pd.concat([cross_df_nested_total], keys=['Total'], axis=1)

                cross_df = pd.concat([cross_df, cross_df_nested_total], axis=1)

    # cross_#df.to_excel("cross_dfFF.xlsx")
    print("SUBTOTALS ADDED TO TABLE SUCCESSFULLY!")
    # exit('emd!!!')
    # cross_#df.to_excel("cross_df_1112.xlsx")
    # exit("cross_df exit nesteed")
    print("nested_crosstab ends!")
    return cross_df

def subtotals_calc(cross_df,percent_calc,row_name,col_name,cross_df_subtotals_single_dict):

    print("subtotals_calc function Running...")
    # print("===cross_df_subtotals_single_dict===",cross_df_subtotals_single_dict)
    # exit("end code at subtotals!")

    # if percent_calc == 'column_percent' or percent_calc == 'actual_count':
    if percent_calc == 'row_percent':

        print("multi_subtotals FUNCTION Running..")
        #########################################################################################################
        cross_df=multi_subtotals(cross_df,row_name,cross_df_subtotals_single_dict,percent_calc)
        #########################################################################################################

    # if percent_calc == 'column_percent':
    if percent_calc == 'column_percent' or percent_calc == 'actual_count':

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
        print("multi_subtotals two rows")

        df1 = list(cross_df_subtotals_single_dict.values())[0]
        # df1.to_excel("df1_df1_before_transpose.xlsx")
        if percent_calc == 'column_percent' or percent_calc == 'actual_count':
            df1=df1.T
            # pass
        # df1.to_excel("df1_df1_after_transpose.xlsx")
        df1.index=pd.MultiIndex.from_arrays([df1.index.values + '_total', len(df1.index) * ['']])

        # df1.to_excel('df1_subtotals.xlsx')
        # df2.index = pd.MultiIndex.from_arrays([df2.index.values + '_total',len(df2.index) * ['']])

        cross_df = pd.concat([cross_df, df1]).sort_index(level=0)


    if len(row_name)==3:
        print("multi_subtotals three rows")

        df1 = list(cross_df_subtotals_single_dict.values())[1]
        if percent_calc == 'column_percent' or percent_calc == 'actual_count':
            df1 = df1.T

        df1.index = pd.MultiIndex.from_arrays([df1.index.get_level_values(0),
                                               df1.index.get_level_values(1) + '_total',
                                               len(df1.index) * ['']])

        # df2 = cross_df.groupby(level=0).sum()
        df2 = list(cross_df_subtotals_single_dict.values())[0]

        if percent_calc == 'column_percent' or percent_calc == 'actual_count':
            df2 = df2.T

        df2.index = pd.MultiIndex.from_arrays([df2.index.values + '_total',
                                               len(df2.index) * [''],
                                               len(df2.index) * ['']])

        # concat all dataframes together, sort index
        cross_df = pd.concat([cross_df, df1, df2]).sort_index(level=[0,1])
        # cross_df = pd.concat([cross_df, df1, df2]).sort_index()

    if len(row_name)==4:
        print("multi_subtotals four rows")
        # df1 = cross_df.groupby(level=[0, 1, 2]).sum()

        df1 = list(cross_df_subtotals_single_dict.values())[2]
        if percent_calc == 'column_percent' or percent_calc == 'actual_count':
            df1 = df1.T
        df1.index = pd.MultiIndex.from_arrays([df1.index.get_level_values(0),
                                               df1.index.get_level_values(1),
                                               df1.index.get_level_values(2) + '_total',
                                               len(df1.index) * ['']])

        print("multi_subtotals three rows")

        df2 = list(cross_df_subtotals_single_dict.values())[1]
        if percent_calc == 'column_percent' or percent_calc == 'actual_count':
            df2 = df2.T
        # df2 = cross_df.groupby(level=[0, 1]).sum()
        df2.index = pd.MultiIndex.from_arrays([df2.index.get_level_values(0),
                                               df2.index.get_level_values(1) + '_total',
                                               len(df2.index) * [''],
                                               len(df2.index) * ['']])

        # df3 = cross_df.groupby(level=0).sum()

        df3 = list(cross_df_subtotals_single_dict.values())[0]
        if percent_calc == 'column_percent' or percent_calc == 'actual_count':
            df3 = df3.T
        df3.index = pd.MultiIndex.from_arrays([df3.index.values + '_total',
                                               len(df3.index) * [''],
                                               len(df3.index) * [''],
                                               len(df3.index) * ['']])

        # concat all dataframes together, sort index
        cross_df = pd.concat([cross_df, df1, df2, df3]).sort_index(level=[0, 1, 2])

    if len(row_name) == 5:
        print("row_name>>>",row_name)

        # df1 = cross_df.groupby(level=[0, 1, 2, 3]).sum()
        df1 = list(cross_df_subtotals_single_dict.values())[3]
        if percent_calc == 'column_percent' or percent_calc == 'actual_count':
            df1 = df1.T

        df1.index = pd.MultiIndex.from_arrays([df1.index.get_level_values(0),
                                               df1.index.get_level_values(1),
                                               df1.index.get_level_values(2),
                                               df1.index.get_level_values(3) + '_total',
                                               len(df1.index) * ['']])


        # df2 = cross_df.groupby(level=[0, 1, 2]).sum()
        df2 = list(cross_df_subtotals_single_dict.values())[2]
        if percent_calc == 'column_percent' or percent_calc == 'actual_count':
            df2 = df2.T

        df2.index = pd.MultiIndex.from_arrays([df2.index.get_level_values(0),
                                               df2.index.get_level_values(1),
                                               df2.index.get_level_values(2) + '_total',
                                               len(df2.index) * [''],
                                               len(df2.index) * ['']])

        # df3 = cross_df.groupby(level=[0, 1]).sum()

        df3 = list(cross_df_subtotals_single_dict.values())[1]
        if percent_calc == 'column_percent' or percent_calc == 'actual_count':
            df3 = df3.T

        df3.index = pd.MultiIndex.from_arrays([df3.index.get_level_values(0),
                                               df3.index.get_level_values(1) + '_total',
                                               len(df3.index) * [''],
                                               len(df3.index) * [''],
                                               len(df3.index) * ['']])

        # df4 = cross_df.groupby(level=0).sum()

        df4 = list(cross_df_subtotals_single_dict.values())[0]
        if percent_calc == 'column_percent' or percent_calc == 'actual_count':
            df4 = df4.T

        df4.index = pd.MultiIndex.from_arrays([df4.index.values + '_total',
                                               len(df4.index) * [''],
                                               len(df4.index) * [''],
                                               len(df4.index) * [''],
                                               len(df4.index) * ['']])

        # concat all dataframes together, sort index
        cross_df = pd.concat([cross_df, df1, df2, df3, df4]).sort_index(level=[0, 1, 2, 3])

    return cross_df

def subtotals_single_cols(df,percent_calc,row_name,col_name,parameter_calc,col_list_vals,row_list_vals,
                          weight_param,selected_weight_column):
    if percent_calc == 'column_percent' or percent_calc == 'actual_count':
    # if percent_calc == 'column_percent':
        col_name1 = col_name[:-1]

        print('col_name_single_lst initial', col_name1)

        cross_df_subtotals_single_dict = {}
        for loop_col in range(len(col_name1)):

            print("loop_col loop_col", loop_col)
            col_name = col_name1[0:loop_col + 1]
            print("col_name col_name", col_name)

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
                                            weight_param, selected_weight_column)

            if percent_calc == 'actual_count':
                cross_df = crosstab_actual_counts(df, row_name, col_name, row_list_vals, col_list_vals, percent_calc,
                                                  parameter_calc,
                                                  selected_weight_column, weight_param)

            try:
                # pass
                # cross_df = cross_df[cross_df.columns.drop(list(cross_df.filter(regex='Total total')))]
                cross_df = cross_df.loc[:, ~cross_df.columns.str.contains('^Total', case=False)]           #####Line 471 ACTUAL_COMMENT
            except:
                pass

            # if len(col_name) == 1 and percent_calc == 'column_percent':
            # if len(col_name) == 1:
            #     cross_df = cross_df.drop('Total', axis=1)

            cross_df_subtotals_single_dict11 = {str(col_name): cross_df}
            cross_df_subtotals_single_dict.update(cross_df_subtotals_single_dict11)

    if percent_calc == 'row_percent':
        row_name1 = row_name[:-1]

        print('row_name1 initial', row_name1)

        cross_df_subtotals_single_dict = {}
        for loop_col in range(len(row_name1)):

            print("loop_col loop_col", loop_col)
            row_name = row_name1[0:loop_col + 1]
            print("row_name row_name", row_name)

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
                                            weight_param, selected_weight_column)

            if len(row_name) == 1:
                # pass
                # print("cross df index",cross_df.index)
                try:
                    cross_df = cross_df.drop(['Total'], axis='index')
                except:
                    pass
                # cross_df = cross_df.drop('Total', axis=1)

            cross_df_subtotals_single_dict11 = {str(row_name): cross_df}
            cross_df_subtotals_single_dict.update(cross_df_subtotals_single_dict11)

    print("cross_df_subtotals_single_dict keyss", cross_df_subtotals_single_dict.keys())
    # exit("end the cross_df_subtotals_single_dict")
    return cross_df_subtotals_single_dict

def crosstab_basic_table(df,percent_calc,row_name,col_name,parameter_calc,col_list_vals,row_list_vals,
                         weight_param,selected_weight_column):

    print("crosstab_basic_table function started!!")

    if weight_param=='weighted' or weight_param == 'unweighted':
        if len(row_name) == 1 and len(col_name) == 1:

            print(" FIRST CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH EQUAL TO 1!")
            row_name_str = ''.join([str(elem) for elem in row_name])
            col_name_str = ''.join([str(elem) for elem in col_name])

            cross_df = pd.crosstab(index=[df[row_name_str]], columns=[df[col_name_str]],
                                   rownames=[row_name_str],
                                   colnames=[col_name_str], values=df[selected_weight_column], aggfunc=sum,
                                   normalize=parameter_calc, margins=True, margins_name='Total')

            ## BOTH ROWS AND COLUMNS HAVE LENGTH GREATER THAN 1
        elif len(row_name) > 1 and len(col_name) > 1:

            print(" SECOND CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH GREATER THAN 1!")
            cross_df = pd.crosstab(index=row_list_vals, columns=col_list_vals, rownames=row_name,
                                   colnames=col_name,
                                   values=df[selected_weight_column], aggfunc=sum,
                                   normalize=parameter_calc)

            ## IF ROW = 1 AND COLUMNS GREATER THAN 1
        elif len(row_name) == 1 and len(col_name) > 1:
            print("THIRD CONDTION SATISFIED :- IF ROW = 1 AND COLUMNS GREATER THAN 1!")
            row_name_str = ''.join([str(elem) for elem in row_name])

            if percent_calc == 'column_percent' or percent_calc == 'actual_count':
                cross_df = pd.crosstab(index=[df[row_name_str]], columns=col_list_vals, rownames=[row_name_str],
                                       colnames=col_name, values=df[selected_weight_column], aggfunc=sum,
                                       normalize=parameter_calc)

            elif percent_calc == 'row_percent':
                cross_df = pd.crosstab(index=[df[row_name_str]], columns=col_list_vals, rownames=[row_name_str],
                                       colnames=col_name, values=df[selected_weight_column], aggfunc=sum,
                                       normalize=parameter_calc, margins=True, margins_name='Total')

            ## IF ROWS GREATER THAN 1 AND COLUMN = 1
        elif len(row_name) > 1 and len(col_name) == 1:
            print("FOURTH CONDTION SATISFIED :- IF ROWS GREATER THAN 1 AND COLUMN = 1!")
            col_name_str = ''.join([str(elem) for elem in col_name])

            if percent_calc == 'column_percent':
                cross_df = pd.crosstab(index=row_list_vals, columns=[df[col_name_str]], rownames=row_name,
                                       colnames=[col_name_str], values=df[selected_weight_column], aggfunc=sum,
                                       normalize=parameter_calc, margins=True, margins_name='Total')

            elif percent_calc == 'row_percent' or percent_calc == 'actual_count':
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
    print("row_name",row_name)
    print("col_name",col_name)

    # cross_df_11 = cross_df.copy()
    return cross_df

def totals_nested(df,row_name,col_name,row_list_vals,col_list_vals,percent_calc,parameter_calc,
                    selected_weight_column,weight_param):
    if percent_calc == 'column_percent' or percent_calc == 'actual_count':
    # if percent_calc == 'column_percent':
        if len(row_name) == 1:
            print("UNWEIGHTED rowname equal to 1 condition seperated COLUMNS")

            cross_df_list = []
            # for col_loop in col_name:
            col_loop = col_name[-1]
            # print(" FIRST CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH EQUAL TO 1!")
            row_name_str = ''.join([str(elem) for elem in row_name])
            col_name_str = ''.join([str(elem) for elem in col_loop])

            cross_df = pd.crosstab(index=[df[row_name_str]], columns=[df[col_name_str]],
                                   rownames=[row_name_str],
                                   colnames=[col_name_str], values=df[selected_weight_column], aggfunc=sum,
                                   normalize=parameter_calc, margins=True, margins_name='Total')

            # if percent_calc == 'actual_count':
            #     cross_df = cross_df.drop('Total', axis=0)

            # cross_df_list.append(cross_df)

            # cross_df = pd.concat(cross_df_list, axis=1)
            # cross_#df.to_excel("Cross_df_nested_collll_rows.xlsx")

        elif len(row_name) > 1:
            print("UNWEIGHTED colname greater than 1 condition seperated COLUMNS")
            # cross_df_list = []
            # for col_loop in col_name:
            col_loop = col_name[-1]
            col_name_str = ''.join([str(elem) for elem in col_loop])

            if percent_calc == 'column_percent' or percent_calc == 'actual_count':
                cross_df = pd.crosstab(index=row_list_vals, columns=[df[col_name_str]], rownames=row_name,
                                       colnames=[col_name_str], values=df[selected_weight_column], aggfunc=sum,
                                       normalize=parameter_calc, margins=True, margins_name='Total')

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

    if percent_calc == 'row_percent':
        if len(col_name) == 1:
            print("WEIGHTED rowname equal to 1 condition seperated ROWS")

            # cross_df_list = []
            # for row_loop in row_name:
            row_loop = row_name[-1]
            # print(" FIRST CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH EQUAL TO 1!")
            row_name_str = ''.join([str(elem) for elem in row_loop])
            col_name_str = ''.join([str(elem) for elem in col_name])

            cross_df = pd.crosstab(index=[df[row_name_str]], columns=[df[col_name_str]],
                                   rownames=[row_name_str],
                                   colnames=[col_name_str], values=df[selected_weight_column], aggfunc=sum,
                                   normalize=parameter_calc, margins=True, margins_name='Total')
            #
            # if percent_calc == 'actual_count':
            #     cross_df = cross_df / 100

            # cross_df_list.append(cross_df)

            # cross_df = pd.concat(cross_df_list, axis=0)

        elif len(col_name) > 1:
            print("WEIGHTED colname greater than 1 condition seperated ROWS")
            # cross_df_list = []
            # for row_loop in row_name:
            row_loop = row_name[-1]
            row_name_str = ''.join([str(elem) for elem in row_loop])

            if percent_calc == 'column_percent' or percent_calc == 'actual_count':
                cross_df = pd.crosstab(index=[df[row_name_str]], columns=col_list_vals, rownames=[row_name_str],
                                       colnames=col_name, values=df[selected_weight_column], aggfunc=sum,
                                       normalize=parameter_calc, margins=True, margins_name='Total')

            elif percent_calc == 'row_percent':
                cross_df = pd.crosstab(index=[df[row_name_str]], columns=col_list_vals, rownames=[row_name_str],
                                       colnames=col_name, values=df[selected_weight_column], aggfunc=sum,
                                       normalize=parameter_calc, margins=True, margins_name='Total')

            # if percent_calc == 'actual_count':
            #     cross_df = cross_df.drop('Total', axis=0)
            #     cross_df = cross_df / 100

            if percent_calc == 'column_percent':
                cross_df = cross_df.drop('Total', axis=1)

            # cross_df_list.append(cross_df)

            # cross_df = pd.concat(cross_df_list, axis=0)

    cross_df_nested_totals = cross_df.copy()
    # cross_df_nested_totals.to_excel("cross_df_nested_totals.xlsx")
    # exit("endit it!")
    return cross_df_nested_totals


def crosstab_actual_counts(df,row_name,col_name,row_list_vals,col_list_vals,percent_calc,parameter_calc,
                    selected_weight_column,weight_param):

    if weight_param == 'weighted' or weight_param == 'unweighted':

        if len(row_name) == 1 and len(col_name) == 1:

            print(" FIRST CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH EQUAL TO 1!")
            row_name_str = ''.join([str(elem) for elem in row_name])
            col_name_str = ''.join([str(elem) for elem in col_name])

            cross_df = pd.crosstab(index=[df[row_name_str]], columns=[df[col_name_str]],
                                   rownames=[row_name_str],
                                   colnames=[col_name_str],values=df[selected_weight_column], aggfunc=sum,
                                   normalize=parameter_calc, margins=True, margins_name='Total')

        ## BOTH ROWS AND COLUMNS HAVE LENGTH GREATER THAN 1
        if len(row_name) > 1 and len(col_name) > 1:

            print(" SECOND CONDITION SATISFIED :- BOTH ROWS AND COLUMNS HAVE LENGTH GREATER THAN 1!")
            cross_df = pd.crosstab(index=row_list_vals, columns=col_list_vals, rownames=row_name,
                                   colnames=col_name,
                                   values=df[selected_weight_column], aggfunc=sum,
                                   normalize=parameter_calc,margins=True,margins_name='Total')
                                   # normalize=parameter_calc)

            ## IF ROW = 1 AND COLUMNS GREATER THAN 1
        elif len(row_name) == 1 and len(col_name) > 1:
            print("THIRD CONDTION SATISFIED :- IF ROW = 1 AND COLUMNS GREATER THAN 1!")
            row_name_str = ''.join([str(elem) for elem in row_name])

            cross_df = pd.crosstab(index=[df[row_name_str]], columns=col_list_vals, rownames=[row_name_str],
                                   colnames=col_name, values=df[selected_weight_column], aggfunc=sum,
                                   normalize=parameter_calc,margins=True,margins_name='Total')
                                   # normalize=parameter_calc)

            ## IF ROWS GREATER THAN 1 AND COLUMN = 1
        elif len(row_name) > 1 and len(col_name) == 1:
            print("FOURTH CONDTION SATISFIED :- IF ROWS GREATER THAN 1 AND COLUMN = 1!")
            col_name_str = ''.join([str(elem) for elem in col_name])

            cross_df = pd.crosstab(index=row_list_vals, columns=[df[col_name_str]], rownames=row_name,
                                   colnames=[col_name_str], values=df[selected_weight_column], aggfunc=sum,
                                   normalize=parameter_calc,margins=True,margins_name='Total')
                                   # normalize=parameter_calc)

    # cross_df = cross_df.mul(100)
    if percent_calc == 'actual_count' and ((len(row_name) == 1 and len(col_name) > 1) or (len(row_name) > 1 and len(col_name) > 1)):
        cross_df = cross_df.drop('Total',axis=1)
    # cross_#df.to_excel("cross_df_11.xlsx")
    # exit("end at 723")
    cross_df_22 = cross_df.copy()
    return cross_df_22

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################


