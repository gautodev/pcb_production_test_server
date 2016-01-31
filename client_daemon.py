#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File          : client_daemon.py
# Author        : bssthu
# Project       : rtk_trans
# Description   :
#

import threading
import time
import log
from client_thread import ClientThread


class ClientDaemon(threading.Thread):
    def __init__(self, server_ip, server_port, got_data_cb):
        super().__init__()
        self.client_thread = None
        self.server_ip = server_ip
        self.server_port = server_port
        self.got_data_cb = got_data_cb
        self.running = True

    def run(self):
        log.info('client daemon: start')
        while self.running:
            self.client_thread = ClientThread(self.server_ip, self.server_port, self.got_data_cb)
            self.client_thread.start()
            self.client_thread.join()
            time.sleep(5)

    def stop_daemon(self):
        self.running = False
        self.client_thread.running = False

