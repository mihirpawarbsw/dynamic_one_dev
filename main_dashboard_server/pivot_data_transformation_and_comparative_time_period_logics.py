import time
from django.conf import settings
import polars as pl
import numpy as np
import pandas as pd
from main_dashboard.pivot_time_period_functions import *

# filepath = r"C:\Mihir_Python_Projects\BCST_Tool_Core_Python_Logic\bsw_pivot_tool\Time_period_logics\\"

################## ADDED ON 18-02-2025 ##############################
def data_transformation(data,measure_columns,selected_full_period,comparative_full_period):
    start_time = time.time()

    df = data.copy()
    # df.replace('#','4444',inplace=True)
    df.fillna('Not Available', axis=0, inplace=True)

    ###################### code to subset data  28-03-2024 #######################################
    # numerical_columns_og = list(df.select_dtypes(include='number').columns)
    numerical_columns_og = df.select_dtypes(include='number').columns.to_list()

    numerical_columns_og.remove('Year')

    drop_measure_cols = [x for x in numerical_columns_og if x not in measure_columns]
    print('drop_measure_cols', drop_measure_cols)

    df.drop(drop_measure_cols, axis=1, inplace=True)
    ###################### code to subset data 28-03-2024########################################

    # df['Period_Year'] = df.apply(lambda row: f"{row['Period']} {row['Year']}", axis=1)
    df['Period_Year'] = df['Period'].astype(str) + ' ' + df['Year'].astype(str)
    # print('Period_Year',df['Period_Year'])

    CY = int(selected_full_period[0].split()[-1])
    # latest_period = selected_full_period[0].split()[1]
    selected_time_period = selected_full_period[0].split()[0]

    PY = int(comparative_full_period[0].split()[-1])
    # comparative_period = comparative_full_period[0].split()[1]

    if selected_time_period in ['MAT', 'YTD', 'QUARTER', 'HY']:
        latest_period = selected_full_period[0].split()[1]
        comparative_period = comparative_full_period[0].split()[1]

    selected_full_period_str = '\t'.join(selected_full_period)
    comparative_full_period_str = '\t'.join(comparative_full_period)
    print('selected_full_period_str',selected_full_period_str)
    print('comparative_full_period_str',comparative_full_period_str)

    def get_quarters(period, year):
        """Helper function to generate quarters based on the period and year."""
        if period == 'H1':
            return [f'Q1 {year}', f'Q2 {year}']
        elif period == 'H2':
            return [f'Q3 {year}', f'Q4 {year}']
        elif period == 'FY':
            return [f'Q{i} {year}' for i in range(1, 5)]
        return [f'{period} {year}']

    if 'QUARTER' in selected_full_period_str and 'QUARTER' in comparative_full_period_str:
        CY_qtrs = [f'{latest_period} {CY}']
        PY_qtrs = [f'{comparative_period} {PY}']

    elif 'HY' in selected_full_period_str and 'HY' in comparative_full_period_str:
        CY_qtrs = get_quarters(latest_period, CY)
        PY_qtrs = get_quarters(comparative_period, PY)

    elif 'FY' in selected_full_period_str and 'FY' in comparative_full_period_str:
        CY_qtrs = get_quarters('FY', CY)
        PY_qtrs = get_quarters('FY', PY)

        latest_period = ''
        comparative_period = ''

    elif 'MAT' in selected_full_period_str and 'MAT' in comparative_full_period_str:
        CY_qtrs = get_final_timeperiods_for_mat(latest_period, CY)
        PY_qtrs = get_final_timeperiods_for_mat(comparative_period, PY)

    elif 'YTD' in selected_full_period_str and 'YTD' in comparative_full_period_str:
        CY_qtrs = get_quarters_for_ytd(latest_period)
        PY_qtrs = get_quarters_for_ytd(comparative_period)
        CY_qtrs = [f'{qtr} {CY}' for qtr in CY_qtrs]
        PY_qtrs = [f'{qtr} {PY}' for qtr in PY_qtrs]
    # if (('QUARTER' in selected_full_period_str) and ('QUARTER' in comparative_full_period_str)):
    #     CY_qtrs = latest_period
    #     PY_qtrs = comparative_period

    #     print('CY_qtrs', CY_qtrs)
    #     print('PY_qtrs', PY_qtrs)

    #     cy_ytd_str = ' ' + str(CY)
    #     ya_ytd_str = ' ' + str(PY)

    #     print('cy_ytd_str', cy_ytd_str)
    #     print('ya_ytd_str', ya_ytd_str)

    #     CY_qtrs = [CY_qtrs + cy_ytd_str]
    #     PY_qtrs = [PY_qtrs + ya_ytd_str]

    # elif (('HY' in selected_full_period_str) and ('HY' in comparative_full_period_str)):

    #     if latest_period == 'H1' and comparative_period == 'H1':
    #         CY_qtrs = ['Q1 ' + str(CY),'Q2 ' + str(CY)]
    #         PY_qtrs = ['Q1 ' + str(PY),'Q2 ' + str(PY)]

    #     elif latest_period == 'H1' and comparative_period == 'H2':
    #         CY_qtrs = ['Q1 ' + str(CY),'Q2 ' + str(CY)]
    #         PY_qtrs = ['Q3 ' + str(PY),'Q4 ' + str(PY)]

    #     elif latest_period == 'H2' and comparative_period == 'H1':
    #         CY_qtrs = ['Q3 ' + str(CY),'Q4 ' + str(CY)]
    #         PY_qtrs = ['Q1 ' + str(PY),'Q2 ' + str(PY)]

    #     elif latest_period == 'H2' and comparative_period == 'H2':
    #         CY_qtrs = ['Q3 ' + str(CY),'Q4 ' + str(CY)]
    #         PY_qtrs = ['Q3 ' + str(PY),'Q4 ' + str(PY)]

    # elif (('FY' in selected_full_period_str) and ('FY' in comparative_full_period_str)):
    #     static_qtr_lst = ['Q1','Q2','Q3','Q4']
    #     CY_qtrs = []
    #     PY_qtrs = []

    #     for static_qtr in static_qtr_lst:
    #         cy_str = static_qtr + ' ' + str(CY)
    #         py_str = static_qtr + ' ' + str(PY)

    #         CY_qtrs.append(cy_str)
    #         PY_qtrs.append(py_str)

    #     latest_period = ''
    #     comparative_period = ''

    # elif (('MAT' in selected_full_period_str) and ('MAT' in comparative_full_period_str)):
    #     CY_qtrs = get_final_timeperiods_for_mat(latest_period, CY)
    #     PY_qtrs = get_final_timeperiods_for_mat(comparative_period, PY)

    # elif (('YTD' in selected_full_period_str) and ('YTD' in comparative_full_period_str)):
    #     CY_qtrs = get_quarters_for_ytd(latest_period)
    #     PY_qtrs = get_quarters_for_ytd(comparative_period)

    #     cy_ytd_str = ' ' + str(CY)
    #     ya_ytd_str = ' ' + str(PY)

    #     CY_qtrs = [item + cy_ytd_str for item in CY_qtrs]
    #     PY_qtrs = [item + ya_ytd_str for item in PY_qtrs]

    print('CY_qtrs', CY_qtrs)
    print('PY_qtrs', PY_qtrs)

    mat_cy = selected_time_period + '_CY'
    mat_ya = selected_time_period + '_YA'

    df[mat_cy] = 0
    df[mat_ya] = 0

    # Update the columns based on conditions using vectorized operations
    df.loc[df['Period_Year'].isin(CY_qtrs), mat_cy] = mat_cy
    df.loc[df['Period_Year'].isin(PY_qtrs), mat_ya] = mat_ya

    # df = df.copy()
    df.drop(columns=['Period', 'Year'], inplace=True)

    ############################ OG CODE ################################################
    ############################ OG CODE ################################################
    df_pivot_mat_cy = df[df[mat_cy].isin([mat_cy])]
    df_pivot_mat_ya = df[df[mat_ya].isin([mat_ya])]

    print('df_pivot_mat_cy shape', df_pivot_mat_cy.shape)
    print('df_pivot_mat_cy shape', df_pivot_mat_ya.shape)

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

    # Create a dictionary of aggregation functions for each measure column
    agg_functions = {measure_column: 'mean' for measure_column in measure_columns}

    # Groupby and aggregate using the dynamic code
    df_pivot_final = df_concat_final.groupby(index_columns_new1 + ['Time Period']).agg(agg_functions).unstack()
    df_pivot_final_level = df_pivot_final.copy()

    df_pivot_final.columns = df_pivot_final.columns.get_level_values(0) + '_' + df_pivot_final.columns.get_level_values(
        1)
    ##################### NEW CODE ###################################################
    ##################### NEW CODE ###################################################
    # selected_time_period_str = '_' + selected_time_period
    # print('selected_time_period_str 134', selected_time_period_str)
    # df_pivot_final.columns = df_pivot_final.columns.str.replace(selected_time_period_str, '')
    selected_time_period_str = f"_{selected_time_period}"
    print('selected_time_period_str 134', selected_time_period_str)
    df_pivot_final.columns = df_pivot_final.columns.str.replace(selected_time_period_str, '', regex=False)

    # df_pivot_final = pd.DataFrame(df_pivot_final.reset_index())
    df_pivot_final = df_pivot_final.reset_index()

    # df_pivot_final['Time'] = str(selected_time_period) + ' ' + str(latest_period) + ' ' + str(CY)
    df_pivot_final['Time'] = f"{selected_time_period} {latest_period} {CY}"

    end_time = time.time()
    print('Time taken to transform data is', end_time - start_time, " seconds")

    ############################ FILL VALUES #########################################################
    # categorical_cols = df_pivot_final.select_dtypes(include=['object']).columns
    # numerical_cols = df_pivot_final.select_dtypes(include=['number']).columns

    # # Fill categorical columns with "Not Available"
    # df_pivot_final[categorical_cols] = df_pivot_final[categorical_cols].fillna("Not Available")

    # # Fill numerical columns with 0
    # df_pivot_final[numerical_cols] = df_pivot_final[numerical_cols].fillna(0)
    df_pivot_final = df_pivot_final.apply(
    lambda col: col.fillna("Not Available") if col.dtypes == 'object' else col.fillna(0),axis=0)
    # df_pivot_final.to_excel('df_pivot_final_COMP.xlsx')

    return df_pivot_final,selected_full_period_str,comparative_full_period_str
