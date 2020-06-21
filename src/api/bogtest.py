# -*-coding: UTF-8 -*-

import logging
import time

from flask_restplus import Resource

from src.dtos import bogtest

__author__ = 'bog'

logger = logging.getLogger(__name__)

api = bogtest.api


@api.route("/hello")
class HelloRestAPI(Resource):
    @api.doc("HelloWorldDoc")
    @api.param("this", "is", "api.param")
    def get(self):
        logger.info("this is in hello/get")
        return {"hello": "world"}
