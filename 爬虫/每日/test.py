# 上证指数、深证指数
# http://quotes.money.163.com/old/#query=sh
# http://quotes.money.163.com/old/#query=sz

# 历史行情
# https://www.nasdaq.com/api/v1/historical/SOHU/stocks/2008-01-01/2020-03-11
# 全部美股-东方财富
# http://quote.eastmoney.com/center/gridlist.html#us_stocks
# 个股-东方财富
# http://quote.eastmoney.com/us/AYTU.html


# http://71.push2.eastmoney.com/api/qt/clist/get?cb=jQuery11240047336080215205856_1583929895093&pn=2&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:105,m:106,m:107&fields=f12&_=1583929895110
# 105(升)、106(降)、107(平)
# 要将代码中的.换成_
# http://push2.eastmoney.com/api/qt/stock/get?secid=105.VIIX&ut=bd1d9ddb04089700cf9c27f6f7426281&fields=f43,f169,f170,f46,f60,f84,f116,f44,f45,f171,f126,f47,f48,f168,f164,f49,f161,f55,f92,f59,f152,f167,f50,f86,f71,f172&type=CT&cmd=VIIX7&sty=FDPBPFB&st=z&js=((x))&token=4f1862fc3b5e77c150a2b985b12db0fd&_=1583983672971
# import requests
#
# res = requests.get(url = 'http://emweb.eastmoney.com/pc_usf10/CoreReading/index?color=web&code=VIR',
#                    headers = {"USER-AGENT":'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
#                    )
#
# print(res.text)
# import pymongo
# con = pymongo.MongoClient('mongodb://localhost:27017')
# db = con['stock']
# mycol = db['USA_stock_daily_data']
# yourcol = db['USA_stock_code']
# for each in mycol.find():
#     yourcol.insert_one({
#         'code':each['code'],
#         'name':each['name'],
#         'status':0
#     })

import pymongo

myclient = pymongo.MongoClient('mongodb://134.175.192.53:27017')
myclient.admin.authenticate('admin','@Admin123')
db = myclient['stock']
mycol = db['USA_stock_code']
for each in mycol.find():
    print(each)

myclient.close()