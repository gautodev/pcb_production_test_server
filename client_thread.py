#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File          : client_thread.py
# Author        : bssthu
# Project       : rtk_trans
# Description   : 
# 

import socket
import threading
import time
import log

BUFFER_SIZE = 4096


class ClientThread(threading.Thread):
    def __init__(self, server_ip, server_port, got_data_cb):
        super().__init__()
        self.server_ip = server_ip
        self.server_port = server_port
        self.got_data_cb = got_data_cb
        self.rcv_count = 0
        self.running = True

    def run(self):
        log.info('client thread: start')
        while self.running:
            try:
                self.receive_data()
            except Exception as e:
                log.error('client thread error: %s' % e)
                time.sleep(3)
        log.info('client thread: bye')

    def receive_data(self):
        client = self.connect()
        log.info('client thread: connected')
        timeout_count = 0
        while self.running:
            try:
                data = client.recv(BUFFER_SIZE)
                if len(data) == 0:
                    raise RuntimeError('socket connection broken')
                self.rcv_count += 1
                log.debug('rcv %d bytes. id: %d' % (len(data), self.rcv_count))
                self.got_data_cb(data, self.rcv_count)
                timeout_count = 0
            except socket.timeout:
                timeout_count += 1
                if timeout_count >= 5:
                    timeout_count = 0
                    client = self.reconnect(client)
                    log.debug('client timeout, reconnect')
        try:
            client.close()
        except socket.error:
            pass
        except Exception as e:
            log.error('client exception when close: %s' % e)

    def connect(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.server_ip, self.server_port))
        client.settimeout(3)
        return client

    def reconnect(self, client):
        try:
            client.close()
        except:
            log.error('client exception when close.')
        return self.connect()
