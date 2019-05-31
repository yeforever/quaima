import redis
import requests
import socket
import time

import urllib3

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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
        }
        try:
            response = requests.get(url=url, headers=headers, timeout=10)
            response.encoding = 'GBK'
            html = response.text

            # print(html)
            if '../404.htm' in html:
                return None

            if '没有找到您要访问的页面，请检查您是否输入正确URL。' in html:
                return html

            # print(html)
            return html
        except socket.timeout:
            return self.download(url)
        except requests.exceptions.ReadTimeout:
            return self.download(url)
        # except Exception as e:
        #     print('其他异常，开始变更IP：', str(e))
        #     self.change_proxy()
        #     return self.download(url)
        except requests.exceptions.ConnectionError:
            self.change_proxy()
            return self.download(url)
        except OSError:
            self.change_proxy()
            return self.download(url)
        except urllib3.exceptions.NewConnectionError:
            self.change_proxy()
            return self.download(url)
        except redis.exceptions.ConnectionError:
            self.change_proxy()
            return self.download(url)
        except ConnectionRefusedError:
            self.change_proxy()
            return self.download(url)
        except ConnectionResetError:
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
