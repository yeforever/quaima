import re
import threading
import time
from queue import Queue

import pymongo
import requests
from lxml import etree

from lib import downloader


class Kuaima(object):

    def __init__(self):
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
        }
        self.download = downloader.Downloader().download
        self.client = pymongo.MongoClient('192.168.0.153', port=27017)
        self.db = self.client.edition
        self.db.authenticate("wangkun", 'wk123456')
        self.contact = self.db['contact']

    # def get_url(self,url_que):
    #     with open('D:/Projects/kuaima/company_url.txt','r',encoding='utf-8') as fp:
    #         urls = fp.readlines()
    #         for url in urls:
    #             url = url.strip()
    #             url_que.put(url)

    def get_url(self,url_que):
        for p in range(1,3):
            url = 'http://www.kmfxx.cn/qiye/{}'.format(p)
            # req = requests.get(url,headers=self.headers)
            # req.encoding = 'gb2312'
            # html = req.text
            html = self.download(url)
            # print(html)

            tree = etree.HTML(html)
            urls = tree.xpath('//*[@id="infolist"]/table/tr/td[1]/a/@href')
            for company_url in urls:
                company_url = company_url + '/liuyan00/'
                print(company_url)
                url_que.put(company_url)
                # with open('company_url.txt','a',encoding='utf-8') as fp:
                #     fp.write(company_url)
                #     fp.write('\n')

    def parse_url(self,url_que):
        while True:
            url = url_que.get()
            print("还剩余:",url_que.qsize())
            # req = requests.get(url,headers=self.headers)
            # req.encoding = 'gb2312'
            # html = req.text
            html = self.download(url)
            # print(html)
            if html is None:
                continue
            tree = etree.HTML(html)
            print(url)
            # title = tree.xpath('//div[@class="content"]//div[@class="main"]/div//div[@class="box"]/div/p/text()')
            # if
            info = {}
            company_names = tree.xpath("//p[contains(text(), '单位名称：')]/text()")
            for company_name in company_names:
                company_name = company_name.strip()
                company_name = company_name.split("：")[1]
                info['company_name'] = company_name
                print(company_name)

            name = tree.xpath("//p[contains(text(), '联系人：')]/text()")[0].strip()
            name = name.split('：')[1]
            info['name'] = name
            print(name)

            tel = tree.xpath("//p[contains(text(), '联系电话：')]/text()")[0].strip()
            tel = tel.split("：")[1]
            info['tel'] = tel
            print(tel)

            address = tree.xpath("//p[contains(text(), '联系地址：')]/text()")[0].strip()
            address = address.split('：')[1].replace(' ','')
            info['address'] = address
            print(address)

            qqs = tree.xpath("//p[contains(text(), '联系QQ：')]/a[1]/@href")
            for qq in qqs:
                qq = re.search(r'(uin=)(.*?)(&)', qq).group(2)
                print(qq)


                self.contact.update_one({'company_name': company_name}, {
                                '$addToSet': {'address': address,'qq':qq},
                                '$set': {'update_time': time.strftime(
                                    "%Y-%m-%d"), 'add': '1'}}, upsert=True)


            if 'name' in info.keys():
                if info['name'] != "":
                    if info['tel'] != "":
                        info['tel'] = info['name'] + ":" + info['tel']
                        contact_num = info['tel']
                        print("组合的联系人", contact_num)
                        company_name = info['company_name']
                        self.contact.update_one({'company_name': company_name}, {
                            '$addToSet': {'contact_num': contact_num},
                            '$set': {'update_time': time.strftime(
                                "%Y-%m-%d"), 'add': '1'}}, upsert=True)
                else:
                    info['name'] = '未知'
                    if info['tel'] != "":
                        info['tel'] = info['name'] + ":" + info['tel']
                        contact_num = info['tel']
                        print("组合的联系人", contact_num)
                        company_name = info['company_name']
                        self.contact.update_one({'company_name': company_name}, {
                            '$addToSet': {'contact_num': contact_num},
                            '$set': {'update_time': time.strftime(
                                "%Y-%m-%d"), 'add': '1'}}, upsert=True)







            if url_que.empty():
                break

url_queue = Queue()
kuai = Kuaima()
kuai.get_url(url_queue)
# kuai.parse_url(url_queue)

t2 = []
for t in range(1):
    k = Kuaima()
    threads = threading.Thread(target=k.parse_url, args=(url_queue,))
    threads.start()
    t2.append(threads)
for i in t2:
    i.join()