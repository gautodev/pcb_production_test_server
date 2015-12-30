#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : client_thread.py
# Author        : bssthu
# Project       : rtk_trans
# Description   : 
# 

import socket
import threading
import time

BUFFER_SIZE = 4096


class ClientThread(threading.Thread):
    def __init__(self, server_ip, server_port, got_data_cb):
        super().__init__()
        self.server_ip = server_ip
        self.server_port = server_port
        self.got_data_cb = got_data_cb
        self.running = True

    def run(self):
        while self.running:
            try:
                client = self.connect()
                timeout_count = 0
                while self.running:
                    try:
                        data = client.recv(BUFFER_SIZE)
                        timeout_count = 0
                        self.got_data_cb(data)
                    except socket.timeout:
                        timeout_count += 1
                        if timeout_count >= 5:
                            client = self.reconnect(client)
                try:
                    client.close()
                except:
                    pass
                print('client thread: bye')
            except Exception as e:
                print('client thread error: %s' % e)

    def connect(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.server_ip, self.server_port))
        client.settimeout(3)
        return client

    def reconnect(self, client):
        try:
            client.close()
        except:
            pass
        return self.connect()
