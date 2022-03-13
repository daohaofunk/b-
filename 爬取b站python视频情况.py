from __future__ import division
import random
import pymongo
import re
import requests
from lxml import etree
# UA伪装，UA池
MY_USER_AGENT = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    ]
# 代理伪装，代理池
proxies = ['125.66.217.114:6675','112.251.161.82:6675',
'117.34.253.157:6675','113.94.72.209:6666',
'114.105.217.144:6673','125.92.110.80:6675',
'112.235.126.55:6675','14.148.99.188:6675',
'112.240.161.20:6668','122.82.160.148:6675',
'175.30.224.66:6675']
# ua，代理随机选择，cookies这里复制的别人的
headers = {
    'User-Agent': random.choice(MY_USER_AGENT)
}
proxiess = {
    'https://': random.choice(proxies)
}
cookies = {
    "CURRENT_FNVAL": "16",
    "_uuid": "A44FDE55-496C-908C-481F-985FD001019907627infoc",
    "buvid3": "6327CADC-50E0-4418-8AFD-FC889EE49D79155823infoc",
    "LIVE_BUVID": "AUTO5615838360099805",
    "rpdid": "|(k|k)m~RR~Y0J'ul)J)JY|u|",
    "CURRENT_QUALITY": "80",
    "INTVER": "1",
    "sid": "7wuvrlef",
    "DedeUserID": "327973223",
    "DedeUserID__ckMd5": "bcb4520ee29c8085",
    "SESSDATA": "2b276f03%2C1599878752%2Cf33af*31",
    "bili_jct": "74a605aedd7eb37ea6249ae8c85ea703",
    "PVID": "11"
}
# MongoDB数据库持久化存储
def insert_mongo(data):
    client = pymongo.MongoClient()
    db = client['bilibili_python']
    database = db['data']
    database.insert_one(data)
# 获取关键字搜索下各视频号的链接
def get_ulr(key,page):
    url_list=[]
    url_list_list=[]
    for i in range(1,int(page)+1):
        url_list.append('https://search.bilibili.com/all?keyword={}&page={}'.format(key,i))
    for url in url_list:
        html=requests.get(url=url,headers=headers,proxies=proxiess,cookies=cookies,timeout=30).text
        tree = etree.HTML(html)
        if url[-1] == '1':li_list = tree.xpath('//*[@id="all-list"]/div[1]/div[2]/ul[3]/li')#首页搜索不同
        else:li_list = tree.xpath('//*[@id="all-list"]/div[1]/ul/li')#获取搜索页面的所有视频的li标签列表
        for li in li_list:
            url_list_list.append('http://'+li.xpath('./a/@href')[0][2:])
    return url_list_list
'''分析各视频页面的信息
    获取视频播放量
    点赞数
    收藏人数
    同时计算收藏率
'''
def anlays(url_list_list,page):
    number = 0#爬取详情页个数
    for url in url_list_list:
        html=requests.get(url=url,headers=headers,proxies=proxiess,cookies=cookies,timeout=30).text
        tree = etree.HTML(html)
        #分析页面的html发现存在播放量以及收藏
        bofangliang = float(tree.xpath('//*[@id="viewbox_report"]/div/span[1]/@title')[0][4:])
        dianzanshu = float(tree.xpath('//*[@id="arc_toolbar_report"]/div[1]/span[1]/@title')[0][3:])
        shoucang = tree.xpath('//*[@id="arc_toolbar_report"]/div[1]/span[3]/@title')[0][4:]
        title = tree.xpath('//*[@id="viewbox_report"]/h1/span/text()')
        #当收藏人数大于1万时页面发生变化，需要重新分析页面的收藏人数
        if len(shoucang)<1:
                # 此处try catch的目的是在爬取过程会出现有些页面请求出现问题，导致无法定位Xpath标签
                try:
                    shoucang = tree.xpath('//*[@id="arc_toolbar_report"]/div[1]/span[3]/text()')[0]
                    #正则表达，获取的文本内容为’xx.x万‘，正则表达获取前面的人数（以万为单位）
                    shoucang = float(re.findall(r'.*?(?=万)',shoucang)[0])*10000
                except Exception as e:
                    print(e)
                    print('爬取失败的网址：'+url)
        dianzanlv = dianzanshu/bofangliang*100#计算点赞率
        if shoucang!='':shoucanglv = float(shoucang)/bofangliang*100#计算收藏率
        else:shoucanglv =None
        #用字典的形式存放每个视频的信息
        dic={
            'title':title,
            'bofangliang' :bofangliang,
            'shoucanglv':shoucanglv,
            'dianzanglv':dianzanlv
        }
        insert_mongo(dic)
        number+=1
        if number%20==0:
            page_info = number/20
            print('\033[32;1m第%s共%s页信息爬取完成...\033[0m' % (page_info,page))
## 主函数程序
if __name__ =='__main__':
    #1.获取关键字和需要爬取的页数
    search_name = input('\033[32;1m您想要爬取的视频关键字是？\n\033[37;1m(输入完毕请按回车)：\033[0m')
    pages = input('\033[32;1m您想要爬取总页数？\n\033[37;1m(输入完毕请按回车)：\033[0m')
    #2.获得所有需要爬取的视频详情页的url
    url_list = get_ulr(search_name, pages)
    #3.分析详情页的信息
    anlays(url_list,pages)
