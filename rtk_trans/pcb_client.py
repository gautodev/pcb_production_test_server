#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File          : pcb_client.py
# Author        : bssthu
# Project       : rtk_trans
# Description   : 
# 

import datetime
from rtk_trans import log

PCB_MAX_TTL = 60


class PcbClient:
    """PCB客户端类"""

    def __init__(self, device_id, timestamp, status):
        """构造函数"""
        super().__init__()
        self.timestamp_last_active = datetime.datetime.now()
        self.status = -1
        # set init info
        self.timestamp_init = timestamp
        self.device_id = device_id
        self.update(timestamp, status)

    def update(self, timestamp, status):
        """线程主函数

        Args:
            timestamp: 时间戳
            status: PCB板发来的心跳包
        """
        log.debug('heartbeat from %s: %s at %s' % (self.device_id, status, timestamp))
        self.timestamp_last_active = timestamp
        self.status = status

    def is_alive(self):
        now = datetime.datetime.now()
        delta_t = (now - self.timestamp_last_active).seconds
        return delta_t <= PCB_MAX_TTL
