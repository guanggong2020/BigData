# ----------------------导入文件
from A_crawler import *
from A_price_code import *
from fund_crawler import  *
from fund_price_code import *
from ZS_crawler import *
from US_crawler import *
import sys
import re
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
def run(field_code,start_time,end_time):
    if field_code == 'A':
        A_price_code('http://quote.eastmoney.com/stock_list.html',A_CODE)
        spider = A_Spider(SEM,A_CODE,A_PATH,A_DATA,start_time,end_time)
        spider.run()

    elif field_code == 'F':
        fund_price_code('http://fund.eastmoney.com/allfund_com.html',FUND_CODE)
        spider = FUND_Spider(SEM,FUND_CODE,start_time,end_time,FUND_DATA)
        spider.run()

    elif field_code == 'Z':
        spider = ZS_Spider(SEM,SH,SZ,ZS_PATH,ZS_DATA,start_time,end_time)
        spider.run()

    elif field_code == 'U':
        spider = US_Spider(SEM,US_CODE,US_PATH,US_DATA,start_time,end_time)
        spider.run()

    else:
        print('INPUT ERROR')

if __name__ == '__main__':
    dic = {
        'A':'A股',
        'F':'国内基金',
        'Z':'指数',
        'U':'美股'
    }
    pattern = re.compile('(\d{4}-\d{2}-\d{2})')
    try:
        time1_match = pattern.match(sys.argv[2])
        time2_match = pattern.match(sys.argv[3])
        if time1_match and time2_match:
            print(f'开始爬取{sys.argv[2]}到{sys.argv[3]}的{dic[sys.argv[1]]}数据...')
            run(sys.argv[1],sys.argv[2],sys.argv[3])
        else:
            print('时间输入有误，请重试。')
    except:
        print('输入有误,提示:\n'
              '命令形式: py main.py [爬取数据类型] [起始时间] [结束时间]\n'
              '时间形式: YYYY-MM-DD\n'
              '爬取数据类型: A--A股，F--基金，Z--指数，U--美股')
