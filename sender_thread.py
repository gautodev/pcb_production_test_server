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
import log


class SenderThread(threading.Thread):
    def __init__(self, client_socket, address, _id):
        super().__init__()
        self.client_socket = client_socket
        self.address = address
        self.sender_id = _id
        self.data_queue = queue.Queue()
        self.running = True

    def run(self):
        log.info('sender thread %d: start, %s' % (self.sender_id, self.address))
        while self.running:
            try:
                # ignore old data
                if self.data_queue.qsize() > 10:
                    self.data_queue.empty()
                # send data
                data = self.data_queue.get(timeout=1)
                try:
                    self.client_socket.settimeout(5)
                    self.client_socket.sendall(data)
                    self.data_queue.task_done()
                except ValueError as e:
                    log.warning('sender thread %d ValueError: %s' % (self.sender_id, e))
                # rcv useless data
                try:
                    self.client_socket.settimeout(0.1)
                    self.client_socket.recv(256)
                except socket.timeout:
                    pass
            except queue.Empty:
                pass
            except Exception as e:
                log.error('sender thread %d error: %s' % (self.sender_id, e))
                self.disconnect()
                self.running = False
        log.info('sender thread %d: bye' % self.sender_id)

    def disconnect(self):
        try:
            self.client_socket.close()
        except socket.error:
            pass
        except Exception as e:
            log.error('sender thread %d exception when close: %s' % (self.sender_id, e))