################## ADDED ON 18-02-2025 ##############################
def data_transformation_OLD_18022025(data,measure_columns,selected_full_period,comparative_full_period):
    start_time = time.time()

    print('measure_columns 12 ',measure_columns)

    #################### SELECTED VALUES ###################################################
    # measure_columns = ['Sales (LC)', 'Sales (M JPY)']
    # selected_full_period = ['MAT Q3 2023']
    # comparative_full_period = ['MAT Q3 2022']
    # static_time_periods = ['QUARTER','MAT','YTD']
    #################### SELECTED VALUES ###################################################

    # data = pd.read_csv(filepath + 'Q3_2023_for_data_upload.csv')
    df = data.copy()
    # df['Year'] = df['Year'].astype(int)
    # df.replace('#','4444',inplace=True)
    df.fillna('Not Available', axis=0, inplace=True)

    ###################### code to subset data  28-03-2024 #######################################
    numerical_columns_og = list(df.select_dtypes(include='number').columns)

    numerical_columns_og.remove('Year')

    drop_measure_cols = [x for x in numerical_columns_og if x not in measure_columns]
    print('drop_measure_cols', drop_measure_cols)

    df.drop(drop_measure_cols, axis=1, inplace=True)
    ###################### code to subset data 28-03-2024########################################

    df['Period_Year'] = df.apply(lambda row: f"{row['Period']} {row['Year']}", axis=1)
    # print('Period_Year',df['Period_Year'])

    CY = int(selected_full_period[0].split()[-1])
    # latest_period = selected_full_period[0].split()[1]
    selected_time_period = selected_full_period[0].split()[0]

    PY = int(comparative_full_period[0].split()[-1])
    # comparative_period = comparative_full_period[0].split()[1]

    if selected_time_period in ['MAT', 'YTD', 'QUARTER', 'HY']:
        latest_period = selected_full_period[0].split()[1]
        comparative_period = comparative_full_period[0].split()[1]

    selected_full_period_str = '\t'.join(selected_full_period)
    comparative_full_period_str = '\t'.join(comparative_full_period)
    print('selected_full_period_str',selected_full_period_str)
    print('comparative_full_period_str',comparative_full_period_str)

    if (('QUARTER' in selected_full_period_str) and ('QUARTER' in comparative_full_period_str)):
        CY_qtrs = latest_period
        PY_qtrs = comparative_period

        print('CY_qtrs', CY_qtrs)
        print('PY_qtrs', PY_qtrs)

        cy_ytd_str = ' ' + str(CY)
        ya_ytd_str = ' ' + str(PY)

        print('cy_ytd_str', cy_ytd_str)
        print('ya_ytd_str', ya_ytd_str)

        CY_qtrs = [CY_qtrs + cy_ytd_str]
        PY_qtrs = [PY_qtrs + ya_ytd_str]

    elif (('HY' in selected_full_period_str) and ('HY' in comparative_full_period_str)):

        if latest_period == 'H1' and comparative_period == 'H1':
            CY_qtrs = ['Q1 ' + str(CY),'Q2 ' + str(CY)]
            PY_qtrs = ['Q1 ' + str(PY),'Q2 ' + str(PY)]

        elif latest_period == 'H1' and comparative_period == 'H2':
            CY_qtrs = ['Q1 ' + str(CY),'Q2 ' + str(CY)]
            PY_qtrs = ['Q3 ' + str(PY),'Q4 ' + str(PY)]

        elif latest_period == 'H2' and comparative_period == 'H1':
            CY_qtrs = ['Q3 ' + str(CY),'Q4 ' + str(CY)]
            PY_qtrs = ['Q1 ' + str(PY),'Q2 ' + str(PY)]

        elif latest_period == 'H2' and comparative_period == 'H2':
            CY_qtrs = ['Q3 ' + str(CY),'Q4 ' + str(CY)]
            PY_qtrs = ['Q3 ' + str(PY),'Q4 ' + str(PY)]

    elif (('FY' in selected_full_period_str) and ('FY' in comparative_full_period_str)):
        static_qtr_lst = ['Q1','Q2','Q3','Q4']
        CY_qtrs = []
        PY_qtrs = []

        for static_qtr in static_qtr_lst:
            cy_str = static_qtr + ' ' + str(CY)
            py_str = static_qtr + ' ' + str(PY)

            CY_qtrs.append(cy_str)
            PY_qtrs.append(py_str)

        latest_period = ''
        comparative_period = ''

    elif (('MAT' in selected_full_period_str) and ('MAT' in comparative_full_period_str)):
        CY_qtrs = get_final_timeperiods_for_mat(latest_period, CY)
        PY_qtrs = get_final_timeperiods_for_mat(comparative_period, PY)

    elif (('YTD' in selected_full_period_str) and ('YTD' in comparative_full_period_str)):
        CY_qtrs = get_quarters_for_ytd(latest_period)
        PY_qtrs = get_quarters_for_ytd(comparative_period)

        cy_ytd_str = ' ' + str(CY)
        ya_ytd_str = ' ' + str(PY)

        CY_qtrs = [item + cy_ytd_str for item in CY_qtrs]
        PY_qtrs = [item + ya_ytd_str for item in PY_qtrs]

    print('CY_qtrs', CY_qtrs)
    print('PY_qtrs', PY_qtrs)

    mat_cy = selected_time_period + '_CY'
    mat_ya = selected_time_period + '_YA'

    df[mat_cy] = df['Period_Year'].apply(lambda x: mat_cy if x in CY_qtrs else 0)
    df[mat_ya] = df['Period_Year'].apply(lambda x: mat_ya if x in PY_qtrs else 0)

    # df = df.copy()
    df.drop(columns=['Period', 'Year'], inplace=True)

    ############################ OG CODE ################################################
    ############################ OG CODE ################################################
    df_pivot_mat_cy = df[df[mat_cy].isin([mat_cy])]
    df_pivot_mat_ya = df[df[mat_ya].isin([mat_ya])]

    print('df_pivot_mat_cy shape', df_pivot_mat_cy.shape)
    print('df_pivot_mat_cy shape', df_pivot_mat_ya.shape)

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

    # df_pivot_final = pd.pivot_table(df_concat_final, values=measure_columns, index=index_columns_new1,columns = ['Time Period'])
    # Create a dictionary of aggregation functions for each measure column
    agg_functions = {measure_column: 'mean' for measure_column in measure_columns}

    # Groupby and aggregate using the dynamic code
    df_pivot_final = df_concat_final.groupby(index_columns_new1 + ['Time Period']).agg(agg_functions).unstack()
    df_pivot_final_level = df_pivot_final.copy()

    df_pivot_final.columns = df_pivot_final.columns.get_level_values(0) + '_' + df_pivot_final.columns.get_level_values(
        1)
    ######################### OG CODE #################################################
    ######################### OG CODE #################################################

    ##################### NEW CODE ###################################################
    ##################### NEW CODE ###################################################
    # # Filter the DataFrame based on specific criteria
    # df_pivot_mat_cy = df[df[mat_cy] == mat_cy]
    # df_pivot_mat_ya = df[df[mat_ya] == mat_ya]

    # print('df_pivot_mat_cy shape:', df_pivot_mat_cy.shape)
    # print('df_pivot_mat_ya shape:', df_pivot_mat_ya.shape)

    # # Identify index columns while excluding measure columns
    # index_columns = [col for col in df.columns if col not in measure_columns]
    # to_remove_lst1 = ['Period_Year', mat_cy, mat_ya]
    # index_columns_new1 = [col for col in index_columns if col not in to_remove_lst1]

    # # Groupby and aggregate for mat_cy
    # df_pivot_cy = df_pivot_mat_cy.groupby(index_columns_new1)[measure_columns].sum().reset_index()
    # df_pivot_cy['Time Period'] = mat_cy
    # # df_pivot_cy.to_excel('df_pivot_cy.xlsx')

    # # Groupby and aggregate for mat_ya
    # df_pivot_ya = df_pivot_mat_ya.groupby(index_columns_new1)[measure_columns].sum().reset_index()
    # df_pivot_ya['Time Period'] = mat_ya
    # # df_pivot_ya.to_excel('df_pivot_ya.xlsx')

    # # Concatenate the two DataFrames
    # df_concat_final = pd.concat([df_pivot_cy, df_pivot_ya], axis=0)
    # # df_concat_final.to_excel('df_concat_final.xlsx')

    # # Create a dictionary of aggregation functions for each measure column
    # agg_functions = {measure_column: 'mean' for measure_column in measure_columns}

    # # Groupby and aggregate using the dynamic code
    # df_pivot_final = df_concat_final.groupby(index_columns_new1 + ['Time Period']).agg(agg_functions).unstack()

    # # Reshape the DataFrame
    # df_pivot_final.columns = df_pivot_final.columns.get_level_values(0) + '_' + df_pivot_final.columns.get_level_values(1)
    # # df_pivot_final.to_excel('df_pivot_final11.xlsx')

    # # Optional: Reset index if needed
    # # df_pivot_final = df_pivot_final.reset_index()

    ##################### NEW CODE ###################################################
    ##################### NEW CODE ###################################################
    selected_time_period_str = '_' + selected_time_period
    print('selected_time_period_str 134', selected_time_period_str)
    df_pivot_final.columns = df_pivot_final.columns.str.replace(selected_time_period_str, '')

    df_pivot_final = pd.DataFrame(df_pivot_final.reset_index())

    df_pivot_final['Time'] = str(selected_time_period) + ' ' + str(latest_period) + ' ' + str(CY)

    end_time = time.time()
    print('Time taken to transform data is', end_time - start_time, " seconds")

    ############################ FILL VALUES #########################################################
    categorical_cols = df_pivot_final.select_dtypes(include=['object']).columns
    numerical_cols = df_pivot_final.select_dtypes(include=['number']).columns

    # Fill categorical columns with "Not Available"
    df_pivot_final[categorical_cols] = df_pivot_final[categorical_cols].fillna("Not Available")

    # Fill numerical columns with 0
    df_pivot_final[numerical_cols] = df_pivot_final[numerical_cols].fillna(0)

    # df_pivot_final.to_excel('df_pivot_final_COMP.xlsx')

    return df_pivot_final,selected_full_period_str,comparative_full_period_str
    ############################ FILL VALUES #########################################################

