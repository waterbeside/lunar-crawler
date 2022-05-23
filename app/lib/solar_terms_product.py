import os
import sys
import json
import math
import datetime
from time import strptime
from dateutil.relativedelta import relativedelta

from const import SOLAR_TREMS
# from lib.const import LUN_MON_DICT, LUN_DAY_DICT, WEEK_DAY, SOLAR_TREMS

# root_path = os.path.abspath(__file__)
# root_path = '/'.join(root_path.split('/')[:-2])
# sys.path.append(root_path)


# print(os.getcwd())
# sys.path.append(os.getcwd() + '/app')

def get_std_data():
  p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'dist', 'solar_term_date_list.json')
  f = open(p, 'r', encoding='utf-8')
  data = json.load(f)
  f.close()
  return data

def get_term_date(year, x):
  '''
  ---- 节气积日公式 ----

  Description:
    把当天和1900年1月0日的差称为积日，
    那么第y年（1900年算第0年）的第x个节气的积日是
      #* F = 365.242 * y + 6.2 + 15.22 * x - 1.9 * math.sin(0.262 * x)
    公式误差为0.05
  
  Args:
    year: 年份
    x: 节气序号
  '''
  F = 365.242 * (year - 1900) + 6.2 + 15.22 * x - 1.9 * math.sin(0.262 * x)
  sdate = datetime.datetime.strptime('1900-01-01', '%Y-%m-%d')
  return sdate + relativedelta(days=+(F-1))


def check_product(year, std_data = None):
  '''
  ---- 检查节气积日公式的准确性 ----
  '''
  # get_term_date
  if std_data is None:
    data = get_std_data()
    std_data = data[year-1901]

  res = True
  err_date = []
  for i in range(0, 24):
    d = get_term_date(year, i)
    std_month =i // 2 + 1
    std_month = '0{}'.format(std_month) if std_month < 10 else str(std_month)
    std_date = std_month + '-' + std_data[i]
    if d.strftime('%m-%d') != std_date:
      res = False
      err_date.append([d.strftime('%y-%m-%d'), std_date])
  return res, err_date


def check_all():
  data = get_std_data()
  res = True
  err_years = []
  for year in range(1901, 2101):
    r, e = check_product(year, data[year-1901])
    if not r:
      res = False
      err_years.append(year)
  return res, err_years
    

if __name__ == '__main__':

  print(check_all())  
  print(check_product(1902))
  pass


