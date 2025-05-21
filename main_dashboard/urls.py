from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [

    # path('',views.main_dashboard),
    path('main_dashboard/',views.dashboard),
    path('crosstab_dash/',views.crosstab_dash),
    path('upload_data',views.upload_data),
    path('display_all_data',views.display_all_data),
    path('display_all_data1',views.display_all_data1),
    path('column_dtypes',views.column_dtypes),
    path('column_data_display',views.column_data_display),
    path('crosstab_table',views.crosstab_table),
    path('crosstab_table_page2',views.crosstab_table_page2),
    path('test_page',views.test_page),
    path('drag_and_drop',views.drag_and_drop),
    path('main_dashboard_db',views.main_dashboard_db_page),
    path('get_electrolux_india_column',views.get_electrolux_india_column),
    # path('main_dashboard_lazyload1',views.main_dashboard_lazyload1),
    path('table_sample_data',views.table_sample_data),
    path('crosstab_v1',views.crosstab_ui_v1),
    path('bar_chart',views.bar_chart),
    path('significance_fn_resp',views.significance_fn_resp),
    path('upload_chunk/', views.upload_chunk, name='upload_chunk'),
    path('store_questionnaire_format', views.store_questionnaire_format, name='store_questionnaire_format'),
    path('current_time_period_resp',views.current_time_period_resp),
    path('comparative_time_period_resp',views.comparative_time_period_resp),
    path('Add_to_favourite',views.Add_to_favourite),
    path('Show_Add_to_favourite_list',views.Show_Add_to_favourite_list),
    path('Delete_recently_added_view',views.Delete_recently_added_view),
    path('display_user_history_view',views.display_user_history_view),
    path('verify_user_history_exit',views.verify_user_history_exit),
    path('upload_chunk_2/',views.upload_chunk_2, name='upload_chunk_2'),
    path('Show_dataupload_list_table',views.Show_dataupload_list_table, name='Show_dataupload_list_table'),
    path('marketwise_latest_quarter',views.marketwise_latest_quarter, name='marketwise_latest_quarter'),
	path('metrics_filter_call',views.metrics_filter_call, name='metrics_filter_call')
]