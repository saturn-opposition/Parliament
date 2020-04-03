import requests
import redis
import time
import logging
import sys
import os
from functools import wraps

pool=redis.ConnectionPool(host='127.0.0.1',port=6379,db=0)
myredis=redis.StrictRedis(connection_pool=pool)

log_file_path = os.path.dirname(os.path.abspath(__file__)) + '/log.log'
def _init_log():
    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.DEBUG)
    format_value = logging.Formatter('%(asctime)s Level:%(levelname)s File:%(filename)s Message:%(message)s',
                                     datefmt='%Y/%m/%d %H:%M:%S')
    # StreamHandler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(level=logging.DEBUG)
    stream_handler.setFormatter(format_value)
    logger.addHandler(stream_handler)

    # FileHandler
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(level=logging.WARN)
    formatter = format_value
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger
# 返回log对象
log = _init_log()

def getproxy():
    return '127.0.0.1:1080'


def request(url, header=None, method='Get', data=None, useproxies=False, retrytime=3, timeout=20, verify=True,
            allow_redirects=True):
    '''
        :param url: 请求链接
        :param header: header信息，伪装浏览器
        :param method: 请求方法 get/post
        :param data:   post方法时所带参数
        :param useproxies: 是否启用代理
        :param retrytime:   失败重试等待时间
        :param timeout:     超时时间
        :param verify:      是否验证
        :param allow_redirects:     是否允许重定向
        :param spider_name:         爬虫名
        :return:    response
        '''

    def do_request():
        _method = (getattr(requests, method.lower()))
        _request = lambda: _method(url, headers=header, params=data, proxies=proxie, timeout=(timeout, timeout),
                                   verify=verify,
                                   allow_redirects=allow_redirects) if _method.__name__ == 'get' else _method(url,
                                                                                                              data=data,
                                                                                                              headers=header,
                                                                                                              proxies=proxie,
                                                                                                              timeout=(
                                                                                                              timeout,
                                                                                                              timeout))
        r = _request()
        return r

    for _ in range(retrytime):
        try:
            proxie = {'https': 'https://' + getproxy(), 'http': 'http://' + getproxy()} if useproxies else None
            r=do_request()
            return r
        except Exception as e:
            log.warning(e)
        if _==retrytime-1:
            return None
        time.sleep(2)

def request_decoreator(fn):
    @wraps(fn)
    def wrapper(*args,**kwargs):
        for _ in range(5):
            print(fn.__name__,args)
            try:
                return fn(*args,**kwargs)
            except Exception as e:
                log.warning(f'{e},func:{fn.__name__}')
            if _==4:
                log.error(f'crawled faild with url:{args}')
                return None
    return wrapper

def create_directory(filepath):
    if not os.path.exists(filepath):
        os.makedirs(filepath)

