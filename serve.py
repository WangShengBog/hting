#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

__author__ = 'bog'
__doc__ = """测试两个项目共用一个日志文件会怎样"""


# -*- coding:UTF-8 -*-
from os import getpid
from utils.loggings import configure_log
from etc.config import config
from src import biz

import logging


class MockApp(object):
    def __init__(self, obj):
        self.config = {k: getattr(obj, k) for k in dir(obj) if not k.startswith('_')}
        self.debug = self.config.get("DEBUG", True)
        self.logger = logging.getLogger(__name__)


if __name__ == "__main__":
    app = MockApp(config['default'])

    config['default'].init_app(app)

    configure_log(app)
    logging.warning('serve日志进来了哈哈哈哈只')

    if not app.debug:
        app.logger.warning("启动生产模式")

