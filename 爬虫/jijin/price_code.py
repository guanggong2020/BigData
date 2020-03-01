import requests
import random
import time
import pymongo
from lxml import etree
from lxml.etree import tostring
import re

# 获取所有基金的代码
# ----------------------数据库连接
myconn = pymongo.MongoClient('mongodb://localhost:27017')
mydb = myconn['keshe']
mycol = mydb['jijin']


# ----------------------user-agent
User_Agent = [
              'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
              'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201',
              'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201',
              'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
              'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0',
              'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)',
              'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
              'Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12'
  ]

def get_price_code(url):
    # 补全请求头
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-Encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8',
        'connection': 'keep-alive',
        'host': 'fund.eastmoney.com',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'user-agent': random.choice(User_Agent)
    }
    code_list = []
    res = requests.get(url=url, headers=headers, timeout=10)
    res.encoding = 'gbk'
    html = res.text
    pageHTML = etree.HTML(html)
    list = pageHTML.xpath('//*[@id="code_content"]/div/ul[ @class="num_right" ]/li/div/a[1]')
    for each in list:
        m = re.compile('\&\#65288\;(.*)\&\#65289\;')
        code = m.findall(str(tostring(each)))[0]
        print(code)
        info = {
            'code':code,
            'status':1,
        }
        code_list.append(info)

    print('The num of code:'+ str(len(code_list)))
    return code_list

def mongo_insert(list):
    mycol.insert_many(list)
    print('save done')

def main(url):
    list = get_price_code(url)
    mongo_insert(list)

if __name__ == '__main__':
    main('http://fund.eastmoney.com/allfund_com.html')





# ------------------------------------------

# # 获取股票代码
# http://quote.eastmoney.com/stock_list.html
# # 历史数据下载
# http://quotes.money.163.com/service/chddata.html?code=0688218&start=20190101&end=20200101&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP
