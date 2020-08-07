#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import requests
import time
import json
import os
from traceback import format_exc
import urllib


__author__ = 'bog'
__doc__ = """模拟服务"""

logger = logging.getLogger(__name__)



class ApiService(object):
    """服务"""


    def __init__(self, base_url):
        """构造一个服务新实例
        self.base_url: 平台接口地址
        """
        self.base_url = base_url

    def test(self):
        pass

    def _invoke(self, url, data, method='POST'):
        """调用接口
        #param @url 接口地址
        #param @data 请求参数对象
        #return 返回调用结果的json对象
        """
        headers = {}
        res = None
        start = time.time()
        try:
            if not url.startswith(self.base_url):
                url = self.base_url + url
            if method == 'POST':
                res = requests.post(headers=headers, url=url, json=data)
            elif method == 'PUT':
                res = requests.put(headers=headers, url=url, data=data)
            elif method == 'GET':
                # res = requests.get(headers=headers, url=url, params=data, cert=(self.domain_ssl_cert_path,
                #                                                                 self.domain_ssl_key_path))
                res = requests.get(headers=headers, url=url, params=data)
            end = time.time()
            result_json = res.content.decode()
            logger.info(f"请求接口: 执行耗时:{end-start} \n请求url:{url} \n请求参数:{str(data)}  "
                        f"\n返回参数:{result_json}")
        except Exception as e:
            logger.error(format_exc())
            logger.error(f'请求错误: \n  请求url: {url}\n  请求参数: {str(data)}')
            return 500, f'error: {str(e)}'
        try:
            result = json.loads(result_json)
            return res.status_code, result
        except Exception as e:
            logger.error(format_exc())
            result = {'message': f'错误编码:{res.status_code}', 'error': str(e)}
            return 500, result


if __name__ == '__main__':
    import requests
    url = 'http://192.168.3.204:9301/agsupport-data/resource/view/图片资源/cim图层树天河影像底图/地面影像地图.jpg'
    res = requests.get(url)
    print(res)