#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File          : sender_thread.py
# Author        : bssthu
# Project       : rtk_trans
# Description   :
#

import socket
import threading
import queue
import datetime
from production import log


class SenderThread(threading.Thread):
    """负责与一个客户端通信的线程"""

    def __init__(self, client_socket, address, _id, got_heartbeat_cb):
        """构造函数

        Args:
            client_socket: 与客户端通信的 socket
            address: 客户端地址
            _id: SenderThread 的 ID
            got_heartbeat_cb: 接收到心跳包的回调函数
        """
        super().__init__()
        self.client_socket = client_socket
        self.address = address
        self.sender_id = _id
        self.got_heartbeat_cb = got_heartbeat_cb
        self.data_queue = queue.Queue()
        self.data_received = ''
        self.send_count = 0
        self.running = True

    def run(self):
        """线程主函数

        循环运行，接收来自客户端的数据并丢弃，向客户端发送 data_queue 中的数据包。
        当 data_queue 过长时，丢弃旧的数据包。
        """
        log.info('sender thread %d: start, %s' % (self.sender_id, self.address))
        while self.running:
            try:
                # ignore old data
                if self.data_queue.qsize() > 10:
                    self.data_queue.empty()
                # send data
                try:
                    data = self.data_queue.get(timeout=1)
                    self.client_socket.settimeout(5)
                    self.client_socket.sendall(data)
                    self.send_count += 1
                    self.data_queue.task_done()
                except queue.Empty:
                    pass
                except ValueError as e:
                    log.warning('sender thread %d ValueError: %s' % (self.sender_id, e))
                # rcv heartbeat data
                try:
                    self.client_socket.settimeout(1)
                    new_recv_data = self.client_socket.recv(1024)
                    if len(new_recv_data) > 0:
                        self.data_received += new_recv_data.decode(encoding='utf-8', errors='ignore')
                    self.parse_heartbeat_recv_buffer()  # 分包
                except socket.timeout:
                    pass
            except Exception as e:
                log.error('sender thread %d error: %s' % (self.sender_id, e))
                self.running = False
        self.disconnect()
        log.info('sender thread %d: bye' % self.sender_id)

    def disconnect(self):
        """断开连接"""
        try:
            self.client_socket.close()
        except socket.error:
            pass
        except Exception as e:
            log.error('sender thread %d exception when close: %s' % (self.sender_id, e))

    def parse_heartbeat_recv_buffer(self):
        """对收到的心跳包进行分包处理，并通知

        心跳包格式为：
        设备ID-解状态\r\n
        """
        heartbeats = self.data_received.split('\r')
        if len(heartbeats) > 1:
            self.data_received = heartbeats[-1]     # 只有一个线程访问 self.data_received
            now = datetime.datetime.now()
            for heartbeat_str in heartbeats[:-1]:
                if heartbeat_str.startswith('\n'):
                    self.got_heartbeat_cb(self.sender_id, heartbeat_str[1:], now)
