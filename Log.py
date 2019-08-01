# -*- coding: utf-8 -*-

import logging
import time
import os
from Utils import singleton

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))


@singleton
class Log:
    def __init__(self):
        log_path = PATH('./Log')
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        # create file handler
        fh = logging.FileHandler(os.path.join(log_path, time.strftime('%Y-%m-%d', time.localtime())+'.log'))
        fh.setLevel(logging.DEBUG)
        # create console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def __console(self, level, msg):
        if level == 'info':
            self.logger.info(msg)
        elif level == 'debug':
            self.logger.debug(msg)
        elif level == 'warning':
            self.logger.warning(msg)
        elif level == 'error':
            self.logger.error(msg)
        # self.logger.removeHandler(fh)
        # self.logger.removeHandler(ch)

    def getLogger(self):
        return self.logger

    def debug(self, msg):
        self.__console('debug', msg)

    def info(self, msg):
        self.__console('info', msg)

    def warning(self, msg):
        self.__console('warning', msg)

    def error(self, msg):
        self.__console('error', msg)


if __name__ == '__main__':
    log = Log()
    log.debug('debug:')
    log.info('info:')
    log.warning('warning:')
    log.error('error:')
