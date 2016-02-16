#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File          : dispatcher_thread.py
# Author        : bssthu
# Project       : rtk_trans
# Description   :
#

import threading
import queue
import log
from sender_thread import SenderThread


class DispatcherThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.data_queue = queue.Queue()
        self.clients = {}
        self.new_client_id = 0
        self.running = True

    def run(self):
        log.info('dispatcher thread: start')
        while self.running:
            try:
                data, rcv_count = self.data_queue.get(timeout=1)
                try:
                    num_clients = self.send_data(data)
                    self.data_queue.task_done()
                    log.debug('send %d bytes to %d clients. id: %d' % (len(data), num_clients, rcv_count))
                except Exception as e:
                    log.error('dispatcher thread error: %s' % e)
            except queue.Empty:
                pass
        self.stop_all_clients()
        log.info('sender thread: bye')

    def send_data(self, data):
        clients = self.clients.copy()
        for _id, sender in clients.items():
            if sender.running:
                sender.data_queue.put(data)
            else:
                del self.clients[_id]
        return len(clients)

    def add_client(self, client_socket, address):
        sender = SenderThread(client_socket, address, self.new_client_id)
        self.clients[self.new_client_id] = sender
        self.new_client_id += 1
        sender.start()

    def stop_all_clients(self):
        for _id, sender in self.clients.items():
            sender.running = False
            sender.join()
