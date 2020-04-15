import requests
import random
import re
import json
import time
from lxml import etree


USER_AGENT_CHOICES = [
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
cookies = 'JSESSIONID=ABAAAECABBJAAGIA437D50912A32DC55E4FCBF9CB2CBC3D; WEBTJ-ID=20200411113745-171675092f31b-0e9264286a1834-5313f6f-1296000-171675092f455f; TG-TRACK-CODE=search_code; _ga=GA1.2.272569761.1586605991; _gid=GA1.2.1573715936.1586605991; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221716916247a195-06befbfd574a4d-5313f6f-1296000-1716916247b5fe%22%2C%22%24device_id%22%3A%221716916247a195-06befbfd574a4d-5313f6f-1296000-1716916247b5fe%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1586605991; user_trace_token=20200411195310-ac5d49d4-975c-4fda-b3e4-3a70b11f4ac4; LGSID=20200411195310-f79c8ec5-d8cc-4c5b-bf07-45533de9c8fe; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fpassport.lagou.com%2Flogin%2Flogin.html%3Fmsg%3Dvalidation%26uStatus%3D2%26clientIp%3D119.133.137.47; LGUID=20200411195310-d48d6ffd-c14b-4e4b-b7dd-b235c751d434; X_MIDDLE_TOKEN=11570637a6598c99168437d68e5bac87; _gat=1; SEARCH_ID=9db5a11f318f4331aa201e76f1c74cde; X_HTTP_TOKEN=5f2f5dcbe20873237406066851bf8d94895980fb6b; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1586606049; LGRID=20200411195408-33edaf9e-e15c-495e-83e8-7fe7fe89558e'
# content = requests.get(url = 'https://www.lagou.com/zhaopin/Java/2/',headers = {
#     'user-agent':random.choice(USER_AGENT_CHOICES),
#     # 'cookie':cookies,
#     'Host': 'www.lagou.com'
# })
# HTML = content.text
# print(HTML)
# pageHTML = etree.HTML(HTML)
# shezhao = pageHTML.xpath('//div[@class="company_navs_wrap"]/ul/li[2]/a/text()')[0]
# xiaozhao = pageHTML.xpath('//div[@class="company_navs_wrap"]/ul/li[3]/a/text()')[0]
# num1 = re.findall(r"（(.*?)）",shezhao)[0]
# num2 = re.findall(r"（(.*?)）",xiaozhao)[0]
# print(num1,num2)
# for each in _url:
#     print(each)



#
# X_Anti_Forge_Token = re.search(r"window.X_Anti_Forge_Token = '(.*?)'", home_resp.text).group(1)
# X_Anti_Forge_Code = re.search(r"window.X_Anti_Forge_Code = '(.*?)'", home_resp.text).group(1)
# params = {
# 'companyId': 4428,
# 'positionFirstType': '全部',
# 'schoolJob': 'false',
# 'pageNo': 1,
# 'pageSize': 20
# }
#


# content = {}
#
# while True:
#     times = 10
#
#     u1 = random.choice(USER_AGENT_CHOICES)
#     # _ip = json.loads(requests.get('http://localhost:5010/get/').text)['proxy']
#     # proxies = {'https': _ip}
#
#     #_ip = json.loads(requests.get('http://localhost:5010/get/').text)['proxy']
#     #proxies = {'https': _ip}
#     # print(proxies)
#     try:
#         print('连接中')
#
#         home_url = 'https://www.lagou.com/jobs/list_Python/p-city_0-jd_2?px=default'
#         home_resp = requests.get(home_url, headers={
#             'user-agent': u1
#         }
#         #proxies=proxies
#                                  )
#         cookies = home_resp.cookies.get_dict()
#         params = {
#             'first': 'false',
#             'pn': 31,
#             'kd': 'Python',
#             'sid': 'aa85c891072f4dc1aa010837e3c82f66'
#         }
#         time.sleep(2)
#
#         content = requests.post(
#             url = 'https://www.lagou.com/jobs/positionAjax.json?jd=天使轮&px=default&needAddtionalResult=false',
#             headers = {
#                     'user-agent':u1,
#                     'X-Anit-Forge-Token':None,
#                     'X-Anit-Forge-Code':'0',
#                     'X-Requested-With':'XMLHttpRequest',
#                     'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
#                     'Referer':'https://www.lagou.com/jobs/list_Python/p-city_0-jd_8?px=default&isSchoolJob=1'
#                     },
#             # proxies = proxies,
#             data = params,
#             cookies = cookies,
#             timeout = 10
#                                 )
#         print(content.text)
#         if content.status_code == 200:
#             break
#     except Exception as e:
#         print(e)
#         times = times - 1
#         # status = requests.get(url = f'http://localhost:5010/delete/?proxy={_ip}')
#         # print(f'delete success---{status}')
#     if times == 0:
#         break
#
# json_data = json.loads(content.content)
# for each in json_data['content']['positionResult']['result']:
#         print(each['firstType'],
#               each['secondType'],
#               each['thirdType'],
#               each['district'],
#               each['jobNature']
#               )


# from urllib import parse
# str = parse.quote('上市公司')
# print(str)




