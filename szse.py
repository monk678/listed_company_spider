def process_xlsx(csv_file_name, xlsx_name,
                 csv_head=['industry_code', 'industry_type', 'company_code', 'company_full_name_CH', 'stock_codeA',
                           'stock_codeB']):
    import xlrd
    import csv
    import sql_process

    data = xlrd.open_workbook(xlsx_name)
    table = data.sheets()[0]
    nrows = table.nrows  # 行数
    ncols = table.ncols  # 列数

    data_head = table.row_values(0)  # 第一行数据

    industry_NO = data_head.index('所属行业')
    company_code_NO = data_head.index('公司代码')
    company_full_name_CH_NO = data_head.index('公司全称')
    stock_codeA_NO = data_head.index('A股代码')
    stock_codeB_NO = data_head.index('B股代码')

    for i in range(1, nrows):
        company_data = []
        rowValues = table.row_values(i)  # 某一行数据
        industry = rowValues[industry_NO]
        industry_code = industry[:1]
        industry_type = industry[1:]
        company_code = rowValues[company_code_NO]
        company_full_name_CH = rowValues[company_full_name_CH_NO]
        stock_codeA = rowValues[stock_codeA_NO]
        stock_codeB = rowValues[stock_codeB_NO]

        if len(stock_codeA) < 3:
            stock_codeA = ''

        if len(stock_codeB) < 3:
            stock_codeB = ''

        sql_process.insert_into_table_credit_file_info(industry_code=industry_code, company_code=company_code,
                                                       industry_type=industry_type,
                                                       company_full_name_CH=company_full_name_CH,
                                                       stock_codeA=stock_codeA,
                                                       stock_codeB=stock_codeB)

        # 按照顺序准备即将写入csv文件的数据
        for csv_head_info in csv_head:
            # eval():将字符串str当成有效的表达式来求值并返回计算结果。
            company_data.append(eval(csv_head_info))

        # 将数据写入csv文件中
        with open(csv_file_name, 'a') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(company_data)
