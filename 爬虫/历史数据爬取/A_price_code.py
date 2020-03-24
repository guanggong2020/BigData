import requests
import random
import time
import pymongo
from lxml import etree
from lxml.etree import tostring
import re

# 获取市场上所有股票的代码

def A_price_code(url,SAVE_COL):
    # 补全请求头
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

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-Encoding': 'gzip, deflate',
        'accept-language': 'zh-CN,zh;q=0.9,ja;q=0.8',
        'connection': 'keep-alive',
        'host': 'quote.eastmoney.com',
        'cache-control': 'max-age=0',
        'upgrade-insecure-requests': '1',
        'cookie':'qgqp_b_id=73554be904b433e9175716f5c5251b59; em-quote-version=topspeed; cowCookie=true; intellpositionL=1138.39px; intellpositionT=655px; em_hq_fls=old; HAList=a-sh-688080-N%u6620%u7FF0%u901A%2Ca-sz-000815-%u7F8E%u5229%u4E91%2Ca-sz-300818-N%u8010%u666E%2Cf-0-000001-%u4E0A%u8BC1%u6307%u6570; st_si=81820354278505; st_asi=delete; st_pvi=42385932726708; st_sp=2020-02-08%2000%3A19%3A32; st_inirUrl=http%3A%2F%2Fwww.eastmoney.com%2F; st_sn=4; st_psi=20200213145316934-113200301321-2150599774',
        'user-agent': random.choice(User_Agent)
    }

    code_list = []
    res = requests.get(url=url, headers=headers, timeout=10)
    res.encoding = 'utf8'
    html = res.text
    pageHTML = etree.HTML(html)
    list = pageHTML.xpath('// *[ @ id = "quotesearch"] / ul / li / a')
    for each in list:
        m = re.compile('\((.*)\)')
        code = m.findall(str(tostring(each)))[0]
        info = {
            'code':code,
            'status':1,

        }
        code_list.append(info)

    if SAVE_COL.count_documents({}) == 0:
        SAVE_COL.insert_many(code_list)

    else:
        print('A股代码已存在')

# ------------------------------------------

# # 获取股票代码
# http://quote.eastmoney.com/stock_list.html
# # 历史数据下载
# http://quotes.money.163.com/service/chddata.html?code=0688218&start=20190101&end=20200101&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP
