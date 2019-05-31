import logging
import os
import time
import requests
from lib.rediscli import redis_cli

NOLIMIT_PROXY_REDIS_NAME = 'nolimit_proxy'
GT10_PROXY_REDIS_NAME = 'gt10_proxy'
GT30_PROXY_REDIS_NAME = 'gt30_proxy'


class KuaiDaiLi(object):
    def __init__(self):
        self.name = 'KuaiDaiLi'
        self.logger = logging.getLogger(self.name)
        curr_path = os.path.dirname(__file__)
        fh = logging.FileHandler(
            '{curr_path}/../../log/{filename}.log'.format(curr_path=curr_path, filename=self.name), 'a'
        )
        fh.setLevel(logging.INFO)
        fh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(fh)

        # 不筛选的
        self.nolimit_url = 'https://dps.kdlapi.com/api/getdps/?orderid=985109353445428&num=100&pt=1&format=json&sep=1'
        # 大于10min
        self.gt10_url = 'https://dps.kdlapi.com/api/getdps/?orderid=985109353445428&num=100&pt=1&ut=1&format=json&sep=1'
        # 大于30min
        self.gt30_url = 'https://dps.kdlapi.com/api/getdps/?orderid=985109353445428&num=100&pt=1&ut=2&format=json&sep=1'

    def put_in_redis(self):
        while True:
            try:
                # 不限制
                if redis_cli.llen(NOLIMIT_PROXY_REDIS_NAME) == 0:
                    response = requests.get(self.nolimit_url, timeout=10)
                    proxy_list = response.json()['data']['proxy_list']
                    for one_proxy in proxy_list:
                        redis_cli.lpush(NOLIMIT_PROXY_REDIS_NAME, one_proxy)
                        self.logger.info('Put {ip} in {name}...'.format(ip=one_proxy, name=NOLIMIT_PROXY_REDIS_NAME))

                # 大于10min
                if redis_cli.llen(GT10_PROXY_REDIS_NAME) == 0:
                    response = requests.get(self.gt10_url, timeout=10)
                    proxy_list = response.json()['data']['proxy_list']
                    for one_proxy in proxy_list:
                        redis_cli.lpush(GT10_PROXY_REDIS_NAME, one_proxy)
                        self.logger.info('Put {ip} in {name}...'.format(ip=one_proxy, name=GT10_PROXY_REDIS_NAME))

                # 大于30min
                if redis_cli.llen(GT30_PROXY_REDIS_NAME) == 0:
                    response = requests.get(self.gt30_url, timeout=10)
                    proxy_list = response.json()['data']['proxy_list']
                    for one_proxy in proxy_list:
                        redis_cli.lpush(GT30_PROXY_REDIS_NAME, one_proxy)
                        self.logger.info('Put {ip} in {name}...'.format(ip=one_proxy, name=GT30_PROXY_REDIS_NAME))
                self.logger.info('Sleep 30s....')
                time.sleep(30)
            except Exception as e:
                self.logger.error(e)
                time.sleep(30)
                continue
