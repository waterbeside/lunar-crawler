import json
from operator import setitem
import os

def extract_data(year):
    '''
    提取数据
    '''
    # print(os.path.abspath('.'))
    # print(os.getcwd())
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'json', '{}.json'.format(year))
    # print('extract', year)
    f = open(p, 'r', encoding='utf-8')
    data = json.load(f)
    f.close()

    big_month_list = hex(data['big_month_list'])
    solar_term_date_list = data['solar_term_date_list']
    # print(big_month_list)
    # print(solar_term_date_list)
    return {
        'lunar_month_datas': big_month_list,
        'solar_term_date_list': solar_term_date_list,
        'lunar_new_year_date': data['lunar_new_year_date']
    }

def set_item_to_js_str(s, item, item_type, year, divisor = 10):
    if s != '':
        s += ','
    if item_type == 'str':
        s += "'" + item + "'"
    else:
        s += str(item)

    if (year - 1900) % divisor == 0:
        sp = ''
        if  year != 2100:
            sp = '\n  ' 
        s += sp
    return s

def js_str(var_name, data_str, is_array=False, no_n = False):
    n = '\n' if not no_n else ''
    if is_array:
        return 'const {} = [{}{}{}]\n\n'.format(var_name, '\n  ' if not no_n else '', data_str, n)
    return 'const {} = {}\n\n'.format(var_name, data_str)

def get_trem_minimum_dates(term_dates_yearlist):
    '''
    获取节气最小日期列表
    '''
    trem_minimum_date_list = []
    for i in range(0, 24):
        mini = term_dates_yearlist[0][i]
        for j in range(1, len(term_dates_yearlist)):
          mini = min(mini, term_dates_yearlist[j][i])
        trem_minimum_date_list.append(mini)
    return trem_minimum_date_list

def compress_trem_data(term_dates_yearlist, trem_minimum_dates = None):
    '''
    压缩节气数据
    '''
    if trem_minimum_dates is None:
        trem_minimum_dates = get_trem_minimum_dates(term_dates_yearlist)
    res = []
    res_hex = []
    res_str = ''
    same_hex = []
    same_hex_str = ''
    hex_map = {}
    res_use_same_hex = []
    res_use_same_hex_str = ''
    for i, item in enumerate(term_dates_yearlist):
        item_res = []
        item_res_hex = 0
        for j in range(0, len(item)):
            item_res.append(item[j] - trem_minimum_dates[j])
            item_res_hex |= (item[j] - trem_minimum_dates[j]) << (j * 2)
        item_res_hex = hex(item_res_hex)
        res_str = set_item_to_js_str(res_str, item_res_hex, 'int', i + 1901)
        res_hex.append(item_res_hex)
        res.append(item_res)
        same_idx = len(same_hex)
        # print(i + 1901, len(same_hex))

        if item_res_hex in hex_map:
            same_idx = hex_map[item_res_hex]
        else:
            same_hex_str = set_item_to_js_str(same_hex_str, item_res_hex, 'int', same_idx + 1901)
            same_hex.append(item_res_hex)
            hex_map[item_res_hex] = same_idx
        res_use_same_hex.append(same_idx)
        res_use_same_hex_str = set_item_to_js_str(res_use_same_hex_str, same_idx, 'int', i + 1901)

    return {
        "list": res,
        "hex_str": res_str,
        "hex_list": res_hex,
        "same_hex": same_hex,
        "same_hex_str": same_hex_str,
        "use_same_hex": res_use_same_hex,
        "use_same_hex_str":  res_use_same_hex_str
    }


def extract_all():
    '''
    提取所有数据
    '''
    lunar_month_datas = []
    solar_term_date_list = []
    solar_term_date_str = ''
    lunar_month_datas_str = ''
    lunar_new_year_dates_str = ''
    for year in range(1901, 2101):
        res = extract_data(year)
        # 节气
        solar_term_date_list.append(res['solar_term_date_list'])

        solar_term_date_str = set_item_to_js_str(solar_term_date_str, ''.join(str(item) for item in res['solar_term_date_list']), None, year, 1)
        # 大小月
        lunar_month_datas_str = set_item_to_js_str(lunar_month_datas_str, res['lunar_month_datas'], 'int', year)
        # 农历年
        lunar_new_year_dates_str = set_item_to_js_str(lunar_new_year_dates_str, res['lunar_new_year_date'], 'int', year)        

    # 农历大小月表
    lunar_month_datas_str = js_str('LUNAR_MONTH_DATAS', lunar_month_datas_str, True)
    # 农历正月初一表
    lunar_new_year_dates_str = js_str('LUNAR_NEW_YEAR_DATE', lunar_new_year_dates_str, True)
    # 节气表
    solar_term_date_str = js_str('SOLAR_TERM_DATE_LIST', solar_term_date_str, True)

    trem_minimum_dates = get_trem_minimum_dates(solar_term_date_list)
    trem_minimum_dates_str = js_str('TERM_MINIMUM_DATES', ','.join(str(item) for item in trem_minimum_dates), True, True)
    compressed_trem_data = compress_trem_data(solar_term_date_list, trem_minimum_dates)
    



    # 写入文件
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'dist', 'lunar_month_datas.js')
    with open(p, 'w', encoding='utf-8') as f:
        f.write(lunar_month_datas_str)
        f.write(lunar_new_year_dates_str)
        # f.write(solar_term_date_str)
        f.write(trem_minimum_dates_str)
        f.write(js_str('TERM_SAME_HEX', compressed_trem_data['same_hex_str'], True))
        # f.write(js_str('TERM_HEX_LIST', compressed_trem_data['hex_list'], False))
        f.write(js_str('TERM_LIST', compressed_trem_data['use_same_hex_str'], True))
        # json.dump(lunar_month_datas, f, ensure_ascii=False, indent=2)
    
    
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'dist', 'solar_term_date_list.json')
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(solar_term_date_list, f, ensure_ascii=False, indent=2)
    


 
    # p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'dist', 'solar_term_date_list.js')
    # with open(p, 'w', encoding='utf-8') as f:

        # json.dump(solar_term_date_list, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    # print(extract_data(1903))
    extract_all()
    pass