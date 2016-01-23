#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File          : log.py
# Author        : bssthu
# Project       : rtk_trans
# Description   : socket 转发数据
# 

import logging
from logging import handlers


logger = None


def initialize_logging(tofile=True):
    global logger
    logger = logging.getLogger('rtk')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # to file
    if tofile:
        fh = logging.handlers.RotatingFileHandler('logs/rtk.log', backupCount=20)
        fh.setLevel(logging.DEBUG)
        fh.doRollover()
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    # to screen
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def debug(msg, *args, **kwargs):
    logger.debug(msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    logger.info(msg, *args, **kwargs)


def warning(msg, *args, **kwargs):
    logger.warning(msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    logger.error(msg, *args, **kwargs)


def critical(msg, *args, **kwargs):
    logger.critical(msg, *args, **kwargs)


def log(lvl, msg, *args, **kwargs):
    logger.log(lvl, msg, *args, **kwargs)
