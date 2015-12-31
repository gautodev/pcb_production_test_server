#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File          : server_thread.py
# Author        : bssthu
# Project       : rtk_trans
# Description   : 
# 

import socket
import threading
import time


class ServerThread(threading.Thread):
    def __init__(self, port):
        super().__init__()
        self.port = port
        self.clients = []
        self.running = True

    def run(self):
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(('0.0.0.0', self.port))
            server.listen(1)
            server.settimeout(3)    # timeout: 3s
            while self.running:
                try:
                    conn, addr = server.accept()
                    self.clients.append(conn)
                except socket.timeout:
                    pass
            self.close_all()
            print('server thread: bye')
        except Exception as e:
            print('server thread error: %s' % e)
            self.running = False

    def close_all(self):
        for client in self.clients:
            try:
                client.close()
            except:
                pass
        self.clients.clear()