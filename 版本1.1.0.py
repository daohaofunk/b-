from __future__ import division
import random
import pymongo
import re
import requests
# UA伪装，UA池
MY_USER_AGENT = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
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
proxies = ['125.66.217.114:6675', '112.251.161.82:6675',
           '117.34.253.157:6675', '113.94.72.209:6666',
           '114.105.217.144:6673', '125.92.110.80:6675',
           '112.235.126.55:6675', '14.148.99.188:6675',
           '112.240.161.20:6668', '122.82.160.148:6675',
           '175.30.224.66:6675']
# ua，代理随机选择，cookies这里复制的别人的
headers = {
    'User-Agent': random.choice(MY_USER_AGENT),
}
proxiess = {
    'https://': random.choice(proxies),
}


# MongoDB数据库持久化存储
def insert_mongo(data):
    client = pymongo.MongoClient()
    db = client['bilibili_python']
    database = db['data']
    database.insert_one(data)


# 获取每页的json包并解析
def analys(keyword, pages):
    for page in range(1,int(pages) + 1):
        url = "https://api.bilibili.com/x/web-interface/search/all/v2"
        if page == 1:
            data = {
                '__refresh__': 'true',
                '_extra': '',
                'context': None,
                'page': str(page),
                'page_size': '42',
                'order': None,
                'duration': None,
                'from_source': None,
                'from_spmid': '333.337',
                'platform': 'pc',
                'highlight': '1',
                'single_column': '0',
                'keyword': keyword,
                'preload': 'true',
                'com2co': 'true',
            }
        else:
            data = {
                '__refresh__': 'true',
                '_extra': None,
                'context': None,
                'page': str(page),
                'page_size': '42',
                'from_source': None,
                'from_spmid': '333.337',
                'platform': 'pc',
                'highlight': '1',
                'single_column': '0',
                'keyword': keyword,
                'category_id': None,
                'search_type': 'video',
                'dynamic_offset': '36',
                'preload': 'true',
                'com2co': 'true',
            }
        responce = requests.get(url=url, params=data, headers=headers)
        for content in responce.json()['data']['result'][10]['data']:
            title = content['title']
            bofanglang = content['play']
            shoucang = content['favorites']
            dianzan = content['like']
            try:
                shoucanglv = float(shoucang)/float(bofanglang)*100
                dianzanlv =float(dianzan)/float(bofanglang)*100
            except:
                pass
            dic = {
                #正则表达式去除html标签
                "标题": re.sub(r'</?\w+[^>]*>','',title),
                "播放量":bofanglang,
                "收藏人数": shoucang,
                "点赞人数": dianzan,
                "收藏率":shoucanglv,
                "点赞率":dianzanlv,
            }
            insert_mongo(dic)
        print('\033[32;1m第%s共%s页信息爬取完成...\033[0m' % (page, pages))


## 主函数程序
if __name__ == '__main__':
    # 1.获取关键字和需要爬取的页数
    search_name = input('\033[32;1m您想要爬取的视频关键字是？\n\033[37;1m(输入完毕请按回车)：\033[0m')
    pages = input('\033[32;1m您想要爬取总页数？\n\033[37;1m(输入完毕请按回车)：\033[0m')
    # 2.分析每个页面的json包
    analys(search_name, pages)
