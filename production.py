#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File          : rtk.py
# Author        : bssthu
# Project       : pcb_production_test_server
# Description   : socket 转发数据
# 

from production.rtk_trans import Rtk


if __name__ == '__main__':
    rtk = Rtk()
    rtk.main()
