# /usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from app.common.billions_logger_py.jsonlogger import JsonFormatter
from app.common.billions_logger_py.lancerhandler import LancerStream


class LogManager(object):
    def __init__(self):
        self.logger = logging.getLogger()
        self.logHandler = logging.StreamHandler(stream=LancerStream("000069", "/var/run/lancer/collector.sock"))
        self.formatter = JsonFormatter(
            additional_fields={
                'app_id': "test.ep.fuzz"})
        self.logHandler.setFormatter(self.formatter)
        self.logger.handlers.clear()
        self.logger.addHandler(self.logHandler)
        self.logger.setLevel(logging.INFO)
