#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File          : pcb_manager.py
# Author        : bssthu
# Project       : rtk_trans
# Description   : 
# 

import threading
from production.pcb_client import PcbClient
from production import utils
from production import log


class PcbManager:
    """维护客户端的心跳信息"""

    def __init__(self):
        """构造函数"""
        super().__init__()
        self.pcbs = {}
        self.lock = threading.Lock()

    def on_recv_heartbeat(self, sender_id, heartbeat, timestamp):
        """收到一条完整心跳包时的处理函数

        由各 sender_thread 调用

        Args:
            sender_id: 收到心跳包的线程 ID
            heartbeat (bytes): 心跳包
            timestamp: 收到心跳包的时间
        """
        log.debug('pcb manager: from sender %d: %s' % (sender_id, heartbeat))
        self.lock.acquire()
        try:
            self.parse_heartbeat(heartbeat, timestamp)
        except Exception as e:
            log.error('pcb manager: when parse from sender %d: %s' % (sender_id, e))
        self.lock.release()

    def parse_heartbeat(self, heartbeat, timestamp):
        """解析心跳包，更新列表

        Args:
            heartbeat (bytes): 心跳包
            timestamp: 收到心跳包的时间
        """
        uuid, status = utils.split(heartbeat, b'-')

        # uuid 一定是可见 ASCII 字符，长度为 12
        uuid = uuid.strip()
        if len(uuid) < 12:
            return

        # 更新 pcb 表
        pcb = self.pcbs.get(uuid)
        if pcb is None:
            pcb = PcbClient(uuid, timestamp, status)
            self.pcbs[uuid] = pcb
        else:
            pcb.update(timestamp, status)

    def get_active_pcbs_info(self):
        """读取当前客户列表"""
        pcb_info_list = b''

        # 检查 pcb 表
        self.lock.acquire()
        try:
            for device_id, pcb in self.pcbs.copy().items():
                if not pcb.is_alive():
                    del self.pcbs[device_id]
                else:
                    line = (
                        pcb.device_id, pcb.status,
                        bytes(pcb.timestamp_init.strftime('%Y/%m/%d,%H:%M:%S'), 'utf-8'),
                        bytes(pcb.timestamp_last_active.strftime('%Y/%m/%d,%H:%M:%S'), 'utf-8')
                    )
                    pcb_info_list += b'-'.join(line) + b'\r\n'
        except Exception as e:
            log.error('pcb manager: when get pcb info: %s' % e)
        self.lock.release()

        return bytes('%d\r\n' % len(pcb_info_list), 'utf-8') + pcb_info_list + b'$bye\r\n'
