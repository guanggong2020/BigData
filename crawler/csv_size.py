import os
import pymongo

# ----------------------数据库连接
myconn = pymongo.MongoClient('mongodb://localhost:27017')
mydb = myconn['keshe']
mycol = mydb['test']

def filesize_filter():
    path = '.\\csv_data\\'
    dirs = os.listdir(path) # 文件夹下所有文件名
    count = 0
    for file in dirs:
        fsize = os.path.getsize(os.path.join(path,file))
        if fsize <= 108000:
            result = mycol.remove({'code':str(file.split('.')[0])})
            os.remove(os.path.join(path,file))
            print(result)
            count += 1
    print(count)

