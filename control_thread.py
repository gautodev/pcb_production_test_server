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
CMD_BEGIN = [c for c in b'*#*#']
CMD_END = [c for c in b'#*#*']


class ControlThread(threading.Thread):
    def __init__(self, port, got_command_cb):
        super().__init__()
        self.port = port
        self.got_command_cb = got_command_cb
        self.client = None
        self.buffer = []
        self.is_in_command = False
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
        while len(self.buffer) >= 4:
            # 解析命令
            try:
                if self.is_in_command:
                    command = self.resolve_command_from_begin()
                    if self.is_in_command:
                        break
                    elif isinstance(command, str):
                        log.info('control command: %s' % command)
                        self.got_command_cb(command)
                elif self.buffer[:4] == CMD_BEGIN:  # begin of command
                    self.is_in_command = True
                else:
                    del self.buffer[0]
            except Exception as e:
                log.warning('control thread resolve: %s' % e)

    def resolve_command_from_begin(self):
        for i in range(5, len(self.buffer) + 1):
            if self.buffer[i - 4:i] == CMD_BEGIN:   # begin again
                del self.buffer[:i - 4]
                return self.resolve_command_from_begin()
            elif i >= 8 and self.buffer[i - 4:i] == CMD_END:   # end of command
                command = ''.join([chr(c) for c in self.buffer[4:i - 4]])
                del self.buffer[:i]
                self.is_in_command = False
                return command
        return None

    def receive_data(self):
        data = self.client.recv(BUFFER_SIZE)
        if len(data) == 0:
            raise RuntimeError('socket connection broken')
        self.buffer.extend(data)
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
        self.buffer.clear()
        self.is_in_command = False
