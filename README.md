# 市场行情数据爬取
#### 现已完成：
A股股票，基金历史行情数据和每日更新数据获取

#### 后续工作：
美股
获取思路： 英为财情 网站上每一支美股都可以下载历史数据，通过抓包发现如下请求url：
> https://cn.investing.com/instruments/HistoricalDataAjax

Post参数为：
> curr_id: 8258 <br> 
smlID: 1161168 <br> 
header: CHK历史数据 <br> 
st_date: 2020/02/09 <br> 
end_date: 2020/02/09 <br> 
interval_sec: Daily <br> 
sort_col: date <br> 
sort_ord: DESC <br> 
action: historical_data

但经post请求测试，返回的只是原网站主页面，原因不明，如果实在不行只能试试通过python的openstock包获取行情数据。