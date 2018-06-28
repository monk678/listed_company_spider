import time
import monk
import os
import csv
import shutil
import configparser

import sse
import szse

cf = configparser.ConfigParser()
cf.read("configparser.ini")
key = cf.get("key", "key")
if key == '1':
    data_save_path = cf.get("data_save_path", "local") + '%s/' % time.strftime('%Y%m%d', time.localtime(time.time()))
else:
    data_save_path = cf.get("data_save_path", "service") + '%s/' % time.strftime('%Y%m%d', time.localtime(time.time()))

# 深交所页面李所有上市公司的excel下载地址
url_szse = "http://www.szse.cn/szseWeb/ShowReport.szse?SHOWTYPE=xlsx&CATALOGID=1110&tab1PAGENO=1&ENCODE=1&TABKEY=tab1"
today = time.strftime("%Y-%m-%d")

# 合并深交所与上交所两边的数据,并保存为csv文件
full_csv_file_name = '%s%s_listed_company_full.csv' % (data_save_path, today)

# 删除full文件,防止覆盖
if os.path.exists(full_csv_file_name):
    os.remove(full_csv_file_name)

data_save_path = data_save_path + 'listed_company'

# 创建文件夹
if not os.path.exists(data_save_path):
    os.makedirs(data_save_path)

# 下载深交所的excel文件
szse_xlsx_name = '%s/szse.xlsx' % data_save_path
# 处理上交所的数据
sse_csv_file_name = '%s/sse.csv' % data_save_path

csv_head = ['industry_code', 'industry_type', 'company_code', 'company_full_name_CH', 'stock_codeA', 'stock_codeB']

with open(sse_csv_file_name, 'a') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(csv_head)

url = 'http://www.sse.com.cn/assortment/stock/areatrade/trade/'
industry = sse.get_industry_info(url)

# 遍历所有行业
while True:
    try:
        industry_info = industry.__next__()
        industry_code = industry_info[2]
        industry_name = industry_info[0]

        # 读取行业代码下的公司列表
        company_data = sse.get_company_info(industry_code=industry_code, csv_file_name=sse_csv_file_name,
                                            csv_head=csv_head)
        # 遍历所有公司
        while True:
            try:
                company_data_info = company_data.__next__()
            except StopIteration:
                print('*******行业%s***%s: 所有公司遍历完毕,开始爬取下一个行业!' % (industry_code, industry_name))
                break
    except StopIteration:
        print('\n>>>>>>上交所_所有行业遍历完毕,所有数据写入文件%s!\n' % sse_csv_file_name)
        break

if os.path.exists(sse_csv_file_name):
    shutil.copyfile(sse_csv_file_name, full_csv_file_name)

# 下载深圳交易所的上市公司名单
monk.down_file_by_url(url_szse, szse_xlsx_name)

print('>>>成功下载深圳交易所上市公司名单:%s' % szse_xlsx_name)

szse.process_xlsx(csv_file_name=full_csv_file_name, xlsx_name=szse_xlsx_name, csv_head=csv_head)

# 删除文件夹
if os.path.exists(data_save_path):
    shutil.rmtree(data_save_path)

print('\n>>>成功合并深交所与上交所的所有数据至文件:%s' % szse_xlsx_name)