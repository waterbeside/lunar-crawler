
import re
import os
import json
import datetime
from lib.const import LUN_MON_DICT, LUN_DAY_DICT, WEEK_DAY, SOLAR_TREMS

def parse_content(content):
  '''
  Parse the content of the file.
  解析文件内容并把结果写到JSON文件中
  # !------------------
    生成阴历的大小月(放到结果中的'big_month_list'属性):
    5 + 12位2进制，
    00000000000000000
    ..。..************
    后12位用于存放每月是否大小月，正月从右开始，1为大月，0为小月
    从右往左的最后4位为该年的闰月月份，如果没有闰月，则为0
    从右往左的第13位，为闰月是否大月，1为大月，0为小月
  # !-----------------
  '''
  res = {}
  lines = content.split('\n')
  fix_lunar_month = None # 记录上年公历年的出现的最后一个月的阴历月份
  current_lunar_month = None
  date_list = []
  is_cur_lunar_year = 0 # 标识是否当前农历年的月份
  res['solar_term_date_list'] = [] # 记录节气日期
  res['lunar_month_list'] = [] # 记录农历月份
  res['big_month_list'] = 0 # 记录大月份
  res['leap_month'] = 0 # 记录闰月月份
  res['leap_month_is_big'] = 0 # 记录闰月是否是大月
  res['lunar_new_year_date'] = None # 记录农历新年的日期
  for index, line in enumerate(lines):
    if index == 0: 
      # 取得年份
      res['year'] = int(line[0:4])
      # 取天干
      res['stem'] = line[5:6]
      # 取地支
      res['branch'] = line[6:7]
    # 

    # 取所有日期对应的信息
    line = re.sub('\s+', ' ', line.strip())
    if line.strip() == '':
      continue
    line_split = [s.strip() for s in line.split(' ')]
    if index > 2 and len(line_split) > 2:
      item = dict()
      # print(line_split[0][4:5])
      if line_split[0][4:5] != '年':
        break
      # 取得日期
      item['date'] = datetime.datetime.strptime(line_split[0], '%Y年%m月%d日').strftime('%Y-%m-%d')
      # 取得阴历日期
      lunar_day = line_split[1]
      if lunar_day == '正月':
        res['lunar_new_year_date'] = int(datetime.datetime.strptime(item['date'], '%Y-%m-%d').strftime('%m%d'))

      if lunar_day[-1] == '月': # 初一
        if current_lunar_month is None:
          fix_lunar_month = 12 if LUN_MON_DICT[lunar_day] == 1 else LUN_MON_DICT[lunar_day] - 1
        current_lunar_month = LUN_MON_DICT[lunar_day]
        item['lunar_day'] = 1
        if current_lunar_month == 1:
          is_cur_lunar_year = 1
      else:
        item['lunar_day'] = LUN_DAY_DICT[lunar_day]

      item['lunar_month'] = current_lunar_month      
      
      # 取得周几
      item['week_day'] = WEEK_DAY[line_split[2]] if len(line_split) > 2  else None
      # 取得节气
      item['solar_term'] =  line_split[3] if len(line_split) > 3  else None
      if item['solar_term'] is not None:
        res['solar_term_date_list'].append(datetime.datetime.strptime(item['date'], '%Y-%m-%d').strftime('%d'))

      if item['lunar_day'] == 1 or len(res['lunar_month_list']) == 0:
        lunar_month_list_item = {
          'month':current_lunar_month,  # 农历月份
          'is_big': False, # 是否是大月
          'is_leap': True if is_cur_lunar_year and current_lunar_month > 100 else False, # 是否是闰月
          'this_lunar_year': is_cur_lunar_year, # 是否是当前农历年的月份
          'date_list': []
        }
        res['lunar_month_list'].append(lunar_month_list_item)
        if is_cur_lunar_year and current_lunar_month > 100: # 处理闰月（放到倒数14位到倒数1）
          leap_month = current_lunar_month - 100
          res['big_month_list'] |= leap_month << 13
          res['leap_month'] = leap_month

      res['lunar_month_list'][-1]['date_list'].append(item)
      

      if item['lunar_day'] > 29: # 如果是大月
        res['lunar_month_list'][-1]['is_big'] = True
        if is_cur_lunar_year == 1:
          if current_lunar_month > 100: # 如果是闰月, 则标识大月在第13位（从右数上）
            res['big_month_list'] |= 1 << 12
            res['leap_month_is_big'] = 1
          else: # 非闰月
            res['big_month_list'] |= 1 << (item['lunar_month'] - 1)


      # print(line_split)
      # print(item)
      date_list.append(item)


  # **第二次遍历，计算上年的月份，补全上年的数据
  pre_year_data = None
  pre_year = res['year'] - 1
  pre_year_leap_month = 0
  pre_year_leap_month_is_big = 0
  pre_year_big_month_list = 0
  for item in res['lunar_month_list']:
    if item['month'] is None:
      item['month'] = fix_lunar_month
    if item['this_lunar_year'] == 0 and item['is_big']:
      if item['month'] > 100: # 闰月
        leap_month = item['month'] - 100
        pre_year_big_month_list |= leap_month << 13
        pre_year_big_month_list |= 1 << 12
        pre_year_leap_month = leap_month
        pre_year_leap_month_is_big = 1
      else: # 非闰月
        pre_year_big_month_list |= 1 << (item['month'] - 1)
      
  if pre_year > 1900:
    json_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'json', '{}.json'.format(pre_year))
    try:
      with open(json_filepath, 'r', encoding='utf-8') as f:
        pre_year_data = json.load(f)
        pre_year_data['big_month_list'] |= pre_year_big_month_list
        if pre_year_leap_month > 0:
          pre_year_data['leap_month'] = pre_year_leap_month
          pre_year_data['leap_month_is_big'] = pre_year_leap_month_is_big
        with open(json_filepath, 'w', encoding='utf-8') as f:
          json.dump(pre_year_data, f, ensure_ascii=False, indent=2)
    except Exception as e:
      print('err', e)
   




  # 保存路径
  p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'json', '{}.json'.format(res['year']))
  with open(p, 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=2)