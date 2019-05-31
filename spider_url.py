import requests
from lxml import etree

from lib import downloader


class Kuaima(object):

    def __init__(self):
        self.headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
        }
        self.download = downloader.Downloader().download


    def get_url(self):
        for p in range(1,51):
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
                with open('company_url.txt','a',encoding='utf-8') as fp:
                    fp.write(company_url)
                    fp.write('\n')


kuai = Kuaima()
kuai.get_url()
