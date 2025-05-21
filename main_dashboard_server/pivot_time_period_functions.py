################################################################################################################
################################################################################################################
################################################################################################################
def get_quarters_for_ytd(timeperiod):
    timeperiod_lower = timeperiod.lower()

    if timeperiod_lower == 'q1':
        qtrs = ['Q1']
    elif timeperiod_lower == 'q2':
        qtrs = ['Q1', 'Q2']
    elif timeperiod_lower == 'q3':
        qtrs = ['Q1', 'Q2', 'Q3']
    elif timeperiod_lower == 'q4':
        qtrs = ['Q1', 'Q2', 'Q3', 'Q4']

    return qtrs


def get_final_timeperiods_for_mat(cur_qtr, year):
    qtrs = ['Q1', 'Q2', 'Q3', 'Q4']
    i = 1
    mat_qtrs = [f'{cur_qtr} {year}']

    while i < 4:
        if i == 1:
            pre_qtr = cur_qtr
        else:
            pre_qtr = pre_qtr

        key = qtrs.index(pre_qtr)

        if key == 0:
            pre_qtr = qtrs[-1]
            year = year - 1
        else:
            pre_qtr = get_prev_value(key, qtrs)

        mat_qtrs.append(f'{pre_qtr} {year}')
        i += 1

    return mat_qtrs


def get_prev_value(key, array):
    keys = list(range(len(array)))
    found_index = keys.index(key)

    if found_index is False or found_index == 0:
        return False

    return array[keys[found_index - 1]]

################################################################################################################
################################################################################################################
################################################################################################################