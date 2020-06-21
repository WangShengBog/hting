# -*-coding: UTF-8 -*-

__author__ = 'bog'

import logging

from flask import make_response, url_for
from flask_restplus import Api


class CustomApi(Api):
    @property
    def specs_url(self):
        """
        The Swagger specifications absolute url (ie. `swagger.json`)
        :return: str
        """
        return url_for(self.endpoint("specs"), _external=False)


def init(app):
    """
    :param app:
    :return:
    """

    @app.after_request
    def af_request(resp):
        """
        请求钩子, 在所有的请求发生后执行, 加入headers
        :param resp:
        :return:
        """
        resp = make_response(resp)
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE"
        resp.headers["Access-Control-Allow-Headers"] = "x-requested-with, content-type"
        return resp

    from src.api.bogtest import api as test_api

    doc_api = CustomApi(title="博神抄作", version='1.0', description=__api_doc_description, ordered=True,
                        doc='/swagger/index.html')

    doc_api.add_namespace(test_api, path="/api/test")

    doc_api.init_app(app)

__api_doc_description = """
<details>
<summary>协议规则</summary>
## 协议规则

### 传输方式
#### RESTful API 接口规范
#### 操作
* GET 从服务器检索特定资源，或资源列表
* POST 在服务器上创建一个新的资源
* PUT 更新服务器上的资源，提供整个资源
* DELETE 从服务器删除资源

#### 路径
* GET /resource 获取所有资源（部分资源,条件参考过滤信息）
* POST /resource 新建一个资源
* PUT /resource/{id} 更新指定id资源
* DELETE /resource/{id} 删除指定id资源

#### 过滤信息
* ?keyword=kw 查询关键字
* ?page=1&limit=20 分页查询 page:查询页,limit:每页大小
* ?sortby=create_time&order=desc 排序 sortby:排序字段,order:排序方式 asc/desc
* ?xx_id=1&xx_xx=value 指定刷选条件

#### 状态码 ([*]标识所有GET/POST/PUT/DELETE操作)
* 200 - [*]服务器成功返回用户请求信息。
* 400 - [*]用户发出的请求有错误（请求的数据验证不通过）。
* 401 - [*]表示用户没有权限（令牌、用户名、密码错误）。
* 403 - [*]表示用户得到授权（与401错误相对），但是访问是被禁止的。
* 404 - [*]用户发出的请求针对的是不存在的记录。
* 500 - [*]服务器发生错误。
* 502 - [*]网关错误
* 503 - [*]服务不可用(可能是连接数太多,或应用程序池假死)
* 504 - [*]网关超时

### 数据格式
标准JSON格式
统一格式
{
    "result":any,
    "error":{
        "code":"错误编码",
        "message":"错误信息",
        "details":"详细信息"
    }
}
返回200 处理 result, result结构参考对应接口的实际返回数据; 
返回其他处理error
### 字符编码
统一采用UTF-8编码


### 安全规则

#### HTTP 消息通用参数
名称|说明|必填
-|-|-
X-AppId|应用ID|必填
X-Authorization|登录令牌|登录后必填
X-Nonce|随机数|非web应用必填
X-Timestamp|UTC时间戳|非web应用必填
X-Sign|签名|非web应用必填
X-Channel|渠道|必填
X-Version|软件版本|选填
X-OS|手机系统版本|选填

#### 签名算法
将 AppSecret, X-Nonce, X-Timestamp, 请求URL 按字典序排序后，采用Sha256签名算法，再base64编码，写入X-Sign。

</details>
"""

