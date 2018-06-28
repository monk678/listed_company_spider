# 链接到数据库
def connect_to_db_spider_work():
    import configparser
    import pymysql

    cf = configparser.ConfigParser()

    cf.read("configparser.ini")

    # read by type
    db_host = cf.get("db", "host")
    db_user = cf.get("db", "user")
    db_port = cf.getint("db", "port")
    db_connect_timeout = cf.get("db", "connect_timeout")
    db_password = cf.get("db", "password")
    db_db = cf.get("db", "db")
    db_charset = cf.get("db", "charset")

    db = pymysql.connect(host=db_host,
                         user=db_user,
                         port=db_port,
                         connect_timeout=int(db_connect_timeout),
                         password=db_password,
                         db=db_db,
                         charset=db_charset)

    cursor = db.cursor()
    # sql_check = 'select * from credit_file_info'
    # print('当前数据库page_1_info中存在', cursor.execute(sql_check), '条记录')
    return db, cursor


# 断开与数据库的链接
def quit_connect_to_db_fengniao(db, cursor):
    cursor.close()
    db.close()


# 将数据插入表credit_file_info
def insert_into_table_credit_file_info(industry_code='', company_code='', industry_type='', company_full_name_CH='',stock_codeA='', stock_codeB=''):
    # 连接配置信息
    import random
    import string
    import pymysql
    import configparser
    import time

    db, cursor = connect_to_db_spider_work()
    id = ''.join(random.sample(string.ascii_letters + string.digits, 20))

    cf = configparser.ConfigParser()
    cf.read("configparser.ini")

    update_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    sql = """INSERT INTO listed_company
        (id, industry_code, company_code, industry_type, company_full_name_CH, stock_codeA, stock_codeB, update_date) values
        (\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", 
        \"%s\", \"%s\", \"%s\");""" % \
          (id, industry_code, company_code, industry_type, company_full_name_CH, stock_codeA, stock_codeB, update_date)
    try:
        cursor.execute(sql)
        db.commit()
        # print('********',  company_code, company_full_name_CH, "数据插入credit_file_info成功!\n*******************")
    except pymysql.err.IntegrityError:
        # print('数据已经存在于表credit_file_info中')
        # print(e)
        pass
    except pymysql.err.ProgrammingError as e:
        print('数据插入表credit_file_info异常:pymysql.err.ProgrammingError')
        print('SQL:', sql)
        print(e)
    except pymysql.err.InternalError as e:
        print('数据插入表credit_file_info异常:pymysql.err.InternalError')
        print('SQL:', sql)
        print(e)
    except pymysql.err.DataError as e:
        print('数据插入表credit_file_info异常:pymysql.err.DataError:')
        print('SQL:', sql)
        print(e)
    except Exception as e:
        raise e
    quit_connect_to_db_fengniao(db=db, cursor=cursor)
