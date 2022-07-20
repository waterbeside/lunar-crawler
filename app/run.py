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