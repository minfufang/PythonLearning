#encoding:utf-8
import urllib.request
from lxml import etree

def get_html(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    return html.decode('utf-8')

def getfilmDict():
    raw_html = get_html('https://dianying.taobao.com/showList.htm')
    html_etree = etree.HTML(raw_html)

    result = html_etree.xpath('//div[@class="movie-card-wrap"]')

    filmDic = {}
    count = 0
    for r in result:
        #print(etree.tostring(r))
        etreeR = etree.HTML(etree.tostring(r))
        imgEle = etreeR.xpath('//img')
        imgurl = imgEle[0].xpath('//@src')[0]
        name = etreeR.xpath('//div[@class="movie-card-name"]/span[@class="bt-l"]')[0].text

        count += 1

        # print(imgurl,name)
        if  not filmDic.keys().__contains__(name):
            filmDic[name] = imgurl
    return filmDic


import pymongo
from bson.objectid import ObjectId

client = pymongo.MongoClient('mongodb://account:password@207.0.0.1:27017/')
db = client.test
collection = db.test01

filmDic = getfilmDict()

for key in filmDic.keys():
    find = collection.find({"Name":key}).count()
    if find < 1:
        doc = {"Name":key,"URL":filmDic[key]}
        collection.insert(doc)
    else:
        print(key,' inserted!')
