# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template
from etc.config import config

__author__ = 'bog'

app = Flask(__name__)

baseDir = os.path.abspath(os.path.dirname(__file__))


def init_app():
    app.config.from_object(config["default"])
    configure_log(app)

