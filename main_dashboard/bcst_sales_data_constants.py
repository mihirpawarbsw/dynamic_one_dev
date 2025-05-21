

category_var_name = 'Category'
channel_var_name = 'B&M Channel Split'
brand_var_name = 'Brand'

def renaming_and_reordering(db_type):
    if db_type == 'Multichannel':
        col_dict = {'Market':'1}Market',
        'Group':'2}Group',
        'Brand':'3}Brand',
        'Category':'4}Category',
        'Channel MOB':'5}Channel MOB',
        'B&M Channel Split':'6}B&M Channel Split',
        'EC Channel Split':'7}EC Channel Split',
        'EC Platform Split':'8}EC Platform Split'
        }

        num_dict = {'Sales (M JPY)':'1}Sales (M JPY)',
                    'Sales (M USD)':'2}Sales (M USD)',
                    'Sales (M EUR)':'3}Sales (M EUR)',
                    'Sales (M Local Currency)':'4}Sales (M Local Currency)'
                    }

        final_dict = col_dict  | num_dict
        print('final_dict 637',final_dict)

    return final_dict