def data_transformation_doors(filename,measure_columns,selected_full_period,comparative_full_period,seperator_param):
    start_time = time.time()
    print('measure_columns 12 ',measure_columns)
    #################### SELECTED VALUES ###################################################
    # measure_columns = ['Sales (LC)', 'Sales (M JPY)']
    # selected_full_period = ['MAT Q3 2023']
    # comparative_full_period = ['MAT Q3 2022']
    # static_time_periods = ['QUARTER','MAT','YTD']
    #################### SELECTED VALUES ###################################################
    transformed_data_lst = []
    for measure_columns_loop in measure_columns:
        data = pd.read_csv(settings.TEMP_UPLOAD + filename)
        # data = pd.read_csv(filepath + 'Q3_2023_for_data_upload.csv')


        ##################### NEW LOGIC TO CONVERT MILLIONS TO THOUSANDS #############################
        if (seperator_param == "thousands"):
            data.rename(columns={col: col.replace('Sales (M', 'Sales (K') for col in data.columns}, inplace=True)

            sales_columns = [col for col in measure_columns if 'Sales' in col]

            for loop_col in sales_columns:
                data[loop_col] = data[loop_col] * 1000
        ##################### NEW LOGIC TO CONVERT MILLIONS TO THOUSANDS #############################

        df = data.copy()
        # df.replace('#','4444',inplace=True)
        df.fillna('Not Available', axis=0, inplace=True)

        ###################### code to subset data  28-03-2024 #######################################
        numerical_columns_og = list(df.select_dtypes(include='number').columns)

        numerical_columns_og.remove('Year')

        drop_measure_cols = [x for x in numerical_columns_og if x not in measure_columns]
        print('drop_measure_cols', drop_measure_cols)

        df.drop(drop_measure_cols, axis=1, inplace=True)

        final_measure_loop = [x for x in measure_columns if x not in measure_columns_loop]
        df.drop(final_measure_loop, axis=1, inplace=True)

        ###################### code to subset data 28-03-2024########################################

        df['Period_Year'] = df.apply(lambda row: f"{row['Period']} {row['Year']}", axis=1)
        # print('Period_Year',df['Period_Year'])

        CY = int(selected_full_period[0].split()[-1])
        # latest_period = selected_full_period[0].split()[1]
        selected_time_period = selected_full_period[0].split()[0]

        PY = int(comparative_full_period[0].split()[-1])
        # comparative_period = comparative_full_period[0].split()[1]

        if selected_time_period in ['MAT', 'YTD', 'QUARTER', 'HY']:
            latest_period = selected_full_period[0].split()[1]
            comparative_period = comparative_full_period[0].split()[1]

        selected_full_period_str = '\t'.join(selected_full_period)
        comparative_full_period_str = '\t'.join(comparative_full_period)
        print('selected_full_period_str',selected_full_period_str)
        print('comparative_full_period_str',comparative_full_period_str)

        if (('QUARTER' in selected_full_period_str) and ('QUARTER' in comparative_full_period_str)):
            CY_qtrs = latest_period
            PY_qtrs = comparative_period

            print('CY_qtrs', CY_qtrs)
            print('PY_qtrs', PY_qtrs)

            cy_ytd_str = ' ' + str(CY)
            ya_ytd_str = ' ' + str(PY)

            print('cy_ytd_str', cy_ytd_str)
            print('ya_ytd_str', ya_ytd_str)

            CY_qtrs = [CY_qtrs + cy_ytd_str]
            PY_qtrs = [PY_qtrs + ya_ytd_str]

        elif (('HY' in selected_full_period_str) and ('HY' in comparative_full_period_str)):

            if latest_period == 'H1' and comparative_period == 'H1':
                CY_qtrs = ['Q1 ' + str(CY),'Q2 ' + str(CY)]
                PY_qtrs = ['Q1 ' + str(PY),'Q2 ' + str(PY)]

            elif latest_period == 'H1' and comparative_period == 'H2':
                CY_qtrs = ['Q1 ' + str(CY),'Q2 ' + str(CY)]
                PY_qtrs = ['Q3 ' + str(PY),'Q4 ' + str(PY)]

            elif latest_period == 'H2' and comparative_period == 'H1':
                CY_qtrs = ['Q3 ' + str(CY),'Q4 ' + str(CY)]
                PY_qtrs = ['Q1 ' + str(PY),'Q2 ' + str(PY)]

            elif latest_period == 'H2' and comparative_period == 'H2':
                CY_qtrs = ['Q3 ' + str(CY),'Q4 ' + str(CY)]
                PY_qtrs = ['Q3 ' + str(PY),'Q4 ' + str(PY)]

        elif (('FY' in selected_full_period_str) and ('FY' in comparative_full_period_str)):
            static_qtr_lst = ['Q1','Q2','Q3','Q4']
            CY_qtrs = []
            PY_qtrs = []

            for static_qtr in static_qtr_lst:
                cy_str = static_qtr + ' ' + str(CY)
                py_str = static_qtr + ' ' + str(PY)

                CY_qtrs.append(cy_str)
                PY_qtrs.append(py_str)

            latest_period = ''
            comparative_period = ''

        elif (('MAT' in selected_full_period_str) and ('MAT' in comparative_full_period_str)):
            CY_qtrs = get_final_timeperiods_for_mat(latest_period, CY)
            PY_qtrs = get_final_timeperiods_for_mat(comparative_period, PY)

        elif (('YTD' in selected_full_period_str) and ('YTD' in comparative_full_period_str)):
            CY_qtrs = get_quarters_for_ytd(latest_period)
            PY_qtrs = get_quarters_for_ytd(comparative_period)

            cy_ytd_str = ' ' + str(CY)
            ya_ytd_str = ' ' + str(PY)

            CY_qtrs = [item + cy_ytd_str for item in CY_qtrs]
            PY_qtrs = [item + ya_ytd_str for item in PY_qtrs]

        if measure_columns_loop == 'Door':
            CY_qtrs = [CY_qtrs[-1]]
            PY_qtrs = [PY_qtrs[-1]]

            selected_time_period = 'QUARTER'

            print('doorrss cy',CY_qtrs)
            print('doorrss py',PY_qtrs)

        print('CY_qtrs', CY_qtrs)
        print('PY_qtrs', PY_qtrs)

        mat_cy = selected_time_period + '_CY'
        mat_ya = selected_time_period + '_YA'

        df[mat_cy] = df['Period_Year'].apply(lambda x: mat_cy if x in CY_qtrs else 0)
        df[mat_ya] = df['Period_Year'].apply(lambda x: mat_ya if x in PY_qtrs else 0)

        # df = df.copy()
        df.drop(columns=['Period', 'Year'], inplace=True)
        # df.to_excel('df_dropped.xlsx')
        df_pivot_mat_cy = df[df[mat_cy].isin([mat_cy])]
        df_pivot_mat_ya = df[df[mat_ya].isin([mat_ya])]

        print('df_pivot_mat_cy shape', df_pivot_mat_cy.shape)
        print('df_pivot_mat_cy shape', df_pivot_mat_ya.shape)

        index_columns = [col for col in df.columns if col not in measure_columns_loop]
        to_remove_lst1 = ['Period_Year', mat_cy, mat_ya]
        index_columns_new1 = [col for col in index_columns if col not in to_remove_lst1]
        # index_columns_new1 = ['Country']

        df_pivot_cy = df_pivot_mat_cy.groupby(index_columns_new1)[measure_columns_loop].sum()
        df_pivot_cy = df_pivot_cy.reset_index()
        df_pivot_cy['Time Period'] = mat_cy
        # df_pivot_cy.to_excel('df_pivot_cy.xlsx')

        df_pivot_ya = df_pivot_mat_ya.groupby(index_columns_new1)[measure_columns_loop].sum()
        df_pivot_ya = df_pivot_ya.reset_index()
        df_pivot_ya['Time Period'] = mat_ya
        # df_pivot_ya.to_excel('df_pivot_ya.xlsx')

        df_concat_final = pd.concat([df_pivot_cy, df_pivot_ya], axis=0)
        # df_concat_final = df_concat_final.reset_index()
        # df_concat_final.to_excel('df_concat_final.xlsx')

        # df_pivot_final = pd.pivot_table(df_concat_final, values=measure_columns_loop, index=index_columns_new1,columns = ['Time Period'])
        # Create a dictionary of aggregation functions for each measure column
        agg_functions = {measure_column: 'mean' for measure_column in [measure_columns_loop]}

        # Groupby and aggregate using the dynamic code
        df_pivot_final = df_concat_final.groupby(index_columns_new1 + ['Time Period']).agg(agg_functions).unstack()
        df_pivot_final_level = df_pivot_final.copy()
        # df_pivot_final_level.to_excel(filepath + 'DF_PIVOT_FINAL22.xlsx')

        df_pivot_final.columns = df_pivot_final.columns.get_level_values(0) + '_' + df_pivot_final.columns.get_level_values(
            1)
        selected_time_period_str = '_' + selected_time_period
        print('selected_time_period_str 134', selected_time_period_str)
        df_pivot_final.columns = df_pivot_final.columns.str.replace(selected_time_period_str, '')

        df_pivot_final = pd.DataFrame(df_pivot_final.reset_index())

        df_pivot_final['Time'] = str(selected_time_period) + ' ' + str(latest_period) + ' ' + str(CY)

        ############################ FILL VALUES #########################################################
        categorical_cols = df_pivot_final.select_dtypes(include=['object']).columns
        numerical_cols = df_pivot_final.select_dtypes(include=['number']).columns

        # Fill categorical columns with "Not Available"
        df_pivot_final[categorical_cols] = df_pivot_final[categorical_cols].fillna("Not Available")

        # Fill numerical columns with 0
        df_pivot_final[numerical_cols] = df_pivot_final[numerical_cols].fillna(0)

        df_pivot_final.set_index(list(categorical_cols),inplace=True)
        transformed_data_lst.append(df_pivot_final)
        # df_pivot_final.to_excel('df_pivot_final_COMP.xlsx')

    transformed_data = pd.concat(transformed_data_lst,axis=1)
    transformed_data.reset_index(inplace=True)

    end_time = time.time()
    print('Time taken to transform data is', end_time - start_time, " seconds")

    return transformed_data,selected_full_period_str,comparative_full_period_str
    ############################ FILL VALUES #########################################################