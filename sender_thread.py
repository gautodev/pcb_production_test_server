#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File          : sender_thread.py
# Author        : bssthu
# Project       : rtk_trans
# Description   :
#

import threading
import queue
import log


class SenderThread(threading.Thread):
    def __init__(self, clients, data_queue):
        super().__init__()
        self.clients = clients
        self.data_queue = data_queue
        self.recv_count = 0
        self.running = True

    def run(self):
        log.info('sender thread: start')
        while self.running:
            try:
                data = self.data_queue.get(timeout=1)
                self.recv_count += 1
                try:
                    (num_clients, num_alive_clients) = self.send_data(data)
                    self.data_queue.task_done()
                    log.debug('send %d bytes to %d/%d clients' % (len(data), num_alive_clients, num_clients))
                except ValueError as e:
                    log.info('sender thread ValueError: %s' % e)
                except Exception as e:
                    log.error('sender thread error: %s' % e)
            except queue.Empty:
                pass
        log.info('sender thread: bye')

    def send_data(self, data):
        clients = self.clients.copy()
        num_alive_clients = 0
        for c in clients:
            try:
                c.sendall(data)
                num_alive_clients += 1
            except:
                pass
        return len(clients), num_alive_clients
