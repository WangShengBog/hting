# -*-coding: UTF-8 -*-
import logging
from sys import argv

from etc.config import config
from application import init_app

__author__ = 'bog'

logger = logging.getLogger(__name__)


logging.warning("======this is manager.py initializing app...")

if len(argv) > 1 and argv[1] == "test":
    config["default"] = config["test"]

app = init_app()


if __name__ == '__main__':
    app.logger.info("this is app.logger.info: Server start...")
    app.run("0.0.0.0", 5000, debug=True)
