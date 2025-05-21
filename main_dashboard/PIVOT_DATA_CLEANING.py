import json

import numpy as np
import pandas as pd
from main_dashboard.pivot_time_period_functions import *
from django.conf import settings
# filepath = r"C:\Mihir_Python_Projects\BCST_Tool_Core_Python_Logic\bsw_pivot_tool\Time_period_logics\\"

################################### NEW CODE -28-03-2024 #####################
def clean_create_data_V2(filename,periodical_type,que_year,que_period,que_numerical_list):
    Year = que_year
    Period = que_period
    selected_time_period_all_list = ['YTD','MAT','QTR']
    # selected_time_period_all_list = ['L3M']
    measure_columns = que_numerical_list

    pivot_data_lst = []
    for selected_time_period in selected_time_period_all_list:

        data = pd.read_excel(settings.TEMP_UPLOAD + filename)
        df = data.copy()
        # df.replace('#','4444',inplace=True)
        df.fillna('Not Available',axis=0,inplace=True)

        ###################### code to subset data  28-03-2024 #######################################
        numerical_columns_og = list(df.select_dtypes(include='number').columns)
        numerical_columns_og.remove('Year')

        drop_measure_cols = [x for x in numerical_columns_og if x not in measure_columns]
        print('drop_measure_cols', drop_measure_cols)

        df.drop(drop_measure_cols, axis=1, inplace=True)
        ###################### code to subset data 28-03-2024########################################

        df['Period_Year'] = df.apply(lambda row: f"{row[Period]} {row[Year]}", axis=1)
        # print('Period_Year',df['Period_Year'])

        ######################### MAT CALCULATIONS #########################################################
        CY = df[Year].max()
        max_year_df = df[df[Year] == CY]
        latest_period = max_year_df[Period].max()

        print('CY', CY)
        print('latest_period', latest_period)

        PY = CY - 1
        YA_period = latest_period

        print('SELECTED TIME PERIOD-',selected_time_period)

        if selected_time_period == 'MAT':
            CY_qtrs = get_final_timeperiods_for_mat(latest_period,CY)
            PY_qtrs = get_final_timeperiods_for_mat(YA_period, PY)

        elif selected_time_period == 'YTD':
            CY_qtrs = get_quarters_for_ytd(latest_period)
            PY_qtrs = get_quarters_for_ytd(latest_period)

            cy_ytd_str = ' '+str(CY)
            ya_ytd_str = ' '+str(PY)

            CY_qtrs = [item + cy_ytd_str  for item in CY_qtrs]
            PY_qtrs = [item + ya_ytd_str  for item in PY_qtrs]

        elif selected_time_period == 'QTR':
            CY_qtrs = latest_period
            PY_qtrs = latest_period

            print('CY_qtrs',CY_qtrs)
            print('PY_qtrs',PY_qtrs)

            cy_ytd_str = ' ' + str(CY)
            ya_ytd_str = ' ' + str(PY)

            print('cy_ytd_str', cy_ytd_str)
            print('ya_ytd_str', ya_ytd_str)

            CY_qtrs = [CY_qtrs + cy_ytd_str]
            PY_qtrs = [PY_qtrs + ya_ytd_str]
        print('CY_qtrs', CY_qtrs)
        print('PY_qtrs',PY_qtrs)

        mat_cy = selected_time_period+'_CY'
        mat_ya = selected_time_period+'_YA'

        df[mat_cy] = df['Period_Year'].apply(lambda x: mat_cy if x in CY_qtrs else 0)
        df[mat_ya] = df['Period_Year'].apply(lambda x: mat_ya if x in PY_qtrs else 0)

        # df = df.copy()
        df.drop(columns=[Period,Year],inplace=True)
        # df.to_excel('df_dropped.xlsx')
        df_pivot_mat_cy = df[df[mat_cy].isin([mat_cy])]
        df_pivot_mat_ya = df[df[mat_ya].isin([mat_ya])]

        print('df_pivot_mat_cy shape',df_pivot_mat_cy.shape)
        print('df_pivot_mat_cy shape',df_pivot_mat_ya.shape)

        index_columns = [col for col in df.columns if col not in measure_columns]
        to_remove_lst1 = ['Period_Year', mat_cy, mat_ya]
        index_columns_new1 = [col for col in index_columns if col not in to_remove_lst1]
        # index_columns_new1 = ['Country']

        df_pivot_cy = df_pivot_mat_cy.groupby(index_columns_new1)[measure_columns].sum()
        df_pivot_cy = df_pivot_cy.reset_index()
        df_pivot_cy['Time Period'] = mat_cy
        # df_pivot_cy.to_excel('df_pivot_cy.xlsx')

        df_pivot_ya = df_pivot_mat_ya.groupby(index_columns_new1)[measure_columns].sum()
        df_pivot_ya = df_pivot_ya.reset_index()
        df_pivot_ya['Time Period'] = mat_ya
        # df_pivot_ya.to_excel('df_pivot_ya.xlsx')

        df_concat_final = pd.concat([df_pivot_cy, df_pivot_ya], axis=0)
        # df_concat_final = df_concat_final.reset_index()
        # df_concat_final.to_excel('df_concat_final.xlsx')

        # df_pivot_final = pd.pivot_table(df_concat_final, values=measure_columns, index=index_columns_new1,columns = ['Time Period'])
        # Create a dictionary of aggregation functions for each measure column
        agg_functions = {measure_column: 'mean' for measure_column in measure_columns}

        # Groupby and aggregate using the dynamic code
        df_pivot_final = df_concat_final.groupby(index_columns_new1 + ['Time Period']).agg(agg_functions).unstack()
        df_pivot_final_level = df_pivot_final.copy()
        # df_pivot_final_level.to_excel(filepath + 'DF_PIVOT_FINAL22.xlsx')

        df_pivot_final.columns = df_pivot_final.columns.get_level_values(0) + '_' + df_pivot_final.columns.get_level_values(1)
        selected_time_period_str = '_' + selected_time_period
        df_pivot_final.columns = df_pivot_final.columns.str.replace(selected_time_period_str, '')

        df_pivot_final = pd.DataFrame(df_pivot_final.reset_index())
        # df_pivot_final['Time'] = selected_time_period
        if selected_time_period == 'QTR':
            df_pivot_final['Time'] = str(latest_period) + '_' + str(CY)
        else:
            df_pivot_final['Time'] = str(selected_time_period) + '_' + str(latest_period) + '_' + str(CY)
        # df_pivot_final.to_excel(filepath + 'DF_PIVOT_FINAL.xlsx')

        pivot_data_lst.append(df_pivot_final)

    final_converted_data = pd.concat(pivot_data_lst,axis=0)

    ###################### code to subset data  28-03-2024 #######################################
    # numerical_columns_og = list(data.select_dtypes(include='number').columns)
    # numerical_columns_og.remove('Year')

    # drop_measure_cols = [x for x in numerical_columns_og if x not in measure_columns]
    # print('drop_measure_cols',drop_measure_cols)

    # final_converted_data.drop(drop_measure_cols,axis=1,inplace=True)
    # ###################### code to subset data 28-03-2024########################################

    numerical_columns = final_converted_data.select_dtypes(include='number').columns
    cat_columns = final_converted_data.select_dtypes(include='object').columns

    cat_columns_dict = {column: [column] for column in cat_columns}

    num_result_dict = {}

    for item in numerical_columns:
        key = item.split('_')[0]  # Extract the key by splitting at '_'
        print('142key',key)
        if key not in num_result_dict:
            num_result_dict[key] = [item]
        else:
            num_result_dict[key].append(item)

    print('num_result_dict==148',num_result_dict)
    final_col_dict = cat_columns_dict.copy()
    final_col_dict.update(num_result_dict)
    print("Resulting Dictionary:")
    print(final_col_dict)

    lst_var = list(final_col_dict.keys())
    lst_codeframe = list(final_col_dict.values())
    counts_list = [len(sublist) for sublist in lst_codeframe]

    # Create a DataFrame from the three lists
    colname_df = pd.DataFrame({'Variable': lst_var, 'Codeframe': lst_codeframe, 'Count': counts_list})
    
    # converted_filename = 'output_file.xlsx'
    converted_filename = filename

    # Save DataFrames to different sheets
    with pd.ExcelWriter(settings.PYTHONPATH + converted_filename, engine='xlsxwriter') as writer:
        final_converted_data.to_excel(writer, sheet_name='Data', index=False)
        colname_df.to_excel(writer, sheet_name='Codeframe', index=False)
