#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os.path import splitext
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import logging

__author__ = 'bog'

logger = logging.getLogger(__name__)

log_format = '[%(asctime)s %(levelname)s] [in %(pathname)s:%(lineno)d]\n%(message)s'


def get_rotatinghandler(level, name, size, count):
    hndr = RotatingFileHandler(name, mode="a", maxBytes=size, backupCount=count, encoding="utf-8")
    hndr.setLevel(level)
    hndr.setFormatter(logging.Formatter(log_format))
    return hndr


def get_timedhandler(level, name, when, count):
    hndr = TimedRotatingFileHandler(name, when=when, interval=1, backupCount=count, encoding="utf-8")
    hndr.setLevel(level)
    hndr.setFormatter(logging.Formatter(log_format))
    return hndr


def log_filename(filename, levelname):
    x = splitext(filename)
    return "".join([x[0], levelname, x[1]])


def get_mongohandler(collection, db='mongolog', host='localhost', port=None,
        username=None, password=None, level=logging.NOTSET):
    """获取mongodb日志处理器
    :param collection 数据集
    :param db 数据库
    :param host 连接地址
    :param port 端口 默认27017
    :param username 登录名
    :param password 密码
    :param level 日志级别
    """
    from mongolog.handlers import MongoHandler
    hndr = MongoHandler.to(collection, db, host, port, username, password, level)
    return hndr


def configure_log(app):
    logger.info("configuring log: app.debug={}, app.config['DEBUG']={}".format(str(app.debug), str(app.config.get("DEBUG"))))
    if app.debug:
        logging.basicConfig(level=logging.DEBUG, format=log_format)
    else:
        filename = app.config.get('LOG_FILEPATH')
        error_handler = get_timedhandler(logging.ERROR,
                                         log_filename(filename, ".error"),
                                         'midnight',
                                         app.config.get('LOG_DAYS', 1))

        warning_handler = get_timedhandler(logging.WARNING,
                                           log_filename(filename, ".warn"),
                                           'midnight',
                                           app.config.get('LOG_DAYS', 1))

        info_handler = get_rotatinghandler(logging.INFO,
                                           log_filename(filename, ".info"),
                                           app.config.get('LOG_SIZE', 50 * 1024 * 1024),
                                           app.config.get('LOG_COUNT', 1))

        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        root_logger.addHandler(error_handler)
        root_logger.addHandler(warning_handler)
        root_logger.addHandler(info_handler)

        if app.logger:
            root_logger.info("this is root_logger logging: app.logger is True, configuring app_logger.......")
            app.logger.setLevel(logging.INFO)
            app.logger.addHandler(error_handler)
            app.logger.addHandler(info_handler)
            app.logger.addHandler(warning_handler)

        if app.config.get("LOG_SQL", False):
            sql_handler = get_rotatinghandler(logging.INFO,
                                              log_filename(filename, ".sql"),
                                              app.config.get('LOG_SIZE', 50 * 1024 * 1024),
                                              app.config.get('LOG_COUNT', 1))
            sql_logger = logging.getLogger("SQL")
            sql_logger.addHandler(sql_handler)

        if app.config.get("LOG_NOTICE", False):
            notice_handler = get_timedhandler(logging.INFO,
                                              log_filename(filename, ".notice"),
                                              'midnight',
                                              30)
            notice_logger = logging.getLogger("notice")
            notice_logger.addHandler(notice_handler)

        if app.config.get("MONGO_LOG"):
            mongo_handler = get_mongohandler(**app.config.get("MONGO_LOG"))
            if app.logger:
                app.logger.addHandler(mongo_handler)
            root_logger.addHandler(mongo_handler)
