#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# File          : control_thread.py
# Author        : bssthu
# Project       : rtk_trans
# Description   : 
# 

import socket
import threading
import log

BUFFER_SIZE = 4096


class ControlThread(threading.Thread):
    def __init__(self, port):
        super().__init__()
        self.port = port
        self.client = None
        self.buffer = []
        self.running = True

    def run(self):
        log.info('control thread: start, port: %d' % self.port)
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.bind(('0.0.0.0', self.port))
            server.listen(1)
            server.settimeout(3)    # timeout: 3s
            while self.running:
                self.accept_client(server)
                self.receive_command()
                self.resolve_command()
            server.close()
            self.disconnect_client()
            log.info('control thread: bye')
        except Exception as e:
            log.error('control thread error: %s' % e)
            self.running = False

    def accept_client(self, server):
        try:
            conn, address = server.accept()
            self.client = conn
            self.client.settimeout(3)
            log.info('new control client from: %s' % str(address))
        except socket.timeout:
            pass

    def receive_command(self):
        if self.client is not None:
            try:
                self.receive_data()
            except socket.timeout:
                pass
            except Exception as e:
                log.error('control client error: %s' % e)
                self.disconnect_client()

    def resolve_command(self):
        while len(self.buffer) > 0:
            # TODO: 解析命令
            self.buffer.remove(0)

    def receive_data(self):
        data = self.client.recv(BUFFER_SIZE)
        if len(data) == 0:
            raise RuntimeError('socket connection broken')
        log.debug('control rcv %d bytes.' % len(data))

    def disconnect_client(self):
        if self.client is not None:
            try:
                self.client.sendall(b'bye')
            except:
                pass

            try:
                self.client.close()
            except socket.error:
                pass
            except Exception as e:
                log.error('control client exception when close: %s' % e)
        self.client = None
