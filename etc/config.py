# -*- coding: utf-8 -*-
import os
import logging

__author__ = 'bog'

logger = logging.getLogger(__name__)

project_base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class Config(object):
    """
    基础配置
    """

    # 数据库
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') \
                              or "mysql+pymysql://root:123456@127.0.0.1:3306/ihospital?charset=utf8mb4"
    # 日志目录
    LOG_FILEPATH = project_base_dir + r"/logs/ht_log"

    @staticmethod
    def init_app(app):
        pass


class DevCfg(Config):
    """
    开发配置
    """
    logger.info("configuring DevCfg...")
    pass


class ProdCfg(Config):
    """
    生产配置
    """
    logger.info("configuring ProdCfg...")
    pass


config = {
    "development": DevCfg,  # 开发环境
    "production": ProdCfg,  # 生产环境
    "default": ProdCfg,  # 默认, 生产环境
}


if __name__ == '__main__':
    print(project_base_dir + r"\logs\ht_log")
