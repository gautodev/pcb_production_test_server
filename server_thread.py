#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File          : server_thread.py
# Author        : bssthu
# Project       : rtk_trans
# Description   : 
# 

import socket
import threading
import log


class ServerThread(threading.Thread):
    def __init__(self, port, got_client_cb):
        super().__init__()
        self.port = port
        self.got_client_cb = got_client_cb
        self.running = True

    def run(self):
        log.info('server thread: start, port: %d' % self.port)
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('0.0.0.0', self.port))
            server.listen(1)
            server.settimeout(3)    # timeout: 3s
            while self.running:
                try:
                    conn, address = server.accept()
                    conn.settimeout(3)
                    self.got_client_cb(conn, address)
                    log.debug('new client from: %s' % str(address))
                except socket.timeout:
                    pass
            server.close()
            log.info('server thread: bye')
        except Exception as e:
            log.error('server thread error: %s' % e)
            self.running = False
