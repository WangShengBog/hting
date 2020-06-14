# -*-coding: UTF-8 -*-

import logging

from utils import file_upload
from src.biz import sql_execute

__author__ = 'bog'


logger = logging.getLogger(__name__)


def init(app):
    from src import api, biz
    biz.init(app)
    api.init(app)

    # file_upload.init(app.config["MR_IMG_HTTP_BASE"], app.config["MR_IMG_PATH_BASE"])
    sql_execute.init(app)