################################### NEW CODE -28-03-2024 #####################

#################################################################################################################
#################################################################################################################
#################################################################################################################
#################################################################################################################
def clean_create_data():
    df = pd.read_csv(filepath + 'Q3_2023_for_data_upload.csv')

    print('df cols',df.columns)
    print('headd',df[['Year','Period']].head(10))

    current_yr = df['Year'].max()

    # df['Year_Period'] = df['Year'].astype(str) + " " + df['Period']
    df['Year_Period'] = df.apply(lambda row: f"{row['Year']} {row['Period']}", axis=1)

    yr_period_lst = df['Year_Period'].unique().tolist()
    period_lst = df['Period'].unique().tolist()
    yr_lst = df['Year'].unique().tolist()
    print('current_yr',current_yr)
    print('yr_period_lst',yr_period_lst)
    print('period_lst',period_lst)
    print('yr_lst',yr_lst)

    ############################### CODDE FOR CURRENT YEAR #####################################################
    # df = df[df['Year'] == current_yr]
    yr_period_MAT = yr_period_lst[-4:]
    print('yr_period_MAT',yr_period_MAT)
    df_MAT = df[df['Year_Period'].isin(yr_period_MAT)]
    # df_MAT.to_excel('df_MAT.xlsx')
    # exit('df_MAT')
    ############################### CODDE FOR CURRENT YEAR #####################################################

    df_groupby_MAT = pd.DataFrame(df_MAT.groupby(['Country', 'Data source', 'Brand', "Brands' owner",
           'Category', 'Channel', 'e-platform','Channel (High Level)','Year','Period','Year_Period'])[['Sales (LC)','Sales (M JPY)',
                                                                         'Sales(EuroM)', 'Sales(USD M)']].sum())
    # previous_yr = current_yr - 1
    #
    # lst_yr = [previous_yr,current_yr]
    # # exit('previous_yr')
    # # lst_yr = df['Year'].unique().tolist()
    #
    # measure = ['Sales (LC)']
    #
    # df = df[df['Year'].isin(lst_yr)]
    # df_new = pd.pivot_table(df, values=measure,
    #                                 index=['Country', 'Period', 'Data source', 'Brand', "Brands' owner",
    #        'Category', 'Channel', 'e-platform','Channel (High Level)'],
    #                                 columns=["Year"], aggfunc=np.sum)
    #
    # df_new = df_new.droplevel(0, axis=1)
    # df_new.to_excel('df_new11.xlsx')

    # def yoy_growth(x, y):
    #     return (((y / x) - 1) * 100)
    #
    #
    # for i in range(0, len(lst_yr) - 1):
    #     print('iiii======',i)
    #     # df_new = df_new.loc[:, df_new.columns.get_level_values(1).isin(list(lst_yr))]
    #     df_new["Growth %"] = yoy_growth(df_new[lst_yr[i]], df_new[lst_yr[i + 1]])

    # df_groupby_MAT.to_excel('df_groupby_MAT.xlsx')
# clean_create_data()


