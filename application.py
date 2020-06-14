# -*- coding: utf-8 -*-

import os

from flask import Flask, render_template
from werkzeug.exceptions import HTTPException

from etc.config import config
from utils.loggings import configure_log

__author__ = 'bog'

app = Flask(__name__)

baseDir = os.path.abspath(os.path.dirname(__file__))


def init_app():
    app.config.from_object(config["default"])
    configure_log(app)
    config["default"].init_app(app)
    if not app.debug:
        app.logger.warn("启动生产模式")

    init_framework(app)
    return app


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error/404.html"), 404


@app.errorhandler(503)
def service_unavailable(e):
    return render_template("error/503.html"), 503


@app.errorhandler(Exception)
def error_handler(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    if e:
        from traceback import format_exc
        app.logger.error(format_exc())
    return render_template("error/503.html"), code
