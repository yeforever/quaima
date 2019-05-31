import requests
import socket
import time
from lib.kuaidaili import NOLIMIT_PROXY_REDIS_NAME
from lib.rediscli import redis_cli


class Downloader(object):
    def __init__(self):
        self.req = requests.Session()
        self.change_proxy()

    def download(self, url):
        time.sleep(2)
        print('正在下载页面：', url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        }
        try:
            response = requests.get(url=url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            html = response.text
            # print(html)
            if '由于您的访问太过于频繁，您的IP被封！' in html:
                self.change_proxy()
                return self.download(url)
            # print(html)
            return html
        except socket.timeout:
            return self.download(url)
        except requests.exceptions.ReadTimeout:
            return self.download(url)
        except Exception as e:
            print('其他异常，开始变更IP：', str(e))
            self.change_proxy()
            return self.download(url)

    def change_proxy(self):
        print('Change proxy.....')
        while True:
            proxy_host_port = redis_cli.rpop(NOLIMIT_PROXY_REDIS_NAME)
            if proxy_host_port is not None:
                self.proxy_host_port = proxy_host_port.decode('ascii')
                break
            print('No IP in Redis, wait 5s.....')
            time.sleep(5)
        self.req.proxies = {
            "http": self.proxy_host_port,
            "https": self.proxy_host_port
        }
        print('New proxy: {0}'.format(self.proxy_host_port))
# d = Downloader()
# doc = d.download('https://su.58.com/tech/')
# print(doc)
