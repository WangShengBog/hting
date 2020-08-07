#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'bog 这是作者: 本神'
__doc__ = """这是这个文件的说明"""

from flask import Flask, request

app = Flask(__name__)

class Config(object):
    """这个也可以写到别的py文件之后import到这个文件"""
    pass

# 导配置
app.config.from_object(Config)


# 这是一个接口
@app.route('/test', methods=['POST'])
def test():
    """这里写接口说明"""
    req_data = request.json  # request.json 就是前端用post请求从body传的json在这里就是自动转为python的dict
    url1 = req_data.get('url1', '')
    url2 = req_data.get('url2', '')
    url3 = req_data.get('url3', '')
    code, data = test2(url1, url2, url3)
    if code != 200:
        return {'错误': "sldfljk"}
    else:
        return data

def test2(url1, url2, url3):
    """这个函数也可以写到别的py文件里然后import到这里用"""
    data = {'测试成功': 12345}

    return 200, data


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=True)
