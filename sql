use spider_work;
drop table if exists listed_company;

create table if not exists listed_company(
-- 评级ID
id varchar(50) NOT NULL,       
-- 行业代码
industry_code varchar(1),
-- 上市公司代码
company_code varchar(10),
-- 行业种类
industry_type varchar(20),
-- 公司中文全称
company_full_name_CH varchar(100),
-- A股代码
stock_codeA varchar(20),
-- B股代码
stock_codeB varchar(50),
-- 爬虫时间
update_date date,
PRIMARY KEY (update_date, company_full_name_CH, company_code)
)DEFAULT CHARSET=utf8;
