import urllib.request
import pymongo

# ----------------------数据库连接
myconn = pymongo.MongoClient('mongodb://localhost:27017')
mydb = myconn['keshe']
mycol = mydb['test']

def get_csv():
    filepath = '.\\csv_data\\'
    count = 0
    list = mycol.find()
    for i in list:
        num = i['code']
        status = i['status']
        if status == 0:
            print('skip---')
        else:
            print('正在获取股票%s数据' % num)
            if num.startswith('0') or num.startswith('1') or num.startswith('2') or num.startswith('3'):
                url = 'http://quotes.money.163.com/service/chddata.html?code=1' + num + \
                      '&start=20190101&end=20200101&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
                print(url)
                urllib.request.urlretrieve(url, filepath + num + '.csv')
                # count +=1
                mycol.update_one({'code':num},{'$set':{'status':0}})
            else:
                url = 'http://quotes.money.163.com/service/chddata.html?code=0' + num + \
                      '&start=20190101&end=20200101&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
                print(url)
                urllib.request.urlretrieve(url, filepath + num + '.csv')
                # count +=1
                # if count > 3:
                #     break
                mycol.update_one({'code': num}, {'$set': {'status': 0}})

if __name__ == '__main__':
    get_csv()