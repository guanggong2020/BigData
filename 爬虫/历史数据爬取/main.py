# ----------------------导入文件
from A_crawler import *
from A_price_code import *
from fund_crawler import  *
from fund_price_code import *
from ZS_crawler import *
from US_crawler import *

# ----------------------数据库连接
myconn = pymongo.MongoClient('mongodb://localhost:27017')
keshe = myconn['keshe'] # A股、基金、指数存储数据库
stock = myconn['stock'] # 美股存储数据库


A_CODE = keshe['A_code'] # A股代码
FUND_CODE = keshe['fund_code'] # 基金代码
US_CODE = stock['USA_stock_code'] # 美股代码

SH = keshe['SH_test']
SZ = keshe['SZ_test']

A_DATA = keshe['A_data'] # A股存储集合
FUND_DATA = keshe['fund_data'] # 基金存储集合
ZS_DATA = keshe['ZS_data'] # 指数存储集合
US_DATA = stock['historialstock'] # 美股存储集合

# ----------------------暂存文件夹
A_PATH = '.\\A_data\\'
ZS_PATH = '.\\ZS_data\\'
US_PATH = '.\\US_data\\'

# ----------------------线程数
SEM = 32 #信号量，控制协程数


# ----------------------爬虫



def run(field_code):
    if field_code == 'A':
        A_price_code('http://quote.eastmoney.com/stock_list.html',A_CODE)
        spider = A_Spider(SEM,A_CODE,A_PATH,A_DATA,'2008-01-01','2020-02-20')
        spider.run()

    elif field_code == 'FUND':
        fund_price_code('http://fund.eastmoney.com/allfund_com.html',FUND_CODE)
        spider = FUND_Spider(SEM,FUND_CODE,'2008-01-01','2020-02-14',FUND_DATA)
        spider.run()

    elif field_code == 'ZS':
        spider = ZS_Spider(SEM,SH,SZ,ZS_PATH,ZS_DATA,'2008-01-01','2020-02-20')
        spider.run()

    elif field_code == 'US':
        spider = US_Spider(SEM,US_CODE,US_PATH,US_DATA,'2008-01-01','2020-02-20')
        spider.run()

    else:
        print('ERROR')

if __name__ == '__main__':
    run('A')
    run('FUND')
    run('ZS')
    run('US')