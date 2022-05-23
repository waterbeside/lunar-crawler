import json
import os

def extract_data(year):
    '''
    提取数据
    '''
    # print(os.path.abspath('.'))
    # print(os.getcwd())
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'json', '{}.json'.format(year))
    print('extract', year)
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

def set_item_to_js_str(s, item, item_type, year):
    if s != '':
        s += ','
    if item_type == 'int':
        s += str(item)
    else:
        s += '"' + item + '"'
    if (year - 1900) % 10 == 0:
        s += '\n' 
    return s

def js_str(var_name, data_str, is_array=False):
    if is_array:
        return 'var {} = [{}];\n'.format(var_name, data_str)
    return 'var {} = {};\n'.format(var_name, data_str)

def extract_all():
    '''
    提取所有数据
    '''
    lunar_month_datas = []
    solar_term_date_list = []
    lunar_month_datas_str = ''
    lunar_new_year_dates_str = ''
    for year in range(1901, 2101):
        res = extract_data(year)
        # 节气
        solar_term_date_list.append(res['solar_term_date_list'])
        # 大小月
        lunar_month_datas.append(res['lunar_month_datas'])
        lunar_month_datas_str = set_item_to_js_str(lunar_month_datas_str, res['lunar_month_datas'], 'int', year)
        # if lunar_month_datas_str != '':
        #     lunar_month_datas_str += ','
        # lunar_month_datas_str += '"' + res['lunar_month_datas'][2:] +'"'

        # 农历年
        lunar_new_year_dates_str = set_item_to_js_str(lunar_new_year_dates_str, res['lunar_new_year_date'], 'int', year)
        # print(year, res['lunar_new_year_date'])
        # if lunar_new_year_dates_str != '':
        #     lunar_new_year_dates_str += ','
        # lunar_new_year_dates_str  +=  str(res['lunar_new_year_date'])

        

    # 农历大小月表
    lunar_month_datas_str = js_str('LUNAR_MONTH_DATAS', lunar_month_datas_str, True)
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'dist', 'lunar_month_datas.js')
    with open(p, 'w', encoding='utf-8') as f:
        f.write(lunar_month_datas_str)
        # json.dump(lunar_month_datas, f, ensure_ascii=False, indent=2)
    
    # 农历正月初一表
    lunar_new_year_dates_str = js_str('LUNAR_NEW_YEAR_DATE', lunar_new_year_dates_str, True)
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'dist', 'lunar_new_year_datas.js')
    with open(p, 'w', encoding='utf-8') as f:
        f.write(lunar_new_year_dates_str)
        # json.dump(lunar_new_year_dates, f, ensure_ascii=False, indent=2)
    


    # 节气表
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'dist', 'solar_term_date_list.json')
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(solar_term_date_list, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    # print(extract_data(1903))
    extract_all()
    pass