# -*-coding: UTF-8 -*-

import logging
import time

from flask_restplus import Resource
from flask import Response

from src.dtos import bogtest
from src.biz.bogtest import get_url

__author__ = 'bog'

logger = logging.getLogger(__name__)

api = bogtest.api


@api.route("/hello")
class HelloRestAPI(Resource):
    @api.doc("HelloWorldDoc")
    @api.param("this", "is", "api.param")
    def get(self):
        code, data = get_url()
        logger.info("this is in hello/get")
        return data
