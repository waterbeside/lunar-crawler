import os
from string import Template
import urllib.request
import sys


from lib import save_to_file
from lib.const import LUN_MON_DICT, LUN_DAY_DICT, WEEK_DAY
from lib.parse_content import parse_content



print(os.getcwd())
sys.path.append(os.getcwd() + '\app')


# import requests
base_url = 'https://www.hko.gov.hk/tc/gts/time/calendar/text/files'

def get_url(year):
  url = Template('${base_url}/T${year}c.txt').substitute(base_url=base_url, year=year)
  return url

def get_year_data(year):
  url = get_url(year)
  print(url)
  res = []
  with urllib.request.urlopen(url) as response:
    text = response.read().decode('big5')
    lines = text.split('\n')
    save_to_file(text, os.getcwd() + '/data/{}.txt'.format(year))
    # for line in lines:
    #   res.append
    return text
    # for line in response.readlines():
    #   line = line.strip('\n')
      # return response.read()
  
# def parse_content(content):
#   '''
#   Parse the content of the file.
#   '''
#   res = {}
#   lines = content.split('\n')
#   fix_lunar_month = None
#   current_lunar_month = None
#   date_list = []
#   for index, line in enumerate(lines):
#     if index == 0: 
#       # 取得年份
#       res['year'] = line[0:4]
#       # 取天干
#       res['stem'] = line[5:6]
#       # 取地支
#       res['branch'] = line[6:7]

#       res['date_list'] = []

#     # 

#     # 取所有日期对应的信息
#     line = re.sub('\s+', ' ', line.strip())
#     if line.strip() == '':
#       continue
#     line_split = [s.strip() for s in line.split(' ')]
#     if index > 2 and len(line_split) > 2:
#       item = dict()
#       # print(line_split[0][4:5])
#       if line_split[0][4:5] != '年':
#         break
#       # 取得日期
#       item['date'] = datetime.datetime.strptime(line_split[0], '%Y年%m月%d日').strftime('%Y-%m-%d')
#       # 取得阴历日期
#       lunar_day = line_split[1]
#       if lunar_day[-1] == '月':
#         if current_lunar_month is None:
#           fix_lunar_month = 12 if LUN_MON_DICT[lunar_day] == 1 else LUN_MON_DICT[lunar_day] - 1
#         current_lunar_month = LUN_MON_DICT[lunar_day]
#         item['lunar_day'] = 1
#       else:
#         item['lunar_day'] = LUN_DAY_DICT[lunar_day]

#       item['lunar_month'] = current_lunar_month
      
      
#       # 取得周几
#       item['week_day'] = WEEK_DAY[line_split[2]] if len(line_split) > 2  else None
#       # 取得节气
#       item['solar_term'] =  line_split[3] if len(line_split) > 3  else None

#       # print(line_split)
#       # print(item)
#       date_list.append(item)

#   # 第二次循环，计算阴历月份
#   month_dict = {}
#   is_cur_lunar_year = 0 # 标识是否当前农历年的月份

#   for item in date_list:
    
#     if item['lunar_month'] is None:
#       item['lunar_month'] = fix_lunar_month

#     if item['lunar_month'] == 1:
#       is_cur_lunar_year = 1

#     month_key = '{},{}'.format(is_cur_lunar_year, item['lunar_month'])
#     if month_key not in month_dict:
#       month_dict[month_key] = { 
#         'month': item['lunar_month'], 
#         'is_big': False,
#         'this_lunar_year': is_cur_lunar_year,
#         'date_list': []
#       }
#     if item['lunar_day'] > 29:
#       month_dict[month_key]['is_big'] = True

#     month_dict[month_key]['date_list'].append(item)
   
      
#   res['month_data'] = month_dict

#   print(res)
#   with open(os.getcwd() + '/data/json/{}.json'.format(res['year']), 'w') as f:
#     json.dump(res, f)

def open_text_data(year):
  with open(os.getcwd() + '/data/txt/{}.txt'.format(year), 'r', encoding='utf-8') as f:
    return f.read()

if __name__ == '__main__':
  # 1901 to 2100 
  # 香港於1941年6月15日至9月30日期間實施了夏令時間
  for year in range(1901, 2101):
    content = open_text_data(year)
    # content = get_year_data(year)
    parse_content(content)
  # res = get_year_data(2100)
  # res = open_text_data(1902)
  # parse_content(res)
  # print(open_text_data(1901))
  # eval(sys.argv[1])(*sys.argv[2:])