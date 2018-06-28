# -*- coding:utf-8 -*-
import monk
import sql_process


# 读取行业列表
def get_industry_info(url='http://www.sse.com.cn/assortment/stock/areatrade/trade/'):
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin
    import re

    html = monk.get_html(url=url)
    datas = html.find('div', class_="table-responsive sse_table_T01 tdclickable").script.get_text()

    # 使用beautifulsoup结构化
    datas = BeautifulSoup(datas, "lxml").find_all('a')

    # 使用正则表达式寻找
    # datas = re.findall('<a href=".*</a>', datas)

    for data in datas:
        industry_url = data.get('href')
        # 行业代码
        industry_code = industry_url.split('=')[-1]
        # 行业URL地址
        industry_url = urljoin('http://www.sse.com.cn/assortment/', industry_url)
        # 行业名称
        industry_name = data.string

        yield industry_name, industry_url, industry_code


# 遍历所有公司
def get_company_info(industry_code, csv_file_name, csv_head):
    import requests
    import json
    import csv

    api_url = "http://query.sse.com.cn/security/stock/queryIndustryIndex.do"
    querystring = {"csrcCode": industry_code}

    headers = {
        'Accept-Encoding': "gzip, deflate",
        'Accept': "*/*",
        'Accept-Language': "en-GB,en;q=0.5",
        'Connection': "keep-alive",
        'Host': "query.sse.com.cn",
        'Referer': "http://www.sse.com.cn/assortment/stock/areatrade/trade/detail.shtml?csrcCode=A",
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0",
    }

    datas = requests.request("GET", api_url, headers=headers, params=querystring).text
    datas = json.loads(datas)['result']

    for data in datas:
        company_data = []

        company_code = data['companycode']  # 上市公司代码
        industry_type = data['csrcCodeDesc']  # 行业种类
        company_full_name_CH = data['fullname']  # 公司中文全称
        stock_codeA = data['securityCodeA']  # A股代码
        stock_codeB = data['securityCodeB']  # B股代码

        if len(stock_codeA) < 3:
            stock_codeA = ''

        if len(stock_codeB) < 3:
            stock_codeB = ''

        sql_process.insert_into_table_credit_file_info(industry_code=industry_code, company_code=company_code,
                                                       industry_type=industry_type,
                                                       company_full_name_CH=company_full_name_CH, stock_codeA=stock_codeA,
                                                       stock_codeB=stock_codeB)

        # 按照顺序准备即将写入csv文件的数据
        for csv_head_info in csv_head:
            # eval():将字符串str当成有效的表达式来求值并返回计算结果。
            company_data.append(eval(csv_head_info))
        # 将数据写入csv文件中
        with open(csv_file_name, 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(company_data)

        yield company_data
