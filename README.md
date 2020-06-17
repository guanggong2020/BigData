## 市场行情爬取系统
### 已实现爬取的网站：
东方财富网、天天基金网、网易财经、纳斯达克</br>
英为财情、拉勾网

#### 使用指南
1. scrapy：存放由scrapy框架编写的爬虫脚本
2. 历史数据爬取：存放爬取历史数据的脚本
```
命令形式: py main.py [爬取数据类型] [起始时间] [结束时间]
时间形式: YYYY-MM-DD
爬取数据类型: A--A股，F--基金，Z--指数，U--美股
```
3. scrapy-pyinstaller:经过pyinstaller打包后的爬虫脚本,启动方式：运行dist/start/start.exe
4. 数据分析

#### 国内股票、基金、指数的数据字段名：
date  日期</br>
code : 股票/基金代码</br>
name : 名称</br>
closingPrice : 收盘价</br>
maxPrice : 最高价</br>
minPrice : 最低价</br>
openingPrice : 开盘价</br>
previousClose : 前收盘</br>
change : 涨跌额</br>
quoteChange : 涨跌幅</br>
turnoverRate : 换手率</br>
volume : 成交量</br>
turnover : 成交金额</br>
totalMarketCapitalization : 总市值</br>
marketCapitalization : 流通市值</br>

 fundName : 基金名称</br>
 unitNetWorth : 单位净值</br>
 cumulativeNetWorth : 累计净值</br>
 growthRate : 增长率</br>
 amplitude : 振幅</br>
 QRR : 量比

#### 美股的数据字段名：
date : 日期</br>
code : 股票/基金代码</br>
name : 名称</br>
latestPrice : 最新价</br>
maxPrice : 最高价</br>
minPrice : 最低价</br>
openingPrice : 开盘价</br>
previousClose : 前收盘</br>
change : 涨跌额</br>
quoteChange : 涨跌幅(百分数)</br>
turnoverRate : 换手率(百分数)</br>
volume : 成交量</br>
turnover : 成交金额</br>
totalMarketCapitalization : 总市值(美元)</br>
amplitude : 振幅(百分数)</br>
PER : 市盈率(百分数)</br>
QRR : 量比</br>
PBR : 市净率(百分数)</br>
TTM : 上市时间</br>
EPS : 每股收益</br>
NAVPS : 每股净资产

#### 美国基金的数据字段名：
date : 日期</br>
code : 代码</br>
fundName : 基金名称</br>
closingPrice : 收盘价</br>
previousClose : 前收盘</br>
growthRate : 增长率(百分数)</br>
change : 涨跌额</br>
OneYearChange : 一年涨跌幅</br>
turnover : 周转率</br>
MorningstarRating : 晨星评级</br>
RiskRating : 风险评级</br>
TTMYield : 过去十二个月收益率</br>
ROE : ROE</br>
ROA : ROA</br>
YTDFundReturn : 年初至今基金回报</br>
ThreeMonthFundReturn : 三个月基金回报</br>
OneYearFundReturn : 一年基金回报</br>
ThreeYearFundReturn : 三年基金回报</br>
FiveYearFundReturn : 五年基金回报</br>
TotalAssets : 总资产</br>
totalMarketCapitalization : 市值</br>
company : 发行商

#### 拉勾网的数据字段名：
职位链接id： positionId</br>
职位名称： positionName</br>
职业第一类别： firstType</br>
职业第二类别： secondType</br>
职业第三类别： thirdType</br>
技能标签： skillLables</br>
薪水： salary</br>
工作城市： city</br>
地区： district</br>
经验要求： workYear</br>
学历要求： education</br>
工作优点： positionAdvantage</br>
工作性质： jobNature</br>
公司全称： companyFullName</br>
公司缩称： companyShortName</br>
公司规模： companySize</br>
产业领域： industryField</br>
融资阶段： financeStage

